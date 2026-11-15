"""Consultas SQL reutilizables (los routers y services no escriben SQL). Dueño: DBA."""

from app.repositories import analyses, climate_cache, crops

__all__ = ["analyses", "crops", "climate_cache"]
