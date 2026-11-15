from fastapi import APIRouter

from app.api.v1 import analyses, climate, crops, soil

router = APIRouter(prefix="/api/v1")
router.include_router(analyses.router)
router.include_router(climate.router)
router.include_router(crops.router)
router.include_router(soil.router)
