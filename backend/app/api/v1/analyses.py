"""Routers delgados: validan, llaman a services/repositories y responden. Dueño: Backend."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, status

from app.api.v1._pending import pending
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisSummary, Location
from app.services import climate as climate_service
from app.services import crops as crops_service
from app.services import geo, recommender
from app.services.crops import CatalogUnavailableError
from app.services.nasa_power import NasaUnavailableError

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResponse, status_code=201,
             summary="Analiza una parcela y recomienda una rotación")
async def create_analysis(req: AnalysisRequest) -> AnalysisResponse:
    # 1. Geometría: área y centroide de la parcela (el formato ya lo validó Pydantic → 422)
    ring = geo.outer_ring(req.geometry.coordinates)
    area = geo.area_ha(ring)
    if area <= 0:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail="El polígono no tiene área (puntos en línea)")
    lat, lon = geo.centroid(ring)

    # 2. Catálogo de cultivos
    try:
        crops = crops_service.load_catalog()
    except CatalogUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    if req.current_crop not in {c.id for c in crops}:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail=f"Cultivo desconocido: {req.current_crop}")

    # 3. Clima de NASA POWER (con caché)
    try:
        climate = await climate_service.get_climate(lat, lon)
    except NasaUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="NASA POWER no disponible") from exc

    # 4. Motor de reglas (puro)
    now = datetime.now(timezone.utc)
    result = recommender.recommend(climate, crops, req, today=now.date())

    # 5. TODO(issue #4): guardar con repositories.analyses.create(db, ...) y usar su id.
    #    Mientras el DBA termina, el análisis NO se guarda y el id es temporal.
    return AnalysisResponse(
        id=uuid4().hex[:12],
        created_at=now.replace(microsecond=0),
        area_ha=round(area, 2),
        location=Location(lat=round(lat, 5), lon=round(lon, 5)),
        metrics=result.metrics,
        rotation=result.rotation,
        impact=result.impact,
        soil_health=result.soil_health,
        climate=result.climate,
        uncertainty=result.uncertainty,
    )


@router.get("", response_model=list[AnalysisSummary], summary="Historial de análisis")
def list_analyses(limit: int = Query(20, ge=1, le=100)) -> list[AnalysisSummary]:
    # TODO(issue #4): repositories.analyses.list_recent(db, limit)
    raise pending("GET /api/v1/analyses (falta repositories.analyses)")


@router.get("/{analysis_id}", response_model=AnalysisResponse, summary="Detalle de un análisis")
def get_analysis(analysis_id: str) -> AnalysisResponse:
    # TODO(issue #4): repositories.analyses.get(db, id) → 404 si no existe
    raise pending("GET /api/v1/analyses/{id} (falta repositories.analyses)")
