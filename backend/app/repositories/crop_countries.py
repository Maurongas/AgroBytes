"""Repositorio de crop_countries (superficie cosechada por cultivo y país)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crop_country import CropCountry


def areas_by_country(db: Session, country_code: str) -> dict[str, float]:
    """{crop_id: ha cosechadas al año} del país. Vacío si el país no tiene datos."""
    stmt = select(CropCountry).where(CropCountry.country_code == country_code)
    return {row.crop_id: row.harvested_area_ha for row in db.scalars(stmt)}


def nitrogen_by_country(db: Session, country_code: str) -> dict[str, float]:
    """{crop_id: balance de N (kg/ha por ciclo) con el rendimiento del país}. Solo cultivos con dato."""
    stmt = select(CropCountry).where(CropCountry.country_code == country_code,
                                     CropCountry.nitrogen_kg_ha.is_not(None))
    return {row.crop_id: row.nitrogen_kg_ha for row in db.scalars(stmt)}
