from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1 import router as api_v1
from app.core.config import settings
from app.db.database import engine

app = FastAPI(
    title="DSS Agrícola — API",
    description="Clima de NASA POWER + reglas agronómicas para recomendar rotaciones de cultivo.",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1)


@app.get("/health", tags=["health"], summary="Estado del backend y de la base de datos")
def health() -> dict[str, str]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db = "ok"
    except Exception:
        db = "error"
    return {"status": "ok", "db": db}
