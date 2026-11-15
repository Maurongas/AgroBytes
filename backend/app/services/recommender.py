"""Motor de reglas: clima + catálogo + petición → rotación, impacto, métricas e incertidumbre.

Función PURA: no lee BD, no llama a internet, no consulta la hora (la fecha llega como parámetro).
Así se prueba con datos inventados y cada número de la respuesta se explica con ARQUITECTURA §7.
"""

from dataclasses import dataclass
from datetime import date

from app.schemas.analysis import (
    AnalysisRequest,
    ImpactItem,
    MonthlyClimate,
    NasaMetric,
    RotationStep,
    Season,
    SoilHealth,
    Status,
    Uncertainty,
    UncertaintyLevel,
)
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

# Pesos del puntaje (suman 1)
W_TEMP, W_WATER, W_SOIL, W_PRIORITY = 0.40, 0.30, 0.15, 0.15
SAME_FAMILY_PENALTY = 0.7
BASE_NITROGEN_KG_HA = 40
FROST_MARGIN_C = 3


@dataclass(frozen=True)
class RecommendationResult:
    metrics: list[NasaMetric]
    rotation: list[RotationStep]
    impact: list[ImpactItem]
    soil_health: SoilHealth
    climate: list[MonthlyClimate]
    uncertainty: Uncertainty


@dataclass(frozen=True)
class SeasonClimate:
    season: Season
    months: tuple[int, int, int]
    temp_c: float  # promedio de los 3 meses
    rain_mm: float  # suma de los 3 meses


@dataclass(frozen=True)
class Candidate:
    crop: CropParams
    score: int
    temp_f: float
    water_f: float
    soil_f: float
    priority_f: float
    same_family: bool


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


def season_climate(season: Season, data: ClimateData) -> SeasonClimate:
    months = season_months(season, data.summary.lat)
    by_month = {p.month: p for p in data.summary.monthly}
    return SeasonClimate(
        season=season,
        months=months,
        temp_c=sum(by_month[m].temp_c for m in months) / 3,
        rain_mm=sum(by_month[m].rain_mm for m in months),
    )


# ---------------------------------------------------------------- factores (0 a 1)


def temperature_factor(temp: float, crop: CropParams) -> float:
    """1 dentro del rango óptimo; baja en línea recta hasta 0 en los límites absolutos."""
    if crop.temp_opt_min <= temp <= crop.temp_opt_max:
        return 1.0
    if temp < crop.temp_opt_min:
        span = crop.temp_opt_min - crop.temp_abs_min
        return max(0.0, (temp - crop.temp_abs_min) / span) if span > 0 else 0.0
    span = crop.temp_abs_max - crop.temp_opt_max
    return max(0.0, (crop.temp_abs_max - temp) / span) if span > 0 else 0.0


def water_factor(rain_mm: float, crop: CropParams) -> float:
    """Qué fracción del agua del ciclo cubre la lluvia de la temporada."""
    return min(1.0, rain_mm / crop.water_need_mm)


def soil_factor(req: AnalysisRequest, crop: CropParams) -> float:
    if req.soil is None or req.soil.texture in crop.soils:
        return 1.0
    return 0.5


def priority_factor(req: AnalysisRequest, crop: CropParams, max_water_need: float) -> float:
    if req.priority == "water":
        return 1 - crop.water_need_mm / max_water_need
    if req.priority == "nitrogen":
        return {"legume": 1.0, "cover": 0.7}.get(crop.family, 0.0)
    return 1.0 if crop.family in ("cereal", "vegetable") else 0.5  # yield


def evaluate(crop: CropParams, sc: SeasonClimate, req: AnalysisRequest, previous: CropParams,
             max_water_need: float) -> Candidate:
    t = temperature_factor(sc.temp_c, crop)
    w = water_factor(sc.rain_mm, crop)
    s = soil_factor(req, crop)
    p = priority_factor(req, crop, max_water_need)
    raw = 100 * (W_TEMP * t + W_WATER * w + W_SOIL * s + W_PRIORITY * p)
    same_family = crop.family == previous.family
    if same_family:
        raw *= SAME_FAMILY_PENALTY  # regla de rotación: cambiar de familia corta plagas y enfermedades
    return Candidate(crop, max(0, min(100, round(raw))), t, w, s, p, same_family)


def choose(crops: list[CropParams], sc: SeasonClimate, req: AnalysisRequest, previous: CropParams,
           max_water_need: float) -> tuple[Candidate, bool]:
    """Mejor cultivo de la temporada. Devuelve (candidato, fuera_de_temporada).

    1) Cultivos de esa temporada que toleran su temperatura. 2) Si no hay, cualquiera que la tolere.
    3) Si tampoco, el mejor aunque no la tolere (con riesgo). Nunca repite el cultivo anterior.
    """
    others = [c for c in crops if c.id != previous.id] or crops
    evaluated = [evaluate(c, sc, req, previous, max_water_need) for c in others]
    in_season = [e for e in evaluated if sc.season in e.crop.seasons and e.temp_f > 0]
    pool = in_season or [e for e in evaluated if e.temp_f > 0] or evaluated
    best = max(pool, key=lambda e: (e.score, -e.crop.water_need_mm))
    return best, not in_season


# ---------------------------------------------------------------- textos


def reasons_for(c: Candidate, sc: SeasonClimate, previous: CropParams, current: CropParams,
                req: AnalysisRequest) -> list[str]:
    reasons: list[str] = []
    label = SEASON_LABEL[sc.season]
    if c.temp_f == 1:
        reasons.append(f"La temperatura de {label} ({sc.temp_c:.0f} °C) está en su rango óptimo")
    elif c.temp_f >= 0.6:
        reasons.append(f"Tolera la temperatura de {label} ({sc.temp_c:.0f} °C)")
    if c.water_f >= 0.9:
        reasons.append(f"La lluvia de {label} ({sc.rain_mm:.0f} mm) cubre casi toda el agua que necesita")
    saving = water_saving_pct(current, c.crop)
    if saving >= 10:
        reasons.append(f"Necesita {saving:.0f} % menos agua que {current.name.lower()}")
    if c.crop.family == "legume":
        reasons.append("Leguminosa: fija nitrógeno en el suelo (estimado)")
    elif c.crop.family == "cover":
        reasons.append("Cultivo de cobertura: protege el suelo de la erosión")
    elif req.priority == "yield" and c.priority_f == 1:
        reasons.append("Cultivo de alto valor productivo")
    if not c.same_family:
        reasons.append(f"Cambia de familia respecto a {previous.name.lower()}: corta el ciclo de plagas")
    return reasons[:3] or ["Es la mejor opción disponible para esta temporada"]


def risks_for(c: Candidate, sc: SeasonClimate, high_uncertainty: bool, out_of_season: bool) -> list[str]:
    risks: list[str] = []
    if sc.temp_c - c.crop.temp_abs_min < FROST_MARGIN_C:
        risks.append("Riesgo de helada")
    if c.temp_f == 0:
        risks.append("La temperatura está fuera del rango del cultivo")
    elif out_of_season:
        risks.append("No es su temporada habitual de siembra")
    if c.water_f < 0.6:
        risks.append(f"Requiere riego: la lluvia cubre ~{c.water_f * 100:.0f} % de lo que necesita")
    if c.same_family:
        risks.append("Misma familia que el cultivo anterior (más riesgo de plagas)")
    if high_uncertainty:
        risks.append("Lluvia muy variable entre años")
    return risks


def water_saving_pct(current: CropParams, crop: CropParams) -> float:
    return round(100 * (current.water_need_mm - crop.water_need_mm) / current.water_need_mm)


def planting_window(months: tuple[int, int, int]) -> str:
    return f"{MONTH_ABBR[months[0] - 1]} – {MONTH_ABBR[months[1] - 1]}"


# ---------------------------------------------------------------- impacto y salud del suelo


def impact(seq: list[CropParams], seasons: list[SeasonClimate]) -> tuple[float, float, float]:
    """(balance hídrico, riego necesario, nitrógeno estimado) para una secuencia de 3 cultivos."""
    balance = sum(sc.rain_mm - c.water_need_mm for c, sc in zip(seq, seasons))
    irrigation = sum(max(0.0, c.water_need_mm - sc.rain_mm) for c, sc in zip(seq, seasons))
    # Sin tope en 0: con el catálogo real casi todo resta nitrógeno y el tope dejaba ambos valores en 0.
    # Negativo = la rotación consume más de lo que el suelo tenía al inicio (hay que fertilizar).
    nitrogen = BASE_NITROGEN_KG_HA + sum(c.nitrogen_delta_kg_ha for c in seq)
    return round(balance), round(irrigation), round(nitrogen)


def soil_health_index(seq: list[CropParams]) -> int:
    """Índice estimado 0-100: premia leguminosas y coberturas, castiga repetir familia."""
    score = 50
    score += 10 * sum(c.family == "legume" for c in seq)
    score += 8 * sum(c.family == "cover" for c in seq)
    score -= 10 * sum(a.family == b.family for a, b in zip(seq, seq[1:]))
    return max(0, min(100, score))


# ---------------------------------------------------------------- métricas NASA


def _status_by_threshold(value: float, danger_below: float, warn_below: float) -> Status:
    if value < danger_below:
        return "danger"
    if value < warn_below:
        return "warn"
    return "ok"


def metrics_for(data: ClimateData, current: CropParams) -> list[NasaMetric]:
    s, r = data.summary, data.recent
    monthly = s.monthly
    period_src = f"NASA POWER · {s.period}"
    recent_src = f"NASA POWER · {r.start:%d/%m}–{r.end:%d/%m/%Y}"

    # 1. Humedad del suelo (raíces): últimos 30 días
    sm_status = _status_by_threshold(r.soil_moisture_30d, 0.3, 0.5)
    sm_meaning = {
        "danger": "Suelo seco: las raíces tienen poca agua",
        "warn": f"Algo seco para {current.name.lower()}",
        "ok": "Humedad adecuada en la zona de raíces",
    }[sm_status]

    # 2. Lluvia de los últimos 90 días contra lo normal para esas fechas
    if r.rain_90d_normal_mm < 10:
        rain_status: Status = "ok"
        rain_meaning = f"Temporada normalmente seca (lo normal es {r.rain_90d_normal_mm:.0f} mm)"
    else:
        diff_pct = (r.rain_90d_mm - r.rain_90d_normal_mm) / r.rain_90d_normal_mm * 100
        rain_status = "danger" if diff_pct < -30 else "warn" if diff_pct < -10 else "ok"
        rain_meaning = f"{abs(diff_pct):.0f} % {'menos' if diff_pct < 0 else 'más'} que el promedio"

    # 3. Temperatura de los últimos 30 días contra lo normal
    diff_t = r.temp_30d_c - r.temp_30d_normal_c
    temp_status: Status = "danger" if diff_t > 2 else "warn" if diff_t > 1 else "ok"
    temp_meaning = f"{abs(diff_t):.1f} °C {'sobre' if diff_t >= 0 else 'bajo'} lo normal"

    # 4. Radiación solar: promedio anual (informativa)
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
    s = data.summary
    levels: list[UncertaintyLevel] = ["low", "medium", "high"]
    i = 0 if s.rain_cv_pct < 15 else 1 if s.rain_cv_pct <= 30 else 2
    reason = f"La lluvia anual varía {s.rain_cv_pct:.0f} % entre años (NASA POWER {s.period})"
    if s.soil_moisture_root < 0.3:
        i = min(2, i + 1)
        reason += "; además el suelo suele estar seco"
    return Uncertainty(level=levels[i], reason=reason)


# ---------------------------------------------------------------- función principal


def recommend(data: ClimateData, crops: list[CropParams], req: AnalysisRequest, today: date) -> RecommendationResult:
    by_id = {c.id: c for c in crops}
    current = by_id[req.current_crop]  # el router ya validó que existe
    max_water_need = max(c.water_need_mm for c in crops)
    uncertainty = uncertainty_for(data)

    seasons = [season_climate(s, data) for s in next_seasons(today, data.summary.lat)]
    rotation: list[RotationStep] = []
    chosen: list[CropParams] = []
    previous = current
    for sc in seasons:
        best, out_of_season = choose(crops, sc, req, previous, max_water_need)
        rotation.append(RotationStep(
            season=sc.season,
            crop_id=best.crop.id,
            score=best.score,
            reasons=reasons_for(best, sc, previous, current, req),
            water_saving_pct=water_saving_pct(current, best.crop),
            nitrogen_delta=best.crop.nitrogen_delta_kg_ha,
            risks=risks_for(best, sc, uncertainty.level == "high", out_of_season),
            planting_window=planting_window(sc.months),
        ))
        chosen.append(best.crop)
        previous = best.crop

    baseline = [current] * len(seasons)  # "seguir igual": repetir el cultivo actual
    bal_cur, irr_cur, n_cur = impact(baseline, seasons)
    bal_rec, irr_rec, n_rec = impact(chosen, seasons)

    return RecommendationResult(
        metrics=metrics_for(data, current),
        rotation=rotation,
        impact=[
            ImpactItem(label="Balance hídrico", unit="mm", current=bal_cur, recommended=bal_rec, better_when="higher"),
            ImpactItem(label="Riego necesario", unit="mm", current=irr_cur, recommended=irr_rec, better_when="lower"),
            ImpactItem(label="Balance de nitrógeno (estimado)", unit="kg/ha", current=n_cur, recommended=n_rec,
                       better_when="higher"),
        ],
        soil_health=SoilHealth(current=soil_health_index(baseline), recommended=soil_health_index(chosen)),
        climate=[MonthlyClimate(month=MONTH_ABBR[p.month - 1], rain=round(p.rain_mm), temp=round(p.temp_c, 1))
                 for p in data.summary.monthly],
        uncertainty=uncertainty,
    )
