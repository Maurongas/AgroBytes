from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class HistorialConsulta(Base):
    __tablename__ = "historial_consultas"

    id = Column(Integer, primary_key=True, index=True)
    temperatura = Column(Float)
    lluvia = Column(Float)
    tipo_suelo = Column(String)
    resultado_cultivos = Column(String)
    fecha_consulta = Column(DateTime(timezone=True), server_default=func.now())