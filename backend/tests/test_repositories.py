"""Pruebas de integración de los repositorios contra PostgreSQL + PostGIS."""

from datetime import datetime, timedelta, timezone

import pytest

from app.db.database import SessionLocal
from app.db.seed import seed_crops
from app.models.analysis import Analysis
from app.models.climate_cache import ClimateCache
from app.repositories import analyses, climate_cache, crops


@pytest.fixture()
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_crops_list_and_get(db):
    seed_crops(db)
    all_crops = crops.list_all(db)
    ids = {c.id for c in all_crops}

    assert {"maize", "wheat", "soy", "bean", "chile", "tomato", "oat", "sorghum"}.issubset(ids)

    maize = crops.get_by_id(db, "maize")
    assert maize is not None
    assert maize.family == "cereal"


def test_climate_cache_upsert_and_expiration(db):
    lat_g = climate_cache.snap_to_grid(31.86)    # -> 32.0
    lon_g = climate_cache.snap_to_grid(-116.60)  # -> -116.5
    period = "2015-2024-test"

    try:
        saved = climate_cache.upsert(db, lat_g, lon_g, period, {"temp_mean_c": 19.4})
        assert saved.id is not None

        hit = climate_cache.get_valid(db, lat_g, lon_g, period, max_days=30)
        assert hit is not None
        assert hit.payload["temp_mean_c"] == 19.4

        updated = climate_cache.upsert(db, lat_g, lon_g, period, {"temp_mean_c": 20.1})
        assert updated.id == saved.id
        assert updated.payload["temp_mean_c"] == 20.1

        updated.fetched_at = datetime.now(timezone.utc) - timedelta(days=40)
        db.commit()

        expired = climate_cache.get_valid(db, lat_g, lon_g, period, max_days=30)
        assert expired is None
    finally:
        db.query(ClimateCache).filter(ClimateCache.period == period).delete()
        db.commit()


def test_analyses_create_get_and_list_recent(db):
    polygon = {
        "type": "Polygon",
        "coordinates": [
            [
                [-116.62, 31.86],
                [-116.61, 31.86],
                [-116.61, 31.87],
                [-116.62, 31.87],
                [-116.62, 31.86],
            ]
        ],
    }

    created = analyses.create(
        db,
        geometry=polygon,
        lat=31.865,
        lon=-116.615,
        area_ha=10.5,
        current_crop="maize",
        priority="water",
        soil={"texture": "loam", "ph": 6.8},
        climate_summary={"temp_mean_c": 19.2, "rain_annual_mm": 280.0},
        result={"id": "test-1", "areaHa": 10.5},
    )

    try:
        assert created.id is not None

        fetched = analyses.get(db, created.id)
        assert fetched is not None
        assert fetched.current_crop == "maize"
        assert fetched.area_ha == 10.5

        recent = analyses.list_recent(db, limit=5)
        assert any(item.id == created.id for item in recent)
    finally:
        db.query(Analysis).filter(Analysis.id == created.id).delete()
        db.commit()


def test_analyses_por_dispositivo_y_borrado(db):
    polygon = {"type": "Polygon",
               "coordinates": [[[-115.36, 32.51], [-115.34, 32.51], [-115.34, 32.53], [-115.36, 32.51]]]}
    comunes = dict(geometry=polygon, lat=32.52, lon=-115.35, area_ha=2.0, current_crop="maize", priority="water",
                   climate_summary={"period": "test"}, result={"rotation": []})
    mio = analyses.create(db, device_id="prueba-repo-aaa", **comunes)
    ajeno = analyses.create(db, device_id="prueba-repo-bbb", **comunes)
    try:
        assert mio.device_id == "prueba-repo-aaa"
        assert [a.id for a in analyses.list_recent(db, 100, device_id="prueba-repo-aaa")] == [mio.id]
        analyses.delete(db, mio)
        assert analyses.get(db, mio.id) is None
        assert analyses.get(db, ajeno.id) is not None
    finally:
        db.query(Analysis).filter(Analysis.device_id.in_(["prueba-repo-aaa", "prueba-repo-bbb"])).delete()
        db.commit()
