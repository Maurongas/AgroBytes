# 08 · Ximena: CI, QA y documentación

Nov 14, 2026 · @Mia

## Qué te toca

Tu menú y barra ya están. Lo que falta no es una pantalla nueva sino **garantizar que todo lo que ya hay se vea bien y no se rompa**, y dejar el repo presentable para el jurado.

- Rama: `feature/ci-qa-docs`, desde `main` actualizado.
- Orden: 1) CI del frontend, 2) QA de todas las vistas en celular y modo oscuro, 3) docs obsoletos, 4) README con capturas.
- Solo tocas `.github/workflows/frontend.yml`, `README.md`, `docs/*` y, si el QA encuentra bugs, **solo clases de Tailwind** en las vistas. Si el bug es de lógica, abre un issue y avisa a su dueño en vez de arreglarlo tú.

## Paso 1 · CI del frontend

Hoy nada revisa que el frontend compile antes de mergear: Mía lo corre a mano. Con esto GitHub lo hace en cada PR y bloquea los que rompen el build.

```bash
cd frontend   # o la raíz del repo
git switch main && git pull
git switch -c feature/ci-qa-docs
mkdir -p ../.github/workflows
```

Crea `.github/workflows/frontend.yml` en la **raíz del repo** (no dentro de `frontend/`):

```yaml
name: frontend
on:
  pull_request:
    paths: ['frontend/**', '.github/workflows/frontend.yml']
  push:
    branches: [main]
    paths: ['frontend/**']

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: npm ci
      - run: npm run lint
      - run: npm run build
```

`npm run build` ya ejecuta `tsc -b` y luego `vite build`, así que revisa tipos y empaquetado. Antes de subir el workflow, corre `npm run lint` en tu máquina: si hoy falla con errores viejos, **no bloquees a todos**: quita la línea de lint del workflow, mergea, y abre un issue "Arreglar lint".

Abre el PR. En la pestaña *Checks* debe aparecer `build` en verde. Luego pide a Mía activar la regla (Settings → Branches → *Require status checks to pass*); eso lo hace solo ella.

**Cuidado con `npm ci`:** si `package-lock.json` no coincide con `package.json` falla. Es una falla real: significa que alguien subió una dependencia sin actualizar el lock (lo que pide la plantilla de PR).

## Paso 2 · QA de todas las vistas

Abre la app (`npm run dev`, http://localhost:3000) y recorre **cada vista** (Seleccionar parcela, Diagnóstico, Historial, Alertas, Calendario, Comparar, Cuenta) con DevTools en modo celular (iPhone 12, 390 px) y luego en escritorio (1280 px). Haz cada prueba en modo claro **y** modo oscuro.

- [ ] No hay scroll horizontal en 390 px.
- [ ] Todos los botones se pueden tocar con el pulgar (al menos 44 px de alto).
- [ ] En modo oscuro no hay fondos blancos ni texto que se pierda.
- [ ] Con `Tab` el foco se ve en cada botón y enlace; los botones que son solo ícono tienen `aria-label`.
- [ ] Cada vista tiene estado de carga, de error y vacío con texto en español (para ver el error: `VITE_USE_MOCK=false` con el backend apagado).
- [ ] La barra inferior y el menú no tapan el contenido ni el panel "Tu parcela".

Dos búsquedas rápidas que encuentran la mayoría de los fallos de modo oscuro:

```bash
grep -rn "bg-white\|text-white\|bg-black\|text-black" src
grep -rnE "#[0-9a-fA-F]{6}" src --include=*.tsx
```

Cada resultado se cambia por su token: `bg-white` → `bg-surface-raised`, `text-white` → `text-paper`, y los colores `#...` por una clase de `src/index.css`. Los gráficos de Recharts (Diagnóstico) pueden llevar colores fijos; revísalos a mano en oscuro.

**Regla de oro:** en archivos que no son tuyos solo cambias *clases de Tailwind*. Si el fallo es de lógica, abre un issue con captura y méntalo a su dueño:

| Archivos | Dueño |
| --- | --- |
| `ParcelMap`, `QuickPanel`, `CompareView`, `AccountView`, login, tema | Mía |
| `HistoryView`, `DiagnosisView`, `OfflineBanner`, `lib/pdf.ts`, `lib/offline.ts` | Fernando |
| `api/client.ts`, `vite.config.ts`, PWA | menaxmn |
| `nav/*`, `AlertsView`, `CalendarView` | tú |

## Pasos 3 y 4 · Docs del frontend, README y PR

**Docs obsoletos del frontend.** Daniel arregla los del backend y los issues; tú estos:

- `docs/contexto/frontend-layout.md`: las líneas 9–11 dicen que hay que "portar" el historial y la barra (ya están hechos) y las líneas 23–24 marcan `HistoryView.tsx` y `Navbar.tsx` como "(por crear)". Quita esas marcas y el texto de "tareas pendientes".
- `docs/contexto/frontend-pwa.md`: línea 21, `offline.ts (por crear)`, ya existe. Después de que menaxmn mergee la PWA, agrega los archivos nuevos: `vite.config.ts` (plugin), `lib/deviceId.ts`, `components/InstallButton.tsx`, `pwa-assets.config.ts`.
- `docs/ARQUITECTURA.md` líneas 147, 151 y 155: quita las marcas `[PWA · pendiente]` y `[Layout · pendiente]` de `offline.ts`, `HistoryView.tsx` y `Navbar.tsx`.

**README con capturas.** El README es lo primero que ve el jurado. Reescríbelo con este orden, corto y sin tecnicismos de más:

1. Título, una frase de qué hace y la captura principal.
2. Qué problema resuelve (3 viñetas).
3. Cómo correrlo: `docker compose up --build`, y las direcciones http://localhost:3000 (app) y http://localhost:8000/docs (API).
4. De dónde salen los datos: NASA POWER (clima), ISRIC SoilGrids (suelo) y FAO ECOCROP (cultivos).
5. Límites honestos: son estimaciones por reglas agronómicas, no una predicción. **No uses las palabras "IA", "ML" ni "satélite"** donde no aplican (lo pide la plantilla de PR).
6. Equipo y roles.

Capturas: **tómalas al final**, cuando Mía avise que ya se mergearon todos los PRs. Guarda PNG de menos de 300 KB en `docs/img/` y enlázalas con `![Mapa con la parcela dibujada](docs/img/mapa.png)`. Cinco capturas bastan: mapa con la barra de herramientas, Diagnóstico, Comparar, Historial en celular y Diagnóstico en modo oscuro. En DevTools, menú de comandos (Cmd+Shift+P) → "Capture screenshot" te da la imagen del tamaño exacto.

**PR:**

```bash
npm run build   # en frontend/, antes de subir
git status
git add .github/workflows/frontend.yml README.md docs/
git commit -m "docs: CI del frontend, README con capturas y docs al día"
git push -u origin feature/ci-qa-docs
```

Si el QA encontró fallos de clases, haz esos arreglos en un PR aparte (`fix: modo oscuro en <vista>`), para que Mía los revise sin mezclarlos con los docs.
