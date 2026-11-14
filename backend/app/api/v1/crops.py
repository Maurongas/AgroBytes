from fastapi import APIRouter, HTTPException, status

from app.schemas.crop import Crop
from app.services import crops as crops_service
from app.services.crops import CatalogUnavailableError

router = APIRouter(prefix="/crops", tags=["crops"])


@router.get("", response_model=list[Crop], summary="Catálogo de cultivos")
def list_crops() -> list[Crop]:
    # Cuando exista la tabla crops (issue #4) esto pasará a repositories.crops.list_all(db)
    try:
        catalog = crops_service.load_catalog()
    except CatalogUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return [Crop.model_validate(c) for c in catalog]
