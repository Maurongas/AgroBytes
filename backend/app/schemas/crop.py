"""Contrato de GET /api/v1/crops. Ver docs/ARQUITECTURA.md §5 y §6."""

from typing import Literal

from app.schemas.analysis import Season, SoilTexture
from app.schemas.base import CamelModel


class Crop(CamelModel):
    id: str
    name: str
    family: Literal["cereal", "legume", "vegetable", "cover"]
    seasons: list[Season]
    soils: list[SoilTexture]
    water_need_mm: float
    nitrogen_delta_kg_ha: float
