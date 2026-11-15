"""Las fórmulas de FAO-56 contra los ejemplos resueltos del propio manual (Allen et al. 1998)."""

import importlib.util
from pathlib import Path

import pytest

from app.services import fao56


def test_presion_y_constante_psicrometrica_ejemplo_2():
    # FAO-56 ejemplo 2: a 1 800 m, P = 81.8 kPa y γ = 0.054 kPa/°C
    p = fao56.atmospheric_pressure(1800)
    assert p == pytest.approx(81.8, abs=0.1)
    assert 0.665e-3 * p == pytest.approx(0.054, abs=0.001)


def test_presion_de_vapor_ejemplo_3():
    # FAO-56 ejemplo 3: Tmax 24.5 °C, Tmin 15 °C → e°(Tmax) 3.075, e°(Tmin) 1.705, es 2.39 kPa
    assert fao56.saturation_vapour_pressure(24.5) == pytest.approx(3.075, abs=0.005)
    assert fao56.saturation_vapour_pressure(15) == pytest.approx(1.705, abs=0.005)


def test_radiacion_extraterrestre_ejemplo_8():
    # FAO-56 ejemplo 8: 20° S, 3 de septiembre → Ra = 32.2 MJ/m²/día
    assert fao56.extraterrestrial_radiation(-20, 9, day=3) == pytest.approx(32.2, abs=0.1)


def test_penman_monteith_mensual_ejemplo_17():
    """FAO-56 ejemplo 17 (Bangkok, abril, datos mensuales): ET₀ = 5.72 mm/día.
    Tmax 34.8, Tmin 25.6, ea 2.85 kPa (rocío ≈ 23.2 °C), u2 2 m/s, Rs 22.65 MJ (de n = 8.5 h), Ra 38.06,
    z = 2 m, G = 0.14 MJ/m²/día."""
    et0 = fao56.et0_penman_monteith(t_max=34.8, t_min=25.6, t_dew=23.22, u2=2.0, rs=22.65, ra=38.06, z=2, g=0.14)
    assert et0 == pytest.approx(5.72, abs=0.1)


def test_hargreaves_ejemplo_17_es_del_mismo_orden():
    # Hargreaves (ec. 52) con los mismos datos da un valor parecido (es el plan B)
    et0 = fao56.et0_hargreaves((34.8 + 25.6) / 2, 34.8, 25.6, 38.06)
    assert 4.5 < et0 < 6.5


def test_humedad_relativa_minima_con_rocio():
    # Si el rocío es igual a la máxima, el aire está saturado
    assert fao56.rh_min_from_dewpoint(20, 20) == pytest.approx(100)
    assert 20 < fao56.rh_min_from_dewpoint(35, 10) < 25


def test_lluvia_efectiva_tabla_6():
    # FAO Training Manual 3, Tabla 6
    assert fao56.effective_rain(0) == 0
    assert fao56.effective_rain(10) == 0
    assert fao56.effective_rain(100) == pytest.approx(55)
    assert fao56.effective_rain(75) == pytest.approx(35.5)  # entre 70 → 32 y 80 → 39
    assert fao56.effective_rain(250) == pytest.approx(175)
    assert fao56.effective_rain(300) == pytest.approx(215)  # misma pendiente (0.8) arriba de la tabla


def test_curva_kc_de_cuatro_etapas():
    etapas = (30, 40, 50, 30)  # maíz, Tabla 11
    kc = (0.3, 1.2, 0.35)
    assert fao56.kc_on_day(0, 150, etapas, *kc) == pytest.approx(0.3)
    assert fao56.kc_on_day(50, 150, etapas, *kc) == pytest.approx(0.75)  # mitad del desarrollo
    assert fao56.kc_on_day(90, 150, etapas, *kc) == pytest.approx(1.2)
    assert fao56.kc_on_day(149.999, 150, etapas, *kc) == pytest.approx(0.35, abs=0.01)


def test_ajuste_de_kc_por_clima():
    # Clima de referencia (HRmín 45 %, viento 2 m/s) → sin cambio; seco y ventoso → más alto; húmedo → más bajo
    assert fao56.adjust_kc_for_climate(1.2, 2.0, 45, 2.0) == pytest.approx(1.2)
    assert fao56.adjust_kc_for_climate(1.2, 4.0, 20, 2.0) > 1.2
    assert fao56.adjust_kc_for_climate(1.2, 1.0, 80, 2.0) < 1.2


# ---------------------------------------------------------------- research/nitrogen.py (modelo de N)


def _nitrogen():
    ruta = Path(__file__).resolve().parents[1] / "research" / "nitrogen.py"
    spec = importlib.util.spec_from_file_location("nitrogen", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_fijacion_de_soya_con_el_modelo_de_herridge():
    n = _nitrogen()
    # Soya 3.4 t/ha (EE. UU.): HI = 0.2775 + 0.1178·ln 3.4 = 0.422; N aéreo 2.96 % → ~204 kg N/ha fijados
    assert n.fixation_kg_ha("soy", 3.4) == pytest.approx(204, abs=3)
    # El grano saca 59 kg N/t × 3.4 t ≈ 200 → balance casi neutro (lo que reporta la literatura para la soya)
    assert abs(n.balance_kg_ha("soy", "legume", 3.4, 59 * 3.4)) < 10


def test_frijol_fija_poco_y_no_leguminosas_no_fijan():
    n = _nitrogen()
    assert n.fixation_kg_ha("bean", 0.74) < 45  # Ndfa 0.38: fijador pobre
    assert n.fixation_kg_ha("maize", 4.0) == 0
    assert n.balance_kg_ha("maize", "cereal", None, n.removal_kg_ha({"56": 3.9}, 1.0)) == pytest.approx(-46.8)
    assert n.balance_kg_ha("vetch", "cover", None, 0) == 119
