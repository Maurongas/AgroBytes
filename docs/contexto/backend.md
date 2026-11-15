# Backend (API + NASA POWER + motor de reglas)

**Responsable:** Mauro (Maurongas) · **Issue:** #5 · **Rama base:** `feature/back-nasa-api`

> Agente: lee primero `docs/ARQUITECTURA.md` §3, §5, §7 y §8. Ese documento manda; si algo de aquí lo
> contradice, gana ARQUITECTURA.md. Cambios de la v2.0: `docs/CAMBIOS-ARQUITECTURA.md`.

## Tu rol
Construyes la API FastAPI, la integración con NASA POWER y el motor de reglas que recomienda una
**rotación de cultivos por temporada**. **No** escribes modelos SQLAlchemy ni migraciones (eso es del DBA,
`backend-dba.md`); los usas a través de `app/repositories/`.

## Stack
Python 3.11 · FastAPI · Pydantic v2 · httpx · pytest. Corre en Docker; el código se monta en `/app` y
uvicorn recarga solo.

## Lo que ya existe (v2.0)
- `app/main.py`: CORS desde `settings`, `/health` (revisa BD), incluye `api/v1`.
- `app/schemas/`: **contrato completo** (`analysis.py`, `climate.py`, `crop.py`; `base.py` convierte a camelCase).
- `app/services/`: `nasa_power.py`, `climate.py` (caché memoria + tabla `climate_cache`), `geo.py`, `crops.py`
  (lee la tabla `crops`), `recommender.py` ✅.
- `app/api/v1/`: **todos los endpoints implementados** y conectados a la BD (`POST/GET /analyses`,
  `/analyses/{id}`, `/climate`, `/crops`). Ya no hay 501.
- `tests/`: 31 pruebas sin internet (`conftest.py` trae un catálogo y un clima inventados).
- Las pruebas de API usan una BD falsa (`get_db` → `None` y `analyses_repo` en memoria); las de PostgreSQL real
  están en `test_repositories.py`. Correr todo: `docker compose exec backend python -m pytest -q`.
- `research/`: `extraer_links.py` + `links.md` (fuentes investigadas) y `fuentes.md` (texto extraído; se regenera con `python extraer_links.py`).

## Archivos que te pertenecen
```
backend/app/main.py
backend/app/schemas/        base.py analysis.py climate.py crop.py
backend/app/api/v1/         analyses.py climate.py crops.py _pending.py
backend/app/services/       geo.py nasa_power.py climate.py recommender.py   (hecho)
backend/tests/              test_api.py test_geo.py test_nasa_power.py test_recommender.py
backend/research/
```
No toques sin avisar a Daniel: `app/core/`, `app/db/`, `app/models/`, `app/repositories/`, `alembic/`,
`app/data/`, `docker-compose.yml`.

## Tareas (en orden)
1. **`services/nasa_power.py`** (no depende de la BD; empieza aquí)
   - `fetch_climatology(lat, lon)`, `fetch_monthly(lat, lon, 2015, 2024)`, `fetch_daily(lat, lon, start, end)`.
   - httpx, timeout 20 s, 2 reintentos, `NasaUnavailableError`. Parámetros y notas: ARQUITECTURA §8.
   - Prueba manual: `docker compose exec backend python -c "import asyncio;from app.services.nasa_power import fetch_climatology as f;print(asyncio.run(f(31.86,-116.6)))"`
2. **`services/climate.py`** → `get_climate_summary(lat, lon, cache=None) -> ClimateSummary` (malla 0.5°, caché
   cuando Daniel tenga `repositories.climate_cache`). Luego **`GET /api/v1/climate`** (503 si NASA falla).
3. **`services/geo.py`**: centroide + área del polígono (puro). Tests.
4. **`services/recommender.py`**: función pura según §7 (rotación, impacto, salud del suelo, métricas,
   incertidumbre). Mientras no exista la tabla `crops`, lee `app/data/crops.json`. Tests con clima inventado.
5. **`POST /api/v1/analyses`**: geo → climate → crops → recommender → `repositories.analyses.create` → 201.
   Avisa al frontend para que cambie a `VITE_USE_MOCK=false`.
6. **`GET /api/v1/analyses`**, **`/analyses/{id}`**, **`/crops`** con los repositorios de Daniel.

## Reglas
- Routers delgados; lógica en `services/`; SQL en `repositories/`. `recommender.py` y `geo.py` sin I/O.
- Errores en español: `{"detail": "..."}`. Respeta los códigos de §5.7.
- Si cambias el contrato: `schemas/` + `frontend/src/api/types.ts` + `mock.ts` + ARQUITECTURA §5 en el mismo PR.
- Nada de "ML", "IA" ni "satélite"; la fuente es **NASA POWER**. Nitrógeno y salud del suelo = "estimado".
- Dependencias nuevas con versión fijada en `requirements.txt` → `docker compose up --build -V backend`.

## Definición de terminado
- `/docs` muestra los endpoints con ejemplos; `docker compose exec backend pytest -q` pasa.
- `curl "http://localhost:8000/api/v1/climate?lat=31.86&lon=-116.6"` responde según §5.5 y la segunda vez es instantáneo.
- Con `VITE_USE_MOCK=false` el frontend muestra un análisis real de punta a punta.
