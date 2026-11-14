# 🌱 NasaSpaceApp — DSS Agrícola

Sistema de apoyo a la decisión para el desafío **"Cambio de campo"** del NASA Space Apps Challenge.

**Cómo funciona:** dibujas tu parcela en el mapa y eliges tu cultivo actual y tu prioridad (ahorrar agua,
regenerar nitrógeno o maximizar rendimiento). El backend obtiene el clima de esa ubicación de
**NASA POWER** y un **motor de reglas agronómicas** recomienda una **rotación de cultivos por temporada**,
con puntaje, razones, riesgos, impacto estimado e incertidumbre.

> Sin "IA" ni "ML": son reglas transparentes y explicables (ver `docs/ARQUITECTURA.md` §7).

## 🧱 ¿De qué está hecho?

```
 Navegador / PWA
       │
       ▼
┌──────────────────┐  REST   ┌──────────────┐  SQL   ┌────────────────────┐
│  frontend        │ ──────► │  backend     │ ─────► │  db                │
│  React + Vite    │         │  FastAPI     │        │  PostgreSQL+PostGIS│
│  :3000 (mapa)    │         │  :8000       │ ─────► │  :5432             │
└──────────────────┘         └──────────────┘ httpx  └────────────────────┘
                                     └──────────────► NASA POWER API
```

| Carpeta | Qué hay |
|---|---|
| `frontend/` | App React 19 + Vite + Tailwind: mapa para dibujar la parcela, resultados, historial, PWA |
| `backend/` | API FastAPI: contrato en `app/schemas/`, rutas en `app/api/v1/`, lógica en `app/services/` |
| `docs/` | Arquitectura, guías y contexto por rol |
| `docker-compose.yml` | Levanta los 3 servicios juntos |

## ⚡ Arranque rápido

> ¿Primera vez? Lee **[docs/GUIA-INICIO.md](docs/GUIA-INICIO.md)** (instalar Docker, qué es, poco espacio).

```bash
docker compose up --build
```

| Qué | URL |
|---|---|
| App | http://localhost:3000 |
| API (documentación interactiva) | http://localhost:8000/docs |

Por defecto el frontend usa **datos de ejemplo** (`VITE_USE_MOCK=true`) mientras el backend implementa los endpoints.

## 📚 Documentación

- [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) — arquitectura, contrato de API, modelo de datos, reglas (**fuente de verdad**)
- [docs/CAMBIOS-ARQUITECTURA.md](docs/CAMBIOS-ARQUITECTURA.md) — qué cambió en la v2.0 y cómo actualizarte
- [docs/GUIA-INICIO.md](docs/GUIA-INICIO.md) — Docker y primeros pasos
- [docs/GUIA-GIT.md](docs/GUIA-GIT.md) — ramas, PRs y conflictos
- [docs/contexto/](docs/contexto/) — qué le toca a cada rol

## 👥 Equipo

| Rol | Responsable | Issue |
|---|---|---|
| Frontend · Layout y navegación | Fernando (FernandoBorbas) | #1 |
| Frontend · Mapa | Mia (hdmiaa) | #2 |
| Frontend · PWA y datos | menaxmn | #3 |
| Backend · Base de datos | Daniel (daniel379618) | #4 |
| Backend · API, NASA POWER y reglas | Mauro (Maurongas) | #5 |
