"""Cliente HTTP de NASA POWER (https://power.larc.nasa.gov/docs/services/api/). Sin BD, sin API key.

Ver docs/ARQUITECTURA.md §8. Solo descarga y limpia datos; los cálculos viven en `climate.py`.

Formato de la respuesta de POWER (lo que nos importa):
    {"properties": {"parameter": {"T2M": {"201501": 15.4, ...}, "PRECTOTCORR": {...}}},
     "header": {"fill_value": -999.0}}
- Las llaves son fechas: "YYYYMM" en el endpoint mensual (el mes "13" es el promedio anual) y
  "YYYYMMDD" en el diario.
- `-999` significa "sin dato" y se descarta aquí.
"""

import asyncio
from datetime import date

import httpx

from app.core.config import settings

# Variables que pedimos (todas en una sola petición):
#   T2M / T2M_MAX / T2M_MIN  temperatura a 2 m (°C): media, máxima y mínima
#   PRECTOTCORR              lluvia corregida (mm/día)
#   GWETROOT                 humedad del suelo en la zona de raíces (0 = seco, 1 = saturado)
#   ALLSKY_SFC_SW_DWN        radiación solar que llega al suelo (MJ/m²/día con community=AG)
PARAMETERS = ("T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "GWETROOT", "ALLSKY_SFC_SW_DWN")
COMMUNITY = "AG"  # comunidad "agricultura": unidades pensadas para agronomía
TIMEOUT_S = 20.0
RETRIES = 2  # reintentos además del primer intento
DEFAULT_FILL_VALUE = -999.0

# {parámetro: {fecha: valor}} ya sin los -999
Series = dict[str, dict[str, float]]


class NasaUnavailableError(Exception):
    """NASA POWER no respondió o respondió algo que no se puede usar. El router lo convierte en 503."""


def parse_response(payload: dict) -> Series:
    """Extrae `properties.parameter` y descarta los valores de relleno (-999)."""
    try:
        raw = payload["properties"]["parameter"]
    except (KeyError, TypeError) as exc:
        raise NasaUnavailableError("Respuesta de NASA POWER sin 'properties.parameter'") from exc
    fill = float(payload.get("header", {}).get("fill_value", DEFAULT_FILL_VALUE))
    series: Series = {}
    for param, values in raw.items():
        series[param] = {
            key: float(value) for key, value in values.items() if value is not None and float(value) != fill
        }
    return series


async def _get(client: httpx.AsyncClient, temporal: str, lat: float, lon: float, extra: dict) -> Series:
    """GET a /temporal/<temporal>/point con reintentos. Errores 4xx no se reintentan (la petición está mal)."""
    url = f"{settings.NASA_POWER_BASE_URL}/temporal/{temporal}/point"
    params = {
        "parameters": ",".join(PARAMETERS),
        "community": COMMUNITY,
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "format": "JSON",
        **extra,
    }
    last_error: Exception | None = None
    for attempt in range(RETRIES + 1):
        try:
            response = await client.get(url, params=params)
            if response.status_code < 500:
                response.raise_for_status()  # 4xx → error definitivo, sin reintento
                return parse_response(response.json())
            last_error = httpx.HTTPStatusError(
                f"NASA POWER respondió {response.status_code}", request=response.request, response=response
            )
        except httpx.HTTPStatusError as exc:
            raise NasaUnavailableError(f"NASA POWER rechazó la petición ({exc.response.status_code})") from exc
        except (httpx.TransportError, ValueError) as exc:  # sin conexión, timeout, JSON inválido
            last_error = exc
        if attempt < RETRIES:
            await asyncio.sleep(0.5 * (attempt + 1))  # espera creciente: 0.5 s, 1 s
    raise NasaUnavailableError("NASA POWER no disponible") from last_error


async def fetch_monthly(
    lat: float, lon: float, start_year: int, end_year: int, client: httpx.AsyncClient | None = None
) -> Series:
    """Serie mensual (llaves "YYYYMM"). Sirve para el clima típico de cada mes y la variabilidad entre años."""
    extra = {"start": start_year, "end": end_year}
    if client is not None:
        return await _get(client, "monthly", lat, lon, extra)
    async with httpx.AsyncClient(timeout=TIMEOUT_S) as own:
        return await _get(own, "monthly", lat, lon, extra)


async def fetch_daily(
    lat: float, lon: float, start: date, end: date, client: httpx.AsyncClient | None = None
) -> Series:
    """Serie diaria (llaves "YYYYMMDD"). Sirve para comparar lo reciente contra lo normal."""
    extra = {"start": start.strftime("%Y%m%d"), "end": end.strftime("%Y%m%d")}
    if client is not None:
        return await _get(client, "daily", lat, lon, extra)
    async with httpx.AsyncClient(timeout=TIMEOUT_S) as own:
        return await _get(own, "daily", lat, lon, extra)
