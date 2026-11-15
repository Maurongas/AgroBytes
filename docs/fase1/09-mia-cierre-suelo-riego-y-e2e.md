# 09 · Mía: cierre, suelo/riego y prueba end-to-end

Nov 14, 2026 · @Mia

## Orden de trabajo

Como dueña del mapa y de `main`, tienes dos trabajos: terminar lo tuyo y ser la que mergea. Este es el orden recomendado:

1. Mergea **#26** (`previewAnalysis`) primero: menaxmn espera que esté en `main` para no chocar con ella en `client.ts`.
2. Mergea el **PR A de menaxmn** (`X-Device-Id`, `deleteAnalysis`, `getSoil`) en cuanto pase `npm run build`, y avísalo en el grupo: Fernando y Mauro lo esperan.
3. Mergea tus **#27** (vistas lazy) y **#28** (barra del mapa), cada uno con `main` actualizado y `npm run build` en verde.
4. Haz tu rama `feature/front-riego-suelo` (siguiente sección).
5. Mergea los PRs de Fernando, el PR B de menaxmn (PWA), el de Ximena (CI y docs) y los de Mauro y Daniel.
6. Prueba end-to-end con el backend real y después pide a Ximena que tome las capturas del README.

Regla para mergear: abre el PR en GitHub, revisa los archivos cambiados (que solo toque lo del dueño), corre `npm run build` en tu máquina con `git fetch origin pull/N/head:prN && git switch prN`, y recién ahí presiona *Merge*.

## Tu rama: riego y suelo en el panel "Tu parcela"

El backend ya acepta `irrigated` y `soil`, y `GET /api/v1/soil` estima la textura del suelo desde SoilGrids. El panel todavía no los pide. Lo agregamos como una sección plegable "4 · Suelo y riego (opcional)" para no alargar el panel en el celular.

```bash
cd frontend
git switch main && git pull   # con #26, el PR A y #27/#28 ya mergeados
git switch -c feature/front-riego-suelo
```

**Paso 1 · `src/store/useStore.ts`.** Ya existen `soil` y `setSoil`; falta `irrigated`. Avísale al grupo que tocas el store. En `interface State` agrega:

```ts
  irrigated: boolean;
  setIrrigated: (v: boolean) => void;
```

Y en el objeto inicial, junto a `soil: null,` y `setSoil`:

```ts
  irrigated: false,
  setIrrigated: (irrigated) => set({ irrigated }),
```

**Paso 2 · `src/components/QuickPanel.tsx`.** Cambia los imports de arriba por:

```tsx
import { useEffect, useMemo, useState, type ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import * as turf from '@turf/turf';
import { motion } from 'framer-motion';
import { Droplets, Sprout, TrendingUp, ArrowRight, Check } from 'lucide-react';
import { useStore } from '../store/useStore';
import { getSoil } from '../api/client';
import { CROPS } from '../lib/crops';
import type { Priority, SoilTexture } from '../api/types';
```

Si en `useStore.ts` importas turf de otra forma (`import * as turf from '@turf/turf'` es lo esperado), copia esa misma línea. Debajo de `PRIORITIES` agrega estas piezas:

```tsx
const TEXTURAS: { id: SoilTexture; nombre: string }[] = [
  { id: 'sandy', nombre: 'Arenoso' },
  { id: 'loam', nombre: 'Franco' },
  { id: 'clay', nombre: 'Arcilloso' },
];
const NOMBRE_TEXTURA: Record<SoilTexture, string> = { sandy: 'Arenoso', loam: 'Franco', clay: 'Arcilloso' };

/** Devuelve `valor` pero solo después de que deja de cambiar `ms` milisegundos (evita pedir suelo en cada arrastre). */
function useRetardo<T>(valor: T, ms: number): T {
  const [v, setV] = useState(valor);
  useEffect(() => {
    const t = setTimeout(() => setV(valor), ms);
    return () => clearTimeout(t);
  }, [valor, ms]);
  return v;
}

function Chip({ activo, onClick, children }: { activo: boolean; onClick: () => void; children: ReactNode }) {
  return (
    <button type="button" aria-pressed={activo} onClick={onClick}
      className={`rounded-full border px-4 py-2 text-sm transition-colors ${
        activo ? 'border-leaf-600 bg-leaf-50 font-medium text-leaf-900' : 'border-line bg-surface-raised text-ink-700 hover:border-leaf-300'}`}>
      {children}
    </button>
  );
}
```

Dentro de `QuickPanel`, cambia la línea del `useStore()` y agrega la consulta del suelo justo debajo:

```tsx
  const { geometry, areaHa, crop, priority, soil, irrigated, setCrop, setPriority, setSoil, setIrrigated } = useStore();

  // Suelo estimado en el centro de la parcela (GeoJSON es [lon, lat]). El retardo evita una consulta por cada arrastre de punto.
  const centro = useMemo(() => (geometry ? turf.centroid(geometry).geometry.coordinates : null), [geometry]);
  const centroQuieto = useRetardo(centro, 800);
  const detectado = useQuery({
    queryKey: ['soil', centroQuieto?.[1].toFixed(3), centroQuieto?.[0].toFixed(3)],
    queryFn: () => getSoil(centroQuieto![1], centroQuieto![0]),
    enabled: centroQuieto !== null,
    staleTime: Infinity,
    retry: false,
  });
```

Y la sección nueva, entre la de "3 · Tu prioridad" y el bloque `{error && ...}`:

```tsx
      <details className="mt-5 rounded-2xl border border-line p-3">
        <summary className="cursor-pointer text-xs font-semibold uppercase tracking-widest text-ink-500">
          4 · Suelo y riego (opcional)
        </summary>
        <div className="mt-3 space-y-4">
          <div>
            <p className="text-sm font-medium">Tipo de suelo</p>
            <p className="mt-1 text-xs text-ink-500" role="status">
              {!geometry
                ? 'Dibuja tu parcela para estimarlo.'
                : detectado.isFetching
                  ? 'Estimando con ISRIC SoilGrids…'
                  : detectado.data
                    ? `Estimado: ${NOMBRE_TEXTURA[detectado.data.texture]} (arcilla ${Math.round(detectado.data.clayPct)} %, arena ${Math.round(detectado.data.sandPct)} %)`
                    : 'No hay dato para este punto; elige el tipo tú.'}
            </p>
            <div className="mt-2 flex flex-wrap gap-2">
              <Chip activo={soil === null} onClick={() => setSoil(null)}>Automático</Chip>
              {TEXTURAS.map((t) => (
                <Chip key={t.id} activo={soil?.texture === t.id} onClick={() => setSoil({ texture: t.id })}>{t.nombre}</Chip>
              ))}
            </div>
          </div>
          <div>
            <p className="text-sm font-medium">¿Tiene riego?</p>
            <div className="mt-2 flex flex-wrap gap-2">
              <Chip activo={!irrigated} onClick={() => setIrrigated(false)}>Temporal (solo lluvia)</Chip>
              <Chip activo={irrigated} onClick={() => setIrrigated(true)}>Con riego</Chip>
            </div>
          </div>
        </div>
      </details>
```

"Automático" deja `soil` en `null`: el backend consulta SoilGrids por su cuenta, y como la consulta de arriba ya la calentó, el análisis llega más rápido.

**Paso 3 · Manda `irrigated` al backend.** En `src/views/SelectView.tsx`, dentro de `onAnalyze`:

```tsx
    const { geometry, crop, priority, soil, irrigated } = useStore.getState();
    if (!geometry || !crop || !priority) return;
    mutation.mutate({ geometry, currentCrop: crop, priority, soil: soil ?? undefined, irrigated });
```

Y en `src/views/CompareView.tsx`, en la función `pedir` (la que llama al cliente con `soil: soil ?? undefined`), agrega `irrigated` igual: toma el valor con `useStore.getState().irrigated` y pásalo en el objeto. Así la comparación usa las mismas condiciones que el análisis.

## Prueba end-to-end con el backend real

Hasta hoy casi todo se probó con datos de ejemplo (`VITE_USE_MOCK=true`). Esta es la prueba que el jurado hará sin saberlo. Corre `npm run build` antes y luego, en la raíz del repo:

```bash
cp .env.example .env     # una sola vez; no se sube a git
# edita .env: VITE_USE_MOCK=false
docker compose up --build
```

Espera a ver `Application startup complete` en el log del backend. Abre http://localhost:8000/docs (debe cargar Swagger) y luego http://localhost:3000. Si cambiaste `.env` con todo levantado: `docker compose up -d --force-recreate frontend`.

Recorre este guion y anota qué falla:

- [ ] **Dibujar en Ensenada** (31.86, -116.60): la barra del mapa funciona y el panel muestra el área.
- [ ] **Suelo**: al abrir "4 · Suelo y riego" dice "Estimando…" y en 3–8 s "Estimado: Franco…" (o "No hay dato", que también es válido).
- [ ] **Analizar**: aparece el escaneo y después el Diagnóstico, con las cuatro tarjetas de NASA, la rotación y el aviso de incertidumbre. La primera vez puede tardar unos 10 s.
- [ ] **Riego**: marca "Con riego", analiza otra vez y compara el chip del encabezado y los mm de riego con el análisis anterior.
- [ ] **Historial**: ambos análisis aparecen. Abre uno y carga completo.
- [ ] **Comparar**: corre una comparación. El Historial **no** debe crecer (es la vista previa con `?guardar=false`). En DevTools → *Network* la respuesta trae un `id` que empieza con `preview-`.
- [ ] **Cabecera**: en *Network*, cualquier petición a `/api/v1/...` lleva `X-Device-Id` (requiere el PR A).
- [ ] **Error**: apaga el backend (`docker compose stop backend`) y analiza: debe salir "No se pudo conectar con el servidor." en el panel, sin pantalla en blanco.
- [ ] **Sin internet de NASA** (solo con Mauro, ver su documento): el mensaje es entendible.

Si la pantalla se rompe con datos reales pero funciona con los de ejemplo, casi siempre es un campo que el backend manda distinto de lo que dice `api/types.ts`. Abre el análisis en Swagger, compara con el tipo y abre un issue para Mauro con la respuesta pegada. No "arregles" el tipo a ojo: el contrato es de los dos (`docs/ARQUITECTURA.md` sección 5).

## Pendientes del mapa y cierre

**Mapa** (rama `feature/front-mapa-busqueda`, solo tus archivos de mapa). Tres cosas chicas que faltan:

1. **Atribución completa de Esri.** En `ParcelMap.tsx`, en el `<TileLayer` de satélite, la propiedad `attribution` debe decir: `Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community`. Es un requisito de la licencia de las imágenes.
2. **Buscar un lugar** y 3. **"Mi ubicación"**: crea `src/components/map/BuscarLugar.tsx`. Usa Nominatim (OpenStreetMap), que es gratis y no pide llave; su política pide **no más de una búsqueda por segundo y solo cuando el usuario la manda** (por eso es un formulario con botón, no autocompletado).

```tsx
import { useEffect, useRef, useState, type FormEvent } from 'react';
import L from 'leaflet';
import { useMap } from 'react-leaflet';
import { LocateFixed, Search } from 'lucide-react';

interface Resultado { place_id: number; display_name: string; lat: string; lon: string }

export default function BuscarLugar() {
  const map = useMap();
  const caja = useRef<HTMLDivElement>(null);
  const [texto, setTexto] = useState('');
  const [resultados, setResultados] = useState<Resultado[]>([]);
  const [aviso, setAviso] = useState<string | null>(null);
  const [cargando, setCargando] = useState(false);

  // Sin esto, tocar el cuadro también "toca el mapa" y se agregaría un punto de la parcela
  useEffect(() => {
    if (!caja.current) return;
    L.DomEvent.disableClickPropagation(caja.current);
    L.DomEvent.disableScrollPropagation(caja.current);
  }, []);

  function ir(lat: number, lon: number) {
    map.flyTo([lat, lon], 16, { duration: 1.2 });
    setResultados([]);
    setAviso(null);
  }

  async function buscar(e: FormEvent) {
    e.preventDefault();
    const q = texto.trim();
    if (q.length < 3) return;
    setCargando(true);
    setAviso(null);
    try {
      const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&limit=5&accept-language=es&q=${encodeURIComponent(q)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error();
      const datos = (await res.json()) as Resultado[];
      setResultados(datos);
      if (datos.length === 0) setAviso('No encontramos ese lugar. Prueba con otro nombre.');
    } catch {
      setAviso('No se pudo buscar ahora. Revisa tu conexión.');
    } finally {
      setCargando(false);
    }
  }

  function miUbicacion() {
    if (!('geolocation' in navigator)) {
      setAviso('Tu navegador no permite obtener la ubicación.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (p) => ir(p.coords.latitude, p.coords.longitude),
      () => setAviso('No pudimos obtener tu ubicación. Revisa el permiso del navegador.'),
      { enableHighAccuracy: true, timeout: 10000 },
    );
  }

  return (
    <div ref={caja} className="absolute left-14 right-3 top-3 z-[1000] max-w-sm">
      <form onSubmit={buscar} className="flex gap-2">
        <input value={texto} onChange={(e) => setTexto(e.target.value)} aria-label="Buscar lugar o dirección"
          placeholder="Buscar lugar o dirección"
          className="min-w-0 flex-1 rounded-full border border-line bg-surface-raised px-4 py-2 text-sm text-ink-900 shadow-card" />
        <button type="submit" disabled={cargando} aria-label="Buscar"
          className="rounded-full bg-leaf-600 p-2.5 text-paper hover:bg-leaf-700 disabled:opacity-50">
          <Search size={18} aria-hidden />
        </button>
        <button type="button" onClick={miUbicacion} aria-label="Mi ubicación"
          className="rounded-full border border-line bg-surface-raised p-2.5 text-ink-700 shadow-card">
          <LocateFixed size={18} aria-hidden />
        </button>
      </form>
      {aviso && <p className="mt-2 rounded-xl bg-surface-raised px-3 py-2 text-xs text-ink-700 shadow-card" role="status">{aviso}</p>}
      {resultados.length > 0 && (
        <ul className="mt-2 overflow-hidden rounded-2xl border border-line bg-surface-raised shadow-lift">
          {resultados.map((r) => (
            <li key={r.place_id}>
              <button type="button" onClick={() => ir(Number(r.lat), Number(r.lon))}
                className="block w-full px-4 py-2.5 text-left text-sm text-ink-900 hover:bg-leaf-50">
                {r.display_name}
              </button>
            </li>
          ))}
          <li className="px-4 py-1.5 text-[11px] text-ink-500">Búsqueda: Nominatim, © colaboradores de OpenStreetMap</li>
        </ul>
      )}
    </div>
  );
}
```

En `ParcelMap.tsx` importa el componente y colócalo dentro del `<MapContainer>`, junto a tus otros hijos: `<BuscarLugar />`. Si choca con la barra de herramientas del doc 04 en el celular, mueve la búsqueda a `top-16`. "Mi ubicación" solo funciona en `localhost` o HTTPS.

**Repositorio.** Cuando los CI de Mauro y Ximena estén mergeados: GitHub → Settings → Branches → *Add branch ruleset* para `main`, marca *Require a pull request* y *Require status checks to pass* con `build` y `pytest`. En Settings → General activa *Automatically delete head branches*. Daniel limpia las ramas y PRs viejos; tú no tienes que hacerlo.

**Guion de demo (3 minutos).** Enséñalo completo dos veces antes de presentar:

1. Abre la app instalada en el celular (la PWA) y di el problema en una frase.
2. Busca "Ensenada" y dibuja una parcela con el rectángulo.
3. Elige cultivo y prioridad y analiza: muestra las tarjetas de NASA y la rotación.
4. Muestra el riego estimado y el suelo detectado.
5. Compara dos escenarios.
6. Activa modo avión: la app abre y muestra el último análisis.
7. Exporta el PDF y cierra con las limitaciones (estimaciones por reglas, no predicción).

Plan B: si falla internet, el paso 6 pasa a ser el principal; ten también el video grabado.
