"""Routers delgados: validan, llaman a services/repositories y responden. Dueño: Backend."""

from fastapi import APIRouter, Query

from app.api.v1._pending import pending
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisSummary

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResponse, status_code=201,
             summary="Analiza una parcela y recomienda una rotación")
def create_analysis(req: AnalysisRequest) -> AnalysisResponse:
    # TODO(issue #5): centroide/área → climate.get_climate_summary → recommender.recommend
    #                 → repositories.analyses.create → respuesta
    raise pending("POST /api/v1/analyses")


@router.get("", response_model=list[AnalysisSummary], summary="Historial de análisis")
def list_analyses(limit: int = Query(20, ge=1, le=100)) -> list[AnalysisSummary]:
    raise pending("GET /api/v1/analyses")


@router.get("/{analysis_id}", response_model=AnalysisResponse, summary="Detalle de un análisis")
def get_analysis(analysis_id: str) -> AnalysisResponse:
    raise pending("GET /api/v1/analyses/{id}")
