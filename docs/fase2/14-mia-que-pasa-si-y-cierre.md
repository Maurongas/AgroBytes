# 14 · Mía: "¿Y si cambia el clima?", merges y demo final

Nov 14, 2026 · Mauro

> **Fase 2.** Empieza cuando termines lo del doc 09. Necesitas el **PR 1 de Mauro** (contrato v2.2, que trae
> `climateShift`). Con datos reales necesitas también su PR 3.

## Por qué

El reto sugiere *"scenario sliders that adjust rainfall or temperature patterns"*. Es lo que más luce en una
demo: mueves un slider y ves qué pasa con la rotación si viene un año seco o más caliente. Tu vista *Comparar*
es el lugar natural para esto. Además, como dueña de `main`, te toca coordinar los merges de esta fase y el
guion final.

## Orden de toda la fase 2 (es el mismo en los 5 documentos)

| # | Quién | Qué | Rama | Espera a |
| --- | --- | --- | --- | --- |
| 1 | Mauro | Contrato v2.2: tipos + datos de ejemplo | `feature/contrato-v22` | nada |
| 2 | menaxmn | Glosario y componente `Termino` | `feature/front-glosario` | nada |
| 3 | Mauro | Motor de estrategias + escenario climático | `feature/back-estrategias` | 1 |
| 4 | Fernando | Estrategias en Resultados | `feature/front-estrategias` | 1 y 2 |
| 5 | Ximena | Vista "Cómo funciona" + suelo descubierto | `feature/front-como-funciona` | 2 |
| 6 | Daniel | Calor, "Antes de decidir" y pre-calentar | `feature/back-calor-confirmar` | 3 |
| 7 | **tú** | **"¿Y si cambia el clima?"** | `feature/front-que-pasa-si` | 1 |
| 8 | Mauro + menaxmn | Publicar | `chore/deploy` | todo |

**Orden de merge sugerido:** 1 → 2 → 3 → 4 → 5 → 7 → 6 → 8. Mergea primero el contrato y el glosario: los
demás dependen de ellos. Ximena va a tocar una palabra de `useStore.ts` (`'method'` en `ViewId`) y `App.tsx`;
ya está avisada de pedirte permiso.

## La idea de diseño

*Comparar* tiene hoy un solo modo (escenario A contra B). Le agregamos un **selector de dos pestañas** arriba,
con la misma pastilla animada que usan las temporadas en *Resultados*:

```
Comparar
[ Decisiones | ¿Y si cambia el clima? ]        ← pastilla animada (layoutId)

  Lluvia      −20 %   ───────●──────          [Año seco] [Más calor] [Seco y caliente]
  Temperatura +1.0 °C ────●─────────
  [ Calcular escenario ]

  ┌ Clima normal ────────┐  →  ┌ Con el escenario ────┐
  │ Inv · Avena          │     │ Inv · Avena          │
  │ Pri · Frijol         │     │ Pri · Garbanzo   ●   │   ← lo que cambia, resaltado
  │ Riego 340 mm         │     │ Riego 410 mm  (+70)  │
  └──────────────────────┘     └──────────────────────┘
  Qué cambia: en primavera el frijol deja su lugar al garbanzo.
```

```bash
cd frontend
git switch main && git pull
git switch -c feature/front-que-pasa-si
```

## Paso 1 · `src/components/EscenarioClima.tsx` (nuevo)

```tsx
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { CloudRain, Thermometer, type LucideIcon } from 'lucide-react';
import { previewAnalysis } from '../api/client';
import type { AnalysisRequest, AnalysisResponse, ClimateShift } from '../api/types';
import { cropName, SEASON_LABEL } from '../lib/crops';

const PRESETS: { texto: string; shift: ClimateShift }[] = [
  { texto: 'Año seco', shift: { rainPct: -30, tempC: 0 } },
  { texto: 'Más calor', shift: { rainPct: 0, tempC: 2 } },
  { texto: 'Seco y caliente', shift: { rainPct: -30, tempC: 2 } },
];

const fmtLluvia = (v: number) => `${v > 0 ? '+' : ''}${v} %`;
const fmtTemp = (v: number) => `${v > 0 ? '+' : ''}${v.toFixed(1)} °C`;
const riego = (a: AnalysisResponse) => a.impact.find((i) => i.label === 'Riego necesario')?.recommended ?? 0;

function Deslizador({ etiqueta, icono: Icono, valor, min, max, paso, formato, onChange }: {
  etiqueta: string; icono: LucideIcon; valor: number; min: number; max: number; paso: number;
  formato: (v: number) => string; onChange: (v: number) => void;
}) {
  return (
    <label className="block">
      <span className="flex items-center justify-between text-sm font-medium text-ink-900">
        <span className="flex items-center gap-2"><Icono size={16} className="text-sky-700" aria-hidden />{etiqueta}</span>
        <span className="font-display text-lg">{formato(valor)}</span>
      </span>
      <input type="range" min={min} max={max} step={paso} value={valor} aria-valuetext={formato(valor)}
        onChange={(e) => onChange(Number(e.target.value))}
        className="mt-1 h-11 w-full cursor-pointer accent-leaf-600" />
      <span className="flex justify-between text-[11px] text-ink-500"><span>{formato(min)}</span><span>{formato(max)}</span></span>
    </label>
  );
}

function Columna({ titulo, a, otra, resaltar }: { titulo: string; a: AnalysisResponse; otra?: AnalysisResponse; resaltar?: boolean }) {
  const dif = otra ? riego(a) - riego(otra) : 0;
  return (
    <section className={`rounded-card border bg-surface-raised p-5 shadow-card ${resaltar ? 'border-sky-500' : 'border-line'}`}>
      <h3 className="font-display text-lg font-semibold">{titulo}</h3>
      <ul className="mt-3 space-y-2">
        {a.rotation.map((p, i) => {
          const cambia = otra && otra.rotation[i]?.cropId !== p.cropId;
          return (
            <li key={p.season} className={`flex items-center justify-between rounded-xl px-3 py-2 text-sm ${cambia ? 'bg-sky-50 ring-1 ring-sky-300' : 'bg-surface-sunken'}`}>
              <span className="text-ink-500">{SEASON_LABEL[p.season]}</span>
              <strong className="text-ink-900">{cropName(p.cropId)}</strong>
            </li>
          );
        })}
      </ul>
      <p className="mt-3 text-sm text-ink-700">
        Riego necesario: <strong className="text-sky-700">{riego(a)} mm</strong>
        {otra && dif !== 0 && <span className={dif > 0 ? 'text-clay-700' : 'text-leaf-700'}> ({dif > 0 ? '+' : '−'}{Math.abs(dif)})</span>}
      </p>
      <p className="text-sm text-ink-700">Salud del suelo (estimada): <strong>{a.soilHealth.recommended} / 100</strong></p>
    </section>
  );
}

/** "¿Y si cambia el clima?": la misma parcela con el clima de siempre y con un escenario hipotético. */
export default function EscenarioClima({ pedido, esEjemplo }: { pedido: AnalysisRequest; esEjemplo: boolean }) {
  const [shift, setShift] = useState<ClimateShift>({ rainPct: -20, tempC: 1 });
  const calcular = useMutation({
    mutationFn: async () => {
      const [normal, escenario] = await Promise.all([
        previewAnalysis(pedido),
        previewAnalysis({ ...pedido, climateShift: shift }),
      ]);
      return { normal, escenario };
    },
  });
  const r = calcular.data;
  const cambios = r
    ? r.normal.rotation
        .map((p, i) => ({ season: p.season, antes: p.cropId, despues: r.escenario.rotation[i]?.cropId }))
        .filter((c) => c.despues && c.antes !== c.despues)
    : [];

  return (
    <div className="mt-6 space-y-6">
      <div className="rounded-card border border-line bg-surface-raised p-5 shadow-card">
        <div className="grid gap-5 md:grid-cols-2">
          <Deslizador etiqueta="Lluvia" icono={CloudRain} valor={shift.rainPct} min={-50} max={30} paso={5}
            formato={fmtLluvia} onChange={(rainPct) => setShift({ ...shift, rainPct })} />
          <Deslizador etiqueta="Temperatura" icono={Thermometer} valor={shift.tempC} min={0} max={4} paso={0.5}
            formato={fmtTemp} onChange={(tempC) => setShift({ ...shift, tempC })} />
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-2">
          {PRESETS.map((p) => {
            const activo = p.shift.rainPct === shift.rainPct && p.shift.tempC === shift.tempC;
            return (
              <button key={p.texto} type="button" aria-pressed={activo} onClick={() => setShift(p.shift)}
                className={`rounded-full border px-3 py-1.5 text-sm transition-colors ${
                  activo ? 'border-leaf-600 bg-leaf-50 font-medium text-leaf-900' : 'border-line text-ink-700 hover:border-leaf-300'}`}>
                {p.texto}
              </button>
            );
          })}
          <button onClick={() => calcular.mutate()} disabled={calcular.isPending}
            className="ml-auto rounded-2xl bg-leaf-600 px-5 py-2.5 font-medium text-paper transition-colors hover:bg-leaf-700 disabled:opacity-60">
            {calcular.isPending ? 'Calculando…' : 'Calcular escenario'}
          </button>
        </div>
        <p className="mt-3 text-xs text-ink-500">
          Cambiamos el clima promedio de cada mes (NASA POWER, últimos 10 años) y volvemos a recomendar. Es un ejercicio "¿qué pasaría si…?", no un pronóstico.
        </p>
      </div>

      {calcular.isError && <p role="alert" className="text-sm text-danger">{calcular.error.message}</p>}

      {r && (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }} className="space-y-4">
          {esEjemplo && (
            <p className="rounded-xl bg-sun-100 p-3 text-sm text-ink-900">Datos de ejemplo: el escenario da lo mismo que el clima normal hasta que el backend esté conectado.</p>
          )}
          <p className="font-display text-xl font-semibold" role="status">
            {cambios.length === 0
              ? 'Tu rotación aguanta este escenario: los cultivos no cambian.'
              : `Con este clima cambian ${cambios.length} de 3 temporadas.`}
          </p>
          <div className="grid gap-4 md:grid-cols-2">
            <Columna titulo="Clima normal" a={r.normal} />
            <Columna titulo={`Lluvia ${fmtLluvia(shift.rainPct)} · ${fmtTemp(shift.tempC)}`} a={r.escenario} otra={r.normal} resaltar />
          </div>
          {cambios.length > 0 && (
            <ul className="space-y-1 text-sm text-ink-700">
              {cambios.map((c) => (
                <li key={c.season}>En {SEASON_LABEL[c.season].toLowerCase()}, <strong>{cropName(c.antes)}</strong> deja su lugar a <strong>{cropName(c.despues!)}</strong>.</li>
              ))}
            </ul>
          )}
        </motion.div>
      )}
    </div>
  );
}
```

## Paso 2 · `src/views/CompareView.tsx`: las dos pestañas

Imports:

```tsx
import { motion } from 'framer-motion';
import EscenarioClima from '../components/EscenarioClima';
```

Dentro de `CompareView`, junto a los otros `useState`:

```tsx
  const [modo, setModo] = useState<'decisiones' | 'clima'>('decisiones');
  const irrigated = useStore((s) => s.irrigated); // lo agregaste en el doc 09
```

Debajo del `<h1>` y del párrafo de introducción, el selector:

```tsx
      <div role="tablist" aria-label="Tipo de comparación" className="mt-5 inline-flex rounded-full border border-line bg-surface-raised p-1">
        {([['decisiones', 'Decisiones'], ['clima', '¿Y si cambia el clima?']] as const).map(([id, texto]) => (
          <button key={id} role="tab" aria-selected={modo === id} onClick={() => setModo(id)}
            className="relative rounded-full px-4 py-2 text-sm font-medium text-ink-700">
            {modo === id && (
              <motion.span layoutId="compare-tab" className="absolute inset-0 rounded-full bg-leaf-100"
                transition={{ type: 'spring', stiffness: 380, damping: 30 }} />
            )}
            <span className="relative">{texto}</span>
          </button>
        ))}
      </div>
```

Y envuelve **todo lo que hoy hay después** (los dos `Selector`, el botón *Comparar* y los resultados) en
`{modo === 'decisiones' && (<> … </>)}`. Luego agrega:

```tsx
      {modo === 'clima' && (
        <EscenarioClima esEjemplo={ES_EJEMPLO} pedido={{
          geometry, currentCrop: crop ?? 'maize', priority: priority ?? 'water', soil: soil ?? undefined, irrigated,
        }} />
      )}
```

Cambia el párrafo de introducción para que sirva a los dos modos: *"Misma parcela, distintas decisiones o
distinto clima. Compara cómo cambia la rotación."*

## Paso 3 · Probar y mandar

Con datos de ejemplo: las pestañas cambian con la pastilla animada; los presets marcan su chip; los sliders se
mueven con el pulgar y con las flechas del teclado (y el lector de pantalla dice "−20 %"); "Calcular" muestra
las dos columnas y el aviso amarillo.

Con el backend real (PR 3 de Mauro mergeado): en **Mexicali** con "Seco y caliente" debe cambiar al menos un
cultivo o subir el riego; en DevTools → *Network* las dos peticiones van a `?guardar=false` y el Historial **no**
crece.

```bash
npm run build
git add src/components/EscenarioClima.tsx src/views/CompareView.tsx
git commit -m "feat: comparar con escenarios de clima (lluvia y temperatura)"
git push -u origin feature/front-que-pasa-si
```

---

## Cierre · Prueba de punta a punta de la fase 2

Con todo mergeado y el backend real (`VITE_USE_MOCK=false`), y mejor aún en la **versión publicada**:

- [ ] **Resultados:** aparecen "Seguir como hoy" y al menos 2 rotaciones más. Cambiar de tarjeta cambia el
      detalle, las barras y el medidor de suelo.
- [ ] **Por qué / Beneficios / A considerar / Evidencia** tienen texto en cada estrategia.
- [ ] **Antes de decidir, confirma** muestra de 1 a 5 puntos; en Mexicali aparece el calor en verano.
- [ ] **ⓘ** en las tarjetas de NASA, en la incertidumbre y en "Tú decides".
- [ ] **Calendario:** filas de suelo cubierto y, si sigues como hoy, el aviso de suelo descubierto.
- [ ] **Cómo funciona** abre desde el menú (en el celular, dentro de "Más").
- [ ] **¿Y si…?** cambia algo en Mexicali con "Seco y caliente".
- [ ] **PDF:** trae estrategias, "Antes de decidir" y "Tú decides".
- [ ] **Celular con la URL pública:** instala, analiza, y en modo avión abre el último análisis.

Si algo se rompe con datos reales pero funciona con los de ejemplo, es casi siempre un campo distinto del
contrato: compara la respuesta de Swagger con `api/types.ts` y abre un issue para Mauro (como en el doc 09).

## Guion de demo actualizado (3 minutos)

Reemplaza el del doc 09. Cada paso cubre algo que pide el reto:

1. **(15 s) El problema.** "Los agricultores eligen qué sembrar con un clima que ya no se comporta como antes."
2. **(20 s) La parcela.** App instalada en el celular → buscar "Mexicali" → dibujar con el rectángulo → maíz,
   "Ahorrar agua", temporal.
3. **(30 s) Datos de NASA.** Las 4 tarjetas: toca la ⓘ de humedad del suelo. "10 años de NASA POWER y los
   últimos 90 días, para esta zona."
4. **(45 s) Tres estrategias contra hoy.** Tarjetas: "Seguir como hoy" deja el suelo descubierto y usa más riego;
   toca "Regenerar el suelo" → beneficios, riesgos, evidencia. "Cada número tiene su fuente."
5. **(15 s) Antes de decidir.** La lista de qué confirmar + "Tú decides": apoyo, no reemplazo.
6. **(30 s) ¿Y si…?** *Comparar* → "Seco y caliente" → qué cultivo cambia y cuánto riego más.
7. **(15 s) Calendario.** Los meses con el suelo descubierto.
8. **(10 s) Sin internet y PDF.** Modo avión → abre el último análisis → exportar PDF.

Plan B: si no hay internet en el lugar, empieza por el paso 8 con un análisis ya guardado y ten el video grabado.
Ensaya dos veces completas con cronómetro.
