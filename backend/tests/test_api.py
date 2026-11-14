"""Endpoints de punta a punta. NASA y el catálogo se reemplazan con datos falsos (monkeypatch)."""

from fastapi.testclient import TestClient

from app.main import app
from app.services import climate as climate_service
from app.services import crops as crops_service
from app.services.crops import CatalogUnavailableError
from app.services.nasa_power import NasaUnavailableError
from tests.conftest import make_climate

client = TestClient(app)

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
    async def get_climate(lat, lon, today=None):
        return make_climate(lat=lat)

    monkeypatch.setattr(climate_service, "get_climate", get_climate)
    monkeypatch.setattr(crops_service, "load_catalog", lambda: catalog)


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


def test_cultivo_desconocido_da_422(monkeypatch, catalog):
    falsear(monkeypatch, catalog)
    r = client.post("/api/v1/analyses", json={**BODY, "currentCrop": "papaya"})
    assert r.status_code == 422
    assert "papaya" in r.json()["detail"]


def test_nasa_caida_da_503(monkeypatch, catalog):
    async def falla(lat, lon, today=None):
        raise NasaUnavailableError("caído")

    monkeypatch.setattr(climate_service, "get_climate", falla)
    monkeypatch.setattr(crops_service, "load_catalog", lambda: catalog)
    r = client.post("/api/v1/analyses", json=BODY)
    assert r.status_code == 503
    assert r.json() == {"detail": "NASA POWER no disponible"}


def test_sin_catalogo_da_503(monkeypatch):
    def falta():
        raise CatalogUnavailableError("Catálogo de cultivos no disponible (falta app/data/crops.json)")

    monkeypatch.setattr(crops_service, "load_catalog", falta)
    assert client.post("/api/v1/analyses", json=BODY).status_code == 503
    assert client.get("/api/v1/crops").status_code == 503
