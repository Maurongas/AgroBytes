"""Motor de reglas con clima y catálogo inventados (es una función pura: no necesita red ni BD)."""

from datetime import date

import pytest

from app.schemas.analysis import AnalysisRequest
from app.services import recommender
from tests.conftest import crop, make_climate

NOV = date(2026, 11, 14)


def req(current="maize", priority="water", soil=None) -> AnalysisRequest:
    body = {
        "geometry": {"type": "Polygon", "coordinates": [[[-116.61, 31.85], [-116.59, 31.85], [-116.59, 31.87],
                                                         [-116.61, 31.85]]]},
        "currentCrop": current,
        "priority": priority,
    }
    if soil:
        body["soil"] = soil if isinstance(soil, dict) else {"texture": soil}
    return AnalysisRequest.model_validate(body)


def test_temporadas_siguientes_norte_y_sur():
    assert recommender.next_seasons(NOV, lat=31.8) == ["winter", "spring", "summer"]
    # En el hemisferio sur noviembre es primavera
    assert recommender.next_seasons(NOV, lat=-33.4) == ["summer", "autumn", "winter"]
    assert recommender.season_months("winter", lat=-33.4) == (6, 7, 8)


def test_factor_temperatura():
    maiz = crop("maize", "cereal", (18, 32), (10, 42), 600, ["summer"], -30)
    assert recommender.temperature_factor(25, maiz) == 1
    assert recommender.temperature_factor(14, maiz) == pytest.approx(0.5)  # a medio camino entre 10 y 18
    assert recommender.temperature_factor(9, maiz) == 0
    assert recommender.temperature_factor(37, maiz) == pytest.approx(0.5)


def test_rotacion_tiene_3_pasos_validos(climate, catalog):
    r = recommender.recommend(climate, catalog, req(), NOV)
    assert [s.season for s in r.rotation] == ["winter", "spring", "summer"]
    ids = ["maize"] + [s.crop_id for s in r.rotation]
    assert all(a != b for a, b in zip(ids, ids[1:])), "nunca el mismo cultivo dos pasos seguidos"
    for step in r.rotation:
        assert 0 <= step.score <= 100
        assert step.reasons
    assert r.rotation[0].planting_window == "Dic – Ene"


def test_prioridad_nitrogeno_prefiere_leguminosas(climate, catalog):
    r = recommender.recommend(climate, catalog, req(priority="nitrogen"), NOV)
    assert "bean" in [s.crop_id for s in r.rotation]
    assert r.soil_health.recommended > r.soil_health.current


def test_impacto_y_metricas_en_orden_del_contrato(climate, catalog):
    r = recommender.recommend(climate, catalog, req(), NOV)
    assert [i.label for i in r.impact] == ["Agua total del cultivo", "Riego necesario",
                                         "Balance de nitrógeno (estimado)"]
    assert [m.id for m in r.metrics] == ["soilMoisture", "rain90d", "tempMean", "solarRadiation"]
    assert all(len(m.series) == 12 for m in r.metrics)
    assert len(r.climate) == 12 and r.climate[0].month == "Ene"
    # Con prioridad "ahorrar agua", la rotación necesita menos riego que repetir maíz
    agua, riego = r.impact[0], r.impact[1]
    assert riego.recommended < riego.current
    assert agua.better_when == "lower"
    # El agua total incluye la lluvia aprovechada: nunca es menor que el riego (antes era −riego en zonas áridas)
    assert agua.current >= riego.current and agua.recommended >= riego.recommended
    assert agua.current != -riego.current


def test_materia_organica_mueve_el_indice_de_suelo(climate, catalog):
    def salud(om):
        soil = {"texture": "loam", "organicMatter": om}
        return recommender.recommend(climate, catalog, req(soil=soil), NOV).soil_health
    base, baja, alta = salud("mid"), salud("low"), salud("high")
    assert baja.current == base.current - 10 and alta.current == base.current + 10
    assert alta.recommended - alta.current == base.recommended - base.current  # la rotación aporta lo mismo


def test_metricas_reflejan_datos_recientes(climate, catalog):
    m = {x.id: x for x in recommender.recommend(climate, catalog, req(), NOV).metrics}
    assert m["soilMoisture"].status == "danger"  # 0.25 < 0.3
    assert m["rain90d"].status == "danger"  # 10 mm vs 30 normales = -67 %
    assert m["rain90d"].meaning == "67 % menos que el promedio"
    assert m["tempMean"].status == "warn"  # +1.5 °C


def test_incertidumbre():
    assert recommender.uncertainty_for(make_climate(rain_cv=10)).level == "low"
    assert recommender.uncertainty_for(make_climate(rain_cv=20)).level == "medium"
    assert recommender.uncertainty_for(make_climate(rain_cv=38)).level == "high"
    # Suelo seco sube un nivel
    assert recommender.uncertainty_for(make_climate(rain_cv=10, soil_root=0.2)).level == "medium"


def test_suelo_incompatible_baja_el_puntaje(climate, catalog):
    tomate = next(c for c in catalog if c.id == "tomato")
    maiz = catalog[0]
    sc = recommender.season_climate("spring", climate)
    ctx = recommender.season_context(catalog, sc)
    con_franco = recommender.evaluate(tomate, sc, req(soil="loam"), maiz, ctx, recommender.SoilInput("loam", None))
    con_arena = recommender.evaluate(tomate, sc, req(soil="sandy"), maiz, ctx, recommender.SoilInput("sandy", None))
    assert con_arena.score < con_franco.score


# ---------------------------------------------------------------- reglas v2 (ECOCROP / FAO-56)


def clima_con(temps: list[float], amplitud: float = 8, lat: float = 31.86):
    """Clima inventado con temperaturas mensuales dadas (mínima = media − amplitud)."""
    base = make_climate(lat=lat)
    monthly = [p.model_copy(update={"temp_c": t, "temp_max_c": t + amplitud, "temp_min_c": t - amplitud})
               for p, t in zip(base.summary.monthly, temps)]
    return base.__class__(summary=base.summary.model_copy(update={"monthly": monthly}), recent=base.recent)


def test_barbecho_si_nada_tolera_el_invierno(catalog):
    # Invierno tipo Iowa: −6 °C de media, mínimas de −14 °C
    frio = clima_con([-6, -4, 2, 9, 15, 21, 24, 22, 17, 10, 3, -4])
    r = recommender.recommend(frio, catalog, req(), NOV)
    invierno = r.rotation[0]
    assert invierno.season == "winter" and invierno.crop_id == "fallow"
    assert invierno.score == 0 and "tolera" in invierno.reasons[0]
    assert all(s.crop_id != "fallow" for s in r.rotation[1:])


def test_helada_descarta_cultivos_sensibles():
    tomate = crop("tomato", "vegetable", (20, 27), (7, 35), 600, ["winter"], -90)
    avena = crop("oat", "cereal", (16, 20), (5, 30), 550, ["winter"], -55).model_copy(update={"frost_kill_c": -1})
    previo = crop("bean", "legume", (16, 25), (7, 32), 400, ["summer"], 18)
    suelo = recommender.SoilInput(None, None)
    cerca = recommender.SeasonClimate("winter", (12, 1, 2), temp_c=12, rain_mm=100, temp_min_c=0.5)
    ctx = recommender.season_context([tomate, avena], cerca)
    assert recommender.evaluate(tomate, cerca, req(), previo, ctx, suelo).frost_risk
    helada = recommender.SeasonClimate("winter", (12, 1, 2), temp_c=12, rain_mm=100, temp_min_c=-0.5)
    assert recommender.evaluate(tomate, helada, req(), previo, ctx, suelo).temp_f == 0  # mata al jitomate
    assert recommender.evaluate(avena, helada, req(), previo, ctx, suelo).temp_f > 0  # la avena aguanta −1 °C


def test_familia_botanica_castiga_solanaceas_seguidas():
    chile = crop("chile", "vegetable", (17, 30), (8, 35), 750, ["summer"], -70).model_copy(
        update={"botanical_family": "Solanaceae"})
    tomate = crop("tomato", "vegetable", (20, 27), (7, 35), 600, ["summer"], -90).model_copy(
        update={"botanical_family": "Solanaceae"})
    calabaza = crop("squash", "vegetable", (17, 30), (6, 40), 500, ["summer"], -40).model_copy(
        update={"botanical_family": "Cucurbitaceae"})
    sc = recommender.season_climate("summer", make_climate())
    ctx = recommender.season_context([tomate, calabaza], sc)
    suelo = recommender.SoilInput(None, None)
    assert recommender.evaluate(tomate, sc, req(), chile, ctx, suelo).same_family
    assert not recommender.evaluate(calabaza, sc, req(), chile, ctx, suelo).same_family


def test_ph_fuera_de_rango_baja_el_puntaje_y_avisa(climate):
    papa = crop("potato", "vegetable", (15, 25), (7, 30), 600, ["spring"], -80).model_copy(
        update={"ph_min": 5.0, "ph_max": 6.2})
    maiz = crop("maize", "cereal", (18, 33), (10, 47), 650, ["summer"], -104)
    sc = recommender.season_climate("spring", climate)
    ctx = recommender.season_context([papa], sc)
    alcalino_suelo = recommender.SoilInput("loam", 7.9)
    ok = recommender.evaluate(papa, sc, req(), maiz, ctx, recommender.SoilInput("loam", 6.0))
    alcalino = recommender.evaluate(papa, sc, req(), maiz, ctx, alcalino_suelo)
    assert ok.ph_ok and not alcalino.ph_ok and alcalino.score < ok.score
    riesgos = recommender.risks_for(alcalino, sc, False, False, False, alcalino_suelo)
    assert any("pH del suelo (7.9)" in r for r in riesgos)


def test_et0_hargreaves_razonable():
    # FAO-56 ejemplo 8: Ra a 20°S el 3 de septiembre = 32.2 MJ/m²/día
    assert recommender.extraterrestrial_radiation(-20, 9, day=3) == pytest.approx(32.2, abs=0.1)
    # Verano desértico (Mexicali) >> invierno costero (Ensenada)
    verano = recommender.et0_hargreaves(33, 42, 24, 32.5, 7)
    invierno = recommender.et0_hargreaves(14, 20, 8, 31.9, 1)
    assert 6 < verano < 10 and 1 < invierno < 3.5


def test_agua_depende_del_clima_si_hay_kc():
    algodon = crop("cotton", "industrial", (22, 36), (15, 42), 1000, ["summer"], -60).model_copy(
        update={"kc_mid": 1.18, "cycle_days": 188})
    caliente = recommender.SeasonClimate("summer", (6, 7, 8), 33, 5, 24, et0_mm_day=8)
    templado = recommender.SeasonClimate("summer", (6, 7, 8), 21, 5, 14, et0_mm_day=4)
    assert recommender.water_need(algodon, caliente) == pytest.approx(2 * recommender.water_need(algodon, templado))
    sin_kc = algodon.model_copy(update={"kc_mid": None})
    assert recommender.water_need(sin_kc, caliente) == 1000  # sin Kc → valor típico de FAO


def test_con_riego_no_se_queja_de_la_lluvia(climate, catalog):
    temporal = recommender.recommend(climate, catalog, req(), NOV)
    body = req().model_dump(by_alias=True) | {"irrigated": True}
    riego = recommender.recommend(climate, catalog, AnalysisRequest.model_validate(body), NOV)
    assert any("Requiere riego" in r for s in temporal.rotation for r in s.risks)
    assert not any("Requiere riego" in r for s in riego.rotation for r in s.risks)
    assert all(s.irrigation_mm >= 0 for s in riego.rotation)
