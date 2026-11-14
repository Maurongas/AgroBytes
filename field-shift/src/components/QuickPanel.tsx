import { motion } from 'framer-motion';
import { Droplets, Sprout, TrendingUp, ArrowRight, Check } from 'lucide-react';
import { useStore } from '../store/useStore';
import { CROPS } from '../lib/crops';
import type { Priority } from '../api/types';

const PRIORITIES: { id: Priority; title: string; text: string; icon: typeof Droplets; tone: string }[] = [
  { id: 'water', title: 'Ahorrar agua', text: 'Menos riego, más retención', icon: Droplets, tone: 'text-sky-500' },
  { id: 'nitrogen', title: 'Regenerar nitrógeno', text: 'Suelo más fértil con leguminosas', icon: Sprout, tone: 'text-nitro' },
  { id: 'yield', title: 'Maximizar rendimiento', text: 'Mayor producción por hectárea', icon: TrendingUp, tone: 'text-leaf-500' },
];

interface Props {
  onAnalyze: () => void;
  pending: boolean;
  error?: string | null;
}

export default function QuickPanel({ onAnalyze, pending, error }: Props) {
  const { geometry, areaHa, crop, priority, setCrop, setPriority } = useStore();
  const ready = !!geometry && !!crop && !!priority;
  const missing = !geometry ? 'Dibuja tu parcela en el mapa' : !crop ? 'Elige tu cultivo actual' : !priority ? 'Elige tu prioridad' : '';

  return (
    <aside className="absolute inset-x-0 bottom-0 z-[1100] max-h-[65%] overflow-auto rounded-t-panel border border-line bg-surface-raised/95 p-5 shadow-lift backdrop-blur md:inset-x-auto md:bottom-4 md:right-4 md:top-4 md:max-h-none md:w-[400px] md:rounded-panel">
      <h1 className="font-display text-2xl font-semibold">Tu parcela</h1>

      <section className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-ink-500">1 · Terreno</p>
        <div className="mt-2 flex items-center gap-2 text-sm">
          <span className={`flex h-5 w-5 items-center justify-center rounded-full ${geometry ? 'bg-leaf-600 text-canvas' : 'bg-surface-sunken text-ink-400'}`}>
            {geometry && <Check size={13} />}
          </span>
          <span className="text-ink-700">{geometry && areaHa ? `${areaHa.toFixed(1)} hectáreas marcadas` : 'Aún no has dibujado tu parcela'}</span>
        </div>
      </section>

      <section className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-ink-500">2 · Cultivo actual</p>
        <div className="mt-2 flex flex-wrap gap-2">
          {CROPS.map((c) => (
            <motion.button key={c.id} whileTap={{ scale: 0.96 }} onClick={() => setCrop(c.id)}
              className={`rounded-full border px-4 py-2 text-sm transition-colors ${
                crop === c.id ? 'border-leaf-600 bg-leaf-50 font-medium text-leaf-900' : 'border-line bg-white text-ink-700 hover:border-leaf-300'}`}>
              {c.name}
            </motion.button>
          ))}
        </div>
      </section>

      <section className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-ink-500">3 · Tu prioridad</p>
        <div className="mt-2 flex flex-col gap-2">
          {PRIORITIES.map(({ id, title, text, icon: Icon, tone }) => (
            <motion.button key={id} whileHover={{ y: -2 }} whileTap={{ scale: 0.98 }} onClick={() => setPriority(id)}
              className={`flex items-center gap-3 rounded-2xl border p-3 text-left transition-colors ${
                priority === id ? 'border-leaf-600 bg-leaf-50' : 'border-line bg-white hover:border-leaf-300'}`}>
              <Icon size={22} className={tone} />
              <span>
                <span className="block text-sm font-medium">{title}</span>
                <span className="block text-xs text-ink-500">{text}</span>
              </span>
            </motion.button>
          ))}
        </div>
      </section>

      {error && <p className="mt-4 rounded-xl bg-danger/10 p-3 text-sm text-danger">{error}</p>}

      <button onClick={onAnalyze} disabled={!ready || pending}
        className="mt-6 flex w-full items-center justify-center gap-2 rounded-2xl bg-leaf-600 px-4 py-3 font-medium text-canvas transition-colors hover:bg-leaf-700 disabled:opacity-50">
        {pending ? 'Analizando…' : 'Analizar parcela'} {!pending && <ArrowRight size={18} />}
      </button>
      {!ready && <p className="mt-2 text-center text-xs text-ink-500">{missing}</p>}
    </aside>
  );
}