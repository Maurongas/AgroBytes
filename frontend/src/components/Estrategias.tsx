import type { ReactNode } from 'react';
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
  titulo: string; valor: number; unidad: string; clase: string; delta?: ReactNode;
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
