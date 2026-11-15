"""Región de trabajo (México, EE. UU. y Canadá), país de la parcela y tamaño permitido. Ver ARQUITECTURA §7.

La herramienta está calibrada para Norteamérica (docs/ALCANCE-GEOGRAFICO.md): el catálogo y la lista de cultivos
que se siembran en cada país (FAOSTAT) solo cubren esos tres países. Contornos: app/data/region.json (Natural
Earth 1:50m simplificado a ~2 km; lo genera research/build_region.py). Por esa simplificación se acepta un punto
que caiga hasta 0.05° (~5 km) fuera del contorno, para no rechazar parcelas en la costa.

Tamaño: el clima se pide en UN punto (el centroide; malla de NASA POWER ~55 km) y el suelo en otro, así que una
parcela enorme no tiene un solo clima ni un solo suelo.

Espejo exacto en el frontend: frontend/src/lib/region.ts (mismo region.json, mismas constantes).
"""

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.services.geo import Ring

REGION_PATH = Path(__file__).resolve().parents[1] / "data" / "region.json"
REGION_NAME = "México, Estados Unidos o Canadá"

# Superficie permitida por parcela (hectáreas)
MIN_AREA_HA = 0.1  # 1 000 m²: menos que eso es un huerto, no una parcela
MAX_AREA_HA = 500.0  # 5 km²: más grande ya no comparte un solo clima/suelo; divídela en parcelas
# Margen fuera del contorno (grados) que compensa la simplificación de la costa
EDGE_TOLERANCE_DEG = 0.05


@dataclass(frozen=True)
class Country:
    code: str  # ISO 3166-1 alfa-2
    name: str
    rings: tuple[tuple[tuple[float, float], ...], ...]  # anillos exteriores [(lon, lat), ...]
    bboxes: tuple[tuple[float, float, float, float], ...]  # (min_lon, min_lat, max_lon, max_lat) por anillo


@lru_cache(maxsize=1)
def countries() -> tuple[Country, ...]:
    data = json.loads(REGION_PATH.read_text(encoding="utf-8"))
    result = []
    for code, c in data["countries"].items():
        rings = tuple(tuple((p[0], p[1]) for p in ring) for ring in c["rings"])
        bboxes = tuple((min(p[0] for p in r), min(p[1] for p in r), max(p[0] for p in r), max(p[1] for p in r))
                       for r in rings)
        result.append(Country(code, c["name"], rings, bboxes))
    return tuple(result)


def _in_ring(lon: float, lat: float, ring) -> bool:
    """Ray casting: cuenta cuántas veces una semirrecta hacia el este cruza el contorno (impar = dentro)."""
    inside = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > lat) != (y2 > lat):
            if lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def _distance_to_ring(lon: float, lat: float, ring) -> float:
    """Distancia (en grados, plano) del punto al borde del anillo."""
    best = math.inf
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        dx, dy = x2 - x1, y2 - y1
        t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((lon - x1) * dx + (lat - y1) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(lon - (x1 + t * dx), lat - (y1 + t * dy)))
    return best


def country_of(lon: float, lat: float) -> Country | None:
    """País que contiene el punto (o el más cercano a menos de EDGE_TOLERANCE_DEG). None = fuera de la región."""
    nearest, nearest_d = None, EDGE_TOLERANCE_DEG
    for c in countries():
        for ring, (x0, y0, x1, y1) in zip(c.rings, c.bboxes):
            t = EDGE_TOLERANCE_DEG
            if not (x0 - t <= lon <= x1 + t and y0 - t <= lat <= y1 + t):
                continue
            if _in_ring(lon, lat, ring):
                return c
            d = _distance_to_ring(lon, lat, ring)
            if d <= nearest_d:
                nearest, nearest_d = c, d
    return nearest


def validate_parcel(ring: Ring, area_ha: float) -> str | None:
    """Mensaje de error para el usuario, o None si la parcela es válida."""
    if not all(country_of(lon, lat) for lon, lat in ring):
        return f"La parcela debe estar completamente dentro de {REGION_NAME}"
    if area_ha < MIN_AREA_HA:
        return f"La parcela es muy pequeña ({area_ha:.2f} ha); el mínimo es {MIN_AREA_HA:g} ha"
    if area_ha > MAX_AREA_HA:
        return (f"La parcela es muy grande ({area_ha:,.0f} ha); el máximo es {MAX_AREA_HA:,.0f} ha. "
                "Divídela en parcelas más pequeñas")
    return None
