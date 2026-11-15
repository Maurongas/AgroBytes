# NasaSpaceApp — DSS Agrícola (NASA Space Apps · "Cambio de campo")

Sistema de apoyo a la decisión agrícola: el usuario **dibuja su parcela en el mapa**, elige cultivo actual y
prioridad → el backend obtiene el clima de **NASA POWER** → un **motor de reglas** recomienda una **rotación
de cultivos por temporada** con puntaje, razones, riesgos, impacto estimado e incertidumbre.

- **Arquitectura y contrato de API (fuente de verdad):** `docs/ARQUITECTURA.md` (v2.0)
- **Qué cambió en la v2.0 y cómo actualizarse:** `docs/CAMBIOS-ARQUITECTURA.md`
- **Contexto por rol:** `docs/contexto/` → `backend.md`, `backend-dba.md`, `frontend-layout.md`, `frontend-mapa.md`, `frontend-pwa.md`
- Cómo correr: `docker compose up --build` (ver `docs/GUIA-INICIO.md`). Frontend :3000, API :8000/docs, BD :5432.

Reglas generales:
- Trabaja solo en los archivos de tu rol; si cambias el contrato (§5) o el modelo de datos (§6), actualiza
  ARQUITECTURA.md **y** los dos espejos del contrato (`backend/app/schemas/`, `frontend/src/api/types.ts` + `mock.ts`) en el mismo PR.
- Rutas reales: `frontend/src/` (React 19 + Vite 8 + Tailwind 4, **no Next.js**), `backend/app/`.
- No asumas APIs de versiones anteriores: React 19, Vite 8, TypeScript 6, Tailwind 4, react-leaflet 5, Pydantic v2, SQLAlchemy 2.
- El backend ya implementa todos los endpoints con NASA POWER real y PostgreSQL. `VITE_USE_MOCK=true` (default
  en compose) muestra datos de ejemplo de `frontend/src/api/mock.ts`; con `false` el frontend usa el backend.
- No describir como "ML"/"IA"/"satélite" algo que no lo es; la fuente de datos es NASA POWER. Nitrógeno y
  salud del suelo son **estimaciones por reglas** y se etiquetan así.
- Commits `feat:/fix:/chore:/docs:/refactor:`, ramas `feature/<area>-<tema>`, PR a `main` con 1 revisión.
