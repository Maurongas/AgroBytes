# Contexto Claude — Frontend: PWA, Offline y Cliente API

**Responsable:** menaxmn · **Issue:** #3 · **Rama base:** `feature/front-pwa`

> Claude: lee primero `docs/ARQUITECTURA.md` (secciones 5 y 9). Ese documento manda.

## Tu rol
Haces que la app se pueda instalar y siga siendo útil sin internet (agricultores en campo con mala señal).
Como el offline vive en la capa de red, también eres responsable del **cliente API** y de los **tipos**
que usa todo el frontend.

## Stack
Next.js 16.4 (App Router, Turbopack) · React 19.3 · TypeScript · Service Worker propio.

**Cambio respecto al issue:** **NO usar `next-pwa`**. No está mantenido y depende de webpack; Next 16
usa Turbopack. Usar en su lugar:
- `app/manifest.ts` (soporte nativo de Next para el manifiesto),
- `public/sw.js` escrito a mano,
- un componente cliente que lo registre.
(Revisa la guía oficial "Progressive Web Apps" de Next.js para la versión instalada.)

**Importante:** la ruta es `frontend/app/` (**no** `frontend/src/app/`).

## Archivos que te pertenecen
```
frontend/app/lib/types.ts         tipos TS = espejo de §5 de ARQUITECTURA (Mauro los revisa)
frontend/app/lib/api.ts           cliente único: getClimate, recommend, getHistory, listFarms, createFarm, listCrops
frontend/app/lib/offline.ts       guardar/leer la última recomendación y el historial
frontend/app/manifest.ts
frontend/public/sw.js
frontend/public/icons/            192x192, 512x512, maskable
frontend/app/components/SWRegister.tsx
frontend/app/components/OfflineBanner.tsx
frontend/app/components/InstallPrompt.tsx
```

## Tareas (en orden; 1 y 2 desbloquean a todo el frontend → hazlas primero)
1. **`lib/types.ts`**: tipos de todas las respuestas y peticiones de §5 (`ClimateSummary`, `RecommendRequest`,
   `RecommendationResponse`, `Recomendacion`, `HistoryItem`, `Farm`, `Ubicacion`, enums como uniones de string).
2. **`lib/api.ts`**:
   - `const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"` (quitar el `localhost:8000` escrito en las páginas).
   - Una función `request<T>()` que lanza `ApiError` con el `detail` del backend.
   - **Mock mode:** si `NEXT_PUBLIC_USE_MOCKS=1`, regresa los ejemplos de §5. Así Fernando y hdmiaa avanzan sin backend.
   - `recommend()` guarda la respuesta exitosa con `offline.saveLastResult()`; si falla por red, regresa la última guardada con la bandera `fromCache: true`.
3. **Manifest** (`app/manifest.ts`): nombre, short_name, `start_url: "/"`, `display: "standalone"`, colores del tema (pídelos a Fernando) e íconos.
4. **`public/sw.js`**:
   - install: precache del app shell (`/`, `/historial`, íconos, manifest).
   - fetch: estáticos de `/_next/static/` → cache-first; páginas → network-first con fallback al cache; `/api/*` → **no** cachear en el SW (eso lo hace `lib/api.ts`, que sabe qué es válido).
   - Versiona el nombre del cache (`dss-v1`) y borra los viejos en `activate`.
   - En desarrollo el SW puede estorbar al hot reload: regístralo solo si `process.env.NODE_ENV === "production"` o con un flag `NEXT_PUBLIC_ENABLE_SW=1`.
5. `SWRegister.tsx` (en `layout.tsx`, coordinado con Fernando), `OfflineBanner.tsx` (escucha `online`/`offline` y avisa "Sin conexión: mostrando la última consulta guardada") e `InstallPrompt.tsx` (`beforeinstallprompt`, botón en la Navbar).
6. Historial offline: `getHistory()` cachea la última lista.

## Cómo probar
- Build de producción dentro del contenedor: `docker compose exec frontend sh -c "npx next build && npx next start -H 0.0.0.0 -p 3001"` (expón el puerto o prueba en 3000 deteniendo el dev).
- DevTools → Application → Manifest / Service Workers. Network → "Offline" → recargar: debe cargar la interfaz y la última consulta.
- Lighthouse → categoría PWA.

## Reglas
- Ningún componente hace `fetch` directo; todos usan `lib/api.ts`.
- Si cambia el contrato en ARQUITECTURA §5, actualizas `types.ts` en el mismo PR.
- No guardes datos sensibles en el cache.

## Definición de terminado
- La app se puede instalar desde Chrome (escritorio y Android).
- En modo offline: carga la interfaz, muestra el banner y la última recomendación.
- `NEXT_PUBLIC_USE_MOCKS=1` permite usar toda la app sin backend.
