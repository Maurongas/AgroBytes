from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.crop import Crop
from app.services import crops as crops_service
from app.services.crops import CatalogUnavailableError

router = APIRouter(prefix="/crops", tags=["crops"])


@router.get("", response_model=list[Crop], summary="Catálogo de cultivos")
def list_crops(db: Session = Depends(get_db)) -> list[Crop]:
    try:
        catalog = crops_service.load_catalog(db)
    except CatalogUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    return [Crop.model_validate(c) for c in catalog]
