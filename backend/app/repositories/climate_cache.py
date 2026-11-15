"""Repositorio de caché climático en malla de 0.5° para NASA POWER."""

from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import and_, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.climate_cache import ClimateCache


def snap_to_grid(coord: float) -> float:
    """Redondea una coordenada (lat o lon) a la malla de 0.5° de NASA POWER."""
    return round(coord * 2.0) / 2.0


def get_valid(
    db: Session,
    lat_grid: float,
    lon_grid: float,
    period: str,
    max_days: int | None = None,
) -> ClimateCache | None:
    """Busca un registro de caché vigente para (lat_grid, lon_grid, period)."""
    ttl_days = settings.CLIMATE_CACHE_DAYS if max_days is None else max_days
    cutoff = datetime.now(timezone.utc) - timedelta(days=ttl_days)

    stmt = select(ClimateCache).where(
        and_(
            ClimateCache.lat_grid == lat_grid,
            ClimateCache.lon_grid == lon_grid,
            ClimateCache.period == period,
            ClimateCache.fetched_at >= cutoff,
        )
    )
    return db.scalars(stmt).first()


def upsert(
    db: Session,
    lat_grid: float,
    lon_grid: float,
    period: str,
    payload: dict[str, Any],
) -> ClimateCache:
    """Inserta o actualiza el caché climático y refresca fetched_at."""
    stmt = (
        insert(ClimateCache)
        .values(
            lat_grid=lat_grid,
            lon_grid=lon_grid,
            period=period,
            payload=payload,
            fetched_at=func.now(),
        )
        .on_conflict_do_update(
            index_elements=["lat_grid", "lon_grid", "period"],
            set_={
                "payload": payload,
                "fetched_at": func.now(),
            },
        )
        .returning(ClimateCache)
    )
    record = db.scalars(stmt).one()
    db.commit()
    db.refresh(record)
    return record
