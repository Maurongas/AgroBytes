import { useEffect, useState } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { Check, Layers, ListChecks, PenTool, Satellite, Scale, Sprout, type LucideIcon } from 'lucide-react';
import { pipeline, slide } from '../content';
import { strategies, strategyEn } from '../data';
import { EASE, NasaDot, Title } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('build');
type InputId = (typeof pipeline.inputs)[number]['id'];
const ICON: Record<InputId, { icon: LucideIcon; tone: string }> = {
  field: { icon: PenTool, tone: 'text-leaf-300' },
  nasa: { icon: Satellite, tone: 'text-paper' },
  soil: { icon: Layers, tone: 'text-clay-300' },
  crops: { icon: Sprout, tone: 'text-leaf-300' },
};

// Geometría del diagrama (coordenadas del escenario 1600×900)
const IN = { x: 96, w: 430, h: 112, tops: [228, 370, 512, 654] };
const ENGINE = { x: 690, w: 320, top: 360, h: 240 };
const OUT = { x: 1160, w: 344, top: 300, h: 360 };
const MID = ENGINE.top + ENGINE.h / 2;
const inPath = (top: number) => {
  const y = top + IN.h / 2;
  const x0 = IN.x + IN.w;
  const x1 = ENGINE.x;
  return `M${x0} ${y} C${x0 + 90} ${y} ${x1 - 90} ${MID} ${x1} ${MID}`;
};
const OUT_PATH = `M${ENGINE.x + ENGINE.w} ${MID} L${OUT.x} ${MID}`;
const CARDS = strategies.slice(0, 4);

export default function S03Build({ preview }: SlideProps) {
  const reduce = useReducedMotion();
  const d = preview ? 0 : 1;
  const [hover, setHover] = useState<InputId | null>(null);
  const [flow, setFlow] = useState(!!preview);
  useEffect(() => {
    if (preview) return;
    const t = setTimeout(() => setFlow(true), 2300);
    return () => clearTimeout(t);
  }, [preview]);

  return (
    <div className="absolute inset-0 overflow-hidden bg-orbit px-24 py-16">
      <div className="absolute inset-0 opacity-[0.07]"
        style={{ backgroundImage: 'linear-gradient(#FBF8F1 1px, transparent 1px), linear-gradient(90deg, #FBF8F1 1px, transparent 1px)', backgroundSize: '80px 80px' }} />
      <Title dark eyebrow={T.eyebrow} className="relative">{T.title}</Title>

      {/* Conexiones + datos que fluyen */}
      <svg viewBox="0 0 1600 900" className="pointer-events-none absolute inset-0 h-full w-full">
        {IN.tops.map((top, i) => {
          const id = pipeline.inputs[i].id;
          const on = hover === null || hover === id;
          return (
            <motion.path key={id} d={inPath(top)} fill="none" stroke="#9CCB86" strokeWidth={on ? 3 : 2} strokeOpacity={on ? 0.75 : 0.2}
              initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ delay: (1.1 + i * 0.15) * d, duration: 0.8 * d, ease: 'easeInOut' }} />
          );
        })}
        <motion.path d={OUT_PATH} fill="none" stroke="#FFCF5C" strokeWidth={3} strokeOpacity={0.8}
          initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ delay: 2.3 * d, duration: 0.6 * d }} />
        {flow && !reduce && (
          <g>
            {IN.tops.map((top, i) => [0, 0.7].map((off) => (
              <circle key={`${i}-${off}`} r={6} fill={i === 1 ? '#E03C21' : '#CDE6BE'}>
                <animateMotion dur="1.6s" begin={`${i * 0.2 + off}s`} repeatCount="indefinite" path={inPath(top)} />
              </circle>
            )))}
            {[0, 0.5, 1].map((off) => (
              <circle key={off} r={7} fill="#FFCF5C">
                <animateMotion dur="1.4s" begin={`${off}s`} repeatCount="indefinite" path={OUT_PATH} />
              </circle>
            ))}
          </g>
        )}
      </svg>

      {/* Entradas */}
      {pipeline.inputs.map((n, i) => {
        const { icon: Icon, tone } = ICON[n.id];
        return (
          <motion.div key={n.id} className="absolute flex items-center gap-5 rounded-panel border border-paper/15 bg-orbit-soft/90 px-6 text-paper shadow-lift backdrop-blur"
            style={{ left: IN.x, top: IN.tops[i], width: IN.w, height: IN.h }}
            initial={{ opacity: 0, x: -40 }} animate={{ opacity: hover && hover !== n.id ? 0.45 : 1, x: 0 }}
            whileHover={{ scale: 1.04 }} onHoverStart={() => setHover(n.id)} onHoverEnd={() => setHover(null)}
            transition={{ delay: hover ? 0 : (0.3 + i * 0.22) * d, duration: 0.6, ease: EASE }}>
            <span className="relative flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-paper/10">
              <Icon size={34} className={tone} strokeWidth={1.75} />
              {n.id === 'nasa' && <NasaDot className="absolute -right-1 -top-1 h-3.5 w-3.5" />}
            </span>
            <span className="min-w-0">
              <span className="block font-display text-3xl font-semibold">{n.title}</span>
              <span className="block text-lg leading-snug text-paper/65">{n.line}</span>
            </span>
          </motion.div>
        );
      })}

      {/* Motor de reglas */}
      <motion.div className="absolute flex flex-col items-center justify-center rounded-[32px] bg-leaf-600 p-6 text-center text-paper shadow-lift"
        style={{ left: ENGINE.x, top: ENGINE.top, width: ENGINE.w, height: ENGINE.h }}
        initial={{ opacity: 0, scale: 0.7 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 1.8 * d, type: 'spring', stiffness: 220, damping: 18 }}>
        {flow && !reduce && (
          <motion.span className="absolute inset-0 rounded-[32px] border-4 border-leaf-300" initial={{ opacity: 0.7, scale: 1 }}
            animate={{ opacity: 0, scale: 1.18 }} transition={{ duration: 1.6, repeat: Infinity, ease: 'easeOut' }} />
        )}
        <motion.span animate={flow && !reduce ? { rotate: [0, -8, 8, 0] } : {}} transition={{ duration: 2.4, repeat: Infinity, ease: 'easeInOut' }}>
          <Scale size={60} strokeWidth={1.6} />
        </motion.span>
        <p className="mt-3 font-display text-4xl font-semibold">{pipeline.engine.title}</p>
        <p className="mt-2 text-lg leading-snug text-paper/85">{pipeline.engine.line}</p>
      </motion.div>

      {/* Salida: las estrategias reales del mock */}
      <motion.div className="absolute flex flex-col rounded-panel border border-paper/15 bg-paper p-6 text-ink-900 shadow-lift"
        style={{ left: OUT.x, top: OUT.top, width: OUT.w, height: OUT.h }}
        initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 2.6 * d, duration: 0.6, ease: EASE }}>
        <p className="flex items-center gap-3 font-display text-3xl font-semibold"><ListChecks size={30} className="text-leaf-600" /> {pipeline.output.title}</p>
        <p className="mt-1 text-base text-ink-500">{pipeline.output.line}</p>
        <ul className="mt-4 flex flex-1 flex-col justify-between">
          {CARDS.map((s, i) => {
            const e = strategyEn(s);
            return (
              <motion.li key={s.id}
                className={`flex items-center gap-3 rounded-2xl px-4 py-2.5 text-xl ${s.isRecommended ? 'bg-leaf-50 font-semibold text-leaf-900 ring-2 ring-leaf-600' : s.isCurrent ? 'bg-surface-sunken text-ink-500' : 'bg-canvas-subtle'}`}
                initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: (3 + i * 0.18) * d, duration: 0.5, ease: EASE }}>
                {s.isRecommended ? <Check size={20} className="text-leaf-600" /> : <span className="h-5 w-5" />}
                {e.title}
                <span className="ml-auto font-mono text-lg">{e.score}</span>
              </motion.li>
            );
          })}
        </ul>
      </motion.div>

      {/* Pie: tecnología + nota */}
      <motion.div className="absolute bottom-12 left-24 right-24 flex items-center justify-between"
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 3.6 * d }}>
        <div className="flex gap-2">
          {pipeline.stack.map((s) => (
            <span key={s} className="rounded-full border border-paper/20 px-4 py-1.5 font-mono text-base text-paper/70">{s}</span>
          ))}
        </div>
        <p className="text-xl text-paper/80">{pipeline.note}</p>
      </motion.div>
    </div>
  );
}
