"""Suelo por coordenadas con ISRIC SoilGrids v2.0 (https://rest.isric.org/soilgrids/v2.0/docs). Sin API key.

Ver docs/INVESTIGACION-CULTIVOS.md §5.5. Es un modelo global (~250 m): sirve para orientar cuando el usuario no
sabe su suelo, no reemplaza un análisis de laboratorio. Si falla o no hay dato (zonas urbanas, agua) → None
y el análisis sigue sin suelo. Nunca lanza excepción.
"""

import logging

import httpx

from app.schemas.analysis import DetectedSoil, SoilTexture

URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"
TIMEOUT_S = 20.0  # SoilGrids suele tardar 5–10 s; el frontend lo pide en cuanto se dibuja la parcela
# Capas superficiales y su grosor (cm) para promediar 0–30 cm
DEPTHS = {"0-5cm": 5, "5-15cm": 10, "15-30cm": 15}

log = logging.getLogger(__name__)
_cache: dict[tuple[float, float], DetectedSoil | None] = {}


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
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        log.warning("SoilGrids no disponible para (%s, %s)", lat, lon, exc_info=True)
        return None  # no se guarda en caché: puede ser un fallo temporal
    _cache[key] = result
    return result
