"""Contrato de GET /api/v1/climate. Ver docs/ARQUITECTURA.md §5."""

from pydantic import Field

from app.schemas.base import CamelModel


class MonthlyClimatePoint(CamelModel):
    month: int = Field(ge=1, le=12)
    temp_c: float
    temp_max_c: float = Field(description="Promedio de la máxima de cada mes (T2M_MAX)")
    temp_min_c: float = Field(description="Promedio de la mínima de cada mes (T2M_MIN)")
    rain_mm: float = Field(description="mm/mes (POWER entrega mm/día: multiplicar por los días del mes)")
    soil_moisture_root: float = Field(ge=0, le=1, description="GWETROOT, fracción 0-1")
    solar_radiation: float = Field(description="ALLSKY_SFC_SW_DWN en kWh/m²/día (POWER da MJ/m²/día; ÷ 3.6)")


class ClimateSummary(CamelModel):
    lat: float
    lon: float
    source: str = Field(default="NASA POWER (community=AG)")
    period: str = Field(examples=["2015-2024"])
    temp_mean_c: float
    rain_annual_mm: float
    rain_cv_pct: float = Field(description="Coeficiente de variación de la lluvia anual → incertidumbre")
    soil_moisture_root: float = Field(ge=0, le=1)
    monthly: list[MonthlyClimatePoint] = Field(min_length=12, max_length=12)
