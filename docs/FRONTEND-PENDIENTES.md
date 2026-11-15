# Frontend: funciones pendientes para aprovechar el backend v2

> Qué debe agregar el frontend para usar todo lo que ya hace el backend (catálogo de 18 cultivos de FAO, riego,
> suelo automático, barbecho, riego estimado, nuevos riesgos). Fecha: 2026-11-14.
> Contrato completo: `ARQUITECTURA.md` §5. Tipos ya actualizados en `frontend/src/api/types.ts` y `mock.ts`.

## Ya hecho en este PR (no hay que hacerlo)
- `api/types.ts`: `irrigated` en la petición; `irrigationMm` por paso; `soilDetected` e `irrigated` en la
  respuesta; tipos `DetectedSoil`, `CropInfo` y `CropRole`.
- `api/mock.ts`: datos de ejemplo con esos campos.
- `lib/crops.ts`: los 18 cultivos y `cropName('fallow')` → "Descanso (barbecho)".
- `tsc -b` compila sin errores. **Nada de la UI cambió**: todo lo de abajo está pendiente.

## Prioridad alta (sin esto la app se ve rota o pierde lo más útil)

### 1. Pregunta de riego · `QuickPanel` (Mapa – Mia)
- Control "¿Tu parcela tiene riego?" con **Sí / No / No sé** → `irrigated: true | false | undefined`.
- Guardarlo en `useStore` (`irrigated: boolean | null`, `setIrrigated`) y mandarlo en `SelectView`:
  ```ts
  mutation.mutate({ geometry, currentCrop: crop, priority, soil: soil ?? undefined, irrigated: irrigated ?? undefined });
  ```
- Por qué importa: en Baja California la mayor parte es de riego; con `true` el motor deja de castigar por falta
  de lluvia y compara cuánto riego necesita cada cultivo.

### 2. Barbecho (`cropId === 'fallow'`) · `DiagnosisView` (Layout – Fernando)
- Un paso puede venir como `{ cropId: 'fallow', score: 0, plantingWindow: '—', irrigationMm: 0 }`.
- Mostrarlo con otro estilo (gris, ícono de descanso), sin "puntaje 0" ni barra de puntaje, con sus `reasons`.
- `cropName('fallow')` ya devuelve "Descanso (barbecho)". Ojo con cualquier lógica que asuma que `cropId` está
  en `CROPS` (íconos, colores por cultivo).
- Pasa en climas fríos (invierno en Iowa, Canadá): sin esto se ve "0 puntos" y parece un error.

### 3. Riego estimado por paso · `DiagnosisView` (Layout – Fernando)
- Mostrar `step.irrigationMm` junto al ahorro de agua: "Riego estimado: 248 mm". Si es 0: "La lluvia alcanza".
- Es FAO-56 con el clima del lugar; mostrar "estimado" en la etiqueta.

### 4. Suelo automático · `SelectView` / `QuickPanel` (Mapa – Mia)
- Al terminar de dibujar (`finishDrawing`), pedir el suelo del centroide **en segundo plano**:
  ```ts
  // api/client.ts
  export async function getSoil(lat: number, lon: number): Promise<DetectedSoil | null> {
    if (USE_MOCK) return mockAnalysis.soilDetected ?? null;
    try { return await request<DetectedSoil>(`/api/v1/soil?lat=${lat}&lon=${lon}`); }
    catch { return null; } // 404 = sin dato; también si tarda o falla
  }
  ```
  El centroide se puede sacar con `turf.centroid(geometry)` (ya está turf en el store).
- **Tarda 5–20 s** la primera vez (SoilGrids es lento y está en beta, límite 5 consultas/min). No bloquear: mostrar
  "Detectando suelo…" y dejar que el usuario siga eligiendo cultivo. El backend lo guarda en caché, así que el
  `POST /analyses` posterior sale rápido.
- Mostrar lo detectado como **valor sugerido editable**: "Suelo detectado: arcilloso, pH 7.8 (ISRIC SoilGrids) —
  [cambiar]". Si el usuario lo cambia → `setSoil({ texture, ph })`, que **manda sobre lo detectado**.
- Si no hay dato: no mostrar nada (o "Sin dato de suelo para este punto").

### 5. Mostrar el suelo usado · `DiagnosisView` (Layout – Fernando)
- Tarjeta pequeña con `analysis.soilDetected` (textura, pH, % arcilla/arena) y la fuente. Si es `null`, ocultarla.
- Los riesgos de pH ya vienen en `step.risks` ("pH del suelo (7.8) fuera de su rango óptimo (5.5–7.0)").

## Prioridad media

### 6. Catálogo desde la API · `QuickPanel` (Mapa – Mia)
- Leer `GET /api/v1/crops` (tipo `CropInfo[]`) con React Query en vez de la lista fija de `lib/crops.ts`.
  Así, al agregar cultivos en el backend, el frontend no se queda atrás. Mantener `lib/crops.ts` como respaldo
  para modo mock / offline.
- Agrupar el selector por `family`: Cereales, Leguminosas, Coberturas, Oleaginosas, Industriales, Hortalizas.
- Mostrar `scientificName` en pequeño y `source` en un tooltip ("Fuente: FAO ECOCROP…").

### 7. Riesgos con más peso visual · `DiagnosisView`
- Hoy se muestran como texto corrido. Llegan nuevos: helada ("Riesgo de helada: mínimas de ~1 °C…"),
  cambio de sistema de producción, pH, fuera de temporada. Sugerencia: chips con ícono por tipo.

### 8. Sección "Fuentes de datos" (Layout – Fernando)
- Pie de página o modal: **NASA POWER** (clima), **FAO ECOCROP** y **FAO-56** (cultivos y agua),
  **ISRIC SoilGrids** (suelo, CC BY 4.0). Las reglas y el nitrógeno son **estimaciones**.
- Importante para el jurado y para no decir "IA"/"satélite" (regla de `AGENTS.md`).

### 9. Historial · `HistoryView` (Layout – Fernando, PR #8)
- `GET /api/v1/analyses` y `/analyses/{id}` ya funcionan. Al terminar el PR #8, usar `cropName()` en
  `rotationCrops` (puede traer `fallow`).

### 10. Offline (PWA – menaxmn)
- Guardar en caché el último análisis **y** el último suelo detectado. Si no hay red, mostrar el último análisis
  con la marca "sin conexión".

## Prioridad baja / para alcance internacional
- Inglés y unidades imperiales (ver `ALCANCE-GEOGRAFICO.md`, nivel 1).
- Aviso cuando el punto está fuera de Norteamérica: "Recomendación orientativa fuera de la región calibrada".

## Configuración
- Después del merge: cambiar el default en `docker-compose.yml` a `VITE_USE_MOCK: ${VITE_USE_MOCK:-false}`.

## Checklist de prueba manual
1. Dibujar en el Valle de Mexicali (32.5, −115.3), trigo, "ahorrar agua", **con riego** → aparece suelo
   arcilloso/pH ~7.8, rotación sin "Requiere riego", con `irrigationMm` por paso.
2. Dibujar en Iowa (42.0, −93.6), maíz → el invierno sale como **Descanso (barbecho)**.
3. Dibujar en una ciudad → sin tarjeta de suelo, el análisis funciona igual.
4. Apagar el backend → mensaje de error legible (viene en `detail`).
