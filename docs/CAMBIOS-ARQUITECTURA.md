# Cambios de arquitectura v1.0 → v2.0 (definitiva)

Fecha: 2026-11-14 · PR: `chore/arquitectura-definitiva`

> **TL;DR:** el frontend oficial ahora es la app con mapa de Mia (antes `field-shift/`), que pasó a `frontend/`
> (React + Vite, puerto 3000). El Next.js viejo se borró. El resultado es una **rotación por temporada**.
> El contrato de la API cambió a `/api/v1/analyses` (camelCase, códigos en inglés). El backend tiene la
> estructura definitiva con el contrato listo y endpoints en 501 hasta que se implementen. El frontend
> funciona con datos de ejemplo mientras tanto.

---

## 1. Por qué

Había **tres contratos distintos** (backend viejo, ARQUITECTURA v1.0 y `field-shift`), **dos frontends**
que hacían lo mismo y un backend que decía "ML" y "satélite" con textos fijos. Era imposible que las
piezas se conectaran. Decisiones:

| Decisión | Elegido | Motivo |
|---|---|---|
| Frontend | La app de Mia (React + Vite) | Es la más completa (mapa, diseño, animaciones) y ya funciona; no necesita Next.js |
| Resultado | Rotación por temporada (3 pasos) | Es lo que ya muestra la UI y encaja con el reto "Cambio de campo" |
| Métricas | Solo lo calculable con NASA POWER | Sin NDVI ni rendimiento inventados; nitrógeno y salud del suelo = "estimado" |
| Alcance de este PR | Esqueleto funcionando | Estructura + contrato + docs; la lógica la hace cada dueño |

---

## 2. Qué cambió (archivo por archivo)

### Borrado
| Qué | Por qué |
|---|---|
| `frontend/` (Next.js completo: `app/page.tsx`, `historial/`, `layout.tsx`…) | Reemplazado por la app de Mia |
| `field-shift/` (como carpeta) | Se movió a `frontend/` con `git mv` (historial conservado) |
| Servicio `field-shift` en `docker-compose.yml` (puerto 5173) | Ya no existe; el frontend está en 3000 |
| `backend/app/services/algorithm.py` | Textos fijos que decían "ML"/"satélite" |
| `backend/app/schemas/recommendation.py` | Contrato viejo (`avg_temp`, `rainfall_mm`…) |
| `backend/app/database.py`, `backend/app/models.py` | Movidos a `app/db/` y `app/models/` (estructura definitiva) |
| Endpoints `POST /api/v1/recommend`, `GET /api/v1/history`, `GET /` | Reemplazados por `/api/v1/analyses` y `/health` |
| `Base.metadata.create_all` en `main.py` | Las tablas se crearán con Alembic (Daniel) |

### Nuevo
| Archivo | Qué es |
|---|---|
| `docs/CAMBIOS-ARQUITECTURA.md` | Este documento |
| `.env.example` (raíz) | Todas las variables, con los mismos valores por defecto que `docker-compose.yml` |
| `backend/app/core/config.py` | `Settings` desde env (DATABASE_URL, CORS_ORIGINS, NASA_POWER_BASE_URL, CLIMATE_CACHE_DAYS) |
| `backend/app/db/database.py` | engine, SessionLocal, `Base` (SQLAlchemy 2), `get_db` |
| `backend/app/models/`, `repositories/`, `services/`, `data/` | Paquetes con la lista de lo pendiente |
| `backend/app/schemas/base.py, analysis.py, climate.py, crop.py` | **Contrato completo** en Pydantic (JSON en camelCase) |
| `backend/app/api/v1/analyses.py, climate.py, crops.py` | Routers con el contrato; responden **501** hasta implementarse |
| `backend/tests/test_api.py` | 3 pruebas (`pytest` pasa) |
| `backend/research/` | Script que extrae el texto de las fuentes de datos sugeridas (`fuentes.md` no se sube) |

### Modificado
| Archivo | Cambio |
|---|---|
| `docs/ARQUITECTURA.md` | Reescrito a v2.0: stack, carpetas, contrato §5, modelo §6, reglas §7, NASA §8, frontend §9 |
| `docs/contexto/*.md` (los 5) | Reescritos: archivos, tareas y reglas de cada rol con la nueva estructura |
| `CLAUDE.md`, `README.md` | Nuevo flujo (mapa → NASA POWER → rotación); sin "IA Agrícola" |
| `docs/GUIA-GIT.md`, `docs/GUIA-INICIO.md` | Ramas por rol, ejemplos actualizados, puerto y mensajes de Vite |
| `.github/pull_request_template.md` | Checklist de contrato, tests y honestidad de datos |
| `docker-compose.yml` | 3 servicios (db, backend, frontend:3000), variables con valores por defecto |
| `.gitignore` (raíz) | `lib/` → `/lib/` (ya no esconde `frontend/src/lib/`) |
| `backend/requirements.txt` | Versiones fijadas; + `pydantic-settings`, `httpx`, `pytest`; − `psycopg2-binary` (se usa psycopg 3) |
| `backend/app/main.py` | CORS desde settings, routers v1, `/health` que revisa la BD |
| `frontend/vite.config.ts`, `Dockerfile` | Puerto 5173 → **3000** |
| `frontend/index.html`, `package.json` | `lang="es"`; nombre `frontend` |
| `frontend/src/api/types.ts` | Espejo del contrato v2.0: − `ndvi`; + `uncertainty`, `location`, `createdAt`, `AnalysisSummary` |
| `frontend/src/api/client.ts` | `POST /api/v1/analyses`; errores con `detail`; + `listAnalyses()`, `getAnalysis()` |
| `frontend/src/api/mock.ts` | − NDVI, − "Rendimiento estimado"; humedad en `0–1`; + incertidumbre, historial de ejemplo |
| `frontend/src/views/DiagnosisView.tsx` | Grid de 4 métricas; "Nitrógeno (estimado)"; pie de datos honesto (antes decía "SMAP · GIBS") |
| `frontend/README.md` | Reescrito como README del frontend oficial |

### Contrato: antes → ahora
| Antes (v1.0) | Ahora (v2.0) |
|---|---|
| `POST /api/v1/recommend` con `lat, lon, tipo_suelo, disponibilidad_agua, prioridad` | `POST /api/v1/analyses` con `geometry` (polígono), `currentCrop`, `priority`, `soil?` |
| 3 estrategias `actual / optimizada / resiliente` | `rotation`: 3 temporadas con cultivo, score, razones, riesgos |
| `GET /api/v1/history` | `GET /api/v1/analyses?limit=20` (+ `GET /api/v1/analyses/{id}`) |
| Campos en español snake_case (`tipo_suelo`) | camelCase; códigos en inglés (`priority: "water"`, `cropId: "maize"`) |
| `prioridad: conservar_agua / mejorar_suelo / ingresos_extra` | `priority: water / nitrogen / yield` |
| Suelo `arcilloso / arenoso / limoso / franco` | `soil.texture: sandy / loam / clay` (opcional) |
| `disponibilidad_agua` | Eliminado (la prioridad `water` lo cubre) |
| Tablas `farms`, `consultas`, `cultivos`, `clima_cache` | `analyses`, `crops`, `climate_cache` (sin `farms` en el MVP) |

---

## 3. Qué hace cada quien para ponerse al día

### Todos (una vez)
```bash
# 1. Guarda lo que tengas (en TU rama, no en main)
git add . && git commit -m "wip: antes de arquitectura v2"   # si tienes cambios

# 2. Trae la arquitectura nueva
git switch main && git pull

# 3. Reconstruye (cambió el puerto del frontend y se quitó un servicio)
docker compose down --remove-orphans
docker compose up --build -V
```
Abre http://localhost:3000 (la app con mapa) y http://localhost:8000/docs (la API nueva).
**No hace falta** `down -v` todavía: la BD se reinicia cuando entre la migración de Daniel (él avisará).

Luego pon al día a tu agente (Claude u otro) con el mensaje de la sección 4.

### Fernando — Layout (#1)
Tus PRs **#7 (Navbar) y #8 (historial)** son sobre el Next.js borrado: **no se pueden mergear**. Tu lógica se reutiliza:
```bash
git switch main && git pull
git switch -c feature/front-navbar          # y luego otra para el historial
# ver tu código anterior sin cambiar de rama:
git show origin/feature/front-historial:frontend/app/historial/page.tsx
git show origin/feature/front-layout:frontend/app/components/Navbar.tsx
```
- Navbar → `frontend/src/components/Navbar.tsx` con los tokens del tema (no el gris oscuro).
- Historial → `frontend/src/views/HistoryView.tsx` usando `listAnalyses()` (ya existe en `src/api/client.ts`, con mock) y el tipo `AnalysisSummary`.
- Cierra #7 y #8 cuando abras los nuevos PRs.
- Detalle: `docs/contexto/frontend-layout.md`.

### Mia — Mapa (#2)
Tu app es ahora el frontend oficial (`frontend/`, puerto **3000**).
- **Si tenías cambios sin subir en `field-shift/`:** haz commit en una rama **antes** de traer `main` y luego
  `git merge main`: git detecta el renombre y mueve tus cambios a `frontend/` solo. No recrees `field-shift/`.
- Rama nueva: `git switch main && git pull && git switch -c feature/front-mapa`.
- Detalle: `docs/contexto/frontend-mapa.md`.

### menaxmn — PWA y datos (#3)
- La PWA ahora es con **`vite-plugin-pwa`** (ya no `app/manifest.ts` de Next).
- Eres dueño de `frontend/src/api/` (cliente, tipos y mock), que ya existe y está alineado con el contrato.
- Rama nueva: `git switch main && git pull && git switch -c feature/front-pwa`.
- Detalle: `docs/contexto/frontend-pwa.md`.

### Daniel — Base de datos (#4)
- `core/config.py` y `db/database.py` ya existen (base mínima): **son tuyos**, ajústalos como necesites.
- Modelos nuevos: `analyses`, `crops` (id texto: `maize`, `bean`…), `climate_cache` (ARQUITECTURA §6).
- Tu rama no tenía commits: `git switch feature/back-db-models && git merge origin/main`.
- Si tenías cambios locales en `app/models.py` o `app/database.py` (borrados): haz commit antes del merge; al
  resolver el conflicto, mueve tu código a `app/models/` y `app/db/`.
- Detalle: `docs/contexto/backend-dba.md`.

### Mauro — Backend (#5)
- El contrato (`schemas/`) y los routers ya están; siguen `services/` (NASA POWER → clima → reglas).
- `git switch feature/back-nasa-api && git merge origin/main`.
- Detalle: `docs/contexto/backend.md`.

---

## 4. Mensaje para tu agente (cópialo y pégalo)

> Cambia `<rol>` por `backend`, `backend-dba`, `frontend-layout`, `frontend-mapa` o `frontend-pwa`.

```text
El proyecto cambió a la arquitectura v2.0 (definitiva). Antes de hacer cualquier cosa:
1. Lee CLAUDE.md, docs/ARQUITECTURA.md, docs/CAMBIOS-ARQUITECTURA.md y docs/contexto/<rol>.md.
2. Descarta cualquier contexto, memoria o plan anterior que mencione: Next.js, frontend/app/, field-shift/,
   el puerto 5173, /api/v1/recommend, /api/v1/history, "3 estrategias" (actual/optimizada/resiliente),
   avg_temp/rainfall_mm, tipo_suelo/disponibilidad_agua, historial_consultas, algorithm.py, next-pwa,
   app/manifest.ts, NDVI o "rendimiento estimado".
3. Hechos actuales: el frontend es React 19 + Vite 8 en frontend/src/ (puerto 3000); el contrato es
   POST/GET /api/v1/analyses en camelCase con códigos en inglés; el resultado es una rotación por temporada;
   los endpoints responden 501 hasta implementarse y el frontend usa VITE_USE_MOCK=true mientras tanto.
4. Trabaja solo en los archivos de mi rol según docs/contexto/<rol>.md. Si algo requiere cambiar el contrato
   (§5) o el modelo de datos (§6), dímelo antes: hay que cambiar ARQUITECTURA.md y ambos espejos del contrato.
Si tienes archivos de memoria con información del proyecto, actualízalos con estos hechos.
```

---

## 5. Pendientes que quedan explícitos (no los hizo este PR)

| Pendiente | Dueño |
|---|---|
| `services/geo.py`, `nasa_power.py`, `climate.py`, `recommender.py`; implementar los 5 endpoints | Mauro |
| Alembic, modelos, primera migración (borra `historial_consultas`), `crops.json`, repositorios | Daniel |
| Navbar, HistoryView, mostrar incertidumbre en DiagnosisView | Fernando |
| Robustez del dibujo, buscar ubicación, atribución completa de Esri | Mia |
| vite-plugin-pwa, `lib/offline.ts`, banner offline, botón instalar | menaxmn |
| Actualizar el texto de los issues #1–#5 en GitHub (aún mencionan Next.js / `src/app`) | Mauro |
