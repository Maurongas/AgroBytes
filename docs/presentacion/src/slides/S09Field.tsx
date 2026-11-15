import { useEffect, useState, type ReactNode } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import { CalendarDays, Check, FileText, ShieldCheck, Snowflake, ThermometerSun, Wifi, WifiOff, type LucideIcon } from 'lucide-react';
import { features, slide, ui } from '../content';
import { analysis, current, uncertaintyEn } from '../data';
import { MONTHS_EN, SEASON_MONTHS } from '../i18n';
import { Title } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('field');

/** Alterna entre `n` estados cada `ms` (se detiene con prefers-reduced-motion). */
function useTick(n: number, ms: number) {
  const reduce = useReducedMotion();
  const [i, setI] = useState(0);
  useEffect(() => {
    if (reduce) return;
    const t = setInterval(() => setI((x) => (x + 1) % n), ms);
    return () => clearInterval(t);
  }, [n, ms, reduce]);
  return i;
}

// Meses sin cultivo según la estrategia «seguir como hoy» del mock
const BARE = new Set((current?.steps ?? []).filter((s) => s.cropId === 'fallow').flatMap((s) => SEASON_MONTHS[s.season]));

function CalendarLoop() {
  return (
    <div className="grid h-full grid-cols-6 content-center gap-1.5">
      {MONTHS_EN.map((m, i) => (
        <div key={m} className={`rounded-lg py-2 text-center text-sm font-medium ${BARE.has(i) ? 'animate-blink border-2 border-dashed border-clay-500 bg-clay-100 text-clay-700' : 'bg-leaf-100 text-leaf-900'}`}>
          {m}
        </div>
      ))}
      <p className="col-span-6 mt-1 flex items-center gap-2 text-sm text-clay-700"><span className="h-3 w-3 rounded border-2 border-dashed border-clay-500" /> {ui.bareSoil}</p>
    </div>
  );
}

function AlertsLoop() {
  const i = useTick(2, 1400);
  const items: { icon: LucideIcon; label: string; tone: string }[] = [
    { icon: Snowflake, label: ui.frost, tone: 'text-sky-500 bg-sky-50' },
    { icon: ThermometerSun, label: ui.heat, tone: 'text-danger bg-sun-100' },
  ];
  return (
    <div className="flex h-full items-center justify-center gap-6">
      {items.map((it, k) => (
        <motion.div key={it.label} className={`relative flex h-24 w-24 items-center justify-center rounded-full ${it.tone}`}
          animate={{ scale: i === k ? 1.12 : 0.92, opacity: i === k ? 1 : 0.45 }} transition={{ type: 'spring', stiffness: 260, damping: 18 }}>
          {i === k && <motion.span className="absolute inset-0 rounded-full border-4 border-current" initial={{ scale: 1, opacity: 0.6 }} animate={{ scale: 1.5, opacity: 0 }} transition={{ duration: 1.2, repeat: Infinity }} />}
          <it.icon size={44} />
        </motion.div>
      ))}
    </div>
  );
}

function OfflineLoop() {
  const off = useTick(2, 1600) === 1;
  return (
    <div className="flex h-full items-center justify-center gap-6">
      <AnimatePresence mode="wait">
        <motion.span key={off ? 'off' : 'on'} initial={{ opacity: 0, scale: 0.7 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.7 }}>
          {off ? <WifiOff size={52} className="text-danger" /> : <Wifi size={52} className="text-leaf-600" />}
        </motion.span>
      </AnimatePresence>
      <div className="rounded-2xl border border-line bg-canvas px-4 py-3 shadow-card">
        <p className="flex items-center gap-2 text-base font-medium"><Check size={18} className="text-ok" /> {ui.planSaved}</p>
        <div className="mt-2 h-2 w-28 rounded-full bg-leaf-100"><div className="h-full w-3/4 rounded-full bg-leaf-500" /></div>
      </div>
    </div>
  );
}

function PdfLoop() {
  const reduce = useReducedMotion();
  return (
    <div className="relative mx-auto flex h-48 items-end justify-center overflow-hidden">
      <motion.div className="absolute bottom-6 flex h-28 w-24 flex-col gap-1.5 rounded-lg border border-line bg-paper p-3 shadow-lift"
        initial={{ y: 90 }} animate={reduce ? { y: 0 } : { y: [90, 0, 0, 90] }}
        transition={{ duration: 3, times: [0, 0.3, 0.8, 1], repeat: Infinity, ease: 'easeInOut' }}>
        <FileText size={22} className="text-danger" />
        <span className="h-1.5 w-full rounded bg-line" /><span className="h-1.5 w-4/5 rounded bg-line" /><span className="h-1.5 w-3/5 rounded bg-leaf-300" />
      </motion.div>
      <div className="relative z-10 h-6 w-40 rounded-t-lg bg-orbit" />
    </div>
  );
}

const LOOPS: Record<(typeof features)[number]['id'], { icon: LucideIcon; body: ReactNode }> = {
  calendar: { icon: CalendarDays, body: <CalendarLoop /> },
  alerts: { icon: Snowflake, body: <AlertsLoop /> },
  offline: { icon: WifiOff, body: <OfflineLoop /> },
  pdf: { icon: FileText, body: <PdfLoop /> },
};

export default function S09Field({ preview }: SlideProps) {
  return (
    <div className="absolute inset-0 flex flex-col bg-canvas px-24 py-16">
      <Title>{T.title}</Title>
      <motion.div className="mt-10 grid flex-1 grid-cols-4 gap-6" initial="hidden" animate="show"
        variants={{ hidden: {}, show: { transition: { staggerChildren: preview ? 0 : 0.22 } } }}>
        {features.map((f) => {
          const { icon: Icon, body } = LOOPS[f.id];
          return (
            <motion.article key={f.id} className="flex flex-col rounded-panel border border-line bg-surface-raised p-6 shadow-card"
              variants={{ hidden: { opacity: 0, y: 40, scale: 0.95 }, show: { opacity: 1, y: 0, scale: 1, transition: { type: 'spring', stiffness: 240, damping: 20 } } }}>
              <h3 className="flex items-center gap-3 font-display text-3xl font-semibold"><Icon size={28} className="text-leaf-600" /> {f.title}</h3>
              <p className="mt-1 text-lg text-ink-500">{f.line}</p>
              <div className="mt-6 flex min-h-[200px] flex-1 flex-col justify-center [&>*]:w-full">{body}</div>
            </motion.article>
          );
        })}
      </motion.div>
      <motion.div className="mt-8 flex items-center gap-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: preview ? 0 : 1.4 }}>
        <span className="rounded-full bg-clay-100 px-5 py-2 text-lg text-ink-900">{ui.uncertainty}: <strong>{uncertaintyEn}</strong></span>
        <span className="flex items-center gap-2 rounded-full bg-leaf-50 px-5 py-2 text-lg text-leaf-900">
          <ShieldCheck size={20} /> {ui.checkLocally} · {analysis.localChecks?.length ?? 0}
        </span>
      </motion.div>
    </div>
  );
}
