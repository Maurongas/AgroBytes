from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
