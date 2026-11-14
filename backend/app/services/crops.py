"""Catálogo de cultivos para el motor de reglas.

Hoy se lee de `app/data/crops.json` (dueño: DBA, formato en ARQUITECTURA §6). Cuando exista la tabla
`crops`, `load_catalog` pasará a usar `repositories.crops.list_all(db)`; `CropParams` acepta también
objetos ORM (`from_attributes=True`), así que el motor de reglas no cambia.
"""

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

from app.schemas.analysis import Season, SoilTexture

CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "crops.json"


class CropParams(BaseModel):
    """Un cultivo con los rangos que usa el motor de reglas (columnas de la tabla `crops`, §6)."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str
    name: str
    family: Literal["cereal", "legume", "vegetable", "cover"]
    temp_opt_min: float
    temp_opt_max: float
    temp_abs_min: float
    temp_abs_max: float
    water_need_mm: float = Field(gt=0, description="Agua que necesita en un ciclo")
    cycle_days: int = Field(gt=0)
    seasons: list[Season]
    soils: list[SoilTexture]
    nitrogen_delta_kg_ha: float = Field(description="Positivo = aporta nitrógeno al suelo")
    source: str


class CatalogUnavailableError(Exception):
    """No hay catálogo de cultivos utilizable. El router lo convierte en 503."""


_catalog_adapter = TypeAdapter(list[CropParams])


def load_catalog(path: Path = CATALOG_PATH) -> list[CropParams]:
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
