# AgroBytes — presentación web (pitch de 4 min)

Presentación tipo PowerPoint, en inglés, para Mia y Mauro. Usa los **componentes reales** de la app y, si el backend
está corriendo, **datos reales de la API** (si no, el mock de `frontend/src/api/mock.ts`). Speech para practicar:
[`SPEECH.md`](SPEECH.md).

## En vivo con la API

Al abrir, la presentación muestra una pantalla de arranque con las peticiones reales (`GET /health` y
`POST /api/v1/analyses?guardar=false` con la parcela del valle de Mexicali). Después usa esa respuesta en todas las
diapositivas ([`src/live.ts`](src/live.ts)). Durante la diapositiva 4:

- Insignia roja **LIVE · NASA POWER API** + enlace **API docs ↗** (Swagger del backend).
- La barra de la ventana muestra la última petición real: método, ruta, estado, ms y kB.
- **NASA data** vuelve a pedir el análisis al entrar; el escaneo muestra el registro real.
- **What if?** manda `climateShift` al backend cada vez que se sueltan los sliders (450 ms) y pinta la rotación y el
  riego que devuelve.

Requisitos: backend en `http://localhost:8000` (o `VITE_PITCH_API`) con `http://localhost:3001` en `CORS_ORIGINS`
(ya viene por defecto en `docker-compose.yml`). Si el backend no responde en 25 s, todo sigue con el mock y dice
«offline · sample data». **Abre la presentación una vez antes de presentar:** la primera consulta a NASA POWER tarda
~10 s; después queda en caché.

## Cómo abrirla

**Con Docker (no hace falta Node):**

```bash
docker compose -f docs/presentacion/compose.yml up --build     # → http://localhost:3001
```

Reutiliza la imagen del frontend y monta `frontend/` y esta carpeta; los cambios se recargan solos.

**Con Node 20+ instalado** (desde `frontend/`, con `npm install` hecho):

```bash
npx vite --config ../docs/presentacion/vite.config.mjs --configLoader native          # dev → :3001
npx vite build --config ../docs/presentacion/vite.config.mjs --configLoader native    # → docs/presentacion/dist/
npx tsc -p ../docs/presentacion/tsconfig.json                                          # revisar tipos
```

`dist/` es estático: se puede abrir con `npx vite preview --config ...` o subir a cualquier hosting.

## Estructura (6 diapositivas, ~4 min)

1. **Portada** — iconos flotando, satélite en órbita, título y equipo → clic: se dibuja la parcela + «Every season is a bet.»
2. **The challenge** — problemas → 40+ años de datos NASA → «Gap» + nuestra idea.
3. **How we built it** — diagrama: parcela + NASA POWER + SoilGrids + catálogo de cultivos → motor de reglas → estrategias.
4. **Live, on real NASA data** — la app en una ventana con pestañas (Draw · NASA data · Options · What if? · In the field).
   Cada clic avanza una parte (`prototypeSteps` en `content.ts`); las pestañas también se pueden pulsar a mano.
   Los paneles están en `src/panes/`.
5. **Impact & validation** — gauges + barras de impacto → «How we keep it honest».
6. **Cierre** — la parcela se aleja hasta Norteamérica y vuelve la portada: equipo y, discretos, los logos de UABC y FIAD
   (`public/uabc.png`, `public/fiad.png`; los nombres están en `team` de `content.ts`).

## Atajos

| Tecla | Acción |
|---|---|
| → · Espacio · PageDown · Enter · clic mitad derecha · swipe ← | Siguiente paso / diapositiva |
| ← · PageUp · Backspace · clic mitad izquierda · swipe → | Atrás (deshace los pasos en orden inverso) |
| Home / End | Primera / última |
| número + Enter (p. ej. `6` Enter) | Saltar a la diapositiva |
| **S** | Ventana de notas del orador (guion, quién habla, cronómetros, siguiente diapositiva) |
| **F** | Pantalla completa |
| **T** | Modo claro / oscuro (claro por defecto) |

- **`?still`** (p. ej. `http://localhost:3001/?still#/4/3`): cada diapositiva en su estado final, sin animaciones. Sirve para
  capturas o para imprimir un respaldo en PDF.
- La URL guarda la posición (`#/4` o `#/4/2` = diapositiva 4, paso 2): recargar no la pierde.
- Las notas se sincronizan con `BroadcastChannel` (misma computadora y navegador). Desde las notas también se puede
  avanzar (flechas o botones) y **R** reinicia el cronómetro, que arranca con el primer avance.
- En el guion, `→` marca dónde hacer clic para el siguiente paso.
- En «What if?» los sliders se pueden mover a mano; el paso automático los lleva a −20 % lluvia / +1.5 °C.
- En «Options» las tarjetas se voltean con hover o clic; el último paso voltea la recomendada.
- Con `prefers-reduced-motion` los movimientos se cambian por fundidos y los bucles se detienen.

## Editar textos

**Todo el texto está en [`src/content.ts`](src/content.ts):** títulos, guion por presentador, duración objetivo,
cuántos pasos (`builds`) tiene cada diapositiva, notas de cada paso y etiquetas de la interfaz.

- `{{clave}}` en el guion se sustituye por un número del mock (`facts` en [`src/data.ts`](src/data.ts)):
  `{{soilNow}}`, `{{soilNew}}`, `{{waterPct}}`, `{{nitroGain}}`, `{{area}}`, `{{soil}}`…
- Los números de pantalla también salen del mock (`src/data.ts`), nunca escritos a mano.
- El mock está en español: [`src/i18n.ts`](src/i18n.ts) traduce cultivos, temporadas, métricas y las frases del mock.
  Si falta una traducción se muestra el texto original; añade la frase en `PHRASES` o un patrón en `PATTERNS`.
- **Pendiente:** `ui.demoUrl` y `ui.qrImage` (imagen del QR en `docs/presentacion/public/`). Mientras estén vacíos la
  última diapositiva no muestra el bloque del QR.

## Qué reutiliza de la app (revisar si el frontend cambia)

| De `frontend/src/` | Dónde | Cómo |
|---|---|---|
| `index.css` (tokens, fuentes, modo oscuro, animación `scan`) | todo | importado en `src/pitch.css` |
| `api/mock.ts`, `api/types.ts` | todo | datos y tipos |
| `components/NasaMetricCard.tsx` | 4 · Prototipo (pestaña NASA data) | tal cual (etiquetas traducidas; en S05Nasa, CSS por fuera: texto más grande y `vector-effect` del sparkline) |
| `components/GaugeSoilHealth.tsx` | 5 · Impact | tal cual |
| `components/CountUp.tsx` | 2, 4 | tal cual |
| `components/map/EditableParcel.tsx` + `store/useStore.ts` | 4 · Prototipo (pestaña Draw) | la parcela terminada se pinta con el componente real |
| `lib/region.ts` (`REGION_LATLNGS`) | 6 · Close | contorno de México, EE. UU. y Canadá |
| Teselas Esri de `ParcelMap.tsx` | 4, 6 | misma URL |

Copias con texto en inglés (tienen texto fijo en español en la app; si cambias el original, revisa la copia):
`components/PitchScan.tsx` ← `ScanOverlay`, `components/PitchImpactBar.tsx` ← `ImpactBar`, `components/ClimateChart.tsx` ← gráfica
de `DiagnosisView`, y el panel de la diapositiva 4 ← `QuickPanel`.

## Notas

- «What if?» se simula en el cliente (`src/components/scenario.ts`, presets normal/seco/caluroso interpolados) y lo dice en
  pantalla. `TODO`: usar `previewAnalysis` con `climateShift` cuando se presente con backend.
- La imagen del mapa usa campos de cultivo del valle de Mexicali (`SPOT` en `src/components/FieldMap.tsx`) porque las
  coordenadas del mock caen en la zona urbana de Ensenada; los datos mostrados siguen siendo los del mock.
- Lienzo fijo de 1600×900 escalado a la ventana (`src/Stage.tsx`): se ve igual en 1920×1080 y en 1366×768.
- Cómo funciona `vite.config.mjs`: esta carpeta no tiene `node_modules`; los paquetes se resuelven desde `frontend/`
  (una sola copia de React) y `@app/…` apunta a `frontend/src/…`.
