from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importamos esquemas y el algoritmo
from app.schemas.recommendation import CropRequest, CropResponse, HistorialResponse
from app.services.algorithm import calculate_crop_recommendation

# Importamos configuración de base de datos y modelos
from app.database import engine, get_db, Base
from app import models

# Crea automáticamente las tablas en PostgreSQL si no existen
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
    # 1. El algoritmo calcula la recomendación
    resultado = calculate_crop_recommendation(
        avg_temp=request.avg_temp, 
        rainfall_mm=request.rainfall_mm, 
        soil_type=request.soil_type
    )
    
    # 2. Extraemos solo los nombres de los cultivos para guardarlos fácil en texto
    nombres_cultivos = ", ".join([item["cultivo"] for item in resultado["recomendaciones"]])
    
    # 3. Preparamos el registro para la base de datos
    nueva_consulta = models.HistorialConsulta(
        temperatura=request.avg_temp,
        lluvia=request.rainfall_mm,
        tipo_suelo=request.soil_type,
        resultado_cultivos=nombres_cultivos
    )
    
    # 4. Guardamos permanentemente en PostgreSQL
    db.add(nueva_consulta)
    db.commit()

    # 5. Retornamos el resultado completo al frontend para que lo dibuje
    return resultado

@app.get("/api/v1/history", response_model=list[HistorialResponse])
def get_history(db: Session = Depends(get_db)):
    # Busca las últimas 10 consultas ordenadas de la más reciente a la más antigua
    historial = db.query(models.HistorialConsulta).order_by(models.HistorialConsulta.fecha_consulta.desc()).limit(10).all()
    return historial