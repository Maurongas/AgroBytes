# Contexto Claude — Backend DBA (Base de datos, modelos, migraciones)

**Responsable:** Daniel (daniel379618) · **Issue:** #4 · **Rama base:** `feature/back-db-models`

> Claude: lee primero `docs/ARQUITECTURA.md` (secciones 4, 6 y 10). Ese documento manda.

## Tu rol
Eres el responsable de datos del DSS agrícola: esquema PostgreSQL/PostGIS, modelos SQLAlchemy,
migraciones Alembic, repositorios (funciones de acceso a datos), catálogo de cultivos y configuración.
El backend (Mauro, `docs/contexto/backend.md`) consume tus repositorios; no escribe SQL.

## Stack
PostgreSQL 15 + PostGIS 3.3 (imagen `postgis/postgis:15-3.3`) · SQLAlchemy 2.x (estilo `Mapped[]`) ·
GeoAlchemy2 · Alembic · psycopg 3 · pydantic-settings.

## Archivos que te pertenecen
```
.env.example
docker-compose.yml          (servicio db y variables de entorno)
backend/alembic.ini
backend/alembic/            env.py, versions/
backend/app/core/config.py  Settings (DATABASE_URL, CORS_ORIGINS, NASA_POWER_BASE_URL, CLIMA_CACHE_DIAS, aportes de riego)
backend/app/db/             database.py, seed.py
backend/app/models/         farm.py consulta.py cultivo.py clima_cache.py __init__.py
backend/app/repositories/   farms.py consultas.py cultivos.py clima_cache.py
backend/app/data/cultivos.json
```

## Estado actual que vas a reemplazar
- `backend/app/database.py` tiene la URL escrita en el código → pasa a `app/db/database.py` + `core/config.py`.
- `backend/app/models.py` tiene `HistorialConsulta` y se crea con `Base.metadata.create_all` en `main.py`.
  `create_all` **no altera** tablas existentes (por eso truena la BD vieja) → se cambia por Alembic.
- `requirements.txt` trae `psycopg2-binary` y `psycopg[binary]` duplicados y sin versión. Deja solo `psycopg[binary]` con versión fijada.

## Tareas (en orden)
1. **Configuración** (lo primero, todos dependen de esto)
   - `core/config.py` con `pydantic-settings`; `.env.example` según §10; `docker-compose.yml` lee `env_file: .env`.
   - Mueve la conexión a `app/db/database.py` (`engine`, `SessionLocal`, `Base = DeclarativeBase`, `get_db`).
   - Deja `app/database.py` como reexport temporal (`from app.db.database import *`) para no romper `main.py`, y avísale a Mauro.
   - **Haz este PR chico y rápido** para que Mauro trabaje encima.
2. **Modelos** según §6: `Farm`, `Consulta`, `Cultivo`, `ClimaCache`.
   - `geom = mapped_column(Geography("POINT", srid=4326))` con índice GIST.
   - `clima_resumen`, `resultado`, `payload` como `JSONB`; `suelos_aptos` como `ARRAY(String)`.
   - Fechas `TIMESTAMPTZ` con `server_default=func.now()`.
   - `UniqueConstraint("lat_grid","lon_grid","periodo")` en `clima_cache`; `nombre` único en `cultivos`.
3. **Alembic**
   - `alembic init alembic`; `env.py` toma la URL de `settings` y el `target_metadata` de `Base`.
   - Primera migración: crea las 4 tablas, `CREATE EXTENSION IF NOT EXISTS postgis` y elimina `historial_consultas`.
   - Arranque: el comando del backend pasa a `sh -c "alembic upgrade head && python -m app.db.seed && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"` (en el Dockerfile o en el compose).
   - Quita `Base.metadata.create_all` de `main.py` (coordina con Mauro).
4. **Catálogo de cultivos** `app/data/cultivos.json`: 12–15 cultivos relevantes para el noroeste de México
   (maíz, trigo, sorgo, frijol, garbanzo, cebada, alfalfa, vid, tomate, chile, mijo, centeno, trébol, haba, girasol).
   Campos exactamente como la tabla `CULTIVOS` de §6. Fuente sugerida: **FAO ECOCROP** (rangos de temperatura y lluvia);
   pon la fuente en el campo `fuente`. `seed.py` hace upsert por `nombre` (correrlo dos veces no duplica nada).
5. **Repositorios** (funciones simples que reciben `db: Session`):
   - `clima_cache.get(db, lat_grid, lon_grid, periodo, max_dias)` / `upsert(...)`
   - `cultivos.list_all(db)` / `get_by_nombre(db, nombre)` (sin distinguir mayúsculas ni acentos)
   - `consultas.create(db, **datos) -> Consulta` / `list_recent(db, limit=20)` (con `farm_nombre` vía join)
   - `farms.create / list_all / get / near(db, lat, lon, km)` (usa `ST_DWithin` para demostrar PostGIS)
6. **Datos de demo:** script o seed opcional con 2–3 parcelas de ejemplo.

## Reglas
- Todo cambio de esquema = nueva migración (`alembic revision --autogenerate -m "..."`), revisada a mano. Nunca edites una migración ya mergeada.
- Nada de credenciales en el código; todo sale de `settings`.
- Si cambias columnas que aparecen en §5/§6 de ARQUITECTURA.md, actualízala en el mismo PR y avisa.

## Comandos útiles
```bash
docker compose exec db psql -U admin -d agridb      # consola SQL
docker compose exec backend alembic revision --autogenerate -m "mensaje"
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.db.seed
docker compose down -v                                # BD limpia (borra datos)
```

## Definición de terminado
- Con BD limpia, `docker compose up --build` crea todo y siembra los cultivos sin pasos manuales.
- `\dt` en psql muestra `farms, consultas, cultivos, clima_cache, alembic_version`.
- `SELECT count(*) FROM cultivos;` ≥ 12.
