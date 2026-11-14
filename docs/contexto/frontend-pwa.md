# Frontend: PWA, offline y capa de datos

**Responsable:** menaxmn · **Issue:** #3 · **Rama base:** `feature/front-pwa`

> Agente: lee primero `docs/ARQUITECTURA.md` §5 y §9. Ese documento manda.
> Cambios de la v2.0: `docs/CAMBIOS-ARQUITECTURA.md`.

## ⚠️ Cambio importante (v2.0)
El frontend ya **no es Next.js**: es **React 19 + Vite 8** en `frontend/src/`. Por eso la PWA se hace con
**`vite-plugin-pwa`** (no `app/manifest.ts` ni `public/sw.js` a mano como decía la v1.0). La capa de datos
ya existe y es tuya: `src/api/` (cliente, tipos y mock), alineada con el contrato v2.0.

## Stack
Vite 8 · vite-plugin-pwa (Workbox) · TanStack Query · TypeScript 6.

## Archivos que te pertenecen
```
frontend/src/api/types.ts     espejo EXACTO de ARQUITECTURA §5 (Mauro revisa cambios)
frontend/src/api/client.ts    cliente único: createAnalysis, listAnalyses, getAnalysis (+ los que se agreguen)
frontend/src/api/mock.ts      datos de ejemplo con la forma de §5
frontend/src/lib/offline.ts   (por crear) guardar/leer último análisis
frontend/src/main.tsx         QueryClient y registro del service worker
frontend/vite.config.ts       plugins (aquí va VitePWA)
frontend/public/              íconos PWA
```

## Lo que ya existe
- `client.ts` con `request()` común: lee `VITE_API_URL`, muestra el `detail` de los errores del backend,
  y si `VITE_USE_MOCK=true` (por defecto en compose) responde con `mock.ts`.
- `types.ts`/`mock.ts` ya incluyen `uncertainty`, `location`, `createdAt` y `AnalysisSummary`.

## Tareas (en orden)
1. **PWA**: instala `vite-plugin-pwa` (versión compatible con Vite 8; `docker compose exec frontend npm install -D vite-plugin-pwa`
   y luego `docker compose up --build -V frontend`). Manifest: nombre, `short_name`, `display: standalone`,
   `theme_color`/`background_color` desde los tokens (`canvas` #FBF8F1, `orbit` #12261F), íconos 192/512 y maskable.
2. **Service worker**: precache del app shell; `NetworkFirst` para `/api/*`; no cachear masivamente tiles del mapa.
3. **Offline** (`lib/offline.ts`): guardar el último `AnalysisResponse` (y el último historial) en
   `localStorage` dentro de try/catch; si la petición falla sin red, devolver lo guardado y avisar en la UI.
4. **Banner offline** y **botón instalar** (componentes en `src/components/`; acuerda la ubicación con Fernando).
5. Mantener `types.ts` y `mock.ts` idénticos al contrato cada vez que cambie §5.

## Reglas
- Nadie hace `fetch` fuera de `src/api/`. Sin `any` en datos de la API.
- Si cambias el contrato: también `backend/app/schemas/` y ARQUITECTURA §5 (coordina con Mauro).

## Definición de terminado
- La app se instala (Chrome → "Instalar"), abre sin red y muestra el último análisis.
- Lighthouse PWA sin errores críticos.
