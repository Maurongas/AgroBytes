from pydantic import BaseModel, Field
from datetime import datetime

class CropRequest(BaseModel):
    avg_temp: float = Field(..., description="Temperatura promedio en grados Celsius")
    rainfall_mm: float = Field(..., description="Lluvia acumulada en milímetros")
    soil_type: str = Field(default="desconocido", description="Tipo de suelo (ej. arcilloso, arenoso)")

class CropResponse(BaseModel):
    status: str
    datos_analizados: dict
    recomendaciones: list

# Molde para enviar el historial al frontend
class HistorialResponse(BaseModel):
    id: int
    temperatura: float
    lluvia: float
    tipo_suelo: str
    resultado_cultivos: str
    fecha_consulta: datetime

    class Config:
        from_attributes = True