"""
nitrogen.py — Balance parcial de nitrógeno de un cultivo (kg N/ha por ciclo): N fijado − N que sale con la cosecha.

Lo usan build_crop_countries.py (balance por país con el rendimiento real de FAOSTAT) y build_crops.py (valor por
defecto del catálogo). El motor (services/recommender.py) solo lee los números ya calculados: no hay supuestos
escondidos en tiempo de ejecución.

Fuentes
-------
1. N extraído por tonelada de producto cosechado (kg N/t): Ludemann, C. I. et al. (2024). "A global FAOSTAT
   reference database of cropland nutrient budgets and nutrient use efficiency (1961–2020): nitrogen, phosphorus and
   potassium". Earth System Science Data 16, 525–541. https://doi.org/10.5194/essd-16-525-2024 — Suplemento,
   Tabla S3 (coeficientes por producto FAOSTAT; son los que usa FAOSTAT para su balance de nutrientes).
   Excepción, algodón: la Tabla S3 da 56 kg N/t de "Seed cotton", que implicaría 5.6 % de N en algodón con
   semilla (la semilla tiene ~3.5–4 % y es ~60 % del peso). Se usa en su lugar Univ. of Missouri Extension G4256
   (35–40 lb N en el algodón con semilla de una paca de 480 lb de fibra; con ~38 % de rendimiento de fibra son
   ~1 260 lb de algodón con semilla → 37.5 / 1 263 ≈ 30 kg N/t).
2. N fijado por leguminosas de grano: modelo de Herridge, D. F. et al. (2022). "Global estimates of nitrogen
   fixation in grain legumes" (Plant and Soil), con los coeficientes resumidos en la Tabla S2 del suplemento de
   Ludemann et al. (2024):
       fijación = Y × (c + d·Y/HI) / HI × BGF × Ndfa,   HI = a + b·ln(Y),   Y = rendimiento de grano (t/ha)
   (BGF = N total de la planta / N aéreo; Ndfa = fracción del N que viene del aire).
3. Veza como abono verde (no se cosecha: todo el N fijado se queda): 107–131 kg N/ha fijados por veza común,
   Kebede, E. (2021). Frontiers in Sustainable Food Systems 5:767998, Tabla 1 → punto medio 119.

Qué NO incluye (por eso se etiqueta "estimado"): pérdidas por lixiviación o volatilización, fertilización, N de
residuos de la cosecha anterior ni mineralización de la materia orgánica. Es el "balance parcial" (entradas por
fijación − salidas por cosecha) que se usa para comparar rotaciones, no una recomendación de fertilización.
"""

from __future__ import annotations

import math

# Producto FAOSTAT (código) → kg N por tonelada de producto (Ludemann et al. 2024, Tabla S3)
N_REMOVAL_KG_T: dict[str, float] = {
    "56": 12,  # Maize (corn)
    "83": 15,  # Sorghum
    "15": 21,  # Wheat
    "44": 18,  # Barley
    "75": 22,  # Oats
    "176": 42,  # Beans, dry
    "236": 59,  # Soya beans
    "191": 28,  # Chick peas, dry
    "187": 38,  # Peas, dry
    "417": 17,  # Peas, green
    "205": 34,  # Vetches
    "270": 31,  # Rapeseed
    "280": 30,  # Safflower seed
    "328": 30,  # Seed cotton → Missouri Extension G4256 (ver nota arriba; la Tabla S3 dice 56)
    "388": 1.4,  # Tomatoes
    "401": 2.2,  # Chillies and peppers, green
    "689": 12,  # Chillies and peppers, dry
    "116": 2.5,  # Potatoes
    "403": 2.6,  # Onions and shallots, dry
    "402": 2.6,  # Onions and shallots, green
    "394": 2.7,  # Pumpkins, squash and gourds
}

# Herridge et al. (2022) vía Ludemann et al. (2024), Tabla S2: (a, b, c, d, BGF, Ndfa)
# Ndfa de soya: 0.61 para Norteamérica (EE. UU., Canadá y México).
BNF_COEFFICIENTS: dict[str, tuple[float, float, float, float, float, float]] = {
    "soy": (0.2775, 0.1178, 0.03913, -0.00118, 1.4, 0.61),
    "bean": (0.2839, 0.0804, 0.025, 0.0, 1.4, 0.38),  # common bean
    "chickpea": (0.2839, 0.0804, 0.019, 0.0, 2.0, 0.62),
    "pea": (0.2839, 0.0804, 0.025, 0.0, 1.4, 0.62),  # "all other grain legumes"
}

VETCH_GREEN_MANURE_N = 119.0  # Kebede (2021): veza común 107–131 kg N/ha → punto medio


def fixation_kg_ha(crop_id: str, grain_yield_t_ha: float) -> float:
    """N fijado (kg/ha) por una leguminosa de grano con el modelo de Herridge et al. (2022). 0 si no es leguminosa."""
    coef = BNF_COEFFICIENTS.get(crop_id)
    if coef is None or grain_yield_t_ha <= 0:
        return 0.0
    a, b, c, d, bgf, ndfa = coef
    hi = a + b * math.log(grain_yield_t_ha)
    if hi <= 0:
        return 0.0
    shoot_n = c + d * grain_yield_t_ha / hi  # fracción de N en la parte aérea
    return grain_yield_t_ha / hi * shoot_n * bgf * ndfa * 1000  # t N → kg N


def removal_kg_ha(production_t_by_item: dict[str, float], area_ha: float) -> float:
    """N que sale con la cosecha (kg/ha): Σ (coeficiente × producción) / superficie."""
    if area_ha <= 0:
        return 0.0
    return sum(N_REMOVAL_KG_T[item] * t for item, t in production_t_by_item.items()) / area_ha


def balance_kg_ha(crop_id: str, role: str, grain_yield_t_ha: float | None, removal: float) -> float:
    """Balance parcial de N (kg/ha por ciclo). `grain_yield_t_ha` = rendimiento de grano seco (para la fijación)."""
    if role == "cover":  # abono verde: se incorpora al suelo, no se cosecha
        return VETCH_GREEN_MANURE_N
    return fixation_kg_ha(crop_id, grain_yield_t_ha or 0.0) - removal
