import { AnimatePresence, motion } from 'framer-motion';
import { CloudRain, Layers, Lightbulb, Lock, Thermometer, type LucideIcon } from 'lucide-react';
import CountUp from '@app/components/CountUp';
import { nasaYears, problems, slide } from '../content';
import { EASE, NasaDot, Title } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('challenge');
const ICON: Record<(typeof problems)[number]['id'], { icon: LucideIcon; tone: string; bg: string }> = {
  heat: { icon: Thermometer, tone: 'text-danger', bg: 'bg-sun-100' },
  rain: { icon: CloudRain, tone: 'text-sky-500', bg: 'bg-sky-50' },
  soil: { icon: Layers, tone: 'text-clay-500', bg: 'bg-clay-100' },
};

/** Candado que se rompe en dos mitades y deja ver la palabra «Gap». */
function BrokenLock({ instant }: { instant: boolean }) {
  const d = instant ? 0 : 1;
  const half = (side: -1 | 1) => (
    <motion.div className="absolute inset-0 flex items-center justify-center text-ink-400"
      style={{ clipPath: side < 0 ? 'inset(0 50% 0 0)' : 'inset(0 0 0 50%)' }}
      initial={{ x: 0, rotate: 0, opacity: 1 }}
      animate={{ x: side * 150, rotate: side * 18, opacity: 0 }}
      transition={{ delay: 0.7 * d, duration: 0.9 * d, ease: EASE }}>
      <Lock size={150} strokeWidth={1.5} />
    </motion.div>
  );
  return (
    <div className="relative flex h-[260px] w-[520px] items-center justify-center">
      <motion.div className="absolute inset-0" initial={{ x: 0 }} animate={{ x: [0, -6, 6, -4, 4, 0] }} transition={{ duration: 0.5 * d }}>
        {half(-1)}
        {half(1)}
      </motion.div>
      <motion.p className="absolute bottom-0 text-lg uppercase tracking-[0.3em] text-ink-500"
        initial={{ opacity: 1 }} animate={{ opacity: 0 }} transition={{ delay: 0.8 * d, duration: 0.4 * d }}>
        {nasaYears.lock}
      </motion.p>
      <motion.span className="relative font-display text-[200px] font-bold leading-none text-clay-500"
        initial={{ opacity: 0, scale: 0.4, letterSpacing: '0.4em' }} animate={{ opacity: 1, scale: 1, letterSpacing: '0em' }}
        transition={{ delay: 1.1 * d, duration: 0.8 * d, ease: EASE }}>
        {nasaYears.gap}
      </motion.span>
    </div>
  );
}

export default function S02Challenge({ step, preview }: SlideProps) {
  return (
    <div className="absolute inset-0 flex flex-col bg-canvas px-24 py-20">
      <Title eyebrow={T.eyebrow}>{T.title}</Title>

      <motion.div className="mt-14 grid grid-cols-3 gap-10" initial="hidden" animate="show"
        variants={{ hidden: {}, show: { transition: { staggerChildren: preview ? 0 : 0.35, delayChildren: preview ? 0 : 0.3 } } }}>
        {problems.map((p) => {
          const { icon: Icon, tone, bg } = ICON[p.id];
          return (
            <motion.div key={p.id} className="flex items-center gap-6"
              variants={{ hidden: { opacity: 0, y: 40, scale: 0.9 }, show: { opacity: 1, y: 0, scale: 1, transition: { type: 'spring', stiffness: 260, damping: 20 } } }}>
              <span className={`flex h-28 w-28 shrink-0 items-center justify-center rounded-[28px] ${bg}`}>
                <Icon size={64} className={tone} strokeWidth={1.75} />
              </span>
              <span className="font-display text-4xl font-semibold leading-tight">{p.label}</span>
            </motion.div>
          );
        })}
      </motion.div>

      <div className="mt-auto flex items-end justify-between">
        <AnimatePresence>
          {step >= 1 && (
            <motion.div key="years" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.6, ease: EASE }}>
              <p className="font-display text-[160px] font-bold leading-none text-orbit">
                <CountUp value={nasaYears.value} /><span className="text-7xl">{nasaYears.suffix}</span>
              </p>
              <p className="mt-4 flex items-center gap-3 text-3xl text-ink-700"><NasaDot className="h-4 w-4" /> {nasaYears.line}</p>
            </motion.div>
          )}
        </AnimatePresence>
        <AnimatePresence>
          {step >= 2 && (
            <motion.div key="gap" className="flex flex-col items-center" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <BrokenLock instant={!!preview} />
              <motion.p className="mt-6 flex items-center gap-3 rounded-full bg-orbit px-7 py-4 text-2xl text-paper shadow-lift"
                initial={{ opacity: 0, y: 20, scale: 0.95 }} animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ delay: preview ? 0 : 1.8, duration: 0.6, ease: EASE }}>
                <Lightbulb size={28} className="text-sun-300" /> {nasaYears.insight}
              </motion.p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
