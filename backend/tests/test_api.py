"""Endpoints de punta a punta. NASA, el catálogo y la BD se reemplazan con datos falsos (monkeypatch).

Las pruebas contra PostgreSQL de verdad están en test_repositories.py.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.db.database import get_db
from app.main import app
from app.repositories import analyses as analyses_repo
from app.services import climate as climate_service
from app.services import crops as crops_service
from app.services.crops import CatalogUnavailableError
from app.services.nasa_power import NasaUnavailableError
from tests.conftest import make_climate

client = TestClient(app)


@pytest.fixture(autouse=True)
def bd_falsa(monkeypatch):
    """Sin PostgreSQL: get_db da None y analyses_repo guarda en una lista."""
    filas: list[SimpleNamespace] = []

    def create(db, *, geometry, lat, lon, area_ha, current_crop, priority, climate_summary, result, soil=None):
        fila = SimpleNamespace(id=len(filas) + 1, created_at=datetime.now(timezone.utc), geometry=geometry, lat=lat,
                               lon=lon, area_ha=area_ha, current_crop=current_crop, priority=priority, soil=soil,
                               climate_summary=climate_summary, result=result)
        filas.append(fila)
        return fila

    monkeypatch.setattr(analyses_repo, "create", create)
    monkeypatch.setattr(analyses_repo, "list_recent", lambda db, limit=20: list(reversed(filas))[:limit])
    monkeypatch.setattr(analyses_repo, "get", lambda db, id: next((f for f in filas if f.id == id), None))
    app.dependency_overrides[get_db] = lambda: None
    yield filas
    app.dependency_overrides.clear()

BODY = {
    "geometry": {"type": "Polygon",
                 "coordinates": [[[-116.61, 31.85], [-116.59, 31.85], [-116.59, 31.87], [-116.61, 31.85]]]},
    "currentCrop": "maize",
    "priority": "water",
}


def test_health_responde():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_coordenadas_invalidas_dan_422():
    r = client.get("/api/v1/climate", params={"lat": 120, "lon": 0})
    assert r.status_code == 422


def test_analisis_valida_el_body():
    r = client.post("/api/v1/analyses", json={"currentCrop": "maize"})
    assert r.status_code == 422


def test_poligono_sin_cerrar_da_422():
    abierto = [[[-116.61, 31.85], [-116.59, 31.85], [-116.59, 31.87], [-116.6, 31.86]]]
    body = {**BODY, "geometry": {"type": "Polygon", "coordinates": abierto}}
    assert client.post("/api/v1/analyses", json=body).status_code == 422


def falsear(monkeypatch, catalog):
    async def get_climate(lat, lon, today=None, db=None):
        return make_climate(lat=lat)

    monkeypatch.setattr(climate_service, "get_climate", get_climate)
    monkeypatch.setattr(crops_service, "load_catalog", lambda db=None: catalog)


def test_analisis_completo(monkeypatch, catalog):
    falsear(monkeypatch, catalog)
    r = client.post("/api/v1/analyses", json=BODY)
    assert r.status_code == 201, r.text
    data = r.json()
    # JSON en camelCase, como lo espera el frontend
    assert {"id", "createdAt", "areaHa", "location", "metrics", "rotation", "impact", "soilHealth", "climate",
            "uncertainty"} <= data.keys()
    assert len(data["rotation"]) == 3
    assert "cropId" in data["rotation"][0] and "waterSavingPct" in data["rotation"][0]
    assert data["areaHa"] > 0
    assert 31.85 < data["location"]["lat"] < 31.87


def test_analisis_se_guarda_y_se_lee(monkeypatch, catalog, bd_falsa):
    falsear(monkeypatch, catalog)
    creado = client.post("/api/v1/analyses", json=BODY).json()
    assert creado["id"] == "1"  # id de la BD (entero) como texto, según el contrato
    fila = bd_falsa[0]
    assert fila.current_crop == "maize" and fila.priority == "water"
    assert fila.geometry["type"] == "Polygon"
    assert "id" not in fila.result and "rotation" in fila.result
    assert fila.climate_summary["period"] == "2016-2025"

    # El detalle devuelve exactamente lo mismo que el POST
    detalle = client.get(f"/api/v1/analyses/{creado['id']}")
    assert detalle.status_code == 200
    assert detalle.json() == creado


def test_historial(monkeypatch, catalog):
    falsear(monkeypatch, catalog)
    primero = client.post("/api/v1/analyses", json=BODY).json()
    segundo = client.post("/api/v1/analyses", json={**BODY, "priority": "nitrogen"}).json()
    r = client.get("/api/v1/analyses", params={"limit": 10})
    assert r.status_code == 200
    historial = r.json()
    assert [h["id"] for h in historial] == [segundo["id"], primero["id"]]  # más reciente primero
    h = historial[0]
    assert {"id", "createdAt", "location", "areaHa", "currentCrop", "priority", "rotationCrops"} == h.keys()
    assert h["priority"] == "nitrogen"
    assert h["rotationCrops"] == [paso["cropId"] for paso in segundo["rotation"]]


def test_historial_limit_fuera_de_rango_da_422():
    assert client.get("/api/v1/analyses", params={"limit": 0}).status_code == 422
    assert client.get("/api/v1/analyses", params={"limit": 101}).status_code == 422


@pytest.mark.parametrize("id_", ["999", "abc", "0", "-1", "99999999999", "²"])
def test_analisis_inexistente_da_404(id_):
    r = client.get(f"/api/v1/analyses/{id_}")
    assert r.status_code == 404
    assert r.json() == {"detail": "Análisis no encontrado"}


def test_cultivo_desconocido_da_422(monkeypatch, catalog):
    falsear(monkeypatch, catalog)
    r = client.post("/api/v1/analyses", json={**BODY, "currentCrop": "papaya"})
    assert r.status_code == 422
    assert "papaya" in r.json()["detail"]


def test_nasa_caida_da_503(monkeypatch, catalog):
    async def falla(lat, lon, today=None, db=None):
        raise NasaUnavailableError("caído")

    monkeypatch.setattr(climate_service, "get_climate", falla)
    monkeypatch.setattr(crops_service, "load_catalog", lambda db=None: catalog)
    r = client.post("/api/v1/analyses", json=BODY)
    assert r.status_code == 503
    assert r.json() == {"detail": "NASA POWER no disponible"}


def test_sin_catalogo_da_503(monkeypatch):
    def falta(db=None):
        raise CatalogUnavailableError("Catálogo de cultivos no disponible (falta app/data/crops.json)")

    monkeypatch.setattr(crops_service, "load_catalog", falta)
    assert client.post("/api/v1/analyses", json=BODY).status_code == 503
    assert client.get("/api/v1/crops").status_code == 503
