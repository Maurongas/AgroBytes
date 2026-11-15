import pytest

from app.services import geo, region


@pytest.mark.parametrize("lugar, lon, lat, pais", [
    ("Ensenada", -116.60, 31.86, "MX"),
    ("Valle de Mexicali", -115.10, 32.30, "MX"),
    ("Bajío (Celaya)", -100.81, 20.52, "MX"),
    ("Chiapas (Tuxtla)", -93.12, 16.75, "MX"),
    ("Iowa", -93.60, 41.86, "US"),
    ("Valle Central de California", -120.50, 37.00, "US"),
    ("Saskatchewan", -106.60, 52.10, "CA"),
    ("Ontario (Guelph)", -80.25, 43.55, "CA"),
])
def test_pais_de_cada_lugar(lugar, lon, lat, pais):
    c = region.country_of(lon, lat)
    assert c is not None and c.code == pais, lugar


@pytest.mark.parametrize("lugar, lon, lat", [
    ("Guatemala", -90.50, 14.60),
    ("Cuba (La Habana)", -82.38, 23.13),
    ("Océano Pacífico", -125.0, 30.0),
    ("Golfo de México", -91.0, 25.0),
    ("Madrid", -3.70, 40.42),
])
def test_lugares_fuera_de_la_region(lugar, lon, lat):
    assert region.country_of(lon, lat) is None, lugar


def test_la_costa_se_acepta_aunque_el_contorno_este_simplificado():
    # Playa de Ensenada: el contorno simplificado (~2 km) puede dejarla fuera; la tolerancia de ~5 km la acepta
    assert region.country_of(-116.63, 31.84).code == "MX"


def cuadrado(lon, lat, lado_grados):
    return [(lon, lat), (lon + lado_grados, lat), (lon + lado_grados, lat + lado_grados), (lon, lat + lado_grados)]


def test_parcela_valida():
    ring = cuadrado(-116.61, 31.85, 0.01)  # ~1 km × 1.1 km ≈ 105 ha
    assert region.validate_parcel(ring, geo.area_ha(ring)) is None


def test_parcela_con_un_vertice_fuera():
    ring = [(-116.61, 31.85), (-116.59, 31.85), (-118.5, 31.87)]  # un vértice en el Pacífico
    assert "dentro de México, Estados Unidos o Canadá" in region.validate_parcel(ring, 50)


def test_parcela_muy_grande():
    ring = cuadrado(-115.5, 32.0, 0.5)  # ~47 km × 55 km
    assert "muy grande" in region.validate_parcel(ring, geo.area_ha(ring))


def test_parcela_muy_pequena():
    ring = cuadrado(-116.61, 31.85, 0.0001)  # ~10 m × 11 m
    assert "muy pequeña" in region.validate_parcel(ring, geo.area_ha(ring))
