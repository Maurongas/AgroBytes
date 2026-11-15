# 06 · Backend (Mauro + Daniel): lo que falta

Nov 14, 2026 · @Mia

## Reparto

El backend ya cumple el contrato v2.1 (CORS con `allow_headers=["*"]` ya deja pasar `X-Device-Id`). Lo que falta es endurecerlo para la demo y limpiar el repo.

| Tarea | Quién | Rama | Depende de |
| --- | --- | --- | --- |
| CI de pytest en GitHub Actions | Mauro | `feature/back-ci` | nada |
| Resiliencia si NASA POWER no responde | Mauro | `feature/back-resiliencia` | nada |
| Activar `REQUIRE_DEVICE_ID=true` | Mauro | `feature/back-device-obligatorio` | PR A de menaxmn (el frontend ya manda el header) |
| Pre-calentar la caché de clima para la demo | Daniel | `feature/back-precalentar` | nada |
| Textos de issues #1–#5 y marcas "por crear" en docs | Daniel | `docs/actualizar-pendientes` | nada |
| Borrar `frontend/next-env.d.ts`, cerrar PRs #6/#7/#8, borrar ramas viejas | Daniel | `chore/limpieza-repo` | nada |

## Mauro: CI, plan B de NASA y device obligatorio

**1 · CI de pytest** (`feature/back-ci`). Hoy nadie corre las pruebas antes de mergear. Crea `.github/workflows/backend.yml`. `test_repositories.py` necesita PostgreSQL con PostGIS, por eso el workflow levanta uno igual al de `docker-compose.yml`:

```yaml
name: backend
on:
  pull_request:
    paths: ['backend/**', '.github/workflows/backend.yml']
  push:
    branches: [main]
    paths: ['backend/**']

jobs:
  pytest:
    runs-on: ubuntu-latest
    services:
      db:
        image: postgis/postgis:15-3.3
        env:
          POSTGRES_USER: admin
          POSTGRES_PASSWORD: password
          POSTGRES_DB: agridb
        ports: ['5432:5432']
        options: >-
          --health-cmd "pg_isready -U admin -d agridb"
          --health-interval 5s --health-timeout 5s --health-retries 10
    env:
      DATABASE_URL: postgresql+psycopg://admin:password@localhost:5432/agridb
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: pip
          cache-dependency-path: backend/requirements.txt
      - run: pip install -r requirements.txt
      - run: alembic upgrade head
      - run: pytest -q
```

La versión de Python (3.11) es la del `backend/Dockerfile`. Abre el PR: la pestaña *Checks* debe mostrar `pytest` en verde. Si falla por la base de datos, revisa que el `DATABASE_URL` use `localhost` (en CI no existe el host `db`).

**2 · Plan B si NASA POWER no responde** (`feature/back-resiliencia`). Hoy ya se usa la caché vencida del clima de largo plazo, pero los últimos 90 días (`fetch_daily`) siempre piden a NASA: si cae justo en la demo, hasta un punto pre-calentado devuelve 503. Propuesta: si lo diario falla pero el largo plazo existe, tratar "lo reciente" como "lo normal" (sin anomalía) y seguir. En `backend/app/services/climate.py` agrega, junto a `build_recent`:

```python
def recent_from_normals(monthly: Series, summary: ClimateSummary, start: date, end: date) -> RecentClimate:
    """Plan B cuando los datos diarios no llegan: lo reciente se toma como igual a lo normal."""
    start_year, end_year = (int(y) for y in summary.period.split("-"))

    def normal(param: str, month: int) -> float | None:
        vals = [
            v for y in range(start_year, end_year + 1)
            if (v := monthly.get(param, {}).get(f"{y}{month:02d}")) is not None
        ]
        return _mean(vals) if vals else None

    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    last_30 = days[-30:]
    normal_temp = {p.month: p.temp_c for p in summary.monthly}
    soil = [s for d in last_30 if (s := normal("GWETROOT", d.month)) is not None]
    if not soil:
        raise NasaUnavailableError("Sin datos normales de humedad de suelo")
    rain_normal = round(sum(normal("PRECTOTCORR", d.month) or 0.0 for d in days), 1)
    temp_normal = round(_mean([normal_temp[d.month] for d in last_30]), 2)
    return RecentClimate(
        start=start, end=end,
        rain_90d_mm=rain_normal, rain_90d_normal_mm=rain_normal,
        temp_30d_c=temp_normal, temp_30d_normal_c=temp_normal,
        soil_moisture_30d=round(_mean(soil), 3),
    )
```

Y en `get_climate`, envuelve el bloque `if recent is None:` así (los datos del plan B **no** se guardan en `_recent_cache`, para que al volver NASA se pidan los reales):

```python
        if recent is None:
            try:
                (summary, monthly), daily = await asyncio.gather(
                    _long_term(client, lat_g, lon_g, today, db),
                    nasa_power.fetch_daily(lat_g, lon_g, start, end, client=client),
                )
                recent = build_recent(daily, monthly, summary, start, end)
                _recent_cache.set((lat_g, lon_g, end), recent)
            except NasaUnavailableError:
                # Si tampoco hay largo plazo (caché ni NASA), esta llamada vuelve a lanzar y la API da 503
                summary, monthly = await _long_term(client, lat_g, lon_g, today, db)
                log.warning("Sin datos diarios de NASA para (%s, %s): se usa lo normal como reciente", lat_g, lon_g)
                recent = recent_from_normals(monthly, summary, start, end)
        else:
            summary, _ = await _long_term(client, lat_g, lon_g, today, db)
```

Agrega una prueba en `backend/tests/` que sustituya `nasa_power.fetch_daily` por una función que lance `NasaUnavailableError` (como hace `test_api.py` con `monkeypatch`) y verifique que `get_climate` devuelve `rain_90d_mm == rain_90d_normal_mm`. Antes de empezar confirma con `grep -n GWETROOT app/services/nasa_power.py` que esa variable también se pide en la serie mensual; si no, no uses este plan y deja el 503.

**3 · Activar `REQUIRE_DEVICE_ID`** (`feature/back-device-obligatorio`). **Solo después** de que el PR A de menaxmn esté en `main`: si lo activas antes, el historial de la app deja de cargar. Cambia solo el valor por defecto de `docker-compose.yml` (en `config.py` déjalo en `False`, las pruebas lo suponen así):

```yaml
      REQUIRE_DEVICE_ID: ${REQUIRE_DEVICE_ID:-true}
```

Y en `.env.example` pon `REQUIRE_DEVICE_ID=true`. CORS ya acepta el header (`allow_headers=["*"]`), no hay que tocarlo.

## Daniel: caché de demo, limpieza y docs del backend

**1 · Pre-calentar el clima de la demo** (`feature/back-precalentar`). La primera consulta de cada lugar tarda varios segundos porque baja 10 años de NASA POWER. Con esto, ese tiempo se paga antes de la presentación. Crea `backend/app/db/precalentar.py`:

```python
"""Pre-calienta la caché de clima (tabla climate_cache) con los lugares de la demo.

Uso, con `docker compose up` corriendo:
    docker compose exec backend python -m app.db.precalentar
Así el primer análisis de cada lugar no espera a NASA POWER durante la presentación.
"""

import asyncio
import time

from app.db.database import SessionLocal
from app.services import climate as climate_service
from app.services.nasa_power import NasaUnavailableError

LUGARES = {
    "Ensenada": (31.86, -116.60),
    "Valle de Guadalupe": (32.08, -116.62),
    "Tijuana": (32.51, -117.04),
    "Mexicali": (32.66, -115.47),
    "Culiacán": (24.80, -107.39),
}


async def main() -> None:
    with SessionLocal() as db:
        for nombre, (lat, lon) in LUGARES.items():
            inicio = time.perf_counter()
            try:
                await climate_service.get_climate(lat, lon, db=db)
                print(f"OK     {nombre:<20} {time.perf_counter() - inicio:5.1f} s")
            except NasaUnavailableError as exc:
                print(f"FALLÓ  {nombre:<20} {exc}")


if __name__ == "__main__":
    asyncio.run(main())
```

Ejecútalo dos veces: la segunda debe tardar menos, porque el clima de largo plazo ya queda en la tabla `climate_cache` (sobrevive reinicios). Compruébalo con:

```bash
docker compose exec db psql -U admin -d agridb -c "select count(*) from climate_cache;"
```

Debe haber al menos una fila por lugar. Los últimos 90 días viven solo en memoria y se renuevan cada día, así que vale la pena correr el script **la mañana de la demo** y otra vez si alguien hace `docker compose down -v` (que borra la base de datos).

**2 · Limpieza del repo** (`chore/limpieza-repo`):

1. Quita el archivo que quedó de Next.js: `git rm frontend/next-env.d.ts`. Corre `npm run build` en `frontend/` para confirmar que no hacía falta.
2. En GitHub, cierra los PRs viejos #6, #7, #8 y el #24 (el de Mía que se reemplazó) con este comentario: "Cerrado: se reemplazó con la arquitectura v2.0 (React + Vite), ver docs/CAMBIOS-ARQUITECTURA.md". **No los mergees.**
3. Borra las ramas viejas **solo después de preguntar a su dueño** (`prueba/mia-todo`, `feature/front-layout`, `fix/field-shift-gitignore`):

```bash
git fetch --prune
git branch -r --merged origin/main   # estas ya están en main: seguras de borrar
git push origin --delete prueba/mia-todo feature/front-layout fix/field-shift-gitignore
```

**3 · Docs y issues del backend** (`docs/actualizar-pendientes`). Ximena actualiza los docs del frontend y el README; tú solo estos:

- `docs/contexto/backend.md` línea 34: `(por crear)` ya no es cierto, los servicios existen. Quita la marca o llámalo "hecho".
- `docs/contexto/backend-dba.md`: busca con `grep -n -i "por crear\|pendiente\|TODO" docs/contexto/backend-dba.md` y actualiza lo que ya exista (migraciones `alembic/versions/`, `device_id`, catálogo v2).
- Los issues #1–#5 de GitHub: abre cada uno, edita el texto y cambia cualquier mención a "Next.js" por "React + Vite". Si el trabajo ya está hecho, ciérralo con un comentario que enlace el PR que lo resolvió.

## Cómo probar y mandar los PRs

Cada tarea va en **su propia rama y su propio PR**, desde `main` actualizado (`git switch main && git pull`). Antes de cada PR, en la raíz del repo:

```bash
docker compose up --build -d
docker compose exec backend pytest -q   # debe pasar todo
git status                              # solo tus archivos, nunca .env
git add <archivo1> <archivo2>           # nombra los archivos; nunca git add .
git commit -m "feat: <qué hiciste>"     # o fix: / docs: / chore:
git push -u origin <tu-rama>
```

Abre el PR hacia `main`, llena la plantilla y menciona a Mía. Verificaciones para dar cada tarea por terminada:

- [ ] **CI**: el PR de `feature/back-ci` muestra `pytest` en verde en la pestaña *Checks*.
- [ ] **Plan B**: con `NASA_POWER_BASE_URL=http://localhost:9 docker compose up -d --force-recreate backend`, un POST a `/api/v1/analyses` en un lugar pre-calentado (Ensenada) responde 200 y en `docker compose logs backend` aparece "se usa lo normal como reciente"; en un lugar nuevo (por ejemplo 20.0, -100.0) responde 503 con `NASA POWER no disponible`. Vuelve a levantar sin esa variable al terminar.
- [ ] **Device obligatorio**: `curl -i http://localhost:8000/api/v1/analyses` responde 400 "Falta el header X-Device-Id", y `curl -i -H "X-Device-Id: prueba-12345678" http://localhost:8000/api/v1/analyses` responde 200.
- [ ] **Pre-calentado**: un análisis en Ensenada desde Swagger (http://localhost:8000/docs) tarda menos de 3 s.
- [ ] **Limpieza**: `frontend/next-env.d.ts` ya no existe y `npm run build` en `frontend/` sigue pasando.
