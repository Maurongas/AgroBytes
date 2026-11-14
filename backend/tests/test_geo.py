import math

import pytest

from app.services import geo

# Cuadrado de 0.01° × 0.01° en el ecuador ≈ 1112 m × 1112 m ≈ 123.6 ha
CUADRADO_ECUADOR = [[[0, 0], [0.01, 0], [0.01, 0.01], [0, 0.01], [0, 0]]]


def test_anillo_quita_el_punto_de_cierre():
    assert geo.outer_ring(CUADRADO_ECUADOR) == [(0, 0), (0.01, 0), (0.01, 0.01), (0, 0.01)]


def test_centroide_devuelve_lat_lon():
    lat, lon = geo.centroid([(-116.61, 31.85), (-116.59, 31.85), (-116.59, 31.87), (-116.61, 31.87)])
    assert lat == pytest.approx(31.86)
    assert lon == pytest.approx(-116.60)


def test_area_cuadrado_en_el_ecuador():
    lado_m = geo.EARTH_RADIUS_M * math.radians(0.01)
    assert geo.area_ha(geo.outer_ring(CUADRADO_ECUADOR)) == pytest.approx(lado_m**2 / 10_000, rel=1e-3)


def test_area_se_reduce_con_la_latitud():
    # El mismo cuadrado en grados mide la mitad a 60° (cos 60° = 0.5)
    norte = [(0, 60), (0.01, 60), (0.01, 60.01), (0, 60.01)]
    ecuador = geo.outer_ring(CUADRADO_ECUADOR)
    assert geo.area_ha(norte) == pytest.approx(geo.area_ha(ecuador) * 0.5, rel=1e-3)


def test_area_no_depende_del_sentido_de_giro():
    ring = geo.outer_ring(CUADRADO_ECUADOR)
    assert geo.area_ha(ring) == pytest.approx(geo.area_ha(ring[::-1]))
