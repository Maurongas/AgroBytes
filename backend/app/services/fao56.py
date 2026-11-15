"""Fórmulas de FAO-56 y del manual FAO de riego. Funciones puras, sin red ni BD.

Fuentes (cada función cita su ecuación):
- Allen, R. G., Pereira, L. S., Raes, D. y Smith, M. (1998). *Crop evapotranspiration — Guidelines for computing
  crop water requirements*. FAO Irrigation and Drainage Paper 56. https://www.fao.org/4/x0490e/x0490e00.htm
- Brouwer, C. y Heibloem, M. (1986). *Irrigation Water Management: Irrigation Water Needs*. FAO Training
  Manual 3, cap. 3, Tabla 6 (lluvia efectiva). https://www.fao.org/4/s2022e/s2022e03.htm
"""

import math
from datetime import date

SIGMA = 4.903e-9  # constante de Stefan-Boltzmann, MJ K⁻⁴ m⁻² día⁻¹
GSC = 0.0820  # constante solar, MJ m⁻² min⁻¹


# ---------------------------------------------------------------- radiación y humedad


def extraterrestrial_radiation(lat: float, month: int, day: int = 15) -> float:
    """Ra (MJ/m²/día) a mitad de mes. FAO-56 ec. 21 (Ra), 23 (dr), 24 (δ) y 25 (ωs)."""
    j = date(2021, month, day).timetuple().tm_yday
    phi = math.radians(lat)
    dr = 1 + 0.033 * math.cos(2 * math.pi * j / 365)
    delta = 0.409 * math.sin(2 * math.pi * j / 365 - 1.39)
    ws = math.acos(max(-1.0, min(1.0, -math.tan(phi) * math.tan(delta))))
    return 24 * 60 / math.pi * GSC * dr * (
        ws * math.sin(phi) * math.sin(delta) + math.cos(phi) * math.cos(delta) * math.sin(ws))


def saturation_vapour_pressure(t: float) -> float:
    """e°(T) en kPa. FAO-56 ec. 11."""
    return 0.6108 * math.exp(17.27 * t / (t + 237.3))


def vapour_pressure_slope(t: float) -> float:
    """Δ en kPa/°C. FAO-56 ec. 13."""
    return 4098 * saturation_vapour_pressure(t) / (t + 237.3) ** 2


def atmospheric_pressure(z: float) -> float:
    """P en kPa a z metros sobre el nivel del mar. FAO-56 ec. 7."""
    return 101.3 * ((293 - 0.0065 * z) / 293) ** 5.26


def rh_min_from_dewpoint(t_max: float, t_dew: float) -> float:
    """Humedad relativa mínima (%) con el punto de rocío: e°(Tdew) / e°(Tmax) × 100 (FAO-56, cap. 6)."""
    return max(0.0, min(100.0, 100 * saturation_vapour_pressure(t_dew) / saturation_vapour_pressure(t_max)))


# ---------------------------------------------------------------- ET₀


def et0_hargreaves(t_mean: float, t_max: float, t_min: float, ra: float) -> float:
    """ET₀ (mm/día) solo con temperatura. FAO-56 ec. 52. Plan B cuando faltan humedad, viento o radiación."""
    return max(0.0, 0.0023 * (t_mean + 17.8) * math.sqrt(max(0.0, t_max - t_min)) * ra * 0.408)


def et0_penman_monteith(t_max: float, t_min: float, t_dew: float, u2: float, rs: float, ra: float,
                        z: float, g: float = 0.0) -> float:
    """ET₀ FAO Penman-Monteith (mm/día), el método de referencia de FAO-56 (ec. 6).

    t_max, t_min, t_dew en °C; u2 = viento a 2 m (m/s); rs = radiación solar (MJ/m²/día); ra = radiación
    extraterrestre (MJ/m²/día); z = altitud (m); g = flujo de calor del suelo (MJ/m²/día).
    """
    t_mean = (t_max + t_min) / 2  # FAO-56 recomienda Tmedia = (Tmax + Tmin) / 2 para estas ecuaciones
    es = (saturation_vapour_pressure(t_max) + saturation_vapour_pressure(t_min)) / 2  # ec. 12
    ea = min(es, saturation_vapour_pressure(t_dew))  # ec. 14
    delta = vapour_pressure_slope(t_mean)
    gamma = 0.665e-3 * atmospheric_pressure(z)  # ec. 8
    rso = (0.75 + 2e-5 * z) * ra  # ec. 37
    rns = (1 - 0.23) * rs  # ec. 38, albedo 0.23 del pasto de referencia
    ratio = min(1.0, rs / rso) if rso > 0 else 0.5
    rnl = (SIGMA * ((t_max + 273.16) ** 4 + (t_min + 273.16) ** 4) / 2
           * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * ratio - 0.35))  # ec. 39
    rn = rns - rnl  # ec. 40
    num = 0.408 * delta * (rn - g) + gamma * 900 / (t_mean + 273) * u2 * (es - ea)
    den = delta + gamma * (1 + 0.34 * u2)
    return max(0.0, num / den)


def monthly_soil_heat_flux(t_prev_month: float, t_next_month: float) -> float:
    """G (MJ/m²/día) de un mes con la temperatura media del mes anterior y del siguiente. FAO-56 ec. 43."""
    return 0.07 * (t_next_month - t_prev_month)


# ---------------------------------------------------------------- lluvia efectiva

# FAO Training Manual 3, cap. 3, Tabla 6: lluvia del mes P (mm) → lluvia efectiva Pe (mm)
_EFFECTIVE_RAIN_TABLE: tuple[tuple[float, float], ...] = (
    (0, 0), (10, 0), (20, 2), (30, 8), (40, 14), (50, 20), (60, 26), (70, 32), (80, 39), (90, 47), (100, 55),
    (110, 63), (120, 71), (130, 79), (140, 87), (150, 95), (160, 103), (170, 111), (180, 119), (190, 127),
    (200, 135), (210, 143), (220, 151), (230, 159), (240, 167), (250, 175),
)
_TABLE_SLOPE_ABOVE = 0.8  # la tabla sube 8 mm por cada 10 mm desde 80 mm; se mantiene esa pendiente arriba de 250


def effective_rain(monthly_rain_mm: float) -> float:
    """Lluvia efectiva del mes (mm): la parte que aprovecha el cultivo. Interpolación lineal de la Tabla 6."""
    p = max(0.0, monthly_rain_mm)
    table = _EFFECTIVE_RAIN_TABLE
    if p >= table[-1][0]:
        return table[-1][1] + _TABLE_SLOPE_ABOVE * (p - table[-1][0])
    for (p0, e0), (p1, e1) in zip(table, table[1:]):
        if p <= p1:
            return e0 + (e1 - e0) * (p - p0) / (p1 - p0)
    return 0.0  # inalcanzable


# ---------------------------------------------------------------- coeficiente de cultivo (Kc)


def adjust_kc_for_climate(kc: float, u2: float, rh_min: float, height_m: float) -> float:
    """Ajuste de Kc mid (y de Kc end si ≥ 0.45) al clima del lugar. FAO-56 ec. 62 y 65.

    Las tablas de FAO-56 son para clima subhúmedo (HRmín ≈ 45 %, viento ≈ 2 m/s). Con clima seco y ventoso
    el cultivo transpira más que eso. FAO-56 limita la fórmula a 1 ≤ u2 ≤ 6, 20 ≤ HRmín ≤ 80, 0.1 ≤ h ≤ 10.
    """
    u2 = min(6.0, max(1.0, u2))
    rh_min = min(80.0, max(20.0, rh_min))
    h = min(10.0, max(0.1, height_m))
    return kc + (0.04 * (u2 - 2) - 0.004 * (rh_min - 45)) * (h / 3) ** 0.3


def kc_on_day(day: float, total_days: float, stages: tuple[float, float, float, float],
              kc_ini: float, kc_mid: float, kc_end: float) -> float:
    """Kc del día `day` (0 = siembra) con la curva de 4 etapas de FAO-56 (fig. 25, ec. 66).

    `stages` = fracción del ciclo de cada etapa (inicial, desarrollo, media, final), de la Tabla 11.
    Inicial: Kc ini constante · desarrollo: sube en línea recta · media: Kc mid · final: baja hasta Kc end.
    """
    total = sum(stages)
    l_ini, l_dev, l_mid, _ = (s / total * total_days for s in stages)
    if day < l_ini:
        return kc_ini
    if day < l_ini + l_dev:
        return kc_ini + (day - l_ini) / l_dev * (kc_mid - kc_ini)
    if day < l_ini + l_dev + l_mid:
        return kc_mid
    l_late = total_days - (l_ini + l_dev + l_mid)
    return kc_mid + (day - l_ini - l_dev - l_mid) / l_late * (kc_end - kc_mid) if l_late > 0 else kc_end
