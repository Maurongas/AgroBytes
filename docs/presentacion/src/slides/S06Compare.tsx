import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { BookOpen, Check, TriangleExclamationPoint, CircleQuestionMark, ThumbsUp, type LucideIcon } from 'lucide-react';
import type { Strategy } from '@app/api/types';
import { slide, ui } from '../content';
import { strategies, strategyEn } from '../data';
import { SEASON_EN, cropEn } from '../i18n';
import { CropIcon, EASE, Title } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('compare');
const CARDS = strategies.slice(0, 4);

const CHIPS: { key: 'why' | 'evidence' | 'benefits' | 'risks'; icon: LucideIcon; tone: string }[] = [
  { key: 'why', icon: CircleQuestionMark, tone: 'bg-sky-50 text-sky-700' },
  { key: 'evidence', icon: BookOpen, tone: 'bg-surface-sunken text-ink-700' },
  { key: 'benefits', icon: ThumbsUp, tone: 'bg-leaf-50 text-leaf-900' },
  { key: 'risks', icon: TriangleExclamationPoint, tone: 'bg-clay-100 text-clay-700' },
];

function Card({ s, forceFlip }: { s: Strategy; forceFlip: boolean }) {
  const [hover, setHover] = useState(false);
  const [clicked, setClicked] = useState(false);
  const flipped = forceFlip ? !clicked : clicked || hover;
  const e = strategyEn(s);
  const tone = s.isRecommended
    ? 'border-leaf-600 ring-4 ring-leaf-600/20 bg-surface-raised'
    : s.isCurrent ? 'border-line bg-surface-sunken' : 'border-line bg-surface-raised';

  return (
    <div data-interactive className="flip h-[560px] cursor-pointer" onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      onClick={() => setClicked((c) => !c)}>
      <div className={`flip-inner relative h-full ${flipped ? 'is-flipped' : ''}`}>
        {/* Frente */}
        <div className={`flip-face absolute inset-0 flex flex-col rounded-panel border-2 p-7 shadow-card ${tone}`}>
          {s.isRecommended && (
            <span className="absolute -top-4 left-6 flex items-center gap-1 rounded-full bg-leaf-600 px-3 py-1 text-sm font-medium text-paper shadow-card">
              <Check size={15} /> {ui.recommended}
            </span>
          )}
          <h3 className={`font-display text-3xl font-semibold leading-tight ${s.isCurrent ? 'text-ink-500' : ''}`}>{e.title}</h3>
          <ul className="mt-6 space-y-3">
            {s.steps.map((st) => (
              <li key={st.season} className={`flex items-center gap-3 rounded-2xl px-4 py-3 ${st.cropId === 'fallow' ? 'border-2 border-dashed border-line-strong' : 'bg-canvas-subtle'}`}>
                <CropIcon id={st.cropId} size={30} />
                <div className="min-w-0">
                  <p className="text-xs uppercase tracking-widest text-ink-500">{SEASON_EN[st.season]}</p>
                  <p className={`truncate text-xl font-medium ${st.cropId === 'fallow' ? 'text-ink-400' : ''}`}>{cropEn(st.cropId)}</p>
                </div>
                {st.cropId !== 'fallow' && <span className="ml-auto font-mono text-base text-ink-500">{st.score}</span>}
              </li>
            ))}
          </ul>
          <div className="mt-auto flex items-end justify-between">
            <div>
              <p className="text-xs uppercase tracking-widest text-ink-500">{ui.score}</p>
              <p className={`font-display text-6xl font-semibold ${s.isRecommended ? 'text-leaf-700' : s.isCurrent ? 'text-ink-500' : ''}`}>{e.score}</p>
            </div>
            <p className="text-right font-mono text-base text-sky-700">{s.irrigationMm} mm<br /><span className="font-sans text-xs text-ink-500">{ui.irrigation}</span></p>
          </div>
        </div>

        {/* Reverso: Why · Evidence · Benefits · Risks */}
        <div className={`flip-face flip-back absolute inset-0 flex flex-col gap-3 rounded-panel border-2 p-6 shadow-card ${tone}`}>
          <h3 className="font-display text-2xl font-semibold">{e.title}</h3>
          {CHIPS.map(({ key, icon: Icon, tone: chip }) => {
            const v = e[key];
            const text = Array.isArray(v) ? v[0] : v;
            return (
              <div key={key} className={`rounded-2xl px-4 py-3 ${chip}`}>
                <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-widest"><Icon size={14} /> {ui[key]}</p>
                <p className="mt-1 text-[15px] leading-snug">{text ?? '—'}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default function S06Compare({ step }: SlideProps) {
  const shown = Math.min(step, CARDS.length);
  const flipRecommended = step > CARDS.length;
  return (
    <div className="absolute inset-0 flex flex-col bg-canvas px-20 py-16">
      <div className="flex items-end justify-between">
        <Title>{T.title}</Title>
        <AnimatePresence>
          {shown === CARDS.length && (
            <motion.p className="text-lg text-ink-400" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>{ui.flipHint}</motion.p>
          )}
        </AnimatePresence>
      </div>
      <div className="mt-10 grid grid-cols-4 gap-6">
        {CARDS.map((s, i) => (
          <div key={s.id} className="relative h-[560px]">
            <div className="absolute inset-0 rounded-panel border-2 border-dashed border-line-soft" />
            <AnimatePresence>
              {i < shown && (
                <motion.div key={s.id} initial={{ opacity: 0, y: 60, scale: 0.94 }} animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 40 }} transition={{ duration: 0.55, ease: EASE }}>
                  <Card s={s} forceFlip={flipRecommended && s.isRecommended} />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </div>
  );
}
