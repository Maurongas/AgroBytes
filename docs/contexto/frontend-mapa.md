# Frontend: Mapa interactivo y selección de parcela

**Responsable:** Mia (hdmiaa) · **Issue:** #2 · **Rama base:** `feature/front-mapa`

> Agente: lee primero `docs/ARQUITECTURA.md` §4, §5.2 y §9. Ese documento manda.
> Cambios de la v2.0: `docs/CAMBIOS-ARQUITECTURA.md`.

## ⚠️ Cambio importante (v2.0)
Tu proyecto `field-shift/` **es ahora el frontend oficial** y vive en `frontend/` (historial de git
conservado). El Next.js viejo se borró. Corre en **http://localhost:3000** (antes 5173). Ajustes que se le
hicieron: puerto 3000, `lang="es"`, cliente apuntando a `POST /api/v1/analyses` con errores `detail`,
sin métrica NDVI ni "Rendimiento estimado", nitrógeno marcado como "(estimado)", unidad de humedad `0–1`.

## Stack
React 19 · Vite 8 · react-leaflet 5 · Leaflet 1.9 · @turf/turf · Zustand · TanStack Query · Tailwind 4.

## Archivos que te pertenecen
```
frontend/src/components/ParcelMap.tsx    mapa + dibujo del polígono
frontend/src/components/QuickPanel.tsx   panel: terreno, cultivo actual, prioridad, botón analizar
frontend/src/components/ScanOverlay.tsx  animación mientras analiza
frontend/src/views/SelectView.tsx
frontend/src/store/useStore.ts           estado global (otros agregan campos coordinando contigo)
frontend/src/lib/crops.ts                catálogo de cultivos de la UI (ids = backend)
```

## Tareas (en orden)
1. **Robustez del dibujo**: deshacer último punto, cancelar, impedir polígonos con < 3 puntos o que se
   crucen; mostrar el área (ya con turf). Recuerda: GeoJSON `[lon, lat]`, Leaflet `[lat, lon]` (conversión
   solo en `useStore.finishDrawing`).
2. **Buscar ubicación**: input de coordenadas y botón "Mi ubicación" (geolocalización del navegador) para
   centrar el mapa.
3. **Suelo (opcional)**: si se agrega al panel, usa `Soil` de `types.ts` (`sandy | loam | clay`) y `setSoil`.
4. **Atribución del mapa base**: Esri World Imagery pide "Esri, Maxar, Earthstar Geographics…" en la atribución.
5. Mantener `lib/crops.ts` alineado con `backend/app/data/crops.json` (mismos ids: ARQUITECTURA §5.1).
6. Agregar `'history'` al tipo `view` cuando Fernando lo necesite (él hace la vista).

## Reglas
- `field-shift/` ya no existe: no lo recrees. Todo cambio va en `frontend/`.
- No hagas `fetch` en componentes: usa `src/api/client.ts` (de menaxmn).
- Colores con tokens de `index.css`. Textos en español.

## Definición de terminado
- Dibujar, corregir y analizar una parcela funciona con mouse y en pantalla táctil.
- El request que sale cumple §5.2 (puedes verlo en la pestaña Red con `VITE_USE_MOCK=false`).
