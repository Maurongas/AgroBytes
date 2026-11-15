"""Centroide y área de la parcela dibujada (funciones puras, sin dependencias extra). Ver ARQUITECTURA §7.

GeoJSON usa coordenadas [longitud, latitud] en grados. Para medir el área en metros se proyecta el
polígono a un plano local (proyección equirectangular centrada en la parcela) y se aplica la fórmula
del "shoelace" (fórmula del área de Gauss). Para parcelas de pocos km el error es < 1 %.
"""

import math

EARTH_RADIUS_M = 6_371_008.8  # radio medio de la Tierra

Ring = list[tuple[float, float]]  # [(lon, lat), ...] sin repetir el punto de cierre


def outer_ring(coordinates: list[list[list[float]]]) -> Ring:
    """Anillo exterior del Polygon (el primero), sin el último punto (que repite al primero)."""
    ring = coordinates[0]
    return [(p[0], p[1]) for p in ring[:-1]]


def centroid(ring: Ring) -> tuple[float, float]:
    """Promedio de los vértices → (lat, lon). Suficiente para pedir el clima (la malla de NASA es de 0.5°)."""
    lon = sum(p[0] for p in ring) / len(ring)
    lat = sum(p[1] for p in ring) / len(ring)
    return lat, lon


def area_ha(ring: Ring) -> float:
    """Área en hectáreas (1 ha = 10 000 m²)."""
    lat0, lon0 = centroid(ring)
    cos_lat0 = math.cos(math.radians(lat0))
    # Proyección local: grados → metros respecto al centroide
    xy = [
        (
            EARTH_RADIUS_M * math.radians(lon - lon0) * cos_lat0,
            EARTH_RADIUS_M * math.radians(lat - lat0),
        )
        for lon, lat in ring
    ]
    # Shoelace: ½ |Σ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|
    twice_area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(xy, xy[1:] + xy[:1]))
    return abs(twice_area) / 2 / 10_000
