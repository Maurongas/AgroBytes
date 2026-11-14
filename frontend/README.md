# 🌱 frontend — React 19 + Vite + Tailwind

App del DSS agrícola: dibujas tu parcela en el mapa, eliges cultivo y prioridad, y ves el diagnóstico
(métricas NASA POWER, rotación recomendada, impacto estimado, clima mensual).

> Antes era el proyecto `field-shift/` (de Mia). Desde la arquitectura v2.0 es **el** frontend oficial.

## Cómo correrlo

**Con Docker (recomendado), desde la raíz del repo:**
```bash
docker compose up --build
```
Abre 👉 http://localhost:3000

**Sin Docker (Node 20+):**
```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

## Datos: ejemplo (mock) o API real

| Variable | Qué hace |
|---|---|
| `VITE_API_URL` | URL del backend (`http://localhost:8000`) |
| `VITE_USE_MOCK` | `true` = usa `src/api/mock.ts`; `false` = llama al backend |

Con Docker se configuran en `docker-compose.yml` (o en un `.env` en la raíz). El mock tiene exactamente la
forma del contrato (`docs/ARQUITECTURA.md` §5), así que pasar a `false` no requiere cambiar código.

## Estructura

```
src/
├── api/         types.ts (contrato), client.ts (único lugar con fetch), mock.ts
├── store/       useStore.ts (Zustand)
├── lib/         crops.ts (catálogo de la UI)
├── views/       SelectView (mapa + panel), DiagnosisView (resultados)
└── components/  ParcelMap, QuickPanel, ScanOverlay, NasaMetricCard, ImpactBar, GaugeSoilHealth, CountUp
```
Quién es dueño de cada archivo: `docs/ARQUITECTURA.md` §4.

## Comandos útiles (dentro del contenedor)
```bash
docker compose exec frontend npx tsc -b      # revisar tipos
docker compose exec frontend npx eslint .    # lint
docker compose exec frontend npm install <paquete>   # luego: docker compose up --build -V frontend
```
