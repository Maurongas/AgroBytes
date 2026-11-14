# Contexto Claude — Frontend: Layout, Navegación, Resultados e Historial

**Responsable:** Fernando (FernandoBorbas) · **Issue:** #1 · **Rama base:** `feature/front-layout`

> Claude: lee primero `docs/ARQUITECTURA.md` (secciones 4, 5 y 9). Ese documento manda.

## Tu rol
Diseñas la estructura visual y la experiencia de la app: layout global, Navbar, tema, tarjetas de
resultados y la página de historial. Eres el "dueño" del aspecto visual; los demás frontends usan tus componentes.

## Stack
Next.js **16.4** (App Router, Turbopack) · React 19.3 · TypeScript · Tailwind CSS 4 · corre en Docker.
Next 16 tiene cambios respecto a versiones anteriores: ante la duda, consulta la documentación incluida en
`node_modules/next/dist/docs/` o la oficial, y no asumas APIs de Next 13/14.

**Importante:** la ruta es `frontend/app/` (**no** `frontend/src/app/` como dice el issue).

## Archivos que te pertenecen
```
frontend/app/layout.tsx
frontend/app/globals.css
frontend/app/historial/page.tsx
frontend/app/components/Navbar.tsx
frontend/app/components/ResultCards.tsx      (las 3 estrategias)
frontend/app/components/ClimateCard.tsx      (resumen climático NASA + gráfica mensual)
frontend/app/components/ui/                  (Button, Card, Select... si se necesitan)
```
`app/page.tsx` es compartido con el equipo del mapa: tú haces el acomodo general (mapa | formulario | resultados) y el mapa lo pone hdmiaa.

## Tareas
1. `layout.tsx`: `<html lang="es">`, `metadata` con título "NasaSpaceApp — DSS Agrícola" y descripción, `<Navbar />` en todas las vistas.
2. `Navbar.tsx` responsivo (menú hamburguesa en móvil): logo/nombre, enlaces "Inicio" y "Historial", espacio a la derecha para `<InstallPrompt />` (lo hace menaxmn).
3. Tema en `globals.css` con variables de Tailwind 4 (`@theme`): colores primario (verde), acento y fondos. Hoy está todo en `bg-gray-900` repetido en cada página; centralízalo.
4. Extrae de la `page.tsx` actual el formulario y las tarjetas a componentes. El formulario ya **no** pide temperatura ni lluvia (las da NASA); pide: tipo de suelo, cultivo actual, disponibilidad de agua y prioridad. La ubicación viene del mapa.
5. `ResultCards.tsx`: recibe `RecommendationResponse` (tipo de `lib/types.ts`); muestra por estrategia: título, cultivo, **puntaje con barra**, lista de `justificacion`, beneficios, riesgos y tradeoff. Arriba, el nivel de incertidumbre con su `motivo`.
6. `ClimateCard.tsx`: temperatura media, lluvia anual, humedad del suelo (mostrar como %), fuente y periodo, y una gráfica sencilla de los 12 meses (puede ser SVG propio o una librería ligera como `recharts`; si agregas librería, avisa).
7. `historial/page.tsx`: tabla con los campos de §5.3; en móvil, tarjetas en lugar de tabla.

## Reglas
- **No hagas `fetch` directo**: usa `lib/api.ts` (lo mantiene menaxmn). Si necesitas una función nueva ahí, pídela o agrégala en coordinación.
- Tipos solo de `lib/types.ts`; nada de `any`.
- Estados de carga, error y vacío en cada vista.
- Textos en español; no digas "ML", "IA" ni "satélite" si no es cierto: la fuente es "NASA POWER".
- Accesible: `label` en cada input, contraste suficiente, que se use con teclado.
- Librería nueva: `docker compose exec frontend npm install <pkg>` y luego `docker compose up --build -V`; sube `package.json` y `package-lock.json`.

## Definición de terminado
- Navbar visible en `/` y `/historial`, y funciona en móvil (prueba a 375 px).
- Con una respuesta de ejemplo (puedes copiar la de §5.2 en un archivo mock), las tarjetas y el clima se ven completos.
- `npm run lint` sin errores: `docker compose exec frontend npm run lint`.
