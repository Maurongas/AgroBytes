"""Motor de reglas: clima + catálogo + petición → rotación, impacto, métricas e incertidumbre.

Función PURA: no lee BD, no llama a internet, no consulta la hora (la fecha llega como parámetro).
Así se prueba con datos inventados y cada número de la respuesta se explica con ARQUITECTURA §7.

Fuentes de cada regla (detalle y referencias completas: docs/METODOLOGIA.md):
- Aptitud por temperatura: modelo EcoCrop (Hijmans et al. 2001; implementación `ecocrop` del paquete dismo):
  rango de ECOCROP aplicado a CADA mes del ciclo y se queda el peor; un mes descarta el cultivo si su mínima media
  está a menos de KILL_MARGIN_C de la temperatura que lo mata (KTMP). Se prueba cada fecha de siembra posible
  dentro de la temporada y se usa la mejor (como EcoCrop, que prueba cada mes de inicio).
- Agua del cultivo: FAO-56. ET₀ por Penman-Monteith (ec. 6) con temperatura, punto de rocío, viento, radiación y
  altitud de NASA POWER (Hargreaves, ec. 52, solo si faltan datos). ETc = Kc × ET₀ día por día con la curva de 4
  etapas (Tablas 11 y 12) y Kc ajustado al clima del lugar (ec. 62 y 65).
- Lluvia que aprovecha el cultivo: FAO Training Manual 3, Tabla 6 (lluvia efectiva mensual).
- Heladas: días con helada de NASA POWER (FROST_DAYS) durante el ciclo. Calor: temperatura media de algún mes
  del ciclo por encima del óptimo de ECOCROP (la misma escala que usa EcoCrop: temperatura media mensual).
- Nitrógeno: balance parcial (fijación − extracción por la cosecha) con el rendimiento FAOSTAT del país
  (Ludemann et al. 2024; Herridge et al. 2022). Lo calcula research/nitrogen.py; aquí solo se suma.
- Anomalías recientes: lluvia por categorías del IMD (normal ±19 %, deficiente −20 a −59 %, muy deficiente ≤ −60 %);
  temperatura en desviaciones estándar respecto a los mismos meses de los 10 años; humedad del suelo por percentil
  frente a las mismas fechas de los 10 años (categorías del U.S. Drought Monitor). Si NASA calculó los días
  recientes con otro modelo (GEOS-IT desde oct-2026), la humedad del suelo no se compara.
- Incertidumbre: variabilidad de la lluvia anual (CV < 20 % baja, 20–30 % media, > 30 % alta; Abdul Talib et al.
  2024, Heliyon 10:e30324, Tabla 2).
- Rotación: no repetir familia botánica (plagas y enfermedades compartidas; guías de extensión universitaria).
- Qué se siembra en cada país: FAOSTAT, área cosechada (solo se recomienda lo que ahí se cultiva).
- Pesos del puntaje, castigos y el índice de salud del suelo: parámetros de diseño propios. No vienen de un
  estudio; se etiquetan como estimación y su efecto se mide con research/validar_motor.py (sensibilidad).
"""

import calendar
import dataclasses
from dataclasses import dataclass, field
from datetime import date, timedelta

from app.schemas.analysis import (
    FALLOW_ID,
    AnalysisRequest,
    ClimateShift,
    DetectedSoil,
    ImpactItem,
    MonthlyClimate,
    NasaMetric,
    Priority,
    RotationStep,
    Season,
    SoilHealth,
    Status,
    Strategy,
    Uncertainty,
    UncertaintyLevel,
)
from app.schemas.climate import ClimateSummary
from app.services import fao56
from app.services.climate import ClimateData
from app.services.crops import CropParams

MONTH_ABBR = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
SEASON_ORDER: list[Season] = ["spring", "summer", "autumn", "winter"]
SEASON_LABEL: dict[Season, str] = {"spring": "primavera", "summer": "verano", "autumn": "otoño", "winter": "invierno"}
# Meses de cada temporada en el hemisferio norte (en el sur se invierten)
NORTH_MONTHS: dict[Season, tuple[int, int, int]] = {
    "spring": (3, 4, 5),
    "summer": (6, 7, 8),
    "autumn": (9, 10, 11),
    "winter": (12, 1, 2),
}
OPPOSITE: dict[Season, Season] = {"spring": "autumn", "autumn": "spring", "summer": "winter", "winter": "summer"}

# ---- Parámetros con fuente (ver docstring del módulo y docs/METODOLOGIA.md)
# EcoCrop: un mes es letal si (mínima diaria media − margen) ≤ KTMP. dismo::ecocrop usa 5 °C; con 34 cultivos
# reales de 11 regiones (USDA, SADER, Sinaloa, Saskatchewan) 2.5 °C acierta más (97 % vs 94 %) sin perder
# especificidad: 5 °C descarta el trigo de diciembre en Arizona. CALIBRADO, no de la literatura: ver
# research/validar_motor.py y docs/VALIDACION.md.
KILL_MARGIN_C = 2.5
DEFAULT_FROST_KILL_C = 0.0  # cultivos sin KTMP en ECOCROP: la helada (0 °C) los daña
PLANTING_DAYS = (1, 16)  # fechas de siembra que se prueban en cada mes de la temporada
MIN_DAYS_IN_MONTH = 10  # un mes cuenta para EcoCrop si el ciclo pasa ahí al menos 10 días
FROST_DAYS_RISK = 1.0  # ≥ 1 día con helada en el ciclo (promedio de 10 años) → riesgo de helada
RAIN_DEFICIT_WARN_PCT = -20  # IMD: "deficiente" de −20 % a −59 %
RAIN_DEFICIT_DANGER_PCT = -60  # IMD: "muy deficiente" ≤ −60 %
DRY_SEASON_MM_PER_MONTH = 10  # FAO Tabla 6: con ≤ 10 mm/mes la lluvia efectiva es 0 (no tiene caso medir anomalía)
Z_WARN, Z_DANGER = 1.0, 2.0  # anomalía de temperatura en desviaciones estándar (≈ 16 % y 2 % de los años)
# Humedad del suelo por percentiles, como el U.S. Drought Monitor (Svoboda et al. 2002, BAMS 83:1181): D1 "sequía
# moderada" = percentil 11–20; D2 "severa" o peor = percentil ≤ 10
SOIL_PCT_WARN, SOIL_PCT_DANGER = 20.0, 10.0
CV_LOW_MAX, CV_MEDIUM_MAX = 20.0, 30.0  # Abdul Talib et al. (2024), Tabla 2
PH_TOLERANCE = 0.5  # ECOCROP da el pH ÓPTIMO; ± 0.5 de tolerancia antes de castigar (criterio propio)
MIN_COUNTRY_AREA_HA = 10_000  # se recomienda un cultivo solo si en el país se cosechan ≥ 10 000 ha al año (FAOSTAT)
TOP_CROPS_IN_COUNTRY = 5  # "uno de los cultivos más sembrados del país"

# ---- Parámetros de diseño (propios; su efecto se mide en el análisis de sensibilidad de docs/VALIDACION.md)
W_TEMP, W_WATER, W_SOIL, W_PRIORITY = 0.40, 0.30, 0.15, 0.15  # pesos del puntaje (suman 1)
SAME_FAMILY_PENALTY = 0.7  # repetir familia botánica
OUT_OF_SEASON_PENALTY = 0.9  # la temporada es preferencia, no filtro (en climas fríos el trigo va en verano)
SYSTEM_CHANGE_PENALTY = 0.85  # pasar de granos a hortalizas (o al revés) exige equipo, mano de obra y mercado
SOIL_TEXTURE_MISMATCH = 0.5  # textura fuera de la que tolera según ECOCROP
SOIL_PH_MISMATCH = 0.6  # pH fuera del óptimo de ECOCROP ± PH_TOLERANCE

PRIORITIES: tuple[Priority, ...] = ("water", "nitrogen", "yield")
STRATEGY_TITLE = {"current": "Seguir como hoy", "water": "Ahorrar agua", "nitrogen": "Regenerar el suelo",
                  "yield": "Más rendimiento"}
STRATEGY_WHY = {
    "current": "Tu cultivo actual en las temporadas en que el clima lo permite; descanso en las demás.",
    "water": "En cada temporada elige lo que menos agua necesita entre lo que el clima permite.",
    "nitrogen": "Da más peso a leguminosas y coberturas, que devuelven nitrógeno y protegen el suelo.",
    "yield": "Da más peso a los cultivos de mayor valor productivo que el clima permite.",
}
MAX_TRADEOFFS = 4
CALENDAR_YEAR = 2021  # año no bisiesto para contar días de las fechas de siembra


@dataclass(frozen=True)
class RecommendationResult:
    metrics: list[NasaMetric]
    rotation: list[RotationStep]
    impact: list[ImpactItem]
    soil_health: SoilHealth
    climate: list[MonthlyClimate]
    uncertainty: Uncertainty
    strategies: list[Strategy] = field(default_factory=list)
    local_checks: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MonthClimate:
    """Clima típico de un mes con lo que necesita el motor (ya con ET₀ y lluvia efectiva calculadas)."""

    month: int
    temp_c: float
    temp_min_c: float
    temp_max_c: float
    rain_mm: float
    et0_mm_day: float
    effective_rain_mm: float
    frost_days: float | None = None
    wind_ms: float | None = None
    rh_min_pct: float | None = None


@dataclass(frozen=True)
class Cycle:
    """Un ciclo de cultivo sembrado en la mejor fecha de la temporada."""

    planting: date
    temp_f: float  # aptitud EcoCrop 0-1 (0 = no tolera o lo mata la helada)
    killed: bool  # alguna mínima del ciclo está en el rango letal de EcoCrop
    water_need_mm: float  # ETc del ciclo (FAO-56)
    effective_rain_mm: float  # lluvia efectiva del ciclo (FAO Tabla 6)
    frost_days: float | None  # días con helada esperados durante el ciclo (NASA POWER); None = sin dato
    months: tuple[int, ...]  # meses que cuentan para EcoCrop (≥ MIN_DAYS_IN_MONTH días)
    window: tuple[int, int]  # primer y último mes de siembra con la mejor aptitud
    hottest_month: int  # mes del ciclo con la temperatura MEDIA más alta (EcoCrop compara la media)
    hottest_temp_c: float
    coldest_month: int
    coldest_tmin_c: float
    harvest: date | None = None  # siembra + días del ciclo
    fits: bool = True  # False = ninguna fecha de siembra cabe entre la cosecha anterior y el límite del plan


@dataclass(frozen=True)
class SeasonClimate:
    season: Season
    months: tuple[int, int, int]
    temp_c: float  # promedio de los 3 meses
    rain_mm: float  # suma de los 3 meses
    temp_min_c: float = 99.0  # promedio de la mínima diaria de los 3 meses (99 = sin dato)
    temp_max_c: float = -99.0  # promedio de la máxima diaria (-99 = sin dato)
    et0_mm_day: float = 0.0  # evapotranspiración de referencia promedio de la temporada
    days: int = 91
    # Los 12 meses del año (para seguir el ciclo completo, que pasa de una temporada a otra). Vacío = se usan los
    # valores de la temporada para todos los meses (pruebas y catálogos sin clima mensual).
    year: tuple[MonthClimate, ...] = ()
    et0_method: str = "Hargreaves"
    first_year: int = CALENDAR_YEAR  # año calendario del primer mes de la temporada (para la línea de tiempo)
    _cycles: dict = field(default_factory=dict, compare=False, hash=False, repr=False)

    def planting_dates(self) -> list[date]:
        """Fechas de siembra que se prueban, en orden (dic de un año → ene y feb del siguiente)."""
        out = []
        for m in self.months:
            y = self.first_year + (1 if m < self.months[0] else 0)
            out.extend(date(y, m, d) for d in PLANTING_DAYS)
        return out

    @property
    def rain_mm_day(self) -> float:
        return self.rain_mm / self.days

    def month(self, m: int) -> MonthClimate:
        if self.year:
            return self.year[m - 1]
        rain = self.rain_mm / 3
        return MonthClimate(month=m, temp_c=self.temp_c, temp_min_c=self.temp_min_c, temp_max_c=self.temp_max_c,
                            rain_mm=rain, et0_mm_day=self.et0_mm_day, effective_rain_mm=fao56.effective_rain(rain))


@dataclass(frozen=True)
class SoilInput:
    """El suelo que usa el motor: el que dio el usuario y, si falta algo, el detectado por SoilGrids."""

    texture: str | None
    ph: float | None


@dataclass(frozen=True)
class Candidate:
    crop: CropParams
    score: int
    temp_f: float
    water_f: float
    soil_f: float
    priority_f: float
    same_family: bool
    water_need_mm: float  # agua del ciclo en este lugar y temporada
    irrigation_mm: float  # lo que la lluvia efectiva no cubre
    frost_risk: bool = False
    heat_risk: bool = False
    ph_ok: bool = True
    in_season: bool = True
    system_change: bool = False
    cycle: Cycle | None = None


# ---------------------------------------------------------------- temporadas


def season_months(season: Season, lat: float) -> tuple[int, int, int]:
    return NORTH_MONTHS[season if lat >= 0 else OPPOSITE[season]]


def season_of(month: int, lat: float) -> Season:
    for season in SEASON_ORDER:
        if month in season_months(season, lat):
            return season
    raise ValueError(month)  # inalcanzable: los 12 meses están cubiertos


def next_seasons(today: date, lat: float, n: int = 3) -> list[Season]:
    """Las n temporadas que siguen a la actual. En noviembre (norte) → invierno, primavera, verano."""
    i = SEASON_ORDER.index(season_of(today.month, lat))
    return [SEASON_ORDER[(i + k) % 4] for k in range(1, n + 1)]


def extraterrestrial_radiation(lat: float, month: int, day: int = 15) -> float:
    return fao56.extraterrestrial_radiation(lat, month, day)


def et0_hargreaves(t_mean: float, t_max: float, t_min: float, lat: float, month: int) -> float:
    """ET₀ en mm/día. FAO-56 ec. 52 (Hargreaves): 0.0023 · (T+17.8) · √(Tmax−Tmin) · Ra · 0.408."""
    return fao56.et0_hargreaves(t_mean, t_max, t_min, fao56.extraterrestrial_radiation(lat, month))


def month_climates(summary: ClimateSummary) -> tuple[tuple[MonthClimate, ...], str]:
    """Los 12 meses con ET₀ y lluvia efectiva. Penman-Monteith si NASA dio rocío, viento y radiación de todos los
    meses; si no, Hargreaves. Devuelve también el método usado (para citarlo en la evidencia)."""
    by_month = {p.month: p for p in summary.monthly}
    points = [by_month[m] for m in range(1, 13)]
    full = all(p.dewpoint_c is not None and p.wind_ms is not None for p in points)
    z = summary.elevation_m or 0.0
    out: list[MonthClimate] = []
    for i, p in enumerate(points):
        ra = fao56.extraterrestrial_radiation(summary.lat, p.month)
        if full:
            g = fao56.monthly_soil_heat_flux(points[i - 1].temp_c, points[(i + 1) % 12].temp_c)
            et0 = fao56.et0_penman_monteith(p.temp_max_c, p.temp_min_c, p.dewpoint_c, p.wind_ms,
                                            p.solar_radiation * 3.6, ra, z, g)  # kWh → MJ
        else:
            et0 = fao56.et0_hargreaves(p.temp_c, p.temp_max_c, p.temp_min_c, ra)
        rh_min = fao56.rh_min_from_dewpoint(p.temp_max_c, p.dewpoint_c) if p.dewpoint_c is not None else None
        out.append(MonthClimate(month=p.month, temp_c=p.temp_c, temp_min_c=p.temp_min_c, temp_max_c=p.temp_max_c,
                                rain_mm=p.rain_mm, et0_mm_day=et0, effective_rain_mm=fao56.effective_rain(p.rain_mm),
                                frost_days=p.frost_days, wind_ms=p.wind_ms, rh_min_pct=rh_min))
    return tuple(out), ("Penman-Monteith" if full else "Hargreaves")


def seasons_ahead(today: date, data: ClimateData, n: int = 4) -> list[SeasonClimate]:
    """Las n temporadas que siguen a la de hoy, en orden y con su año (la línea de tiempo del plan: 12 meses)."""
    year, method = month_climates(data.summary)
    out: list[SeasonClimate] = []
    first_year, prev_first_month = CALENDAR_YEAR, None
    for s in next_seasons(today, data.summary.lat, n):
        first_month = season_months(s, data.summary.lat)[0]
        if prev_first_month is not None and first_month < prev_first_month:
            first_year += 1  # el plan cruzó a otro año
        out.append(season_climate(s, data, first_year, (year, method)))
        prev_first_month = first_month
    return out


def season_climate(season: Season, data: ClimateData, first_year: int = CALENDAR_YEAR,
                   months_table: tuple[tuple[MonthClimate, ...], str] | None = None) -> SeasonClimate:
    lat = data.summary.lat
    months = season_months(season, lat)
    year, method = months_table or month_climates(data.summary)
    points = [year[m - 1] for m in months]
    return SeasonClimate(
        season=season,
        months=months,
        temp_c=sum(p.temp_c for p in points) / 3,
        rain_mm=sum(p.rain_mm for p in points),
        temp_min_c=sum(p.temp_min_c for p in points) / 3,
        temp_max_c=sum(p.temp_max_c for p in points) / 3,
        et0_mm_day=sum(p.et0_mm_day for p in points) / 3,
        days=sum(calendar.monthrange(CALENDAR_YEAR, m)[1] for m in months),
        year=year,
        et0_method=method,
        first_year=first_year,
    )


# ---------------------------------------------------------------- ciclo del cultivo (EcoCrop + FAO-56)


def frost_limit(crop: CropParams) -> float:
    return crop.frost_kill_c if crop.frost_kill_c is not None else DEFAULT_FROST_KILL_C


def temperature_factor(temp: float, crop: CropParams) -> float:
    """Respuesta de EcoCrop a la temperatura media: 1 en el óptimo; baja en línea recta hasta 0 en los límites."""
    if crop.temp_opt_min <= temp <= crop.temp_opt_max:
        return 1.0
    if temp < crop.temp_opt_min:
        span = crop.temp_opt_min - crop.temp_abs_min
        return max(0.0, (temp - crop.temp_abs_min) / span) if span > 0 else 0.0
    span = crop.temp_abs_max - crop.temp_opt_max
    return max(0.0, (crop.temp_abs_max - temp) / span) if span > 0 else 0.0


def _kc_parameters(crop: CropParams, sc: SeasonClimate, months: list[int]) -> tuple[float, float, float] | None:
    """(Kc ini, Kc mid, Kc end) del cultivo con Kc mid y Kc end ajustados al viento y la humedad del ciclo."""
    if crop.kc_mid is None:
        return None
    kc_ini = crop.kc_ini if crop.kc_ini is not None else crop.kc_mid
    kc_mid = crop.kc_mid
    kc_end = crop.kc_end if crop.kc_end is not None else crop.kc_mid
    winds = [w for m in months if (w := sc.month(m).wind_ms) is not None]
    rhs = [r for m in months if (r := sc.month(m).rh_min_pct) is not None]
    if winds and rhs and crop.crop_height_m is not None:
        u2, rh = sum(winds) / len(winds), sum(rhs) / len(rhs)
        kc_mid = fao56.adjust_kc_for_climate(kc_mid, u2, rh, crop.crop_height_m)
        if kc_end >= 0.45:  # FAO-56 ec. 65: solo se ajusta si Kc end ≥ 0.45
            kc_end = fao56.adjust_kc_for_climate(kc_end, u2, rh, crop.crop_height_m)
    return kc_ini, kc_mid, kc_end


def _simulate(crop: CropParams, sc: SeasonClimate, start: date) -> Cycle:
    """Recorre el ciclo día por día desde la siembra: aptitud EcoCrop, ETc (FAO-56) y lluvia efectiva."""
    n = crop.cycle_days
    days = [start + timedelta(days=d) for d in range(n)]
    per_month: dict[int, int] = {}
    for d in days:
        per_month[d.month] = per_month.get(d.month, 0) + 1
    months = [m for m, k in per_month.items() if k >= MIN_DAYS_IN_MONTH] or list(per_month)

    # EcoCrop: el peor mes manda; un mes con mínima media en el rango letal descarta el cultivo
    temp_f = min(temperature_factor(sc.month(m).temp_c, crop) for m in months)
    killed = any(sc.month(m).temp_min_c - KILL_MARGIN_C <= frost_limit(crop) for m in months)
    if killed:
        temp_f = 0.0

    # Agua: ETc = Σ Kc(día) × ET₀(mes del día); lluvia efectiva repartida por día
    kc = _kc_parameters(crop, sc, months)
    stages = crop.kc_stages
    need = rain = 0.0
    for i, d in enumerate(days):
        mc = sc.month(d.month)
        dim = calendar.monthrange(d.year, d.month)[1]
        rain += mc.effective_rain_mm / dim
        if kc is not None:
            k = (fao56.kc_on_day(i, n, stages, *kc) if stages is not None else kc[1])
            need += k * mc.et0_mm_day
    if kc is None or need <= 0:
        need = crop.water_need_mm  # sin Kc o sin ET₀: el valor típico de FAO (Tabla 5)

    frost = None
    if all(sc.month(m).frost_days is not None for m in per_month):
        frost = sum(sc.month(m).frost_days * k / calendar.monthrange(CALENDAR_YEAR, m)[1]
                    for m, k in per_month.items())
    hottest = max(months, key=lambda m: sc.month(m).temp_c)
    coldest = min(months, key=lambda m: sc.month(m).temp_min_c)
    return Cycle(planting=start, temp_f=temp_f, killed=killed, water_need_mm=need, effective_rain_mm=rain,
                 frost_days=frost, months=tuple(months), window=(start.month, start.month),
                 hottest_month=hottest, hottest_temp_c=sc.month(hottest).temp_c,
                 coldest_month=coldest, coldest_tmin_c=sc.month(coldest).temp_min_c,
                 harvest=start + timedelta(days=n))


def cycle_for(crop: CropParams, sc: SeasonClimate, not_before: date | None = None,
              deadline: date | None = None) -> Cycle:
    """El ciclo sembrado en la mejor fecha de la temporada (como EcoCrop: se prueban todas y gana la de mayor
    aptitud). Si varias empatan, la ventana de siembra es todo ese rango y los números (agua, cosecha) son los de
    la fecha a la MITAD de la ventana: neutral, sin escoger la fecha que más le conviene a una estrategia.
    Se guarda en `sc` para no recalcularlo.

    Línea de tiempo de la rotación: solo cuentan las fechas de siembra desde `not_before` (cosecha del cultivo
    anterior) y cuya cosecha llega a más tardar en `deadline` (para que quepan los pasos que siguen). Si ninguna
    cabe, el ciclo sale con `fits=False` y aptitud 0."""
    key = (crop.id, crop.cycle_days, crop.kc_mid, crop.temp_opt_min, crop.temp_opt_max, crop.frost_kill_c,
           not_before, deadline)
    if key in sc._cycles:
        return sc._cycles[key]
    dates = [d for d in sc.planting_dates() if not_before is None or d >= not_before]
    options = [_simulate(crop, sc, d) for d in dates]
    options = [o for o in options if deadline is None or o.harvest <= deadline]
    if not options:  # no cabe: se simula la primera fecha solo para tener números de referencia
        ref = _simulate(crop, sc, sc.planting_dates()[0])
        result = dataclasses.replace(ref, temp_f=0.0, fits=False)
    else:
        best_f = max(o.temp_f for o in options)
        tied = [o for o in options if o.temp_f >= best_f - 1e-9]
        middle = tied[(len(tied) - 1) // 2]
        result = dataclasses.replace(middle, window=(tied[0].planting.month, tied[-1].planting.month))
    sc._cycles[key] = result
    return result


def last_planting(sc: SeasonClimate) -> date:
    return sc.planting_dates()[-1]


def water_need(crop: CropParams, sc: SeasonClimate) -> float:
    """Agua del ciclo (mm): FAO-56 con el clima del lugar; sin Kc, el valor típico de FAO."""
    return cycle_for(crop, sc).water_need_mm


def cycle_rain(crop: CropParams, sc: SeasonClimate) -> float:
    """Lluvia efectiva durante el ciclo (mm), FAO Training Manual 3, Tabla 6."""
    return cycle_for(crop, sc).effective_rain_mm


def tolerates(crop: CropParams, sc: SeasonClimate) -> bool:
    """¿Puede crecer si se siembra en esta temporada? (aptitud EcoCrop > 0 en la mejor fecha)."""
    return cycle_for(crop, sc).temp_f > 0


# ---------------------------------------------------------------- factores (0 a 1)


def water_factor(need: float, rain: float, irrigated: bool, max_irrigation: float) -> float:
    """Temporal: qué fracción del agua cubre la lluvia. Con riego: menos riego que las otras opciones = mejor."""
    if irrigated:
        return 1.0 if max_irrigation <= 0 else 1 - max(0.0, need - rain) / max_irrigation
    return min(1.0, rain / need) if need > 0 else 1.0


def ph_in_range(ph: float | None, crop: CropParams) -> bool:
    if ph is None or crop.ph_min is None or crop.ph_max is None:
        return True
    return crop.ph_min - PH_TOLERANCE <= ph <= crop.ph_max + PH_TOLERANCE


def soil_factor(soil: SoilInput, crop: CropParams) -> float:
    texture = 1.0 if soil.texture is None or soil.texture in crop.soils else SOIL_TEXTURE_MISMATCH
    return texture * (1.0 if ph_in_range(soil.ph, crop) else SOIL_PH_MISMATCH)


def priority_factor(req: AnalysisRequest, crop: CropParams, need: float, max_need: float) -> float:
    if req.priority == "water":
        return 1 - need / max_need if max_need > 0 else 1.0
    if req.priority == "nitrogen":
        return {"legume": 1.0, "cover": 0.7}.get(crop.family, 0.0)
    return 1.0 if crop.family in ("cereal", "vegetable", "oilseed", "industrial") else 0.5  # yield


def family_of(crop: CropParams) -> str:
    """Familia botánica si el catálogo la trae; si no, el rol (catálogos viejos / pruebas)."""
    return crop.botanical_family or crop.family


@dataclass(frozen=True)
class SeasonContext:
    """Lo que comparten todos los candidatos de una temporada (para compararlos entre ellos)."""

    max_need: float
    max_irrigation: float


@dataclass(frozen=True)
class Window:
    """Cuándo se puede sembrar en este paso de la rotación (línea de tiempo)."""

    not_before: date | None = None  # cosecha del cultivo anterior
    deadline: date | None = None  # cosecha a más tardar (para que quepan los pasos siguientes)


def season_context(crops: list[CropParams], sc: SeasonClimate, window: Window = Window()) -> SeasonContext:
    cycles = [cycle_for(c, sc, window.not_before, window.deadline) for c in crops]
    needs = [(cy.water_need_mm, cy.effective_rain_mm) for cy in cycles]
    return SeasonContext(max_need=max(n for n, _ in needs),
                         max_irrigation=max(max(0.0, n - r) for n, r in needs))


def is_horticultural(crop: CropParams) -> bool:
    return crop.family == "vegetable"


def changes_system(crop: CropParams, current: CropParams) -> bool:
    """Granos/industriales ↔ hortalizas. Las coberturas encajan en ambos sistemas."""
    return crop.family != "cover" and is_horticultural(crop) != is_horticultural(current)


def evaluate(crop: CropParams, sc: SeasonClimate, req: AnalysisRequest, previous: CropParams,
             ctx: SeasonContext, soil: SoilInput, current: CropParams | None = None,
             window: Window = Window()) -> Candidate:
    cyc = cycle_for(crop, sc, window.not_before, window.deadline)
    need, rain = cyc.water_need_mm, cyc.effective_rain_mm
    t = cyc.temp_f
    w = water_factor(need, rain, bool(req.irrigated), ctx.max_irrigation)
    s = soil_factor(soil, crop)
    p = priority_factor(req, crop, need, ctx.max_need)
    raw = 100 * (W_TEMP * t + W_WATER * w + W_SOIL * s + W_PRIORITY * p)
    same_family = family_of(crop) == family_of(previous)
    if same_family:
        raw *= SAME_FAMILY_PENALTY  # regla de rotación: cambiar de familia corta plagas y enfermedades
    in_season = sc.season in crop.seasons
    if not in_season:
        raw *= OUT_OF_SEASON_PENALTY
    system_change = changes_system(crop, current or previous)
    if system_change:
        raw *= SYSTEM_CHANGE_PENALTY
    return Candidate(crop, max(0, min(100, round(raw))), t, w, s, p, same_family,
                     water_need_mm=need, irrigation_mm=max(0.0, need - rain),
                     frost_risk=cyc.frost_days is not None and cyc.frost_days >= FROST_DAYS_RISK,
                     heat_risk=cyc.hottest_temp_c > crop.temp_opt_max,
                     ph_ok=ph_in_range(soil.ph, crop),
                     in_season=in_season, system_change=system_change, cycle=cyc)


def choose(crops: list[CropParams], sc: SeasonClimate, req: AnalysisRequest, previous: CropParams,
           soil: SoilInput, current: CropParams | None = None,
           window: Window = Window(), used: frozenset[str] = frozenset()) -> tuple[Candidate | None, bool]:
    """Mejor cultivo de la temporada. Devuelve (candidato, fuera_de_temporada).

    Entre los cultivos que toleran el clima de su ciclo (EcoCrop) y caben en la línea de tiempo, gana el de mayor
    puntaje; estar fuera de su temporada habitual o cambiar de sistema de producción solo resta. Si ninguno →
    None = barbecho (descanso). Nunca repite el cultivo anterior y, si hay alternativa, tampoco uno que ya está en
    la rotación (`used`): repetir el mismo cultivo en 12 meses acumula sus plagas y enfermedades.
    """
    others = ([c for c in crops if c.id != previous.id and c.id not in used]
              or [c for c in crops if c.id != previous.id] or crops)
    ctx = season_context(others, sc, window)
    evaluated = [evaluate(c, sc, req, previous, ctx, soil, current, window) for c in others]
    pool = [e for e in evaluated if e.temp_f > 0]
    if not pool:
        return None, False
    best = max(pool, key=lambda e: (e.score, -e.water_need_mm))
    return best, not best.in_season


# ---------------------------------------------------------------- textos


def grown_in_country(crops: list[CropParams], country_areas: dict[str, float] | None) -> list[CropParams]:
    """Cultivos que se siembran en el país (≥ MIN_COUNTRY_AREA_HA). Los de cobertura no se filtran: se incorporan
    al suelo y no aparecen en estadísticas de cosecha. Sin datos del país → todos."""
    if not country_areas:
        return crops
    return [c for c in crops if c.family == "cover" or country_areas.get(c.id, 0) >= MIN_COUNTRY_AREA_HA]


def top_in_country(country_areas: dict[str, float] | None) -> set[str]:
    if not country_areas:
        return set()
    ranked = sorted((a, crop_id) for crop_id, a in country_areas.items() if a >= MIN_COUNTRY_AREA_HA)
    return {crop_id for _, crop_id in ranked[-TOP_CROPS_IN_COUNTRY:]}


def month_span(first: int, last: int) -> str:
    return MONTH_ABBR[first - 1] if first == last else f"{MONTH_ABBR[first - 1]} – {MONTH_ABBR[last - 1]}"


def cycle_span(cyc: Cycle) -> str:
    """Meses del ciclo, p. ej. «Dic–Abr»."""
    return f"{MONTH_ABBR[cyc.months[0] - 1]}–{MONTH_ABBR[cyc.months[-1] - 1]}"


def reasons_for(c: Candidate, sc: SeasonClimate, previous: CropParams, current: CropParams,
                req: AnalysisRequest, country_name: str | None = None, popular: bool = False) -> list[str]:
    reasons: list[str] = []
    label = SEASON_LABEL[sc.season]
    cyc = c.cycle or cycle_for(c.crop, sc)
    if c.temp_f == 1:
        reasons.append(f"Todo su ciclo ({cycle_span(cyc)}) cae en su rango óptimo de temperatura (ECOCROP)")
    elif c.temp_f >= 0.6:
        reasons.append(f"Tolera las temperaturas de su ciclo ({cycle_span(cyc)})")
    if popular and country_name:
        reasons.append(f"Es de los {TOP_CROPS_IN_COUNTRY} cultivos más sembrados en {country_name} (FAOSTAT): "
                       "hay mercado e insumos")
    if req.irrigated and c.water_f >= 0.8:
        reasons.append(f"Es de las opciones que menos riego necesitan (~{c.irrigation_mm:.0f} mm en el ciclo)")
    elif not req.irrigated and c.water_f >= 0.9:
        reasons.append(f"La lluvia de {label} cubre casi toda el agua que necesita "
                       f"(~{cyc.effective_rain_mm:.0f} de {c.water_need_mm:.0f} mm)")
    saving = water_saving_pct(water_need(current, sc), c.water_need_mm)
    if saving >= 10:
        reasons.append(f"Necesita {saving:.0f} % menos agua que {current.name.lower()}")
    if c.crop.family == "legume":
        reasons.append("Leguminosa: fija nitrógeno del aire (estimado)")
    elif c.crop.family == "cover":
        reasons.append("Cultivo de cobertura: protege el suelo de la erosión")
    elif req.priority == "yield" and c.priority_f == 1:
        reasons.append("Cultivo de alto valor productivo")
    if not c.system_change and current.id != c.crop.id and len(reasons) < 3:
        reasons.append("Encaja en tu sistema de producción actual ("
                       + ("hortalizas" if is_horticultural(current) else "granos y forrajes") + ")")
    if not c.same_family:
        reasons.append(f"Cambia de familia respecto a {previous.name.lower()} ({family_of(previous)} → "
                       f"{family_of(c.crop)}): corta el ciclo de plagas")
    return reasons[:3] or ["Es la mejor opción disponible para esta temporada"]


def risks_for(c: Candidate, sc: SeasonClimate, high_uncertainty: bool, out_of_season: bool,
              irrigated: bool, soil: SoilInput) -> list[str]:
    risks: list[str] = []
    cyc = c.cycle or cycle_for(c.crop, sc)
    if c.frost_risk and cyc.frost_days is not None:
        risks.append(f"Riesgo de helada: ~{cyc.frost_days:.0f} día(s) con helada durante su ciclo en un año "
                     f"típico (NASA POWER); se daña desde {frost_limit(c.crop):.0f} °C")
    if c.heat_risk:
        risks.append(f"Calor: en {MONTH_ABBR[cyc.hottest_month - 1].lower()} la temperatura media (~"
                     f"{cyc.hottest_temp_c:.0f} °C) pasa su óptimo ({c.crop.temp_opt_max:.0f} °C, ECOCROP); "
                     "el rendimiento puede bajar: siembra temprano o elige una variedad tolerante")
    if out_of_season:
        risks.append("Fuera de su temporada habitual de siembra; confirma las fechas locales")
    if c.system_change:
        risks.append("Cambia tu sistema de producción (requiere otro equipo, mano de obra y mercado)")
    if not irrigated and c.water_f < 0.6:
        risks.append(f"Puede requerir riego: la lluvia del ciclo cubre ~{c.water_f * 100:.0f} % de lo que necesita "
                     "(no cuenta el agua que el suelo ya guarda al sembrar)")
    if not c.ph_ok and soil.ph is not None:
        risks.append(f"pH del suelo ({soil.ph:.1f}) fuera de su rango óptimo "
                     f"({c.crop.ph_min:.1f}–{c.crop.ph_max:.1f})")
    if c.same_family:
        risks.append("Misma familia que el cultivo anterior (más riesgo de plagas)")
    if high_uncertainty and not irrigated:
        risks.append("Lluvia muy variable entre años")
    return risks


def water_saving_pct(current_need: float, need: float) -> float:
    return round(100 * (current_need - need) / current_need) if current_need > 0 else 0.0


def planting_window(cyc: Cycle) -> str:
    """Meses de siembra con la mejor aptitud dentro de la temporada, p. ej. «Abr – May»."""
    return month_span(*cyc.window)


# ---------------------------------------------------------------- impacto y salud del suelo


@dataclass(frozen=True)
class Slot:
    """Un paso de la rotación ya decidido: temporada, cultivo elegido (None = descanso) y por qué descansa."""

    sc: SeasonClimate
    candidate: Candidate | None
    out_of_season: bool = False
    fallow_reason: tuple[str, ...] = ()

    @property
    def crop(self) -> CropParams | None:
        return self.candidate.crop if self.candidate else None


def impact(slots: list[Slot]) -> tuple[float, float, float]:
    """(agua total del cultivo, riego necesario, balance de nitrógeno) de una rotación. Descanso = 0.

    Agua total = ETc del ciclo (FAO-56), venga de la lluvia o del riego; riego = la parte que la lluvia efectiva
    no cubre. Nitrógeno = suma de los balances parciales (fijación − cosecha) de cada cultivo: negativo = la
    rotación saca más N del que repone (hay que fertilizar)."""
    water = sum(s.candidate.water_need_mm for s in slots if s.candidate)
    irrigation = sum(s.candidate.irrigation_mm for s in slots if s.candidate)
    nitrogen = sum(s.crop.nitrogen_delta_kg_ha for s in slots if s.crop is not None)
    return round(water), round(irrigation), round(nitrogen)


# Materia orgánica que reporta el usuario → ajuste del índice de salud del suelo (regla propia, estimación)
ORGANIC_MATTER_POINTS = {"low": -10, "mid": 0, "high": 10}


def soil_health_index(seq: list[CropParams | None], organic_matter: str | None = None) -> int:
    """Índice ESTIMADO 0-100 (regla propia, ilustrativa): premia leguminosas y coberturas y castiga repetir familia
    botánica, en la dirección que reporta la literatura (más diversidad y leguminosas → mejor suelo). Los puntos no
    vienen de un estudio. Parte de 50 (o 40/60 si el usuario dijo que su materia orgánica es baja/alta)."""
    crops = [c for c in seq if c is not None]
    score = 50 + ORGANIC_MATTER_POINTS.get(organic_matter or "mid", 0)
    score += 10 * sum(c.family == "legume" for c in crops)
    score += 8 * sum(c.family == "cover" for c in crops)
    score -= 10 * sum(family_of(a) == family_of(b) for a, b in zip(crops, crops[1:]))
    return max(0, min(100, score))


def fallow_step(slot: Slot) -> RotationStep:
    return RotationStep(
        season=slot.sc.season, crop_id=FALLOW_ID, score=0, reasons=list(slot.fallow_reason),
        water_saving_pct=100, nitrogen_delta=0, risks=[], planting_window="—", irrigation_mm=0,
    )


# ---------------------------------------------------------------- métricas NASA


def _z(value: float, normal: float | None, sd: float | None) -> float | None:
    if normal is None or sd is None or sd <= 0:
        return None
    return (value - normal) / sd


def _z_text(z: float | None) -> str:
    return f" ({abs(z):.1f} desviaciones estándar)" if z is not None else ""


def metrics_for(data: ClimateData, current: CropParams) -> list[NasaMetric]:
    s, r = data.summary, data.recent
    monthly = s.monthly
    period_src = f"NASA POWER · {s.period}"
    recent_src = (f"Promedio NASA POWER {s.period} (sin datos recientes)" if r.estimated
                  else f"NASA POWER · {r.start:%d/%m}–{r.end:%d/%m/%Y}")

    # 1. Humedad del suelo (raíces), últimos 30 días: percentil frente a las mismas fechas de los 10 años, con las
    #    categorías del U.S. Drought Monitor (D1 ≤ percentil 20, D2 o peor ≤ percentil 10)
    p_sm = r.soil_moisture_30d_percentile
    if r.estimated:
        sm_status: Status = "ok"
        sm_meaning = "Promedio de estas fechas (no llegaron los datos recientes)"
    elif r.recent_model_change:
        sm_status = "ok"
        sm_meaning = (f"No se compara con el histórico: NASA POWER calculó los días recientes con otro modelo "
                      f"({r.recent_model_change}) y la humedad del suelo no es continua con MERRA-2")
    elif p_sm is None:
        sm_status, sm_meaning = "ok", "Sin datos suficientes para compararla con lo normal"
    else:
        sm_status = "danger" if p_sm <= SOIL_PCT_DANGER else "warn" if p_sm <= SOIL_PCT_WARN else "ok"
        years_wetter = round((100 - p_sm) / 10)
        sm_meaning = {
            "danger": f"Muy seca: más seca que en {years_wetter} de los últimos 10 años en estas fechas",
            "warn": f"Seca: más seca que en {years_wetter} de los últimos 10 años en estas fechas",
            "ok": "Dentro de lo normal para estas fechas",
        }[sm_status]

    # 2. Lluvia de los últimos 90 días contra lo normal (categorías del IMD)
    if r.rain_90d_normal_mm <= 3 * DRY_SEASON_MM_PER_MONTH:
        rain_status: Status = "ok"
        rain_meaning = (f"Temporada normalmente seca (lo normal es {r.rain_90d_normal_mm:.0f} mm): "
                        "esa lluvia casi no la aprovecha el cultivo (FAO)")
    else:
        diff_pct = (r.rain_90d_mm - r.rain_90d_normal_mm) / r.rain_90d_normal_mm * 100
        rain_status = ("danger" if diff_pct <= RAIN_DEFICIT_DANGER_PCT
                       else "warn" if diff_pct <= RAIN_DEFICIT_WARN_PCT else "ok")
        category = {"danger": "muy deficiente", "warn": "deficiente",
                    "ok": "normal" if diff_pct < 20 else "excesiva"}[rain_status]
        rain_meaning = f"{abs(diff_pct):.0f} % {'menos' if diff_pct < 0 else 'más'} que el promedio ({category})"

    # 3. Temperatura de los últimos 30 días contra lo normal (en desviaciones estándar de esos meses)
    diff_t = r.temp_30d_c - r.temp_30d_normal_c
    z_t = _z(r.temp_30d_c, r.temp_30d_normal_c, r.temp_30d_sd_c)
    if z_t is None:
        temp_status: Status = "ok"
    else:
        temp_status = "danger" if abs(z_t) >= Z_DANGER else "warn" if abs(z_t) >= Z_WARN else "ok"
    temp_meaning = f"{abs(diff_t):.1f} °C {'sobre' if diff_t >= 0 else 'bajo'} lo normal{_z_text(z_t)}"

    # 4. Radiación solar: promedio anual (informativa, sin alerta)
    solar = sum(p.solar_radiation for p in monthly) / 12
    solar_meaning = (
        "Alta: buena para cultivos de sol" if solar >= 5 else "Moderada" if solar >= 3.5 else "Baja"
    )

    return [
        NasaMetric(id="soilMoisture", label="Humedad del suelo", value=round(r.soil_moisture_30d, 2), unit="0–1",
                   status=sm_status, meaning=sm_meaning,
                   series=[p.soil_moisture_root for p in monthly], source=recent_src),
        NasaMetric(id="rain90d", label="Lluvia 90 días", value=round(r.rain_90d_mm), unit="mm",
                   status=rain_status, meaning=rain_meaning,
                   series=[p.rain_mm for p in monthly], source=recent_src),
        NasaMetric(id="tempMean", label="Temperatura media", value=round(r.temp_30d_c, 1), unit="°C",
                   status=temp_status, meaning=temp_meaning,
                   series=[p.temp_c for p in monthly], source=recent_src),
        NasaMetric(id="solarRadiation", label="Radiación solar", value=round(solar, 1), unit="kWh/m²/día",
                   status="ok", meaning=solar_meaning,
                   series=[p.solar_radiation for p in monthly], source=period_src),
    ]


def uncertainty_for(data: ClimateData) -> Uncertainty:
    """Nivel por la variabilidad de la lluvia anual (CV): < 20 % baja, 20–30 % media, > 30 % alta
    (Abdul Talib et al. 2024, Heliyon 10:e30324, Tabla 2). Sube un nivel si no llegaron los datos recientes."""
    s = data.summary
    levels: list[UncertaintyLevel] = ["low", "medium", "high"]
    i = 0 if s.rain_cv_pct < CV_LOW_MAX else 1 if s.rain_cv_pct <= CV_MEDIUM_MAX else 2
    reason = f"La lluvia anual varía {s.rain_cv_pct:.0f} % entre años (NASA POWER {s.period})"
    if data.recent.estimated:
        i = min(2, i + 1)
        reason += "; no llegaron los datos de los últimos 90 días y se usó el promedio"
    return Uncertainty(level=levels[i], reason=reason)


def apply_shift(data: ClimateData, shift: ClimateShift | None) -> ClimateData:
    """Escenario «¿y si…?»: cambia la lluvia (%) y suma °C al clima histórico de cada mes. No toca el original.
    El punto de rocío sube igual que la temperatura (humedad relativa casi constante, lo habitual en escenarios
    de calentamiento). Lo reciente (90 días) no se toca: el escenario es sobre las temporadas típicas."""
    if shift is None or (shift.rain_pct == 0 and shift.temp_c == 0):
        return data
    f, d = 1 + shift.rain_pct / 100, shift.temp_c
    s = data.summary
    def plus(v: float | None) -> float | None:
        return v + d if v is not None else None

    monthly = [p.model_copy(update={"temp_c": p.temp_c + d, "temp_max_c": p.temp_max_c + d,
                                    "temp_min_c": p.temp_min_c + d, "rain_mm": p.rain_mm * f,
                                    "temp_max_abs_c": plus(p.temp_max_abs_c), "temp_min_abs_c": plus(p.temp_min_abs_c),
                                    "dewpoint_c": plus(p.dewpoint_c)})
               for p in s.monthly]
    summary = s.model_copy(update={"monthly": monthly, "temp_mean_c": s.temp_mean_c + d,
                                   "rain_annual_mm": s.rain_annual_mm * f})
    return dataclasses.replace(data, summary=summary)


# ---------------------------------------------------------------- rotaciones y estrategias


def _fallow_reason(pool: list[CropParams], sc: SeasonClimate, window: Window, previous: CropParams,
                   monoculture: bool) -> tuple[str, ...]:
    """Por qué descansa la parcela: el clima no deja, o no hay tiempo entre la cosecha anterior y lo que sigue."""
    label = SEASON_LABEL[sc.season]
    climate_ok = any(cycle_for(c, sc).temp_f > 0 for c in pool)
    if climate_ok and window.not_before is not None:
        return (f"Ningún ciclo cabe entre la cosecha de {previous.name.lower()} "
                f"({MONTH_ABBR[window.not_before.month - 1].lower()}) y la siembra que sigue",
                "Deja el rastrojo o siembra una cobertura corta para no dejar el suelo desnudo")
    if monoculture:
        return (f"El {pool[0].name.lower()} no tolera un ciclo sembrado en {label} en este lugar",
                "Hoy la parcela queda sin cultivo en esta temporada")
    return (f"Ningún cultivo del catálogo tolera un ciclo sembrado en {label} en este lugar "
            f"({sc.temp_c:.0f} °C de media, mínimas de {sc.temp_min_c:.0f} °C)",
            "Dejar el suelo en descanso, con rastrojo o cubierto, lo protege de la erosión")


def plan(candidates: list[CropParams], seasons: list[SeasonClimate], req: AnalysisRequest, current: CropParams,
         soil: SoilInput, monoculture: bool = False, steps: int = 3) -> list[Slot]:
    """Rotación como línea de tiempo de 12 meses (las 4 temporadas que siguen; se eligen 3 pasos).

    Cada cultivo se siembra DESPUÉS de cosechar el anterior, en la primera temporada que todavía permite sembrar,
    y su cosecha debe dejar lugar a los pasos que faltan. Una temporada que el cultivo anterior todavía ocupa no se
    muestra. Así no se traslapan ciclos (antes el plan suponía un cultivo de 3 meses por temporada).
    `monoculture` = «Seguir como hoy»: el cultivo actual en cada paso donde quepa y lo tolere el clima."""
    slots: list[Slot] = []
    previous = current
    not_before: date | None = None
    j = 0
    n = len(seasons)
    for k in range(steps):
        remaining = steps - 1 - k
        latest = n - 1 - remaining  # índice máximo para que queden temporadas para los pasos siguientes
        jj = next((i for i in range(j, latest + 1)
                   if not_before is None or last_planting(seasons[i]) >= not_before), min(j, latest))
        sc = seasons[jj]
        deadline = last_planting(seasons[n - remaining]) if remaining > 0 else None
        window = Window(not_before, deadline)
        if monoculture:
            ctx = season_context([*candidates, current], sc, window)
            cand = evaluate(current, sc, req, current, ctx, soil, current, window)
            best, oos = (cand, not cand.in_season) if cand.temp_f > 0 else (None, False)
        else:
            used = frozenset(s.candidate.crop.id for s in slots if s.candidate)
            best, oos = choose(candidates, sc, req, previous, soil, current, window, used)
        if best is None:
            pool = [current] if monoculture else candidates
            slots.append(Slot(sc, None, fallow_reason=_fallow_reason(pool, sc, window, previous, monoculture)))
        else:
            slots.append(Slot(sc, best, oos))
            previous = best.crop
            not_before = best.cycle.harvest if best.cycle else not_before
        j = jj + 1
    return slots


def rotation_steps(slots: list[Slot], req: AnalysisRequest, current: CropParams, soil: SoilInput,
                   uncertainty: Uncertainty, country_name: str | None = None, popular: set[str] | None = None,
                   monoculture: bool = False) -> list[RotationStep]:
    """Textos y números de cada paso."""
    irrigated = bool(req.irrigated)
    out: list[RotationStep] = []
    previous = current
    for slot in slots:
        c = slot.candidate
        if c is None:
            out.append(fallow_step(slot))
            continue
        sc = slot.sc
        if monoculture:
            reasons = ["Es lo que siembras hoy", *reasons_for(c, sc, current, current, req)[:2]]
            saving = 0.0
        else:
            reasons = reasons_for(c, sc, previous, current, req, country_name, c.crop.id in (popular or set()))
            saving = water_saving_pct(water_need(current, sc), c.water_need_mm)
        out.append(RotationStep(
            season=sc.season, crop_id=c.crop.id, score=c.score, reasons=reasons, water_saving_pct=saving,
            nitrogen_delta=c.crop.nitrogen_delta_kg_ha,
            risks=risks_for(c, sc, uncertainty.level == "high", slot.out_of_season, irrigated, soil),
            planting_window=planting_window(c.cycle) if c.cycle else "—",
            irrigation_mm=round(c.irrigation_mm),
        ))
        previous = c.crop
    return out


def describe(sid: str, steps: list[RotationStep], slots: list[Slot], base: tuple[float, float, float, int, int],
             organic_matter: str | None, priority: Priority) -> Strategy:
    """Números y textos de una estrategia. `base` = (agua, riego, nitrógeno, suelo, ciclos) de «Seguir como hoy»."""
    water, irrigation, nitrogen = impact(slots)
    seq = [s.crop for s in slots]
    soil_h = soil_health_index(seq, organic_matter)
    bare = sum(c is None for c in seq)
    b_water, b_irr, b_n, b_soil, b_cycles = base
    cycles = sum(c is not None for c in seq)
    benefits: list[str] = []
    tradeoffs: list[str] = []
    if sid == "current":
        benefits.append("Ya conoces el cultivo, tienes el equipo y sabes dónde venderlo")
    else:
        if irrigation < b_irr:
            benefits.append(f"{b_irr - irrigation:.0f} mm menos de riego que seguir como hoy")
        elif cycles > b_cycles > 0 and irrigation / cycles < b_irr / b_cycles:
            # Más ciclos gastan más en total; por ciclo puede ser más eficiente (comparación justa)
            benefits.append(f"Menos riego por ciclo: ~{irrigation / cycles:.0f} mm contra "
                            f"~{b_irr / b_cycles:.0f} mm de seguir como hoy")
        if nitrogen > b_n:
            benefits.append(f"Balance de nitrógeno {nitrogen - b_n:.0f} kg/ha mejor que seguir como hoy (estimado)")
        if soil_h > b_soil:
            benefits.append(f"Salud del suelo de {b_soil} a {soil_h} / 100 (estimado)")
        if water > b_water:
            tradeoffs.append(f"Usa {water - b_water:.0f} mm más de agua en total: hay más ciclos de cultivo")
    # Misma regla que la rotación y el índice de suelo: se comparan cultivos consecutivos (el barbecho no cuenta)
    families = [family_of(c) for c in seq if c is not None]
    repeats = any(a == b for a, b in zip(families, families[1:]))
    if repeats:
        tradeoffs.append("Repite familia botánica: plagas y enfermedades se acumulan")
    elif len(families) >= 2:
        benefits.append("Cada ciclo cambia de familia botánica: corta ciclos de plagas")
    if bare:
        tradeoffs.append(f"{bare} temporada(s) sin cultivo: deja rastrojo o una cobertura para evitar erosión")
    seen = {t.split(":")[0] for t in tradeoffs}
    for risk in (r for s in steps for r in s.risks):
        key = risk.split(":")[0]  # «Requiere riego: …7 %» y «…1 %» son el mismo aviso
        if key in seen or (repeats and risk.startswith("Misma familia")) or len(tradeoffs) >= MAX_TRADEOFFS:
            continue
        seen.add(key)
        tradeoffs.append(risk)
    evidence = []
    for slot in slots:
        c = slot.candidate
        if c is None or c.cycle is None:
            continue
        evidence.append(
            f"{c.crop.name}, siembra {planting_window(c.cycle).lower()} (ciclo {cycle_span(c.cycle)}): necesita "
            f"~{c.water_need_mm:.0f} mm (FAO-56, ET₀ {slot.sc.et0_method}) y la lluvia efectiva aporta "
            f"~{c.cycle.effective_rain_mm:.0f} mm (NASA POWER)")
    return Strategy(
        id=sid, title=STRATEGY_TITLE[sid], is_current=sid == "current", is_recommended=sid == priority,
        steps=steps, water_mm=water, irrigation_mm=irrigation, nitrogen_kg_ha=nitrogen, soil_health=soil_h,
        bare_seasons=bare, why=STRATEGY_WHY[sid],
        benefits=benefits or ["Resultados parecidos a seguir como hoy"], tradeoffs=tradeoffs, evidence=evidence,
    )


def merge_duplicates(strategies: list[Strategy]) -> list[Strategy]:
    """Si dos prioridades dan los mismos cultivos, se muestran como una sola («Ahorrar agua · Regenerar el suelo»)."""
    out: list[Strategy] = []
    for s in strategies:
        firma = [(x.season, x.crop_id) for x in s.steps]
        twin = next((o for o in out if [(x.season, x.crop_id) for x in o.steps] == firma), None)
        if twin is None:
            out.append(s)
        else:
            twin.title = f"{twin.title} · {s.title}"
            twin.is_recommended = twin.is_recommended or s.is_recommended
    return out


# ---------------------------------------------------------------- función principal


def local_checks_for(slots: list[Slot], current: CropParams, req: AnalysisRequest,
                     detected_soil: DetectedSoil | None, uncertainty: Uncertainty) -> list[str]:
    """Qué confirmar con productores o un agrónomo de la zona antes de cambiar la rotación (máx. 5)."""
    checks = ["Confirma las fechas de siembra y las variedades con productores o el extensionista de tu zona."]
    if (req.soil is None or req.soil.ph is None) and detected_soil is not None:
        checks.append("Haz un análisis de suelo: la textura y el pH vienen de un modelo global de unos 250 m, "
                      "no de tu parcela.")
    crops = [s.crop for s in slots if s.crop is not None]
    for c in crops:
        if c.family == "legume":
            checks.append(f"Revisa que haya semilla e inoculante de {c.name.lower()} en tu zona antes de sembrarlo.")
            break
    if any(changes_system(c, current) for c in crops):
        checks.append("Algún cultivo cambia tu sistema de producción: confirma que tienes equipo, mano de obra "
                      "y comprador.")
    if uncertainty.level == "high" and not req.irrigated:
        checks.append("La lluvia varía mucho entre años: ten un plan por si el temporal falla.")
    empty = next((SEASON_LABEL[s.sc.season] for s in slots if s.crop is None), None)
    if empty:
        checks.append(f"Planea cómo cubrir el suelo en {empty} (rastrojo o una cobertura).")
    checks.append("Pregunta qué plagas y enfermedades son comunes en tu zona para estos cultivos.")
    return checks[:5]


def recommend(data: ClimateData, crops: list[CropParams], req: AnalysisRequest, today: date,
              detected_soil: DetectedSoil | None = None, country_areas: dict[str, float] | None = None,
              country_name: str | None = None, country_nitrogen: dict[str, float] | None = None
              ) -> RecommendationResult:
    """`country_areas` = {crop_id: ha cosechadas al año} del país de la parcela (FAOSTAT). Solo se recomiendan
    cultivos que ahí se siembran; el cultivo actual del usuario puede ser cualquiera del catálogo.
    `country_nitrogen` = {crop_id: balance de N con el rendimiento del país}; reemplaza el valor del catálogo."""
    if country_nitrogen:
        crops = [c.model_copy(update={"nitrogen_delta_kg_ha": country_nitrogen[c.id]})
                 if c.id in country_nitrogen else c for c in crops]
    by_id = {c.id: c for c in crops}
    current = by_id[req.current_crop]  # el router ya validó que existe
    candidates = grown_in_country(crops, country_areas)
    popular = top_in_country(country_areas)
    uncertainty = uncertainty_for(data)
    # Lo que dijo el usuario manda; lo que falte se completa con SoilGrids
    soil = SoilInput(
        texture=req.soil.texture if req.soil else (detected_soil.texture if detected_soil else None),
        ph=(req.soil.ph if req.soil and req.soil.ph is not None else (detected_soil.ph if detected_soil else None)),
    )
    data = apply_shift(data, req.climate_shift)
    if req.climate_shift is not None:
        uncertainty = uncertainty.model_copy(update={"reason": uncertainty.reason + (
            f"; escenario hipotético: lluvia {req.climate_shift.rain_pct:+.0f} %, "
            f"temperatura {req.climate_shift.temp_c:+.1f} °C")})
    seasons = seasons_ahead(today, data)
    organic_matter = req.soil.organic_matter if req.soil else None

    # 1. «Seguir como hoy»: el cultivo actual cada vez que cabe y el clima lo permite; descanso donde no
    #    (p. ej. trigo en Mexicali: invierno sí, verano no). Así el impacto compara contra algo realista.
    base_slots = plan(candidates, seasons, req, current, soil, monoculture=True)
    base_numbers = (*impact(base_slots), soil_health_index([s.crop for s in base_slots], organic_matter),
                    sum(s.crop is not None for s in base_slots))
    # 2. Una rotación por prioridad (priority_factor cambia el puntaje). La elegida va primero, así al fusionar
    #    repetidas conserva su id.
    order = [req.priority, *[p for p in PRIORITIES if p != req.priority]]
    built = {p: plan(candidates, seasons, req.model_copy(update={"priority": p}), current, soil) for p in order}
    chosen = built[req.priority]
    rotation = rotation_steps(chosen, req, current, soil, uncertainty, country_name, popular)
    strategies = merge_duplicates([
        describe("current", rotation_steps(base_slots, req, current, soil, uncertainty, monoculture=True),
                 base_slots, base_numbers, organic_matter, req.priority),
        *[describe(p, rotation_steps(slots, req.model_copy(update={"priority": p}), current, soil, uncertainty,
                                     country_name, popular), slots, base_numbers, organic_matter, req.priority)
          for p, slots in built.items()],
    ])
    water_cur, irr_cur, n_cur, soil_cur, _ = base_numbers
    water_rec, irr_rec, n_rec = impact(chosen)

    return RecommendationResult(
        metrics=metrics_for(data, current),
        rotation=rotation,
        impact=[
            ImpactItem(label="Agua total del cultivo", unit="mm", current=water_cur, recommended=water_rec,
                       better_when="lower"),
            ImpactItem(label="Riego necesario", unit="mm", current=irr_cur, recommended=irr_rec, better_when="lower"),
            ImpactItem(label="Balance de nitrógeno (estimado)", unit="kg/ha", current=n_cur, recommended=n_rec,
                       better_when="higher"),
        ],
        soil_health=SoilHealth(current=soil_cur, recommended=soil_health_index([s.crop for s in chosen],
                                                                              organic_matter)),
        climate=[MonthlyClimate(month=MONTH_ABBR[p.month - 1], rain=round(p.rain_mm), temp=round(p.temp_c, 1))
                 for p in data.summary.monthly],
        uncertainty=uncertainty,
        strategies=strategies,
        local_checks=local_checks_for(chosen, current, req, detected_soil, uncertainty),
    )
