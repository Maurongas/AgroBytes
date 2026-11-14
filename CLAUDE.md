# NasaSpaceApp — DSS Agrícola (NASA Space Apps)

Sistema de apoyo a la decisión agrícola: el usuario elige su ubicación en un mapa → el backend obtiene el clima
de NASA POWER → un motor de reglas recomienda 3 estrategias de cultivo con puntaje, explicación e incertidumbre.

- **Arquitectura y contrato de API (fuente de verdad):** `docs/ARQUITECTURA.md`
- **Contexto por rol:** `docs/contexto/` → `backend.md`, `backend-dba.md`, `frontend-layout.md`, `frontend-mapa.md`, `frontend-pwa.md`
- Cómo correr: `docker compose up --build` (ver `docs/GUIA-INICIO.md`). Frontend :3000, API :8000/docs, BD :5432.

Reglas generales:
- Trabaja solo en los archivos de tu rol; si cambias el contrato (§5) o el modelo de datos (§6), actualiza ARQUITECTURA.md en el mismo PR.
- Rutas reales: `frontend/app/` (sin `src/`), `backend/app/`.
- Next.js 16 / React 19 / Tailwind 4: no asumas APIs de versiones anteriores.
- No describir como "ML"/"IA"/"satélite" algo que no lo es; la fuente de datos es NASA POWER.
- Commits `feat:/fix:/chore:/docs:`, ramas `feature/<area>-<tema>`, PR a `main`.
