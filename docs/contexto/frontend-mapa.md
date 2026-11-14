# Contexto Claude — Frontend: Mapa Interactivo y Selección de Ubicación

**Responsable:** hdmiaa · **Issue:** #2 · **Rama base:** `feature/front-mapa`

> Claude: lee primero `docs/ARQUITECTURA.md` (secciones 3, 5.1, 5.4 y 9). Ese documento manda.

## Tu rol
El mapa es la entrada principal de la app: el usuario elige su parcela con un clic y de ahí salen
`lat` y `lon` para pedir el clima de NASA y la recomendación.

## Stack
Next.js 16.4 (App Router) · React 19.3 · TypeScript · Tailwind 4 · **react-leaflet 5 + leaflet** (react-leaflet 5 es la versión para React 19).
Tiles: OpenStreetMap (sin API key). No uses Mapbox, para no depender de llaves.

**Importante:** la ruta es `frontend/app/` (**no** `frontend/src/app/` como dice el issue).

## Archivos que te pertenecen
```
frontend/app/components/MapComponent.tsx     (mapa Leaflet, solo cliente)
frontend/app/components/LocationPicker.tsx   (envoltura con dynamic() + input de coordenadas + botón "Mi ubicación")
```
En `app/page.tsx` (compartido con Fernando) solo insertas `<LocationPicker value onChange />`.

## Puntos técnicos clave
- Leaflet usa `window` → **no puede renderizarse en servidor**. En `LocationPicker.tsx`:
  ```tsx
  const MapComponent = dynamic(() => import("./MapComponent"), { ssr: false });
  ```
  `MapComponent.tsx` lleva `"use client"`.
- Importa el CSS: `import "leaflet/dist/leaflet.css"` dentro de `MapComponent.tsx`.
- Ícono del marcador: con bundlers se rompe la ruta por defecto → configura `L.icon` con imágenes en `public/` o importadas.
- El contenedor del mapa necesita una altura explícita (`h-[400px]` o `h-full` dentro de un padre con altura).

## Tareas
1. Instalar: `docker compose exec frontend npm install leaflet react-leaflet` y `npm install -D @types/leaflet`, y luego `docker compose up --build -V`.
2. `MapComponent`: centrado por defecto en Ensenada, B.C. (31.86, -116.60), zoom 9. Un clic coloca o mueve el marcador y llama a `onChange({lat, lon})`.
3. `LocationPicker`:
   - Inputs de lat/lon sincronizados con el mapa (escribir mueve el marcador; un clic actualiza los inputs).
   - Botón "Usar mi ubicación" (`navigator.geolocation`), con manejo de permiso denegado.
   - Validación: lat ∈ [-90, 90], lon ∈ [-180, 180]; redondeo a 4 decimales.
   - Mostrar "Celda NASA ~50 km": la resolución de NASA POWER es de ~0.5°; opcional, dibujar el rectángulo de la celda.
4. Interfaz controlada: `type Ubicacion = { lat: number; lon: number }` (desde `lib/types.ts`); props `value: Ubicacion | null`, `onChange(u: Ubicacion)`.
5. (Fase 3) Mostrar las parcelas guardadas (`api.listFarms()`) como marcadores; clic en una → selecciona esa ubicación. Botón "Guardar parcela" (nombre + tipo de suelo) → `api.createFarm()`.
6. (Opcional) Al seleccionar el punto, llamar a `api.getClimate(lat, lon)` y mostrar un mini resumen en un popup.

## Reglas
- No hagas `fetch` directo: usa `lib/api.ts`.
- El mapa debe funcionar en móvil (touch) y no romper el layout de Fernando.
- Offline: si no hay red, los tiles no cargan. Muestra un aviso y deja usar los inputs de coordenadas (coordina con menaxmn).
- Librerías nuevas: sube `package.json` y `package-lock.json`.

## Definición de terminado
- Clic en el mapa → los inputs se actualizan → el formulario recibe `{lat, lon}`.
- Sin errores de `window is not defined` al recargar `/`.
- `npm run lint` sin errores.
