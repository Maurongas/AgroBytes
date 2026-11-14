from fastapi import APIRouter

from app.api.v1._pending import pending
from app.schemas.crop import Crop

router = APIRouter(prefix="/crops", tags=["crops"])


@router.get("", response_model=list[Crop], summary="Catálogo de cultivos")
def list_crops() -> list[Crop]:
    # TODO(issue #4/#5): repositories.crops.list_all(db)
    raise pending("GET /api/v1/crops")
