"""Datos inventados para probar sin internet ni catálogo real (crops.json es del DBA)."""

from datetime import date

import pytest

from app.schemas.climate import ClimateSummary, MonthlyClimatePoint
from app.services import climate as climate_service
from app.services.climate import ClimateData, RecentClimate
from app.services.crops import CropParams


def crop(id: str, family: str, opt: tuple[float, float], abs_: tuple[float, float], water: float,
         seasons: list[str], nitrogen: float, soils: list[str] | None = None) -> CropParams:
    return CropParams(
        id=id, name=id.capitalize(), family=family, temp_opt_min=opt[0], temp_opt_max=opt[1],
        temp_abs_min=abs_[0], temp_abs_max=abs_[1], water_need_mm=water, cycle_days=100,
        seasons=seasons, soils=soils or ["sandy", "loam", "clay"], nitrogen_delta_kg_ha=nitrogen, source="prueba",
    )


@pytest.fixture
def catalog() -> list[CropParams]:
    # Valores de juguete, solo para pruebas
    return [
        crop("maize", "cereal", (18, 32), (10, 42), 600, ["spring", "summer"], -30),
        crop("wheat", "cereal", (12, 24), (3, 33), 450, ["autumn", "winter"], -20),
        crop("bean", "legume", (16, 28), (8, 35), 350, ["spring", "summer"], 40),
        crop("oat", "cover", (8, 22), (0, 30), 300, ["autumn", "winter"], -8),
        crop("sorghum", "cereal", (22, 35), (12, 44), 450, ["summer"], -25),
        crop("tomato", "vegetable", (18, 28), (10, 35), 550, ["spring", "summer"], -15, ["loam"]),
    ]


def make_climate(lat: float = 31.86, rain_cv: float = 38.0, soil_root: float = 0.43) -> ClimateData:
    """Clima tipo Ensenada: inviernos templados con lluvia, veranos secos."""
    temps = [14, 14.5, 15, 16, 17, 19, 21, 22, 21.5, 19, 16.5, 14]
    rains = [50, 55, 40, 12, 3, 1, 1, 2, 5, 12, 25, 45]
    monthly = [
        MonthlyClimatePoint(month=m, temp_c=temps[m - 1], temp_max_c=temps[m - 1] + 8, temp_min_c=temps[m - 1] - 8,
                            rain_mm=rains[m - 1], soil_moisture_root=soil_root, solar_radiation=5.5)
        for m in range(1, 13)
    ]
    summary = ClimateSummary(lat=lat, lon=-116.5, period="2016-2025", temp_mean_c=17.5, rain_annual_mm=251,
                             rain_cv_pct=rain_cv, soil_moisture_root=soil_root, monthly=monthly)
    recent = RecentClimate(start=date(2026, 8, 10), end=date(2026, 11, 7), rain_90d_mm=10, rain_90d_normal_mm=30,
                           temp_30d_c=21, temp_30d_normal_c=19.5, soil_moisture_30d=0.25)
    return ClimateData(summary=summary, recent=recent)


@pytest.fixture
def climate() -> ClimateData:
    return make_climate()


@pytest.fixture(autouse=True)
def limpiar_cache():
    """Cada prueba empieza con el caché vacío."""
    climate_service._long_term_cache.clear()
    climate_service._recent_cache.clear()
    yield
