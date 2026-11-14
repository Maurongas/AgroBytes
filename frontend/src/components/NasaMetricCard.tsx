import { motion } from 'framer-motion';
import CountUp from './CountUp';
import type { NasaMetric } from '../api/types';

const DOT = { ok: 'bg-ok', warn: 'bg-warn', danger: 'bg-danger' } as const;

function Sparkline({ data }: { data: number[] }) {
  const min = Math.min(...data), max = Math.max(...data);
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * 100;
    const y = 28 - ((v - min) / (max - min || 1)) * 24;
    return `${x},${y}`;
  });
  return (
    <svg viewBox="0 0 100 30" className="mt-3 h-8 w-full" preserveAspectRatio="none">
      <motion.polyline points={pts.join(' ')} fill="none" stroke="#7CC3EE" strokeWidth="2"
        vectorEffect="non-scaling-stroke" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }} />
    </svg>
  );
}

export default function NasaMetricCard({ m }: { m: NasaMetric }) {
  const decimals = m.value < 1 ? 2 : m.value < 10 ? 1 : 0;
  return (
    <div className="rounded-2xl bg-orbit-soft p-4 text-paper">
      <div className="flex items-center justify-between">
        <p className="text-xs uppercase tracking-widest text-paper/60">{m.label}</p>
        <span className={`h-2.5 w-2.5 rounded-full ${DOT[m.status]}`} />
      </div>
      <p className="mt-2 font-display text-3xl font-semibold">
        <CountUp value={m.value} decimals={decimals} />
        <span className="ml-1 font-sans text-sm font-normal text-paper/60">{m.unit}</span>
      </p>
      <p className="mt-1 text-sm text-paper/80">{m.meaning}</p>
      <Sparkline data={m.series} />
      <p className="mt-2 text-[11px] text-paper/50">{m.source}</p>
    </div>
  );
}