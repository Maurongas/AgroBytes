from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.analysis import DetectedSoil
from app.services import soil as soil_service

router = APIRouter(prefix="/soil", tags=["soil"])


@router.get("", response_model=DetectedSoil, summary="Suelo estimado de un punto (ISRIC SoilGrids)",
            responses={404: {"description": "SoilGrids no tiene dato para ese punto o no respondió"}})
async def get_soil(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180)) -> DetectedSoil:
    # Tarda 3–8 s la primera vez (timeout 10 s). Si el frontend lo pide al terminar de dibujar la parcela,
    # el análisis (POST /analyses) ya lo encuentra en caché o espera la misma consulta en curso.
    soil = await soil_service.get_soil(lat, lon)
    if soil is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No hay dato de suelo para este punto")
    return soil
