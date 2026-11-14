from pydantic import BaseModel, Field
from datetime import datetime

class CropRequest(BaseModel):
    ubicacion: str = Field(default="No especificada", description="Ubicación o coordenadas") # NUEVO
    avg_temp: float = Field(..., description="Temperatura promedio en grados Celsius")
    rainfall_mm: float = Field(..., description="Lluvia acumulada en milímetros")
    humedad_suelo_pct: float = Field(default=50.0, description="Humedad subsuperficial del suelo (%)")
    soil_type: str = Field(default="desconocido", description="Tipo de suelo")
    cultivo_actual: str = Field(default="ninguno")
    disponibilidad_agua: str = Field(default="media")
    prioridad_agricultor: str = Field(default="conservar_agua")

class CropResponse(BaseModel):
    status: str
    confianza_modelo_ml: str
    margen_incertidumbre: str
    datos_analizados: dict
    recomendaciones: list

class HistorialResponse(BaseModel):
    id: int
    ubicacion: str # NUEVO
    temperatura: float
    lluvia: float
    humedad_suelo: float # NUEVO
    tipo_suelo: str
    resultado_cultivos: str
    fecha_consulta: datetime

    class Config:
        from_attributes = True