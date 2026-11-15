import { useEffect, useState, type ComponentType } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { BarChart3, CalendarDays, Layers3, PenTool, SlidersHorizontal, type LucideIcon } from 'lucide-react';
import { paneFinalStep, panes, prototypeSteps, slide, type PaneId } from '../content';
import DrawPane from '../panes/Draw';
import NasaPane from '../panes/Nasa';
import ComparePane from '../panes/Compare';
import WhatIfPane from '../panes/WhatIf';
import FieldPane from '../panes/Field';
import { EASE, Eyebrow } from '../components/ui';
import { ApiTicker, LiveBadge } from '../components/ApiStatus';
import type { SlideProps } from './types';

const T = slide('prototype');
const ORDER: PaneId[] = ['draw', 'nasa', 'compare', 'whatif', 'field'];
const PANE: Record<PaneId, { C: ComponentType<SlideProps>; icon: LucideIcon }> = {
  draw: { C: DrawPane, icon: PenTool },
  nasa: { C: NasaPane, icon: BarChart3 },
  compare: { C: ComparePane, icon: Layers3 },
  whatif: { C: WhatIfPane, icon: SlidersHorizontal },
  field: { C: FieldPane, icon: CalendarDays },
};

// Ventana del prototipo dentro del escenario 1600×900. El contenido se dibuja a 1600 px de ancho y se escala.
const FRAME = { x: 64, top: 96, w: 1472, h: 784, bar: 64 };
const SCALE = FRAME.w / 1600;
const INNER_H = Math.round((FRAME.h - FRAME.bar) / SCALE);

/**
 * La solución como demo del prototipo: una ventana de la app con pestañas. Cada clic del guion
 * avanza a la siguiente parte (prototypeSteps en content.ts); las pestañas también se pueden pulsar a mano.
 */
export default function S04Prototype({ step, preview }: SlideProps) {
  const [manual, setManual] = useState<PaneId | null>(null);
  useEffect(() => setManual(null), [step]);

  const scripted = prototypeSteps[Math.min(step, prototypeSteps.length - 1)];
  const view = manual ? { pane: manual, step: paneFinalStep[manual] } : scripted;
  const { C } = PANE[view.pane];
  const at = ORDER.indexOf(view.pane);

  return (
    <div className="absolute inset-0 overflow-hidden bg-canvas">
      <div className="absolute -right-40 -top-40 h-[520px] w-[520px] rounded-full bg-leaf-100 opacity-60 blur-3xl" />
      <div className="absolute -bottom-48 -left-40 h-[520px] w-[520px] rounded-full bg-sky-50 opacity-80 blur-3xl" />

      {/* Encabezado en una línea */}
      <motion.header className="absolute left-16 right-16 top-6 flex items-center gap-6"
        initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, ease: EASE }}>
        {T.eyebrow && <Eyebrow>{T.eyebrow}</Eyebrow>}
        <h1 className="font-display text-5xl font-semibold tracking-tight">{T.title}</h1>
        <LiveBadge />
      </motion.header>

      {/* Ventana */}
      <motion.div className="absolute overflow-hidden rounded-[28px] border border-line bg-surface-raised shadow-lift"
        style={{ left: FRAME.x, top: FRAME.top, width: FRAME.w, height: FRAME.h }}
        initial={{ opacity: 0, y: 40, scale: 0.97 }} animate={{ opacity: 1, y: 0, scale: 1 }} transition={{ duration: 0.7, ease: EASE }}>
        {/* Barra: semáforo · pestañas · marca */}
        <div className="flex items-center gap-5 border-b border-line bg-surface-sunken/70 px-6" style={{ height: FRAME.bar }}>
          <span className="flex gap-2">
            <span className="h-3.5 w-3.5 rounded-full bg-danger/70" />
            <span className="h-3.5 w-3.5 rounded-full bg-sun-500/80" />
            <span className="h-3.5 w-3.5 rounded-full bg-ok/70" />
          </span>
          <nav className="flex gap-1.5">
            {ORDER.map((id, i) => {
              const Icon = PANE[id].icon;
              const on = id === view.pane;
              const done = i < at;
              return (
                <button key={id} type="button" data-interactive onClick={() => setManual(id)}
                  className={`relative flex items-center gap-2 rounded-full px-4 py-2 text-lg font-medium transition-colors ${on ? 'bg-leaf-600 text-paper shadow-card' : done ? 'text-leaf-700 hover:bg-leaf-50' : 'text-ink-500 hover:bg-surface-raised'}`}>
                  <span className={`flex h-6 w-6 items-center justify-center rounded-full font-mono text-sm ${on ? 'bg-paper/20' : done ? 'bg-leaf-100' : 'bg-surface-raised'}`}>{i + 1}</span>
                  <Icon size={18} /> {panes[id].tab}
                </button>
              );
            })}
          </nav>
          <ApiTicker />
        </div>

        {/* Contenido de la pestaña (la app real, escalada) */}
        <div className="relative overflow-hidden" style={{ height: FRAME.h - FRAME.bar }}>
          <div className="absolute left-0 top-0 origin-top-left [&_header_h1]:text-5xl"
            style={{ width: 1600, height: INNER_H, transform: `scale(${SCALE})` }}>
            <AnimatePresence mode="wait" initial={false}>
              <motion.div key={view.pane} className="absolute inset-0"
                initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }}
                transition={{ duration: 0.35, ease: EASE }}>
                <C step={view.step} preview={preview} />
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
