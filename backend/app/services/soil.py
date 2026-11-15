"""Suelo por coordenadas con ISRIC SoilGrids v2.0 (https://rest.isric.org/soilgrids/v2.0/docs). Sin API key.

Ver docs/INVESTIGACION-CULTIVOS.md §5.5. Es un modelo global (~250 m): sirve para orientar cuando el usuario no
sabe su suelo, no reemplaza un análisis de laboratorio. Si falla o no hay dato (zonas urbanas, agua) → None
y el análisis sigue sin suelo. Nunca lanza excepción.
"""

import asyncio
import logging
import time

import httpx

from app.schemas.analysis import DetectedSoil, SoilTexture

URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"
TIMEOUT_S = 10.0  # SoilGrids suele tardar 3–8 s; si no contesta en 10 s el análisis sigue sin suelo
# Capas superficiales y su grosor (cm) para promediar 0–30 cm
DEPTHS = {"0-5cm": 5, "5-15cm": 10, "15-30cm": 15}

log = logging.getLogger(__name__)
_cache: dict[tuple[float, float], DetectedSoil | None] = {}
# Si SoilGrids falla (timeout, 5xx), no se reintenta ese punto durante un rato: sin esto cada análisis
# esperaba los 20 s del timeout, y «Comparar escenarios» hace dos análisis seguidos.
FAILURE_TTL_S = 300
_failed_at: dict[tuple[float, float], float] = {}
# Consultas en curso: si llegan dos análisis del mismo punto a la vez (p. ej. «Comparar escenarios»),
# el segundo espera la misma respuesta en lugar de hacer otra consulta.
_inflight: dict[tuple[float, float], asyncio.Task] = {}


def texture_class(clay_pct: float, sand_pct: float) -> SoilTexture:
    """Simplificación del triángulo textural USDA a 3 clases (las que usa el catálogo)."""
    if clay_pct >= 35:
        return "clay"
    if sand_pct >= 65 and clay_pct < 15:
        return "sandy"
    return "loam"


def parse(payload: dict) -> DetectedSoil | None:
    """SoilGrids da enteros escalados: clay/sand en g/kg (÷10 → %), phh2o en pH×10 (÷10)."""
    values: dict[str, float] = {}
    for layer in payload.get("properties", {}).get("layers", []):
        total = weight = 0.0
        for depth in layer.get("depths", []):
            mean = depth.get("values", {}).get("mean")
            cm = DEPTHS.get(depth.get("label"))
            if mean is not None and cm:
                total += mean * cm
                weight += cm
        if weight:
            values[layer["name"]] = total / weight / 10
    if "clay" not in values or "sand" not in values:
        return None
    ph = values.get("phh2o")
    return DetectedSoil(
        texture=texture_class(values["clay"], values["sand"]),
        ph=round(ph, 1) if ph is not None else None,
        clay_pct=round(values["clay"], 1),
        sand_pct=round(values["sand"], 1),
    )


async def get_soil(lat: float, lon: float, client: httpx.AsyncClient | None = None) -> DetectedSoil | None:
    key = (round(lat, 2), round(lon, 2))  # ~1 km: más fino que la resolución útil del dato
    if key in _cache:
        return _cache[key]
    if time.monotonic() - _failed_at.get(key, float("-inf")) < FAILURE_TTL_S:
        return None
    task = _inflight.get(key)
    if task is None or task.get_loop() is not asyncio.get_running_loop():
        task = asyncio.ensure_future(_fetch(key, lat, lon, client))
        _inflight[key] = task
        task.add_done_callback(lambda done: _inflight.pop(key, None) if _inflight.get(key) is done else None)
    # shield: si un cliente cancela su petición, la consulta compartida sigue para los demás
    return await asyncio.shield(task)


async def _fetch(key: tuple[float, float], lat: float, lon: float,
                 client: httpx.AsyncClient | None) -> DetectedSoil | None:
    params = [("lon", round(lon, 4)), ("lat", round(lat, 4)), ("value", "mean"),
              *[("property", p) for p in ("clay", "sand", "phh2o")], *[("depth", d) for d in DEPTHS]]
    try:
        if client is None:
            async with httpx.AsyncClient(timeout=TIMEOUT_S) as own:
                response = await own.get(URL, params=params)
        else:
            response = await client.get(URL, params=params)
        response.raise_for_status()
        result = parse(response.json())
    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        log.warning("SoilGrids no disponible para (%s, %s): %r", lat, lon, exc)
        _failed_at[key] = time.monotonic()  # fallo temporal: no va a _cache, se reintenta en FAILURE_TTL_S
        return None
    _cache[key] = result
    return result
