"""Contrato de GET /api/v1/crops. Ver docs/ARQUITECTURA.md §5 y §6."""

from app.schemas.analysis import CropRole, Season, SoilTexture
from app.schemas.base import CamelModel


class Crop(CamelModel):
    id: str
    name: str
    scientific_name: str
    family: CropRole
    botanical_family: str
    seasons: list[Season]
    soils: list[SoilTexture]
    water_need_mm: float
    cycle_days: int
    nitrogen_delta_kg_ha: float
    source: str
