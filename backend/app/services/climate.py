"""Resumen climático de un punto a partir de NASA POWER, con caché. Ver docs/ARQUITECTURA.md §3 y §8.

Dos bloques de datos:
- **Largo plazo** (endpoint mensual, últimos 10 años completos): cómo es cada mes "típico" y cuánto
  varía la lluvia entre años. Cambia poco → caché de `CLIMATE_CACHE_DAYS` días.
- **Reciente** (endpoint diario, últimos 90 días): cómo viene este año contra lo normal. Cambia cada
  día → su llave de caché incluye la fecha, así que se renueva sola a diario.

Caché del largo plazo, en dos niveles:
1. Memoria (`_long_term_cache`): lo más rápido, se pierde al reiniciar el backend.
2. Tabla `climate_cache` (si el router pasa una sesión `db`): sobrevive reinicios y la comparten todos.
   Si NASA POWER se cae, se usa el registro guardado aunque esté vencido (mejor un dato viejo que un 503).
Si la BD falla, se sigue sin ella: la caché nunca debe tumbar un análisis.
El bloque reciente solo se guarda en memoria (cambia cada día).

Importante: la llave de la tabla es el centro de celda de `snap_to_grid` de este módulo (0.5° × 0.625°,
la malla real de POWER), no el `snap_to_grid` de `repositories.climate_cache` (0.5° × 0.5°).
"""

import asyncio
import calendar
import logging
import statistics
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Generic, TypeVar

import httpx
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories import climate_cache as cache_repo
from app.schemas.climate import ClimateSummary, MonthlyClimatePoint
from app.services import nasa_power
from app.services.nasa_power import NasaUnavailableError, Series

# Malla de NASA POWER (meteorología de MERRA-2): celdas de 0.5° de latitud × 0.625° de longitud.
# Todos los puntos dentro de una celda reciben el mismo dato, así que el centro de la celda es la llave
# del caché y el punto que se consulta.
GRID_LAT_DEG = 0.5
GRID_LON_DEG = 0.625
YEARS = 10
DATA_DELAY_DAYS = 7  # los datos diarios de POWER llegan con unos días de retraso
RECENT_DAYS = 90
MJ_TO_KWH = 1 / 3.6  # 1 kWh = 3.6 MJ
STALE_MAX_DAYS = 3650  # si NASA está caído, se acepta un registro de la tabla de hasta 10 años

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RecentClimate:
    """Lo que pasó en los últimos días contra lo normal para esas mismas fechas."""

    start: date
    end: date
    rain_90d_mm: float
    rain_90d_normal_mm: float
    temp_30d_c: float
    temp_30d_normal_c: float
    soil_moisture_30d: float
    estimated: bool = False  # True = NASA no dio los datos diarios y se usó el promedio (plan B)
    # Variabilidad normal de esas fechas en los 10 años, para medir anomalías sin umbrales fijos. None = sin dato.
    temp_30d_sd_c: float | None = None  # desviación estándar de la temperatura de esos meses entre años
    soil_moisture_30d_normal: float | None = None  # humedad promedio de esas fechas
    soil_moisture_30d_percentile: float | None = None  # en qué percentil cae lo reciente frente a los 10 años
    # Modelo de NASA de los días recientes distinto al del histórico (p. ej. GEOS-IT vs MERRA-2): la humedad del
    # suelo no es comparable. None = mismo modelo.
    recent_model_change: str | None = None


@dataclass(frozen=True)
class ClimateData:
    """Todo lo que el motor de reglas necesita del clima."""

    summary: ClimateSummary
    recent: RecentClimate


# ---------------------------------------------------------------- utilidades


def snap_to_grid(lat: float, lon: float) -> tuple[float, float]:
    """Centro de la celda de POWER que contiene el punto. Ej. (31.86, -116.6) → (32.0, -116.875)."""
    lat_g = round(lat / GRID_LAT_DEG) * GRID_LAT_DEG
    lon_g = -180 + round((lon + 180) / GRID_LON_DEG) * GRID_LON_DEG
    if lon_g >= 180:  # 180° y -180° son el mismo meridiano
        lon_g -= 360
    return round(lat_g, 3), round(lon_g, 3)


def climate_period(today: date) -> tuple[int, int]:
    """Últimos 10 años completos. En 2026 → (2016, 2025)."""
    end = today.year - 1
    return end - YEARS + 1, end


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


K = TypeVar("K")
V = TypeVar("V")


class TTLCache(Generic[K, V]):
    """Diccionario cuyos valores caducan después de `ttl`."""

    def __init__(self, ttl: timedelta) -> None:
        self.ttl = ttl
        self._data: dict[K, tuple[datetime, V]] = {}

    def get(self, key: K) -> V | None:
        item = self._data.get(key)
        if item is None:
            return None
        saved_at, value = item
        if datetime.now(timezone.utc) - saved_at > self.ttl:
            del self._data[key]
            return None
        return value

    def set(self, key: K, value: V) -> None:
        self._data[key] = (datetime.now(timezone.utc), value)

    def clear(self) -> None:
        self._data.clear()


_long_term_cache: TTLCache[tuple[float, float, str], tuple[ClimateSummary, Series]] = TTLCache(
    timedelta(days=settings.CLIMATE_CACHE_DAYS)
)
_recent_cache: TTLCache[tuple[float, float, date], RecentClimate] = TTLCache(timedelta(days=1))


# ---------------------------------------------------------------- cálculos (puros, se prueban sin red)


def build_summary(monthly: Series, lat: float, lon: float, start_year: int, end_year: int) -> ClimateSummary:
    """Convierte la serie mensual de POWER en el clima típico de cada mes + variabilidad de la lluvia."""

    def value(param: str, year: int, month: int) -> float | None:
        return monthly.get(param, {}).get(f"{year}{month:02d}")

    def optional_mean(param: str, month: int) -> float | None:
        vals = [v for y in range(start_year, end_year + 1) if (v := value(param, y, month)) is not None]
        return _mean(vals) if vals else None

    points: list[MonthlyClimatePoint] = []
    for month in range(1, 13):
        temps, tmax, tmin, rain, soil, solar = [], [], [], [], [], []
        for year in range(start_year, end_year + 1):
            if (v := value("T2M", year, month)) is not None:
                temps.append(v)
            if (v := value("T2M_MAX", year, month)) is not None:
                tmax.append(v)
            if (v := value("T2M_MIN", year, month)) is not None:
                tmin.append(v)
            if (v := value("PRECTOTCORR", year, month)) is not None:
                # POWER da mm/día → mm/mes con los días reales de ese mes (incluye años bisiestos)
                rain.append(v * calendar.monthrange(year, month)[1])
            if (v := value("GWETROOT", year, month)) is not None:
                soil.append(v)
            if (v := value("ALLSKY_SFC_SW_DWN", year, month)) is not None:
                solar.append(v * MJ_TO_KWH)
        if not (temps and tmax and tmin and rain and soil and solar):
            raise NasaUnavailableError(f"NASA POWER no tiene datos completos para el mes {month}")
        dew, wind, frost, rng = (optional_mean(p, month) for p in ("T2MDEW", "WS2M", "FROST_DAYS", "T2M_RANGE"))
        t_mean = _mean(temps)
        # En el endpoint mensual T2M_MAX/T2M_MIN son extremos; la máxima/mínima diaria PROMEDIO sale del rango
        # diario promedio. Sin T2M_RANGE (registros viejos) se usan los extremos, como antes.
        day_max = t_mean + rng / 2 if rng is not None else _mean(tmax)
        day_min = t_mean - rng / 2 if rng is not None else _mean(tmin)
        points.append(
            MonthlyClimatePoint(
                month=month,
                temp_c=round(t_mean, 2),
                temp_max_c=round(day_max, 2),
                temp_min_c=round(day_min, 2),
                temp_max_abs_c=round(_mean(tmax), 2),
                temp_min_abs_c=round(_mean(tmin), 2),
                rain_mm=round(_mean(rain), 1),
                soil_moisture_root=round(_mean(soil), 3),
                solar_radiation=round(_mean(solar), 2),
                dewpoint_c=round(dew, 2) if dew is not None else None,
                wind_ms=round(wind, 2) if wind is not None else None,
                frost_days=round(frost, 2) if frost is not None else None,
            )
        )

    # Lluvia total de cada año (solo años con los 12 meses) → promedio y coeficiente de variación
    annual_rain: list[float] = []
    for year in range(start_year, end_year + 1):
        months = [value("PRECTOTCORR", year, m) for m in range(1, 13)]
        if all(v is not None for v in months):
            annual_rain.append(sum(v * calendar.monthrange(year, m)[1] for m, v in enumerate(months, start=1)))
    if len(annual_rain) < 2:
        raise NasaUnavailableError("NASA POWER no tiene suficientes años completos de lluvia")
    rain_mean = _mean(annual_rain)
    # CV = desviación estándar / promedio: cuánto cambia la lluvia de un año a otro, en %
    rain_cv = statistics.stdev(annual_rain) / rain_mean * 100 if rain_mean > 0 else 0.0

    elevation = monthly.get(nasa_power.ELEVATION_KEY, {}).get("m")
    return ClimateSummary(
        lat=lat,
        lon=lon,
        elevation_m=round(elevation, 1) if elevation is not None else None,
        source=f"NASA POWER (community={nasa_power.COMMUNITY})",
        period=f"{start_year}-{end_year}",
        temp_mean_c=round(_mean([p.temp_c for p in points]), 2),
        rain_annual_mm=round(rain_mean, 1),
        rain_cv_pct=round(rain_cv, 1),
        soil_moisture_root=round(_mean([p.soil_moisture_root for p in points]), 3),
        monthly=points,
    )


def monthly_spread(monthly: Series, param: str, start_year: int, end_year: int
                   ) -> dict[int, tuple[float, float | None]]:
    """{mes: (promedio, desviación estándar entre años)} de un parámetro mensual. Sin 2 años → sd None."""
    out: dict[int, tuple[float, float | None]] = {}
    for month in range(1, 13):
        vals = [v for y in range(start_year, end_year + 1)
                if (v := monthly.get(param, {}).get(f"{y}{month:02d}")) is not None]
        if vals:
            out[month] = (_mean(vals), statistics.stdev(vals) if len(vals) >= 2 else None)
    return out


def _window_normal(spread: dict[int, tuple[float, float | None]], days: list[date]
                   ) -> tuple[float | None, float | None]:
    """Promedio y desviación estándar normales de una ventana de días (ponderados por los días de cada mes)."""
    means = [spread[d.month][0] for d in days if d.month in spread]
    sds = [sd for d in days if d.month in spread and (sd := spread[d.month][1]) is not None]
    return (_mean(means) if means else None, _mean(sds) if sds else None)


def build_recent(daily: Series, monthly: Series, summary: ClimateSummary, start: date, end: date) -> RecentClimate:
    """Últimos 90 días contra lo normal de esas mismas fechas (normal = promedio de los 10 años)."""
    start_year, end_year = (int(y) for y in summary.period.split("-"))

    # Lluvia normal de cada mes en mm/día (promedio de los 10 años)
    normal_rain_rate: dict[int, float] = {}
    for month in range(1, 13):
        rates = [
            v for y in range(start_year, end_year + 1)
            if (v := monthly.get("PRECTOTCORR", {}).get(f"{y}{month:02d}")) is not None
        ]
        normal_rain_rate[month] = _mean(rates) if rates else 0.0
    normal_temp = {p.month: p.temp_c for p in summary.monthly}

    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    last_30 = days[-30:]

    def get(param: str, day: date) -> float | None:
        return daily.get(param, {}).get(day.strftime("%Y%m%d"))

    rain = [v for d in days if (v := get("PRECTOTCORR", d)) is not None]
    temps = [v for d in last_30 if (v := get("T2M", d)) is not None]
    soil = [v for d in last_30 if (v := get("GWETROOT", d)) is not None]
    if len(rain) < len(days) * 0.8 or not temps or not soil:
        raise NasaUnavailableError("NASA POWER no tiene suficientes datos diarios recientes")

    # Si faltan algunos días, se escala la suma a 90 días con el promedio de los días que sí hay
    rain_90d = sum(rain) * len(days) / len(rain)
    _, temp_sd = _window_normal(monthly_spread(monthly, "T2M", start_year, end_year), last_30)
    soil_now = _mean(soil)
    soil_normal, _ = _window_normal(monthly_spread(monthly, "GWETROOT", start_year, end_year), last_30)
    new_models = set(daily.get(nasa_power.SOURCES_KEY, {})) - nasa_power.CLIMATOLOGY_MODELS
    return RecentClimate(
        start=start,
        end=end,
        rain_90d_mm=round(rain_90d, 1),
        rain_90d_normal_mm=round(sum(normal_rain_rate[d.month] for d in days), 1),
        temp_30d_c=round(_mean(temps), 2),
        temp_30d_normal_c=round(_mean([normal_temp[d.month] for d in last_30]), 2),
        soil_moisture_30d=round(soil_now, 3),
        temp_30d_sd_c=round(temp_sd, 2) if temp_sd is not None else None,
        soil_moisture_30d_normal=round(soil_normal, 3) if soil_normal is not None else None,
        soil_moisture_30d_percentile=window_percentile(monthly, "GWETROOT", start_year, end_year, last_30, soil_now),
        recent_model_change=", ".join(sorted(new_models)) or None,
    )


def window_percentile(monthly: Series, param: str, start_year: int, end_year: int, days: list[date],
                      value: float) -> float | None:
    """Percentil (0-100) de `value` frente al mismo periodo de cada uno de los 10 años (rango medio en empates).
    El valor de cada año es el promedio de sus meses ponderado por los días de la ventana en cada mes."""
    weights: dict[int, int] = {}
    for d in days:
        weights[d.month] = weights.get(d.month, 0) + 1
    per_year = []
    for y in range(start_year, end_year + 1):
        vals = {m: monthly.get(param, {}).get(f"{y}{m:02d}") for m in weights}
        if all(v is not None for v in vals.values()):
            per_year.append(sum(vals[m] * w for m, w in weights.items()) / sum(weights.values()))
    if len(per_year) < 5:
        return None
    below = sum(v < value for v in per_year)
    ties = sum(v == value for v in per_year)
    return round(100 * (below + ties / 2) / len(per_year), 1)


def recent_from_normals(monthly: Series, summary: ClimateSummary, start: date, end: date) -> RecentClimate:
    """Plan B cuando los datos diarios no llegan: lo reciente se toma como igual a lo normal (sin anomalía)."""
    start_year, end_year = (int(y) for y in summary.period.split("-"))

    def normal(param: str, month: int) -> float | None:
        vals = [
            v for y in range(start_year, end_year + 1)
            if (v := monthly.get(param, {}).get(f"{y}{month:02d}")) is not None
        ]
        return _mean(vals) if vals else None

    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    last_30 = days[-30:]
    normal_temp = {p.month: p.temp_c for p in summary.monthly}
    soil = [s for d in last_30 if (s := normal("GWETROOT", d.month)) is not None]
    if not soil:
        raise NasaUnavailableError("Sin datos normales de humedad de suelo")
    rain_normal = round(sum(normal("PRECTOTCORR", d.month) or 0.0 for d in days), 1)
    temp_normal = round(_mean([normal_temp[d.month] for d in last_30]), 2)
    soil_normal = round(_mean(soil), 3)
    return RecentClimate(
        start=start,
        end=end,
        rain_90d_mm=rain_normal,
        rain_90d_normal_mm=rain_normal,
        temp_30d_c=temp_normal,
        temp_30d_normal_c=temp_normal,
        soil_moisture_30d=soil_normal,
        estimated=True,
        soil_moisture_30d_normal=soil_normal,
    )


# ---------------------------------------------------------------- API del módulo (con red y caché)


def _to_payload(summary: ClimateSummary, monthly: Series) -> dict:
    """Lo que se guarda en `climate_cache.payload` (JSONB)."""
    return {"summary": summary.model_dump(mode="json"), "monthly": monthly}


def _from_payload(payload: dict) -> tuple[ClimateSummary, Series]:
    return ClimateSummary.model_validate(payload["summary"]), payload["monthly"]


def has_all_parameters(monthly: Series) -> bool:
    """¿El registro trae las variables que se agregaron después (rocío, viento, heladas)? Si no, se vuelve a pedir
    a NASA (los registros viejos solo se usan como plan B cuando NASA está caído)."""
    return all(monthly.get(p) for p in nasa_power.OPTIONAL_PARAMETERS)


def _db_get(db: Session, lat_g: float, lon_g: float, period: str, max_days: int | None = None,
            require_complete: bool = True) -> tuple[ClimateSummary, Series] | None:
    try:
        row = cache_repo.get_valid(db, lat_g, lon_g, period, max_days)
        if row is None:
            return None
        stored = _from_payload(row.payload)
        return stored if not require_complete or has_all_parameters(stored[1]) else None
    except (SQLAlchemyError, KeyError, TypeError, ValidationError):
        log.warning("No se pudo leer climate_cache; se sigue sin caché de BD", exc_info=True)
        db.rollback()
        return None


def _db_save(db: Session, lat_g: float, lon_g: float, period: str, value: tuple[ClimateSummary, Series]) -> None:
    try:
        cache_repo.upsert(db, lat_g, lon_g, period, _to_payload(*value))
    except SQLAlchemyError:
        log.warning("No se pudo guardar en climate_cache", exc_info=True)
        db.rollback()


async def _long_term(client: httpx.AsyncClient, lat_g: float, lon_g: float, today: date,
                     db: Session | None = None) -> tuple[ClimateSummary, Series]:
    start_year, end_year = climate_period(today)
    period = f"{start_year}-{end_year}"
    key = (lat_g, lon_g, period)
    if (cached := _long_term_cache.get(key)) is not None:
        return cached
    if db is not None and (stored := _db_get(db, lat_g, lon_g, period)) is not None:
        _long_term_cache.set(key, stored)
        return stored
    try:
        monthly = await nasa_power.fetch_monthly(lat_g, lon_g, start_year, end_year, client=client)
        result = (build_summary(monthly, lat_g, lon_g, start_year, end_year), monthly)
    except NasaUnavailableError:
        # NASA caído: si hay un registro vencido en la tabla, se usa (ARQUITECTURA §5.7: 503 solo "sin caché")
        if db is not None and (stale := _db_get(db, lat_g, lon_g, period, STALE_MAX_DAYS,
                                                require_complete=False)) is not None:
            log.warning("NASA POWER no disponible; se usa caché vencida de (%s, %s)", lat_g, lon_g)
            return stale
        raise
    _long_term_cache.set(key, result)
    if db is not None:
        _db_save(db, lat_g, lon_g, period, result)
    return result


async def get_climate_summary(lat: float, lon: float, today: date | None = None,
                              db: Session | None = None) -> ClimateSummary:
    """Solo el clima de largo plazo (lo usa GET /api/v1/climate)."""
    today = today or datetime.now(timezone.utc).date()
    async with httpx.AsyncClient(timeout=nasa_power.TIMEOUT_S) as client:
        summary, _ = await _long_term(client, *snap_to_grid(lat, lon), today, db)
    return summary


async def get_climate(lat: float, lon: float, today: date | None = None, db: Session | None = None) -> ClimateData:
    """Largo plazo + reciente (lo usa POST /api/v1/analyses). Las dos descargas van en paralelo."""
    today = today or datetime.now(timezone.utc).date()
    lat_g, lon_g = snap_to_grid(lat, lon)
    end = today - timedelta(days=DATA_DELAY_DAYS)
    start = end - timedelta(days=RECENT_DAYS - 1)

    async with httpx.AsyncClient(timeout=nasa_power.TIMEOUT_S) as client:
        recent = _recent_cache.get((lat_g, lon_g, end))
        if recent is None:
            # asyncio.gather lanza las dos peticiones a la vez: tarda lo que la más lenta, no la suma.
            # return_exceptions=True: si falla lo diario, el largo plazo ya descargado no se vuelve a pedir.
            long_res, daily_res = await asyncio.gather(
                _long_term(client, lat_g, lon_g, today, db),
                nasa_power.fetch_daily(lat_g, lon_g, start, end, client=client),
                return_exceptions=True,
            )
            if isinstance(long_res, BaseException):
                raise long_res  # sin largo plazo (ni caché ni NASA) no hay plan B → la API responde 503
            summary, monthly = long_res
            try:
                if isinstance(daily_res, BaseException):
                    raise daily_res
                recent = build_recent(daily_res, monthly, summary, start, end)
                _recent_cache.set((lat_g, lon_g, end), recent)
            except NasaUnavailableError:
                # Plan B: sin datos diarios se usa lo normal como reciente (estimated=True). No se guarda en
                # _recent_cache para que, al volver NASA, se pidan los datos reales.
                log.warning("Sin datos diarios de NASA para (%s, %s): se usa lo normal como reciente", lat_g, lon_g)
                recent = recent_from_normals(monthly, summary, start, end)
        else:
            summary, _ = await _long_term(client, lat_g, lon_g, today, db)
    return ClimateData(summary=summary, recent=recent)
