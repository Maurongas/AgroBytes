"""Contrato de GET /api/v1/climate. Ver docs/ARQUITECTURA.md §5."""

from pydantic import Field

from app.schemas.base import CamelModel


class MonthlyClimatePoint(CamelModel):
    month: int = Field(ge=1, le=12)
    temp_c: float
    temp_max_c: float = Field(description="Máxima diaria promedio del mes: T2M + T2M_RANGE/2 "
                                          "(sin T2M_RANGE, registros viejos: el extremo T2M_MAX)")
    temp_min_c: float = Field(description="Mínima diaria promedio del mes: T2M − T2M_RANGE/2 "
                                          "(sin T2M_RANGE, registros viejos: el extremo T2M_MIN)")
    temp_max_abs_c: float | None = Field(default=None, description="Máxima más alta del mes (T2M_MAX mensual)")
    temp_min_abs_c: float | None = Field(default=None, description="Mínima más baja del mes (T2M_MIN mensual)")
    rain_mm: float = Field(description="mm/mes (POWER entrega mm/día: multiplicar por los días del mes)")
    soil_moisture_root: float = Field(ge=0, le=1, description="GWETROOT, fracción 0-1")
    solar_radiation: float = Field(description="ALLSKY_SFC_SW_DWN en kWh/m²/día (POWER da MJ/m²/día; ÷ 3.6)")
    # Opcionales: registros viejos del caché no los traen (entonces ET₀ se calcula con Hargreaves)
    dewpoint_c: float | None = Field(default=None, description="T2MDEW, punto de rocío (°C)")
    wind_ms: float | None = Field(default=None, description="WS2M, viento a 2 m (m/s)")
    frost_days: float | None = Field(default=None, description="FROST_DAYS, días con helada en el mes (promedio)")


class ClimateSummary(CamelModel):
    lat: float
    lon: float
    elevation_m: float | None = Field(default=None, description="Altitud de la celda de NASA POWER (m)")
    source: str = Field(default="NASA POWER (community=AG)")
    period: str = Field(examples=["2015-2024"])
    temp_mean_c: float
    rain_annual_mm: float
    rain_cv_pct: float = Field(description="Coeficiente de variación de la lluvia anual → incertidumbre")
    soil_moisture_root: float = Field(ge=0, le=1)
    monthly: list[MonthlyClimatePoint] = Field(min_length=12, max_length=12)
