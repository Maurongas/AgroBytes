import { motion } from 'framer-motion';
import type { ImpactItem } from '../api/types';

export default function ImpactBar({ item, etiqueta = 'Recomendado' }: { item: ImpactItem; etiqueta?: string }) {
  const max = Math.max(Math.abs(item.current), Math.abs(item.recommended)) || 1;
  const better = item.betterWhen === 'higher' ? item.recommended > item.current : item.recommended < item.current;
  const delta = item.current === 0 ? 0 : ((item.recommended - item.current) / Math.abs(item.current)) * 100;

  const bar = (value: number, color: string, delay: number) => (
    <div className="h-2.5 w-full rounded-full bg-surface-sunken">
      <motion.div className={`h-full rounded-full ${color}`} initial={{ width: 0 }}
        animate={{ width: `${(Math.abs(value) / max) * 100}%` }}
        transition={{ duration: 0.9, delay, ease: [0.22, 1, 0.36, 1] }} />
    </div>
  );

  return (
    <div>
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium">{item.label}</span>
        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${better ? 'bg-ok/15 text-ok' : 'bg-danger/10 text-danger'}`}>
          {delta > 0 ? '+' : ''}{Math.round(delta)} %
        </span>
      </div>
      <div className="mt-2 space-y-1.5">
        <div className="flex items-center gap-2 text-xs text-ink-500">
          <span className="w-20 shrink-0">Actual</span>{bar(item.current, 'bg-line-strong', 0)}
          <span className="w-16 shrink-0 text-right">{item.current} {item.unit}</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-ink-700">
          <span className="w-20 shrink-0 truncate">{etiqueta}</span>{bar(item.recommended, 'bg-leaf-600', 0.15)}
          <span className="w-16 shrink-0 text-right">{item.recommended} {item.unit}</span>
        </div>
      </div>
    </div>
  );
}