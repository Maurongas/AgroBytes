# Backend DBA (base de datos, migraciones, catálogo)

**Responsable:** Daniel (daniel379618) · **Issue:** #4 · **Rama base:** `feature/back-db-models`

> Agente: lee primero `docs/ARQUITECTURA.md` §4, §6 y §10. Ese documento manda.
> Cambios de la v2.0: `docs/CAMBIOS-ARQUITECTURA.md`.

## Tu rol
Diseñas y mantienes PostgreSQL + PostGIS: modelos SQLAlchemy, migraciones Alembic, repositorios
(consultas reutilizables), el catálogo de cultivos y el caché de clima. Mauro (backend) consume tus
repositorios; no escribe SQL.

## Stack
PostgreSQL 15 + PostGIS 3.3 · SQLAlchemy 2 · GeoAlchemy2 · Alembic · psycopg 3 · pydantic-settings.

## Lo que ya existe (v2.0)
- `app/core/config.py`: `Settings` (DATABASE_URL, CORS_ORIGINS, NASA_POWER_BASE_URL, CLIMATE_CACHE_DAYS) desde env.
- `app/db/database.py`: `engine`, `SessionLocal`, `Base(DeclarativeBase)`, `get_db`.
- `app/models/`, `app/repositories/`, Alembic y `seed.py`: ✅ hechos (migraciones `7c4987b08e73` → `c4e8a2f7b913`, incluye catálogo v2, `analyses.device_id` y `crop_countries`).
- **Catálogo v2:** `crops.json` (18 cultivos) **ya no se edita a mano**: lo genera `backend/research/build_crops.py`
  desde FAO ECOCROP + tablas FAO (`cd backend && python research/build_crops.py`). Para agregar un cultivo: un renglón
  en `CULTIVOS` del script, regenerar, y agregar el id en `frontend/src/lib/crops.ts`. Ver `docs/INVESTIGACION-CULTIVOS.md`.
- `app/data/README.md`: formato e ids obligatorios del catálogo.
- **Se borraron** `app/database.py`, `app/models.py` (`HistorialConsulta`) y el `create_all` de `main.py`.
  La tabla vieja `historial_consultas` sigue en tu BD local hasta tu primera migración.
- `requirements.txt` ya usa `psycopg[binary]` (v3); la URL es `postgresql+psycopg://...`.

## Archivos que te pertenecen
```
backend/app/core/config.py
backend/app/db/             database.py seed.py precalentar.py
backend/app/models/         __init__.py analysis.py crop.py climate_cache.py crop_country.py
backend/app/repositories/   analyses.py crops.py climate_cache.py crop_countries.py
backend/app/data/           crops.json crop_countries.json
backend/alembic.ini  backend/alembic/
backend/tests/test_repositories.py
docker-compose.yml (servicio db y el comando del backend)
```

## Tareas (en orden)
1. ✅ **Alembic**: `alembic init`, `env.py` leyendo `settings.DATABASE_URL` y `Base.metadata`. Agrega `alembic`
   (versión fijada) a `requirements.txt`. El contenedor backend debe correr `alembic upgrade head` antes de
   uvicorn (cambia el `CMD` del Dockerfile o agrega `command:` en compose; avisa al equipo).
2. ✅ **Modelos** (§6): `Analysis` (geom `Geography(POLYGON, 4326)` con índice GIST, lat/lon del centroide,
   `result` JSONB…), `Crop` (id texto: `maize`, `bean`…), `ClimateCache` (único `lat_grid, lon_grid, period`).
3. ✅ **Primera migración**: `CREATE EXTENSION IF NOT EXISTS postgis`, crea las 3 tablas y **elimina `historial_consultas`**.
4. ✅ **Catálogo** `app/data/crops.json` (hoy: 18 ids de ARQUITECTURA §5.1, generado por `research/build_crops.py`) y los campos de §6 (rangos de FAO ECOCROP/GAEZ, `source` por cultivo). `seed.py`
   idempotente (upsert por `id`). Si agregas cultivos, avisa a Mia para que los agregue en `frontend/src/lib/crops.ts`.
5. ✅ **Repositorios**: `analyses.create(db, ...) / list_recent(db, limit) / get(db, id)`,
   `crops.list_all(db)`, `climate_cache.get_valid(db, lat_grid, lon_grid, period, max_days) / upsert(...)`.
6. ✅ Tests de repositorios contra la BD del contenedor.

## Reglas
- Nada de `Base.metadata.create_all`: todo por migraciones.
- Cambios al modelo (§6) → actualiza ARQUITECTURA.md en el mismo PR y avisa a Mauro.
- Cuando tu migración llegue a `main`, avisa en el grupo: todos deben correr `docker compose down -v && docker compose up --build`.

## Definición de terminado
- `docker compose up --build` en una BD vacía deja las 3 tablas creadas y `crops` sembrada.
- `docker compose exec db psql -U admin -d agridb -c '\dt'` ya no muestra `historial_consultas`.
