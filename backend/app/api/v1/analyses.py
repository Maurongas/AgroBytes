"""Routers delgados: validan, llaman a services/repositories y responden. Dueño: Backend."""

import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.analysis import Analysis
from app.repositories import analyses as analyses_repo
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisSummary, Location
from app.services import climate as climate_service
from app.services import crops as crops_service
from app.services import geo, recommender
from app.services import soil as soil_service
from app.services.crops import CatalogUnavailableError
from app.services.nasa_power import NasaUnavailableError

router = APIRouter(prefix="/analyses", tags=["analyses"])

async def _none() -> None:
    return None


MAX_DB_ID = 2**31 - 1  # analyses.id es INTEGER en PostgreSQL
NOT_FOUND = "Análisis no encontrado"


def to_response(row: Analysis) -> AnalysisResponse:
    """`result` guarda el AnalysisResponse sin `id` ni `created_at`; esos dos salen de la fila.
    El id es INTEGER en la BD y texto en el contrato (§5)."""
    return AnalysisResponse.model_validate(
        {**row.result, "id": str(row.id), "created_at": row.created_at.replace(microsecond=0)}
    )


def to_summary(row: Analysis) -> AnalysisSummary:
    return AnalysisSummary(
        id=str(row.id),
        created_at=row.created_at.replace(microsecond=0),
        location=Location(lat=row.lat, lon=row.lon),
        area_ha=row.area_ha,
        current_crop=row.current_crop,
        priority=row.priority,
        rotation_crops=[step["crop_id"] for step in row.result.get("rotation", [])],
    )


@router.post("", response_model=AnalysisResponse, status_code=201,
             summary="Analiza una parcela y recomienda una rotación")
async def create_analysis(req: AnalysisRequest, db: Session = Depends(get_db)) -> AnalysisResponse:
    # 1. Geometría: área y centroide de la parcela (el formato ya lo validó Pydantic → 422)
    ring = geo.outer_ring(req.geometry.coordinates)
    area = geo.area_ha(ring)
    if area <= 0:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail="El polígono no tiene área (puntos en línea)")
    lat, lon = geo.centroid(ring)

    # 2. Catálogo de cultivos (tabla crops)
    try:
        crops = crops_service.load_catalog(db)
    except CatalogUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    if req.current_crop not in {c.id for c in crops}:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail=f"Cultivo desconocido: {req.current_crop}")

    # 3. Clima de NASA POWER (caché en memoria + tabla climate_cache) y, en paralelo, suelo de SoilGrids
    #    (solo si el usuario no dio textura y pH; si SoilGrids falla, sigue sin suelo).
    need_soil = req.soil is None or req.soil.ph is None
    try:
        climate, detected_soil = await asyncio.gather(
            climate_service.get_climate(lat, lon, db=db),
            soil_service.get_soil(lat, lon) if need_soil else _none(),
        )
    except NasaUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="NASA POWER no disponible") from exc

    # 4. Motor de reglas (puro)
    result = recommender.recommend(climate, crops, req, today=datetime.now(timezone.utc).date(),
                                   detected_soil=detected_soil)
    location = Location(lat=round(lat, 5), lon=round(lon, 5))
    body = {
        "area_ha": round(area, 2),
        "location": location.model_dump(),
        "metrics": [m.model_dump(mode="json") for m in result.metrics],
        "rotation": [r.model_dump(mode="json") for r in result.rotation],
        "impact": [i.model_dump(mode="json") for i in result.impact],
        "soil_health": result.soil_health.model_dump(mode="json"),
        "climate": [c.model_dump(mode="json") for c in result.climate],
        "uncertainty": result.uncertainty.model_dump(mode="json"),
        "soil_detected": detected_soil.model_dump(mode="json") if detected_soil else None,
        "irrigated": req.irrigated,
    }

    # 5. Guardar (analyses) y responder con el id de la BD
    try:
        row = analyses_repo.create(
            db,
            geometry=req.geometry.model_dump(),
            lat=location.lat,
            lon=location.lon,
            area_ha=body["area_ha"],
            current_crop=req.current_crop,
            priority=req.priority,
            soil=req.soil.model_dump(mode="json") if req.soil else None,
            irrigated=req.irrigated,
            climate_summary=climate.summary.model_dump(mode="json"),
            result=body,
        )
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="No se pudo guardar el análisis (base de datos no disponible)") from exc
    return to_response(row)


@router.get("", response_model=list[AnalysisSummary], summary="Historial de análisis")
def list_analyses(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)) -> list[AnalysisSummary]:
    try:
        rows = analyses_repo.list_recent(db, limit)
    except SQLAlchemyError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Base de datos no disponible") from exc
    return [to_summary(row) for row in rows]


@router.get("/{analysis_id}", response_model=AnalysisResponse, summary="Detalle de un análisis")
def get_analysis(analysis_id: str, db: Session = Depends(get_db)) -> AnalysisResponse:
    # El id es texto en el contrato; en la BD es un entero positivo. Cualquier otra cosa no existe.
    if not (analysis_id.isascii() and analysis_id.isdigit()) or not 0 < int(analysis_id) <= MAX_DB_ID:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    try:
        row = analyses_repo.get(db, int(analysis_id))
    except SQLAlchemyError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Base de datos no disponible") from exc
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return to_response(row)
