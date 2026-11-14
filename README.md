# 🚀 NasaSpaceApp — IA Agrícola

Plataforma de apoyo a la toma de decisiones agrícolas para el desafío **"Cambio de campo"** del NASA Space Apps Challenge.

El usuario captura temperatura, lluvia y tipo de suelo → el backend recomienda cultivos → la consulta se guarda en la base de datos y aparece en el historial.

## 🧱 ¿De qué está hecho?

```
 Navegador (tú)
     │
     ▼
┌──────────────┐  fetch   ┌──────────────┐   SQL    ┌──────────────────┐
│  frontend    │ ───────► │   backend    │ ───────► │       db         │
│  Next.js     │          │   FastAPI    │          │ PostgreSQL+PostGIS│
│  :3000       │          │   :8000      │          │  :5432           │
└──────────────┘          └──────────────┘          └──────────────────┘
  frontend/                 backend/                  (vive en Docker)
```

| Carpeta | Qué hay | Archivos importantes |
|---|---|---|
| `frontend/` | Página web (React / Next.js + Tailwind) | `app/page.tsx` (formulario), `app/historial/page.tsx` |
| `backend/` | API en Python (FastAPI + SQLAlchemy) | `app/main.py` (rutas), `app/services/algorithm.py` (reglas de cultivos), `app/models.py` (tablas) |
| `field-shift/` | Interfaz de diagnóstico de parcela (React + Vite + Tailwind, con mapa) | [field-shift/README.md](field-shift/README.md) |
| `docker-compose.yml` | Receta que levanta los 3 servicios juntos | — |

## ⚡ Arranque rápido

> ¿Primera vez? Lee primero **[docs/GUIA-INICIO.md](docs/GUIA-INICIO.md)** (instalar Docker, qué es, qué hacer si tienes poco espacio).

```bash
git clone https://github.com/nahuumm/NasaSpaceApp.git
cd NasaSpaceApp
docker compose up --build
```

Cuando termine de cargar:

- 🌐 Página web: http://localhost:3000
- 📜 Historial: http://localhost:3000/historial
- 🔧 API (documentación interactiva): http://localhost:8000/docs
- 🌱 field-shift: http://localhost:5173

Para apagar: `Ctrl + C` y luego `docker compose down`.

## 📚 Guías del equipo

- **[Guía de inicio (Docker + cómo desarrollar)](docs/GUIA-INICIO.md)**
- **[Guía de Git y GitHub (ramas, PRs, conflictos)](docs/GUIA-GIT.md)**
