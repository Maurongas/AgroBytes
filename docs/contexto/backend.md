# Contexto Claude — Backend (API + NASA + Recomendación)

**Responsable:** Mauro (Maurongas) · **Issue:** #5 · **Rama base:** `feature/back-nasa-api`

> Claude: lee primero `docs/ARQUITECTURA.md` (secciones 3, 5, 7 y 8). Ese documento manda.
> Si algo de aquí lo contradice, gana ARQUITECTURA.md.

## Tu rol
Eres el desarrollador backend de un DSS agrícola para NASA Space Apps. Construyes la API FastAPI,
la integración con NASA POWER y el motor de recomendación por reglas. **No** manejas modelos de
SQLAlchemy ni migraciones (eso es del DBA, `docs/contexto/backend-dba.md`); los consumes por medio de
`app/repositories/`.

## Stack
Python 3.11 · FastAPI · Pydantic v2 · httpx (async) · pytest · corre en Docker (`docker compose up`).
El código se monta en `/app` dentro del contenedor y uvicorn hace `--reload`.

## Archivos que te pertenecen
```
backend/app/main.py
backend/app/schemas/        farm.py climate.py recommendation.py history.py
backend/app/api/v1/         climate.py recommend.py farms.py history.py
backend/app/services/       nasa_power.py climate.py recommender.py
backend/tests/              test_nasa_power.py test_recommender.py test_api.py
```
Archivos que **no** tocas sin avisar a Daniel: `app/db/`, `app/models/`, `app/repositories/`,
`alembic/`, `app/core/config.py`, `docker-compose.yml`.

## Tareas (en orden)
1. **`services/nasa_power.py`** (no depende de la BD; empieza aquí)
   - `async def fetch_climatology(lat, lon) -> dict` y `async def fetch_monthly(lat, lon, start=2015, end=2024) -> dict`.
   - httpx.AsyncClient, timeout de 20 s, 2 reintentos, lanza `NasaUnavailableError` propia.
   - Parámetros: `T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,GWETROOT`, `community=AG`.
   - Filtra `-999`. Convierte la precipitación de mm/día a mm/mes (verifica unidades en `parameters.<X>.units`).
   - Prueba manual: `docker compose exec backend python -c "import asyncio;from app.services.nasa_power import fetch_climatology as f;print(asyncio.run(f(31.86,-116.6)))"`.
2. **`services/climate.py`**: `get_climate_summary(db, lat, lon) -> ClimateSummary`.
   - Redondea a la malla de 0.5° → busca en el caché (`repositories.clima_cache`) → si no hay, llama a NASA y guarda.
   - Calcula: temperatura media/max/min anual, lluvia anual, humedad del suelo en raíz media, `cv_lluvia_pct` (de la serie anual de 10 años) y `mensual[12]`.
   - Mientras Daniel no tenga el repositorio del caché, deja la función con el parámetro `cache=None` y sin caché.
3. **`schemas/`**: copia exacta de §5 de ARQUITECTURA (enums con `Literal`, validación de lat/lon con `Field(ge=, le=)`).
4. **`GET /api/v1/climate`**: router delgado que llama a `climate.get_climate_summary`. 503 si NASA falla.
5. **`services/recommender.py`**: función pura `recommend(clima, cultivos, req) -> RecommendationResult` según §7.
   - Mientras no exista la tabla `cultivos`, lee `app/data/cultivos.json` (mismo formato que usa el seed de Daniel).
   - Tests con pytest: un clima de prueba y 3–4 cultivos inventados → verifica puntajes y el orden de las estrategias.
6. **`POST /api/v1/recommend`**: clima → cultivos → recommender → `repositories.consultas.create(...)` → respuesta.
7. **`/history`, `/farms`, `/crops`**: routers que llaman a los repositorios de Daniel.
8. `main.py`: CORS desde `settings.CORS_ORIGINS`, `include_router` de v1, `/health` que también revisa la BD.

## Reglas
- Routers delgados: la lógica va en `services/`, el SQL en `repositories/`.
- `recommender.py` no hace I/O (ni BD ni HTTP), así se prueba fácil.
- Mensajes de error en español, formato `{"detail": "..."}`.
- Nada de "ML" ni "satélite" en textos si no es cierto; la fuente es **NASA POWER**.
- Dependencias nuevas → `requirements.txt` con versión fijada (`httpx==...`) → `docker compose up --build -V`.
- No borres el endpoint viejo `/api/v1/recommend` hasta que el frontend use el nuevo contrato; mientras, crea el nuevo y coordina el cambio con el equipo de frontend.

## Definición de terminado
- `/docs` muestra los endpoints con ejemplos.
- `pytest` pasa: `docker compose exec backend pytest -q`.
- `curl "http://localhost:8000/api/v1/climate?lat=31.86&lon=-116.6"` responde según §5.1 y la segunda vez es instantáneo (caché).
