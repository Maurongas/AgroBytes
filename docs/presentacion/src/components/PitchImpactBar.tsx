import { motion } from 'framer-motion';
import type { ImpactItem } from '@app/api/types';
import { ui } from '../content';
import { EASE, Estimated } from './ui';

/**
 * Misma lógica y estilo que frontend/src/components/ImpactBar.tsx, en inglés y a tamaño de escenario.
 * Si cambias ImpactBar (colores, cálculo del %), revisa este archivo.
 */
export default function PitchImpactBar({ item, estimated, delay = 0 }: { item: ImpactItem; estimated?: boolean; delay?: number }) {
  const max = Math.max(Math.abs(item.current), Math.abs(item.recommended)) || 1;
  const better = item.betterWhen === 'higher' ? item.recommended > item.current : item.recommended < item.current;
  const delta = item.current === 0 ? 0 : ((item.recommended - item.current) / Math.abs(item.current)) * 100;

  const bar = (value: number, color: string, d: number) => (
    <div className="h-4 w-full rounded-full bg-surface-sunken">
      <motion.div className={`h-full rounded-full ${color}`} initial={{ width: 0 }}
        animate={{ width: `${(Math.abs(value) / max) * 100}%` }}
        transition={{ duration: 1.1, delay: delay + d, ease: EASE }} />
    </div>
  );

  return (
    <div>
      <div className="flex items-center justify-between gap-3">
        <span className="flex items-center gap-2 text-xl font-medium">
          {item.label} {estimated && <Estimated className="text-nitro" />}
        </span>
        <motion.span className={`rounded-full px-3 py-1 text-lg font-semibold ${better ? 'bg-ok/15 text-ok' : 'bg-danger/10 text-danger'}`}
          initial={{ opacity: 0, scale: 0.6 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: delay + 0.9, type: 'spring', stiffness: 300, damping: 18 }}>
          {delta > 0 ? '+' : ''}{Math.round(delta)} %
        </motion.span>
      </div>
      <div className="mt-3 space-y-2">
        <div className="flex items-center gap-3 text-base text-ink-500">
          <span className="w-32 shrink-0">{ui.today}</span>{bar(item.current, 'bg-line-strong', 0)}
          <span className="w-28 shrink-0 text-right font-mono">{item.current} {item.unit}</span>
        </div>
        <div className="flex items-center gap-3 text-base text-ink-700">
          <span className="w-32 shrink-0">{ui.withRotation}</span>{bar(item.recommended, 'bg-leaf-600', 0.2)}
          <span className="w-28 shrink-0 text-right font-mono">{item.recommended} {item.unit}</span>
        </div>
      </div>
    </div>
  );
}
