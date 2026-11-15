"""Contrato de /api/v1/analyses. Espejo exacto: frontend/src/api/types.ts. Ver docs/ARQUITECTURA.md §5."""

from datetime import datetime
from typing import Literal

from pydantic import Field, field_validator

from app.schemas.base import CamelModel

Priority = Literal["water", "nitrogen", "yield"]
Season = Literal["autumn", "winter", "spring", "summer"]
Status = Literal["ok", "warn", "danger"]
SoilTexture = Literal["sandy", "loam", "clay"]
MetricId = Literal["soilMoisture", "rain90d", "tempMean", "solarRadiation"]
UncertaintyLevel = Literal["low", "medium", "high"]
CropRole = Literal["cereal", "legume", "cover", "vegetable", "oilseed", "industrial"]
CountryCode = Literal["MX", "US", "CA"]  # ISO 3166-1 alfa-2; región de trabajo (ver ARQUITECTURA §7)
StrategyId = Literal["current", "water", "nitrogen", "yield"]
# Paso de la rotación sin cultivo: ningún cultivo del catálogo tolera el clima de esa temporada
FALLOW_ID = "fallow"


class Polygon(CamelModel):
    """GeoJSON Polygon. Coordenadas en orden [longitud, latitud]; el anillo debe cerrarse."""

    type: Literal["Polygon"]
    coordinates: list[list[list[float]]] = Field(min_length=1)

    @field_validator("coordinates")
    @classmethod
    def anillo_valido(cls, coordinates: list[list[list[float]]]) -> list[list[list[float]]]:
        """Pydantic convierte cualquier ValueError de aquí en un 422 con el mensaje."""
        ring = coordinates[0]
        if len(ring) < 4:
            raise ValueError("El polígono necesita al menos 3 vértices y repetir el primero al final")
        for point in ring:
            if len(point) < 2:
                raise ValueError("Cada punto debe ser [longitud, latitud]")
            lon, lat = point[0], point[1]
            if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                raise ValueError("Coordenada fuera de rango; el orden es [longitud, latitud]")
        if ring[0][:2] != ring[-1][:2]:
            raise ValueError("El anillo del polígono debe cerrarse (el último punto = el primero)")
        if len({(p[0], p[1]) for p in ring}) < 3:
            raise ValueError("El polígono necesita al menos 3 vértices distintos")
        return coordinates


class Soil(CamelModel):
    texture: SoilTexture
    ph: float | None = Field(default=None, ge=0, le=14)
    organic_matter: Literal["low", "mid", "high"] | None = None


class ClimateShift(CamelModel):
    """Escenario hipotético «¿y si…?»: modifica el clima histórico antes de recomendar. Solo con guardar=false."""

    rain_pct: float = Field(default=0, ge=-60, le=60, description="% de cambio en la lluvia de cada mes")
    temp_c: float = Field(default=0, ge=-3, le=5, description="°C que se suman a la temperatura de cada mes")


class AnalysisRequest(CamelModel):
    geometry: Polygon
    current_crop: str = Field(examples=["maize"], description="id del catálogo de cultivos")
    priority: Priority
    soil: Soil | None = None
    irrigated: bool | None = Field(
        default=None,
        description="¿La parcela tiene riego? true = el agua se compara por riego necesario; "
                    "false/null = temporal (depende de la lluvia)",
    )
    climate_shift: ClimateShift | None = Field(
        default=None, description="Escenario climático hipotético (solo con guardar=false; si no, 422)")


class Location(CamelModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class NasaMetric(CamelModel):
    id: MetricId
    label: str
    value: float
    unit: str
    status: Status
    meaning: str = Field(examples=["Algo seco para maíz"])
    series: list[float] = Field(description="12 valores mensuales para el sparkline")
    source: str = Field(examples=["NASA POWER · 2015-2024"])


class RotationStep(CamelModel):
    season: Season
    crop_id: str = Field(description='id del catálogo, o "fallow" = descanso/barbecho')
    score: int = Field(ge=0, le=100)
    reasons: list[str]
    water_saving_pct: float
    nitrogen_delta: float = Field(description="kg/ha estimado por reglas; positivo = aporta")
    risks: list[str]
    planting_window: str = Field(examples=["Sep – Oct"])
    irrigation_mm: float = Field(default=0, description="Riego estimado para el ciclo (FAO-56: Kc × ET₀ − lluvia)")


class ImpactItem(CamelModel):
    label: str
    unit: str
    current: float
    recommended: float
    better_when: Literal["higher", "lower"]


class SoilHealth(CamelModel):
    """Índice 0-100 estimado por reglas (no es una medición)."""

    current: int = Field(ge=0, le=100)
    recommended: int = Field(ge=0, le=100)


class MonthlyClimate(CamelModel):
    month: str = Field(examples=["Ene"])
    rain: float = Field(description="mm/mes")
    temp: float = Field(description="°C")


class DetectedSoil(CamelModel):
    """Suelo estimado por coordenadas (ISRIC SoilGrids, 0–30 cm). Es un modelo global de ~250 m, no una muestra."""

    texture: SoilTexture
    ph: float | None
    clay_pct: float
    sand_pct: float
    source: str = "ISRIC SoilGrids v2.0 (0–30 cm)"


class Uncertainty(CamelModel):
    level: UncertaintyLevel
    reason: str = Field(examples=["La lluvia anual varía 38 % entre años"])


class Strategy(CamelModel):
    """Una forma de usar la parcela las próximas 3 temporadas. `current` = seguir como hoy."""

    id: StrategyId
    title: str = Field(examples=["Ahorrar agua"])
    is_current: bool
    is_recommended: bool = Field(description="La de la prioridad elegida: sus pasos son los mismos que `rotation`")
    steps: list[RotationStep] = Field(min_length=3, max_length=3)
    water_mm: float = Field(description="Agua total de los cultivos (FAO-56)")
    irrigation_mm: float = Field(description="Parte del agua que la lluvia no cubre")
    nitrogen_kg_ha: float = Field(description="Balance de nitrógeno ESTIMADO por reglas")
    soil_health: int = Field(ge=0, le=100, description="Índice ESTIMADO por reglas")
    bare_seasons: int = Field(ge=0, le=3, description="Temporadas con el suelo sin cultivo")
    why: str
    benefits: list[str]
    tradeoffs: list[str] = Field(description="Riesgos y costos a revisar")
    evidence: list[str] = Field(description="Datos que respaldan la estrategia, con su fuente")


class AnalysisResponse(CamelModel):
    id: str
    created_at: datetime
    area_ha: float
    location: Location = Field(description="Centroide de la parcela")
    country: CountryCode | None = Field(
        default=None,
        description="País de la parcela; solo se recomiendan cultivos que ahí se siembran (FAOSTAT). "
                    "null en análisis guardados antes de este campo",
    )
    metrics: list[NasaMetric]
    rotation: list[RotationStep]
    impact: list[ImpactItem]
    soil_health: SoilHealth
    climate: list[MonthlyClimate] = Field(min_length=12, max_length=12)
    uncertainty: Uncertainty
    soil_detected: DetectedSoil | None = Field(default=None, description="null si SoilGrids no tiene dato o no respondió")
    irrigated: bool | None = None
    strategies: list[Strategy] = Field(
        default_factory=list, description="Seguir como hoy + una rotación por prioridad. [] en análisis viejos")
    local_checks: list[str] = Field(
        default_factory=list, description="Qué confirmar con productores o un agrónomo de la zona")
    climate_shift: ClimateShift | None = None


class AnalysisSummary(CamelModel):
    """Un renglón del historial (GET /api/v1/analyses)."""

    id: str
    created_at: datetime
    location: Location
    area_ha: float
    current_crop: str
    priority: Priority
    rotation_crops: list[str] = Field(examples=[["bean", "oat", "sorghum"]])
