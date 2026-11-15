"""Catálogo de cultivos para el motor de reglas.

Fuente oficial: la tabla `crops` (la siembra `app/db/seed.py` desde `app/data/crops.json` al arrancar el
contenedor). `load_catalog(db)` la lee con `repositories.crops.list_all`. Sin sesión (`db=None`) se lee el
JSON directamente; eso solo lo usan scripts y pruebas.
"""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.repositories import crops as crops_repo
from app.schemas.analysis import CropRole, Season, SoilTexture

CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "crops.json"


class CropParams(BaseModel):
    """Un cultivo con los rangos que usa el motor de reglas (columnas de la tabla `crops`, §6)."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str
    name: str
    scientific_name: str = ""
    family: CropRole  # rol en la rotación
    botanical_family: str = ""  # vacío = se usa `family` para la regla de rotación
    temp_opt_min: float
    temp_opt_max: float
    temp_abs_min: float
    temp_abs_max: float
    frost_kill_c: float | None = Field(default=None, description="ECOCROP KTMP; None = sensible a helada (0 °C)")
    ph_min: float | None = None
    ph_max: float | None = None
    water_need_mm: float = Field(gt=0, description="Agua que necesita en un ciclo (FAO, valor típico)")
    kc_mid: float | None = Field(default=None, description="FAO-56: con ET₀ da el agua según el clima local")
    cycle_days: int = Field(gt=0)
    seasons: list[Season]
    soils: list[SoilTexture]
    nitrogen_delta_kg_ha: float = Field(description="Positivo = aporta nitrógeno al suelo")
    source: str


class CatalogUnavailableError(Exception):
    """No hay catálogo de cultivos utilizable. El router lo convierte en 503."""


_catalog_adapter = TypeAdapter(list[CropParams])


def load_catalog(db: Session | None = None) -> list[CropParams]:
    """Catálogo desde la BD (o desde el JSON si no hay sesión). Lanza `CatalogUnavailableError` → 503."""
    if db is None:
        return load_catalog_file()
    try:
        rows = crops_repo.list_all(db)
    except SQLAlchemyError as exc:
        db.rollback()
        raise CatalogUnavailableError("Catálogo de cultivos no disponible (error de base de datos)") from exc
    if not rows:
        raise CatalogUnavailableError("La tabla crops está vacía (corre: python -m app.db.seed)")
    try:
        return [CropParams.model_validate(row) for row in rows]
    except ValidationError as exc:
        raise CatalogUnavailableError(f"El catálogo de cultivos tiene errores de formato: {exc.error_count()}") from exc


def load_catalog_file(path: Path = CATALOG_PATH) -> list[CropParams]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CatalogUnavailableError("Catálogo de cultivos no disponible (falta app/data/crops.json)") from exc
    except json.JSONDecodeError as exc:
        raise CatalogUnavailableError("El catálogo de cultivos (crops.json) no es JSON válido") from exc
    try:
        crops = _catalog_adapter.validate_python(raw)
    except ValidationError as exc:
        raise CatalogUnavailableError(f"El catálogo de cultivos tiene errores de formato: {exc.error_count()}") from exc
    if not crops:
        raise CatalogUnavailableError("El catálogo de cultivos está vacío")
    return crops
