"""Repositorio de análisis agronómicos con soporte espacial PostGIS."""

import json
from typing import Any

from geoalchemy2 import Geography
from sqlalchemy import Text, cast, func, select
from sqlalchemy.orm import Session

from app.models.analysis import Analysis


def create(
    db: Session,
    *,
    geometry: dict[str, Any] | str,
    lat: float,
    lon: float,
    area_ha: float,
    current_crop: str,
    priority: str,
    climate_summary: dict[str, Any],
    result: dict[str, Any],
    soil: dict[str, Any] | None = None,
    irrigated: bool | None = None,
) -> Analysis:
    """Inserta un análisis convirtiendo el polígono GeoJSON a Geography(POLYGON, 4326)."""
    if isinstance(geometry, dict) and geometry.get("type") == "Feature":
        geometry = geometry["geometry"]

    geojson_str = geometry if isinstance(geometry, str) else json.dumps(geometry)
    geom_expr = cast(
        func.ST_SetSRID(func.ST_GeomFromGeoJSON(cast(geojson_str, Text)), 4326),
        Geography(geometry_type="POLYGON", srid=4326),
    )

    analysis = Analysis(
        geom=geom_expr,
        lat=lat,
        lon=lon,
        area_ha=area_ha,
        current_crop=current_crop,
        priority=priority,
        soil=soil,
        irrigated=irrigated,
        climate_summary=climate_summary,
        result=result,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def list_recent(db: Session, limit: int = 20) -> list[Analysis]:
    """Devuelve los análisis más recientes ordenados de nuevo a antiguo."""
    stmt = (
        select(Analysis)
        .order_by(Analysis.created_at.desc(), Analysis.id.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def get(db: Session, analysis_id: int) -> Analysis | None:
    """Obtiene un análisis por su ID o None si no existe."""
    return db.get(Analysis, analysis_id)
