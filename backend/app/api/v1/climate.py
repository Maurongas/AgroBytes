from fastapi import APIRouter, Query

from app.api.v1._pending import pending
from app.schemas.climate import ClimateSummary

router = APIRouter(prefix="/climate", tags=["climate"])


@router.get("", response_model=ClimateSummary, summary="Resumen climático NASA POWER de un punto")
def get_climate(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180)) -> ClimateSummary:
    # TODO(issue #5): services.climate.get_climate_summary(db, lat, lon); 503 si NASA falla y no hay caché
    raise pending("GET /api/v1/climate")
