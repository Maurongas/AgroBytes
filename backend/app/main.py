from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.schemas.recommendation import CropRequest, CropResponse, HistorialResponse
from app.services.algorithm import calculate_crop_recommendation
from app.database import engine, get_db, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NASA Space Apps - API Agrícola")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend operativo"}

@app.post("/api/v1/recommend", response_model=CropResponse)
def get_recommendation(request: CropRequest, db: Session = Depends(get_db)):
    resultado = calculate_crop_recommendation(
        avg_temp=request.avg_temp, 
        rainfall_mm=request.rainfall_mm, 
        humedad_suelo_pct=request.humedad_suelo_pct,
        soil_type=request.soil_type,
        cultivo_actual=request.cultivo_actual,
        disponibilidad_agua=request.disponibilidad_agua,
        prioridad_agricultor=request.prioridad_agricultor
    )
    
    nombres_cultivos = ", ".join([item["cultivo"] for item in resultado["recomendaciones"]])
    
    # AQUI ESTÁ LA MAGIA: Guardamos la ubicación y humedad en DB
    nueva_consulta = models.HistorialConsulta(
        ubicacion=request.ubicacion,
        temperatura=request.avg_temp,
        lluvia=request.rainfall_mm,
        humedad_suelo=request.humedad_suelo_pct,
        tipo_suelo=request.soil_type,
        resultado_cultivos=nombres_cultivos
    )
    
    db.add(nueva_consulta)
    db.commit()

    return resultado

@app.get("/api/v1/history", response_model=list[HistorialResponse])
def get_history(db: Session = Depends(get_db)):
    historial = db.query(models.HistorialConsulta).order_by(models.HistorialConsulta.fecha_consulta.desc()).limit(10).all()
    return historial