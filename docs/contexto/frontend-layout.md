# Frontend: Layout, navegación y resultados

**Responsable:** Fernando (FernandoBorbas) · **Issue:** #1 · **Rama base:** `feature/front-layout`

> Agente: lee primero `docs/ARQUITECTURA.md` §4, §5 y §9. Ese documento manda.
> Cambios de la v2.0: `docs/CAMBIOS-ARQUITECTURA.md`.

## ⚠️ Cambio importante (v2.0)
El frontend ya **no es Next.js**. La app es la que hizo Mía (antes `field-shift/`), ahora en `frontend/`: **React 19 + Vite 8 + TypeScript + Tailwind 4**, rutas en `frontend/src/`. El historial (#8) y la barra de navegación (#7) ya se portaron a esta versión, y conservan su lógica: formatos de fecha/número, estados de carga/error/vacío, tabla + tarjetas móviles.

## Stack
React 19 · Vite 8 · Tailwind 4 (tokens en `src/index.css` con `@theme`) · Framer Motion · Recharts ·
lucide-react · Zustand (`src/store/useStore.ts`) · TanStack Query.

## Archivos que te pertenecen
```
frontend/src/App.tsx                  navegación entre vistas (select | diagnosis | history)
frontend/src/index.css                tema: tokens de color y fuentes
frontend/src/views/DiagnosisView.tsx  resultados del análisis
frontend/src/views/HistoryView.tsx    historial
frontend/src/components/NasaMetricCard.tsx  ImpactBar.tsx  GaugeSoilHealth.tsx  CountUp.tsx
```
Compartido: `useStore.ts` es de Mía y `api/` es de menaxmn: usa sus funciones, no hagas `fetch` directo.

## Estado
Las tareas de esta fase ya están terminadas:
- **Barra de navegación** portada a `components/nav/` (Sidebar y BottomBar).
- **HistoryView** portado: usa `listAnalyses()` y abre el diagnóstico al hacer clic.
- **DiagnosisView** muestra `analysis.uncertainty` y las 4 métricas.
- **Responsivo y accesible:** revisado en 390 px y 1280 px, en modo claro y oscuro.

## Reglas
- Colores siempre con tokens del tema (`bg-leaf-600`, `text-ink-700`…), nada de hex sueltos en componentes.
- Textos en español; no digas "ML", "IA" ni "satélite": la fuente es "NASA POWER".
- Etiquetas de enums en español (`PRIORITY_LABEL`, `SEASON_LABEL`); los códigos llegan en inglés.

## Definición de terminado
- Se navega Analizar ⇄ Resultados ⇄ Historial sin recargar, en escritorio y móvil.
- Con `VITE_USE_MOCK=true` todo funciona sin backend; con `false` usa la API real sin cambios de código.
