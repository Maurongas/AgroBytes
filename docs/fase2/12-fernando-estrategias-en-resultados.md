# 12 · Fernando: estrategias en Resultados

Nov 14, 2026 · Mauro

> **Fase 2.** Empieza cuando termines lo del doc 07. Necesitas el **PR 1 de Mauro** (contrato v2.2: trae los
> datos de ejemplo) y el **PR 2 de menaxmn** (componente `Termino`). Mientras tanto puedes leer esto y bocetar.

## Por qué esto es lo más importante de la fase 2

El reto pide **comparar al menos tres estrategias de rotación, incluida la actual**, y explicar en cada una
**por qué** se sugiere, **qué evidencia** la respalda, sus **beneficios** y sus **riesgos**. Ahora el backend
manda eso en `analysis.strategies`. Tu trabajo es mostrarlo en *Resultados* sin romper lo bonito que ya está.

## Orden de toda la fase 2 (es el mismo en los 5 documentos)

| # | Quién | Qué | Rama | Espera a |
| --- | --- | --- | --- | --- |
| 1 | Mauro | Contrato v2.2: tipos + datos de ejemplo | `feature/contrato-v22` | nada |
| 2 | menaxmn | Glosario y componente `Termino` | `feature/front-glosario` | nada |
| 3 | Mauro | Motor de estrategias + escenario climático | `feature/back-estrategias` | 1 |
| 4 | **tú** | **Estrategias en Resultados** | `feature/front-estrategias` | 1 y 2 |
| 5 | Ximena | Vista "Cómo funciona" + suelo descubierto | `feature/front-como-funciona` | 2 |
| 6 | Daniel | Calor, "Antes de decidir" y pre-calentar | `feature/back-calor-confirmar` | 3 |
| 7 | Mía | "¿Y si cambia el clima?" | `feature/front-que-pasa-si` | 1 |
| 8 | Mauro + menaxmn | Publicar | `chore/deploy` | todo |

## La idea de diseño

Hoy *Resultados* es: datos de NASA → incertidumbre → rotación + impacto → clima. **No agregamos una página
nueva**: agregamos una franja "Compara estrategias" justo debajo de la incertidumbre, y la página entera pasa a
mostrar **la estrategia elegida**:

```
┌ Datos de la NASA (igual que hoy, con ⓘ en cada tarjeta) ───────────────┐
└────────────────────────────────────────────────────────────────────────┘
  Incertidumbre alta ⓘ …
  Compara estrategias
  ┌ Seguir como hoy ┐ ┌ Ahorrar agua  ✓ ┐ ┌ Regenerar suelo ┐ ┌ Más rendim. ┐   ← en el celular se
  │ Hoy             │ │ Para tu priorid.│ │                 │ │             │     desliza de lado
  │ Oto · Maíz      │ │ Oto · Frijol    │ │ …               │ │ …           │
  │ Inv · Descanso  │ │ Inv · Avena     │ │                 │ │             │
  │ 520mm 52 38kg   │ │ 340 −180 74 +22 │ │                 │ │             │
  └─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────┘
  ┌ Por qué · Beneficios · A considerar · Evidencia (de la elegida) ─────────┐
  Detalle: Ahorrar agua  [pastillas de temporada como hoy]   │ Impacto vs. hoy
                                                             │ Suelo de la parcela
                                                             │ Antes de decidir, confirma
  Clima de la parcela (igual)
  Tú decides: … (aviso de apoyo, no reemplazo)
```

Reglas: la tarjeta "Seguir como hoy" lleva **borde punteado** (es la referencia). La recomendada lleva una chip
verde. Los números muestran la **diferencia contra hoy** en verde o rojo. Si un análisis viejo no trae
`strategies`, la página se ve exactamente como hoy.

```bash
cd frontend
git switch main && git pull
git switch -c feature/front-estrategias
```

## Paso 1 · `src/lib/estrategias.ts` (nuevo)

```ts
import type { ImpactItem, Strategy } from '../api/types';

/** La estrategia que se muestra al abrir: la recomendada; si no hay, la primera que no sea "seguir como hoy". */
export function estrategiaInicial(lista: Strategy[]): string | null {
  return (lista.find((s) => s.isRecommended) ?? lista.find((s) => !s.isCurrent) ?? lista[0])?.id ?? null;
}

/** Las barras de impacto de una estrategia contra "seguir como hoy" (mismas etiquetas que el backend). */
export function impactoContra(base: Strategy, s: Strategy): ImpactItem[] {
  return [
    { label: 'Agua total del cultivo', unit: 'mm', current: base.waterMm, recommended: s.waterMm, betterWhen: 'lower' },
    { label: 'Riego necesario', unit: 'mm', current: base.irrigationMm, recommended: s.irrigationMm, betterWhen: 'lower' },
    { label: 'Balance de nitrógeno (estimado)', unit: 'kg/ha', current: base.nitrogenKgHa, recommended: s.nitrogenKgHa, betterWhen: 'higher' },
  ];
}
```

## Paso 2 · `src/components/Estrategias.tsx` (nuevo)

```tsx
import { motion } from 'framer-motion';
import { AlertTriangle, Check, FileText, Lightbulb } from 'lucide-react';
import type { Strategy } from '../api/types';
import { cropName, SEASON_BG, SEASON_LABEL } from '../lib/crops';

const COLUMNAS: Record<number, string> = { 2: 'lg:grid-cols-2', 3: 'lg:grid-cols-3', 4: 'lg:grid-cols-4' };

function Delta({ valor, base, mejorSi }: { valor: number; base: number; mejorSi: 'higher' | 'lower' }) {
  const d = Math.round(valor - base);
  if (d === 0) return <span className="text-ink-400">igual</span>;
  const bueno = mejorSi === 'higher' ? d > 0 : d < 0;
  return <span className={bueno ? 'text-leaf-700' : 'text-clay-700'}>{d > 0 ? '+' : '−'}{Math.abs(d)}</span>;
}

function Dato({ titulo, valor, unidad, clase, delta }: {
  titulo: string; valor: number; unidad: string; clase: string; delta?: React.ReactNode;
}) {
  return (
    <div>
      <dt className="text-[11px] text-ink-500">{titulo}</dt>
      <dd className={`font-display text-lg font-semibold leading-tight ${clase}`}>
        {valor}<span className="ml-0.5 font-sans text-[11px] font-normal text-ink-500">{unidad}</span>
      </dd>
      {delta && <dd className="text-[11px] font-medium">{delta}</dd>}
    </div>
  );
}

function Tarjeta({ s, base, activa, onElegir }: { s: Strategy; base?: Strategy; activa: boolean; onElegir: () => void }) {
  const comparar = base && !s.isCurrent;
  return (
    <button type="button" onClick={onElegir} aria-pressed={activa}
      className={`flex min-w-[250px] snap-start flex-col rounded-card border bg-surface-raised p-4 text-left shadow-card transition-all focus-visible:outline-2 focus-visible:outline-leaf-600 lg:min-w-0 ${
        s.isCurrent ? 'border-dashed' : ''} ${
        activa ? 'border-leaf-600 ring-2 ring-leaf-600/25' : 'border-line hover:-translate-y-0.5 hover:border-leaf-300'}`}>
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-display text-lg font-semibold leading-tight">{s.title}</h3>
        {s.isCurrent ? (
          <span className="shrink-0 rounded-full bg-surface-sunken px-2.5 py-0.5 text-[11px] font-medium text-ink-700">Hoy</span>
        ) : s.isRecommended ? (
          <span className="shrink-0 rounded-full bg-leaf-600 px-2.5 py-0.5 text-[11px] font-medium text-paper">Para tu prioridad</span>
        ) : null}
      </div>
      <ol className="mt-3 space-y-1.5" aria-label="Cultivos por temporada">
        {s.steps.map((p) => (
          <li key={p.season} className={`flex items-center justify-between gap-2 rounded-lg px-2.5 py-1 text-xs ${SEASON_BG[p.season]}`}>
            <span className="text-ink-500">{SEASON_LABEL[p.season]}</span>
            <span className="truncate font-medium text-ink-900">{cropName(p.cropId)}</span>
          </li>
        ))}
      </ol>
      <dl className="mt-auto grid grid-cols-3 gap-2 border-t border-line-soft pt-3">
        <Dato titulo="Riego" valor={s.irrigationMm} unidad="mm" clase="text-sky-700"
          delta={comparar && <Delta valor={s.irrigationMm} base={base.irrigationMm} mejorSi="lower" />} />
        <Dato titulo="Suelo" valor={s.soilHealth} unidad="/100" clase="text-leaf-700"
          delta={comparar && <Delta valor={s.soilHealth} base={base.soilHealth} mejorSi="higher" />} />
        <Dato titulo="Nitrógeno" valor={s.nitrogenKgHa} unidad="kg" clase="text-nitro"
          delta={comparar && <Delta valor={s.nitrogenKgHa} base={base.nitrogenKgHa} mejorSi="higher" />} />
      </dl>
    </button>
  );
}

function Lista({ titulo, icono: Icono, clase, items }: {
  titulo: string; icono: typeof Check; clase: string; items: string[];
}) {
  if (items.length === 0) return null;
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-widest text-ink-500">{titulo}</p>
      <ul className="mt-2 space-y-1.5 text-sm text-ink-700">
        {items.map((t) => (
          <li key={t} className="flex gap-2"><Icono size={16} className={`mt-0.5 shrink-0 ${clase}`} aria-hidden />{t}</li>
        ))}
      </ul>
    </div>
  );
}

/** Tarjetas para elegir estrategia + el porqué de la elegida. */
export default function Estrategias({ lista, elegida, onElegir }: {
  lista: Strategy[]; elegida: Strategy; onElegir: (id: string) => void;
}) {
  const base = lista.find((s) => s.isCurrent);
  return (
    <section className="px-6 pt-6" aria-labelledby="titulo-estrategias">
      <h2 id="titulo-estrategias" className="font-display text-2xl font-semibold">Compara estrategias</h2>
      <p className="mt-1 text-sm text-ink-500">
        Seguir como hoy contra {lista.length - 1} rotaciones posibles para las próximas tres temporadas. Toca una para ver su detalle.
      </p>
      <div className={`-mx-6 mt-4 flex snap-x snap-mandatory gap-3 overflow-x-auto px-6 pb-2 lg:mx-0 lg:grid lg:overflow-visible lg:px-0 ${COLUMNAS[lista.length] ?? 'lg:grid-cols-4'}`}>
        {lista.map((s) => (
          <Tarjeta key={s.id} s={s} base={base} activa={s.id === elegida.id} onElegir={() => onElegir(s.id)} />
        ))}
      </div>
      <motion.div key={elegida.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }}
        className="mt-4 rounded-card border border-line bg-surface-raised p-5 shadow-card">
        <p className="flex items-start gap-2 text-sm text-ink-900">
          <Lightbulb size={18} className="mt-0.5 shrink-0 text-sun-700" aria-hidden />
          <span><strong>Por qué:</strong> {elegida.why}</span>
        </p>
        <div className="mt-4 grid gap-5 md:grid-cols-3">
          <Lista titulo="Beneficios" icono={Check} clase="text-leaf-700" items={elegida.benefits} />
          <Lista titulo="A considerar" icono={AlertTriangle} clase="text-clay-700" items={elegida.tradeoffs} />
          <Lista titulo="Evidencia" icono={FileText} clase="text-sky-700" items={elegida.evidence} />
        </div>
      </motion.div>
    </section>
  );
}
```

> Si TypeScript se queja de `React.ReactNode`, agrega `import type { ReactNode } from 'react';` y usa `ReactNode`.

## Paso 3 · `src/components/ImpactBar.tsx`: etiqueta configurable

Cuando eliges "Regenerar el suelo", la barra no debe decir "Recomendado". Cambia la firma y la etiqueta:

```tsx
export default function ImpactBar({ item, etiqueta = 'Recomendado' }: { item: ImpactItem; etiqueta?: string }) {
```

```tsx
          <span className="w-20 shrink-0 truncate">{etiqueta}</span>{bar(item.recommended, 'bg-leaf-600', 0.15)}
```

## Paso 4 · `src/views/DiagnosisView.tsx`

**(a) Imports nuevos:**

```tsx
import { ArrowLeft, ChevronDown, ClipboardCheck, Download, Users } from 'lucide-react';
import Estrategias from '../components/Estrategias';
import Termino from '../components/Termino';
import { estrategiaInicial, impactoContra } from '../lib/estrategias';
```

**(b) Estado y datos derivados.** Debajo de `const [open, setOpen] = useState(true);`:

```tsx
  const [elegidaId, setElegidaId] = useState<string | null>(null);
```

Y reemplaza `const step = analysis.rotation[active];` por:

```tsx
  const estrategias = analysis.strategies ?? [];
  const base = estrategias.find((s) => s.isCurrent);
  const idValido = elegidaId && estrategias.some((s) => s.id === elegidaId) ? elegidaId : estrategiaInicial(estrategias);
  const elegida = estrategias.find((s) => s.id === idValido);
  const pasos = elegida?.steps ?? analysis.rotation;
  const step = pasos[Math.min(active, pasos.length - 1)];
  const impacto = elegida && base ? impactoContra(base, elegida) : analysis.impact;
  const suelo = elegida && base ? { current: base.soilHealth, recommended: elegida.soilHealth } : analysis.soilHealth;
  const etiqueta = elegida && !elegida.isRecommended ? 'Esta opción' : 'Recomendado';
  const elegir = (id: string) => { setElegidaId(id); setActive(0); setOpen(true); };
```

(`idValido` evita un `useEffect`: si abres otro análisis desde el Historial, se vuelve a elegir la recomendada.)

**(c) Glosario en la incertidumbre.** Cambia el `<strong>` de la nota de incertidumbre por:

```tsx
        <strong><Termino id="incertidumbre">Incertidumbre {INCERTIDUMBRE[analysis.uncertainty.level].texto}.</Termino></strong> {analysis.uncertainty.reason}.
```

**(d) Las tarjetas.** Justo después de esa nota (`</p>`), antes de `<div className="grid gap-6 p-6 lg:grid-cols-5">`:

```tsx
      {elegida && <Estrategias lista={estrategias} elegida={elegida} onElegir={elegir} />}
```

**(e) La rotación usa la estrategia elegida.** En la sección de la izquierda:

- el título: `{elegida ? `Detalle: ${elegida.title}` : 'Rotación recomendada'}`;
- las pastillas: cambia `analysis.rotation.map(` por `pasos.map(`;
- en `<motion.article key={step.season}`, usa `key={`${idValido}-${step.season}`}` para que se anime al cambiar.

Junto al título `<h2>` de esa sección agrega `<Termino id="puntaje" />` para explicar el "/ 100". **No** lo
metas dentro del encabezado del paso: ese encabezado ya es un `<button>` y un botón dentro de otro es HTML
inválido (falla con teclado y lectores de pantalla). Si quieres que las pastillas expliquen "rotación", pon
`<Termino id="rotacion" />` junto al mismo título.

**(f) Impacto y suelo.** En la columna derecha:

```tsx
          <h2 className="font-display text-2xl font-semibold">{elegida && !elegida.isCurrent ? 'Contra seguir como hoy' : 'Impacto comparado'}</h2>
```

El medidor de suelo usa `suelo.current` y `suelo.recommended` (en vez de `analysis.soilHealth.*`). Su segunda
etiqueta: `{elegida ? elegida.title : 'Con la rotación'}`. Las barras:

```tsx
            {impacto.map((it) => <ImpactBar key={it.label} item={it} etiqueta={etiqueta} />)}
```

Y debajo de "Suelo de la parcela" (tu tarjeta del doc 07), la lista de qué confirmar:

```tsx
          {(analysis.localChecks?.length ?? 0) > 0 && (
            <div className="rounded-card border border-line bg-surface-raised p-5 shadow-card">
              <p className="flex items-center gap-2 text-sm font-medium">
                <ClipboardCheck size={16} className="text-leaf-700" aria-hidden /> Antes de decidir, confirma
              </p>
              <ul className="mt-3 space-y-2 text-sm text-ink-700">
                {analysis.localChecks!.map((c) => (
                  <li key={c} className="flex gap-2">
                    <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-leaf-500" aria-hidden />{c}
                  </li>
                ))}
              </ul>
            </div>
          )}
```

**(g) Aviso "Tú decides".** Reemplaza el último `<p className="px-6 pb-6 text-xs text-ink-500">…</p>` por:

```tsx
      <aside className="mx-6 mb-6 flex gap-3 rounded-card border border-line bg-canvas-subtle p-4 text-sm text-ink-700">
        <Users size={20} className="mt-0.5 shrink-0 text-leaf-700" aria-hidden />
        <p>
          <strong className="text-ink-900">Tú decides.</strong> Field Shift te ayuda a explorar opciones con clima de
          NASA POWER y reglas agronómicas; no reemplaza tu experiencia ni la de un agrónomo de tu zona. El nitrógeno y
          la salud del suelo son <Termino id="estimado">estimaciones</Termino>.
        </p>
      </aside>
```

## Paso 5 · `src/components/NasaMetricCard.tsx`: ⓘ en cada dato de NASA

```tsx
import Termino from './Termino';
import type { TerminoId } from '../lib/glosario';

const TERMINO: Record<NasaMetric['id'], TerminoId> = {
  soilMoisture: 'humedad-suelo', rain90d: 'anomalia', tempMean: 'anomalia', solarRadiation: 'radiacion',
};
```

y en la etiqueta: `<p className="text-xs uppercase tracking-widest text-paper/60"><Termino id={TERMINO[m.id]} claro>{m.label}</Termino></p>`.

## Paso 6 · `src/lib/pdf.ts`: estrategias, qué confirmar y aviso

Después de la tabla "Por qué se recomienda / Riesgos":

```ts
  if (a.strategies?.length) {
    titulo('Estrategias comparadas');
    tabla(
      ['Estrategia', 'Cultivos por temporada', 'Riego (mm)', 'Nitrógeno (kg/ha, est.)', 'Suelo (/100, est.)'],
      a.strategies.map((s) => [
        s.isRecommended ? `${s.title} (recomendada)` : s.title,
        s.steps.map((p) => `${SEASON_LABEL[p.season]}: ${cropName(p.cropId)}`).join('\n'),
        String(s.irrigationMm), String(s.nitrogenKgHa), String(s.soilHealth),
      ]),
    );
  }
```

Y después de la incertidumbre:

```ts
  if (a.localChecks?.length) {
    titulo('Antes de decidir, confirma');
    parrafo(a.localChecks.map((c) => `- ${c}`).join('\n'));
  }
  titulo('Tú decides');
  parrafo('Este plan es una guía para explorar opciones con datos de NASA POWER y reglas agronómicas. No reemplaza tu experiencia ni la de un agrónomo de tu zona.');
```

(Recuerda la regla del archivo: nada de flechas ni emojis en el PDF.)

## Cómo probar y mandar el PR

Con datos de ejemplo (`VITE_USE_MOCK=true`):

1. Analiza: aparecen 4 tarjetas. "Seguir como hoy" con borde punteado y chip "Hoy"; "Ahorrar agua" con
   "Para tu prioridad" y elegida al abrir.
2. Toca "Regenerar el suelo": cambian el "Por qué", la rotación de abajo (garbanzo/veza/sorgo), las barras
   (etiqueta "Esta opción") y el medidor de suelo (52 → 86).
3. Toca "Seguir como hoy": las barras quedan iguales y el detalle muestra el descanso de invierno.
4. Celular (390 px): las tarjetas se deslizan de lado sin mover la página; las ⓘ no se salen de la pantalla.
5. Modo oscuro: borde punteado, chips y deltas verde/rojo legibles.
6. Abre un análisis viejo del Historial (sin `strategies`): la página se ve como antes, sin tarjetas.
7. Exporta el PDF: trae "Estrategias comparadas", "Antes de decidir" y "Tú decides".
8. Con el backend real (cuando el PR 3 de Mauro esté en `main`): Ensenada y Mexicali dan estrategias distintas.

```bash
npm run build
git add src/lib/estrategias.ts src/components/Estrategias.tsx src/components/ImpactBar.tsx \
        src/components/NasaMetricCard.tsx src/views/DiagnosisView.tsx src/lib/pdf.ts
git commit -m "feat: comparar estrategias de rotación en Resultados (incluye seguir como hoy)"
git push -u origin feature/front-estrategias
```

Adjunta al PR dos capturas (escritorio y celular) y menciona a Mía.
