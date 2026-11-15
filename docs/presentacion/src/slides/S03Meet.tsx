import { motion } from 'framer-motion';
import { ListChecks, PenTool, Sprout, type LucideIcon } from 'lucide-react';
import { slide, steps } from '../content';
import Logo from '../components/Logo';
import { EASE, NasaDot } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('meet');
const ICON: Record<(typeof steps)[number]['id'], LucideIcon> = { draw: PenTool, choose: ListChecks, decide: Sprout };

export default function S03Meet({ preview }: SlideProps) {
  const d = preview ? 0 : 1;
  return (
    <div className="absolute inset-0 flex flex-col items-center justify-center bg-canvas">
      <motion.div initial={{ opacity: 0, scale: 0.92 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.8 * d, ease: EASE }}>
        <Logo />
      </motion.div>
      <motion.p className="mt-6 flex items-center gap-3 text-3xl text-ink-500" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.9 * d }}>
        <NasaDot /> {T.subtitle}
      </motion.p>

      <div className="relative mt-24 flex items-center gap-40">
        <div className="absolute left-16 right-16 top-1/2 h-1 -translate-y-1/2 rounded-full bg-line-soft">
          <motion.div className="h-full origin-left rounded-full bg-leaf-500" initial={{ scaleX: 0 }} animate={{ scaleX: 1 }}
            transition={{ delay: 1.4 * d, duration: 1.8 * d, ease: 'easeInOut' }} />
        </div>
        {steps.map((s, i) => {
          const Icon = ICON[s.id];
          const at = (1.4 + i * 0.9) * d;
          return (
            <div key={s.id} className="relative flex flex-col items-center">
              <motion.span className="flex h-32 w-32 items-center justify-center rounded-full border-4"
                initial={{ backgroundColor: 'var(--color-surface-raised)', borderColor: 'var(--color-line)', color: 'var(--color-ink-400)', scale: 1 }}
                animate={{ backgroundColor: 'var(--color-leaf-600)', borderColor: 'var(--color-leaf-600)', color: '#FBF8F1', scale: [1, 1.12, 1] }}
                transition={{ delay: at, duration: 0.5 * d }}>
                <Icon size={56} strokeWidth={1.75} />
              </motion.span>
              <motion.span className="mt-5 font-display text-4xl font-semibold" initial={{ opacity: 0.35 }} animate={{ opacity: 1 }} transition={{ delay: at }}>
                {s.label}
              </motion.span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
