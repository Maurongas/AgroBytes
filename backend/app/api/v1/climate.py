from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.climate import ClimateSummary
from app.services import climate as climate_service
from app.services.nasa_power import NasaUnavailableError

router = APIRouter(prefix="/climate", tags=["climate"])


@router.get("", response_model=ClimateSummary, summary="Resumen climático NASA POWER de un punto")
async def get_climate(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180),
                      db: Session = Depends(get_db)) -> ClimateSummary:
    try:
        return await climate_service.get_climate_summary(lat, lon, db=db)
    except NasaUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="NASA POWER no disponible") from exc
