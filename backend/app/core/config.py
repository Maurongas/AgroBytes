"""Configuración desde variables de entorno (ver .env.example en la raíz). Dueño: DBA."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg://admin:password@db:5432/agridb"
    # Orígenes permitidos para CORS, separados por coma
    CORS_ORIGINS: str = "http://localhost:3000"
    NASA_POWER_BASE_URL: str = "https://power.larc.nasa.gov/api"
    # Días que es válido un registro de climate_cache
    CLIMATE_CACHE_DAYS: int = 30
    # Máximo de POST /analyses por IP por minuto (0 = sin límite). Protege la cuota de NASA POWER y SoilGrids
    RATE_LIMIT_ANALYSES_PER_MIN: int = 30
    # true = el historial, el detalle y el borrado exigen el header X-Device-Id (activar cuando el
    # frontend ya lo mande; mientras, sin header se ve todo como antes)
    REQUIRE_DEVICE_ID: bool = False

    @field_validator("DATABASE_URL")
    @classmethod
    def usar_psycopg(cls, url: str) -> str:
        """Render, Neon y Supabase dan la URL como postgres:// o postgresql://; SQLAlchemy necesita el driver."""
        for prefijo in ("postgres://", "postgresql://"):
            if url.startswith(prefijo):
                return "postgresql+psycopg://" + url[len(prefijo):]
        return url

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
