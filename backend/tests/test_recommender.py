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
        body["soil"] = {"texture": soil}
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
    assert [i.label for i in r.impact] == ["Balance hídrico", "Riego necesario", "Nitrógeno en suelo (estimado)"]
    assert [m.id for m in r.metrics] == ["soilMoisture", "rain90d", "tempMean", "solarRadiation"]
    assert all(len(m.series) == 12 for m in r.metrics)
    assert len(r.climate) == 12 and r.climate[0].month == "Ene"
    # Con prioridad "ahorrar agua", la rotación necesita menos riego que repetir maíz
    riego = r.impact[1]
    assert riego.recommended < riego.current


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
    con_franco = recommender.evaluate(tomate, sc, req(soil="loam"), maiz, 600)
    con_arena = recommender.evaluate(tomate, sc, req(soil="sandy"), maiz, 600)
    assert con_arena.score < con_franco.score
