# Frontend: Layout, navegación y resultados

**Responsable:** Fernando (FernandoBorbas) · **Issue:** #1 · **Rama base:** `feature/front-layout`

> Agente: lee primero `docs/ARQUITECTURA.md` §4, §5 y §9. Ese documento manda.
> Cambios de la v2.0: `docs/CAMBIOS-ARQUITECTURA.md`.

## ⚠️ Cambio importante (v2.0)
El frontend ya **no es Next.js**. La app es la que hizo Mia (antes `field-shift/`), ahora en `frontend/`:
**React 19 + Vite 8 + TypeScript + Tailwind 4**, rutas en `frontend/src/`. Tus PRs #7 (Navbar) y #8
(historial) se hicieron sobre el Next.js borrado: hay que **portarlos** (ver tareas 1 y 2). Tu lógica sí
se reutiliza: formatos de fecha/número, estados de carga/error/vacío, tabla + tarjetas móviles.

## Stack
React 19 · Vite 8 · Tailwind 4 (tokens en `src/index.css` con `@theme`) · Framer Motion · Recharts ·
lucide-react · Zustand (`src/store/useStore.ts`) · TanStack Query.

## Archivos que te pertenecen
```
frontend/src/App.tsx                  navegación entre vistas (select | diagnosis | history)
frontend/src/index.css                tema: tokens de color y fuentes
frontend/src/views/DiagnosisView.tsx  resultados del análisis
frontend/src/views/HistoryView.tsx    (por crear) historial
frontend/src/components/Navbar.tsx    (por crear)
frontend/src/components/NasaMetricCard.tsx  ImpactBar.tsx  GaugeSoilHealth.tsx  CountUp.tsx
```
Compartido: `useStore.ts` es de Mia; para agregar `'history'` al tipo `view` (y una acción `goToHistory`)
coordina con ella. `api/` es de menaxmn: usa sus funciones, no hagas `fetch` directo.

## Tareas (en orden)
1. **Navbar** (de tu PR #7): `components/Navbar.tsx` con los tokens del tema (canvas/ink/leaf), no el tema
   oscuro gris del Next viejo. Enlaces: "Analizar" (`view='select'`) e "Historial" (`view='history'`).
   Debe convivir con el mapa a pantalla completa de `SelectView` (no taparlo en móvil).
2. **HistoryView** (de tu PR #8): usa `listAnalyses()` de `src/api/client.ts` con `useQuery`; tipo
   `AnalysisSummary` (§5.3). Columnas: fecha, ubicación (lat, lon), área, cultivo actual (`cropName`),
   prioridad, cultivos de la rotación. Clic en un renglón → `getAnalysis(id)` → `view='diagnosis'`.
   En modo mock ya devuelve 2 renglones de ejemplo.
3. **DiagnosisView**: mostrar `analysis.uncertainty` (nivel + motivo) de forma visible; revisar que las
   4 métricas se vean bien (ya está en `lg:grid-cols-4`); mantener las etiquetas "(estimado)" del nitrógeno
   y salud del suelo.
4. Responsivo y accesible (contraste, foco visible, `aria-label` en botones con solo ícono).

## Reglas
- Colores siempre con tokens del tema (`bg-leaf-600`, `text-ink-700`…), nada de hex sueltos en componentes.
- Textos en español; no digas "ML", "IA" ni "satélite": la fuente es "NASA POWER".
- Etiquetas de enums en español (`PRIORITY_LABEL`, `SEASON_LABEL`); los códigos llegan en inglés.

## Definición de terminado
- Se navega Analizar ⇄ Resultados ⇄ Historial sin recargar, en escritorio y móvil.
- Con `VITE_USE_MOCK=true` todo funciona sin backend; con `false` usa la API real sin cambios de código.
