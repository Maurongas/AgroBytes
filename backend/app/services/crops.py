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

from app.repositories import crop_countries as crop_countries_repo
from app.repositories import crops as crops_repo
from app.schemas.analysis import CropRole, Season, SoilTexture

CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "crops.json"
COUNTRIES_PATH = CATALOG_PATH.with_name("crop_countries.json")


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
    water_need_mm: float = Field(gt=0, description="Agua que necesita en un ciclo (FAO, valor típico; plan B)")
    # Curva Kc de FAO-56 (Tablas 11 y 12). Sin kc_mid el motor usa water_need_mm; sin el resto, Kc constante.
    kc_ini: float | None = Field(default=None, description="FAO-56 Tabla 12, etapa inicial")
    kc_mid: float | None = Field(default=None, description="FAO-56 Tabla 12, etapa media")
    kc_end: float | None = Field(default=None, description="FAO-56 Tabla 12, al cosechar")
    crop_height_m: float | None = Field(default=None, description="FAO-56 Tabla 12, para ajustar Kc al clima")
    kc_stages: tuple[float, float, float, float] | None = Field(
        default=None, description="FAO-56 Tabla 11: fracción del ciclo de las etapas inicial/desarrollo/media/final")
    cycle_days: int = Field(gt=0)
    seasons: list[Season]
    soils: list[SoilTexture]
    nitrogen_delta_kg_ha: float = Field(description="Balance parcial de N por ciclo (estimado); positivo = aporta")
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


def load_country_areas(country_code: str, db: Session | None = None) -> dict[str, float]:
    """{crop_id: ha cosechadas al año en el país} (tabla crop_countries, FAOSTAT). Sin sesión, del JSON.

    Si no hay datos (tabla vacía o error de BD) devuelve {} y el motor recomienda sin filtrar por país: es mejor
    una recomendación sin ese filtro que un 503.
    """
    if db is None:
        try:
            data = json.loads(COUNTRIES_PATH.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        return {k: float(v) for k, v in data.get("countries", {}).get(country_code, {}).items()}
    try:
        return crop_countries_repo.areas_by_country(db, country_code)
    except SQLAlchemyError:
        db.rollback()
        return {}


def load_country_nitrogen(country_code: str, db: Session | None = None) -> dict[str, float]:
    """{crop_id: balance de N (kg/ha por ciclo)} con el rendimiento FAOSTAT del país. Sin dato → {} y el motor usa
    el valor por defecto del catálogo (`nitrogen_delta_kg_ha`)."""
    if db is None:
        try:
            data = json.loads(COUNTRIES_PATH.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        return {k: float(v) for k, v in data.get("nitrogen_kg_ha", {}).get(country_code, {}).items()}
    try:
        return crop_countries_repo.nitrogen_by_country(db, country_code)
    except SQLAlchemyError:
        db.rollback()
        return {}
