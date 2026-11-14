# 🌱 field-shift — Diagnóstico de parcela

Interfaz web (React + Vite + TypeScript + Tailwind) para seleccionar una parcela en el mapa y ver su diagnóstico: salud del suelo, métricas de la NASA e impacto.

Es un proyecto **independiente** dentro del repo: no modifica `frontend/` ni `backend/`.

## ⚡ Cómo correrlo

### Opción A — con Docker (junto con el resto del proyecto)

Desde la raíz del repo:

```bash
docker compose up --build
```

Abre 👉 http://localhost:5173

### Opción B — sin Docker (necesitas Node 20+)

```bash
cd field-shift
npm install
npm run dev
```

Abre 👉 http://localhost:5173

## 🔌 Datos: ejemplo (mock) o API real

Por defecto usa **datos de ejemplo**, así funciona sin backend.

Para conectarlo a una API, copia `.env.example` como `.env.local` y llena:

```
VITE_API_URL=http://localhost:8000
VITE_USE_MOCK=false
```

> ⚠️ La app espera la ruta `POST /api/analyses`, que **todavía no existe** en `backend/` (el backend actual tiene `/api/v1/recommend` y `/api/v1/history`). Mientras no se agregue, déjala en modo mock.

## 📁 Estructura

| Carpeta | Qué hay |
|---|---|
| `src/views/` | Pantallas: `SelectView` (elegir parcela) y `DiagnosisView` (resultados) |
| `src/components/` | Mapa, medidores, tarjetas de métricas NASA, animaciones |
| `src/api/` | Cliente de la API, tipos y datos de ejemplo (`mock.ts`) |
| `src/store/` | Estado global (zustand) |
