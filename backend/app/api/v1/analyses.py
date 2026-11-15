"""Routers delgados: validan, llaman a services/repositories y responden. Dueño: Backend."""

import asyncio
import uuid
from datetime import datetime, timezone

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rate_limit import limit_analyses
from app.db.database import get_db
from app.models.analysis import Analysis
from app.repositories import analyses as analyses_repo
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisSummary, Location
from app.services import climate as climate_service
from app.services import crops as crops_service
from app.services import geo, recommender, region
from app.services import soil as soil_service
from app.services.crops import CatalogUnavailableError
from app.services.nasa_power import NasaUnavailableError

router = APIRouter(prefix="/analyses", tags=["analyses"])

async def _none() -> None:
    return None


MAX_DB_ID = 2**31 - 1  # analyses.id es INTEGER en PostgreSQL
NOT_FOUND = "Análisis no encontrado"

# Identificador anónimo del dispositivo (p. ej. un UUID que el frontend genera y guarda en localStorage).
# No es autenticación: solo separa el historial de cada dispositivo.
DeviceId = Annotated[str | None, Header(
    alias="X-Device-Id", pattern=r"^[A-Za-z0-9_-]{8,64}$",
    description="Dispositivo anónimo (8–64 caracteres: letras, números, - y _). Separa el historial por dispositivo.",
)]


def require_device(device_id: str | None) -> None:
    if settings.REQUIRE_DEVICE_ID and device_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Falta el header X-Device-Id")


def visible(row: Analysis, device_id: str | None) -> bool:
    """Un análisis de otro dispositivo no existe para quien manda su propio X-Device-Id.
    Sin header (clientes viejos) o en análisis sin dueño (anteriores a la v2.1), se ve."""
    return device_id is None or row.device_id is None or row.device_id == device_id


def parse_id(analysis_id: str) -> int:
    """El id es texto en el contrato; en la BD es un entero positivo. Cualquier otra cosa no existe."""
    if not (analysis_id.isascii() and analysis_id.isdigit()) or not 0 < int(analysis_id) <= MAX_DB_ID:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return int(analysis_id)


def load_row(db: Session, analysis_id: str, device_id: str | None) -> Analysis:
    pk = parse_id(analysis_id)
    try:
        row = analyses_repo.get(db, pk)
    except SQLAlchemyError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Base de datos no disponible") from exc
    if row is None or not visible(row, device_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return row


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
             summary="Analiza una parcela y recomienda una rotación",
             dependencies=[Depends(limit_analyses)],
             responses={200: {"description": "Con `guardar=false`: el análisis sin guardar (id `preview-…`)"},
                        429: {"description": "Demasiados análisis desde esta IP en el último minuto"}})
async def create_analysis(
    req: AnalysisRequest,
    response: Response,
    guardar: bool = Query(
        True,
        description="false = solo calcula y devuelve el análisis, sin guardarlo en el historial "
                    "(p. ej. «Comparar escenarios»). Responde 200 con un id `preview-…` que no existe en la BD.",
    ),
    device_id: DeviceId = None,
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    # 1. Geometría: área y centroide de la parcela (el formato ya lo validó Pydantic → 422)
    if req.climate_shift is not None and guardar:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="Los escenarios hipotéticos solo se calculan sin guardar (guardar=false)")
    ring = geo.outer_ring(req.geometry.coordinates)
    area = geo.area_ha(ring)
    if area <= 0:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail="El polígono no tiene área (puntos en línea)")
    if (error := region.validate_parcel(ring, area)) is not None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail=error)
    lat, lon = geo.centroid(ring)
    # País por el centroide (si el centroide cae fuera, p. ej. una parcela en forma de U en la costa, el del
    # primer vértice; validate_parcel ya garantizó que todos los vértices están en la región)
    country = region.country_of(lon, lat) or region.country_of(*ring[0])

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
    country_areas = crops_service.load_country_areas(country.code, db) if country else None
    country_nitrogen = crops_service.load_country_nitrogen(country.code, db) if country else None
    result = recommender.recommend(climate, crops, req, today=datetime.now(timezone.utc).date(),
                                   detected_soil=detected_soil, country_areas=country_areas,
                                   country_name=country.name if country else None,
                                   country_nitrogen=country_nitrogen)
    location = Location(lat=round(lat, 5), lon=round(lon, 5))
    body = {
        "area_ha": round(area, 2),
        "location": location.model_dump(),
        "country": country.code if country else None,
        "metrics": [m.model_dump(mode="json") for m in result.metrics],
        "rotation": [r.model_dump(mode="json") for r in result.rotation],
        "impact": [i.model_dump(mode="json") for i in result.impact],
        "soil_health": result.soil_health.model_dump(mode="json"),
        "climate": [c.model_dump(mode="json") for c in result.climate],
        "uncertainty": result.uncertainty.model_dump(mode="json"),
        "soil_detected": detected_soil.model_dump(mode="json") if detected_soil else None,
        "irrigated": req.irrigated,
        "strategies": [s.model_dump(mode="json") for s in result.strategies],
        "local_checks": list(result.local_checks),
        "climate_shift": req.climate_shift.model_dump(mode="json") if req.climate_shift else None,
    }

    # 5a. Sin guardar: id temporal no numérico (GET /analyses/{id} lo trata como inexistente → 404)
    if not guardar:
        response.status_code = status.HTTP_200_OK
        return AnalysisResponse.model_validate(
            {**body, "id": f"preview-{uuid.uuid4().hex[:12]}",
             "created_at": datetime.now(timezone.utc).replace(microsecond=0)}
        )

    # 5b. Guardar (analyses) y responder con el id de la BD
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
            device_id=device_id,
            climate_summary=climate.summary.model_dump(mode="json"),
            result=body,
        )
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="No se pudo guardar el análisis (base de datos no disponible)") from exc
    return to_response(row)


@router.get("", response_model=list[AnalysisSummary], summary="Historial de análisis")
def list_analyses(limit: int = Query(20, ge=1, le=100), device_id: DeviceId = None,
                  db: Session = Depends(get_db)) -> list[AnalysisSummary]:
    require_device(device_id)
    try:
        rows = analyses_repo.list_recent(db, limit, device_id=device_id)
    except SQLAlchemyError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Base de datos no disponible") from exc
    return [to_summary(row) for row in rows]


@router.get("/{analysis_id}", response_model=AnalysisResponse, summary="Detalle de un análisis")
def get_analysis(analysis_id: str, device_id: DeviceId = None, db: Session = Depends(get_db)) -> AnalysisResponse:
    require_device(device_id)
    return to_response(load_row(db, analysis_id, device_id))


@router.delete("/{analysis_id}", status_code=204, summary="Borra un análisis del historial",
               responses={404: {"description": "No existe o es de otro dispositivo"}})
def delete_analysis(analysis_id: str, device_id: DeviceId = None, db: Session = Depends(get_db)) -> Response:
    require_device(device_id)
    row = load_row(db, analysis_id, device_id)
    if row.device_id != device_id:  # solo el dispositivo que lo creó (o, si no tiene dueño, un cliente sin header)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    try:
        analyses_repo.delete(db, row)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Base de datos no disponible") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
