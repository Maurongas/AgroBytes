from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base
import datetime

class HistorialConsulta(Base):
    __tablename__ = "historial_consultas"

    id = Column(Integer, primary_key=True, index=True)
    ubicacion = Column(String, default="No especificada") # NUEVO CAMPO
    temperatura = Column(Float)
    lluvia = Column(Float)
    humedad_suelo = Column(Float, default=50.0) # NUEVO CAMPO
    tipo_suelo = Column(String)
    resultado_cultivos = Column(String)
    fecha_consulta = Column(DateTime, default=datetime.datetime.utcnow)