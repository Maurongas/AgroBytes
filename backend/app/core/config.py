"""Configuración desde variables de entorno (ver .env.example en la raíz). Dueño: DBA."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg://admin:password@db:5432/agridb"
    # Orígenes permitidos para CORS, separados por coma
    CORS_ORIGINS: str = "http://localhost:3000"
    NASA_POWER_BASE_URL: str = "https://power.larc.nasa.gov/api"
    # Días que es válido un registro de climate_cache
    CLIMATE_CACHE_DAYS: int = 30

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
