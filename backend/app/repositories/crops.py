"""Repositorio del catálogo de cultivos."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.crop import Crop


def list_all(db: Session) -> list[Crop]:
    """Lista todos los cultivos ordenados alfabéticamente por nombre."""
    stmt = select(Crop).order_by(Crop.name.asc())
    return list(db.scalars(stmt).all())


def get_by_id(db: Session, crop_id: str) -> Crop | None:
    """Obtiene un cultivo por su identificador (ej. 'maize', 'bean')."""
    return db.get(Crop, crop_id)
