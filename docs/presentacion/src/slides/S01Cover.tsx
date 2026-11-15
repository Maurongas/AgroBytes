import { AnimatePresence, motion } from 'framer-motion';
import { deck, slide, team, ui } from '../content';
import Floaters, { FloatingTitle } from '../components/Floaters';
import { EASE, NasaDot } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('cover');
// Parcela en coordenadas del escenario (1600×900)
const FIELD = [[620, 520], [740, 190], [1120, 235], [1200, 480], [920, 610]];
const PATH = `M${FIELD.map((p) => p.join(' ')).join(' L')} Z`;

/**
 * Paso 0: portada «vacía» — tierra, iconos flotando, satélite en órbita, título letra por letra y el equipo.
 * Paso 1: el título sube, se dibuja la parcela y aparece el gancho («Every season is a bet.»).
 */
export default function S01Cover({ step, preview }: SlideProps) {
  const d = preview ? 0 : 1;
  const hook = step >= 1;
  const words = (T.hook ?? '').split(' ');

  return (
    <div className="absolute inset-0 overflow-hidden bg-orbit">
      <motion.div className="soil-texture absolute inset-0" initial={{ opacity: 0, scale: 1.08 }} animate={{ opacity: hook ? 0.55 : 0.32, scale: 1 }}
        transition={{ duration: 2.4 * d, ease: EASE }} />
      <div className="absolute inset-0 bg-gradient-to-t from-orbit via-orbit/40 to-orbit/80" />
      {/* halo que respira detrás del título */}
      <motion.div className="absolute left-1/2 top-[400px] h-[700px] w-[1100px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-leaf-500/25 blur-[120px]"
        animate={{ scale: [1, 1.12, 1], opacity: hook ? 0.25 : [0.7, 1, 0.7] }} transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }} />

      <Floaters instant={!!preview} dim={hook} orbit={!hook} />

      {/* Título: grande al centro → pequeño arriba al dibujar la parcela */}
      <motion.div className="absolute inset-x-0 top-[215px] flex flex-col items-center text-center" style={{ originY: 0 }}
        initial={false} animate={hook ? { y: -190, scale: 0.42 } : { y: 0, scale: 1 }} transition={{ duration: 0.9 * d, ease: EASE }}>
        <motion.p className="mb-6 flex items-center gap-3 text-xl uppercase tracking-[0.3em] text-paper/70"
          initial={{ opacity: 0, y: -10 }} animate={{ opacity: hook ? 0 : 1, y: 0 }} transition={{ delay: hook ? 0 : 0.3 * d, duration: 0.6 }}>
          <NasaDot className="h-3.5 w-3.5" /> {deck.event}
        </motion.p>
        <FloatingTitle text={T.title} accentAt={4} instant={!!preview} delay={0.5}
          className="font-display text-[210px] font-semibold leading-[0.95] tracking-tight text-paper drop-shadow-[0_8px_40px_rgba(0,0,0,.45)]" />
        <motion.p className="mt-14 font-display text-5xl text-paper/85"
          initial={{ opacity: 0, y: 16 }} animate={{ opacity: hook ? 0 : 1, y: 0 }} transition={{ delay: hook ? 0 : 1.6 * d, duration: 0.7, ease: EASE }}>
          {T.subtitle}
        </motion.p>
      </motion.div>

      {/* Equipo (solo en la portada vacía) */}
      <AnimatePresence>
        {!hook && (
          <motion.div key="team" className="absolute inset-x-0 bottom-14 flex flex-col items-center gap-4"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0, y: 20 }} transition={{ delay: 2 * d, duration: 0.6 }}>
            <p className="text-sm uppercase tracking-[0.35em] text-paper/45">{deck.challenge}</p>
            <div className="flex flex-wrap justify-center gap-3">
              {team.map((n, i) => (
                <motion.span key={n} className="rounded-full border border-paper/15 bg-paper/[0.08] px-5 py-2 text-xl text-paper/90 backdrop-blur"
                  initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: [0, -5, 0] }}
                  transition={{ opacity: { delay: (2.2 + i * 0.12) * d }, y: { duration: 4, repeat: Infinity, ease: 'easeInOut', delay: i * 0.3 } }}>
                  {n}
                </motion.span>
              ))}
            </div>
            <span className="sr-only">{ui.team}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Parcela + gancho */}
      <AnimatePresence>
        {hook && (
          <motion.div key="hook" className="absolute inset-0" exit={{ opacity: 0 }}>
            <svg viewBox="0 0 1600 900" className="absolute inset-0 h-full w-full">
              <motion.path d={PATH} fill="#4E9F3D" stroke="#FBF8F1" strokeWidth="5" strokeLinejoin="round"
                initial={{ pathLength: 0, fillOpacity: 0 }} animate={{ pathLength: 1, fillOpacity: 0.28 }}
                transition={{ pathLength: { duration: 2 * d, delay: 0.3 * d, ease: 'easeInOut' }, fillOpacity: { delay: 2.2 * d, duration: 0.8 * d } }} />
              {FIELD.map(([x, y], i) => (
                <motion.circle key={i} cx={x} cy={y} r="10" fill="#FBF8F1" stroke="#3F7D4A" strokeWidth="4"
                  initial={{ scale: 0 }} animate={{ scale: 1 }}
                  transition={{ delay: (0.3 + i * 0.4) * d, type: 'spring', stiffness: 500, damping: 16 }} />
              ))}
            </svg>
            <h2 className="absolute bottom-24 left-24 font-display text-8xl font-semibold tracking-tight text-paper">
              {words.map((w, i) => (
                <motion.span key={i} className="mr-[0.25em] inline-block" initial={{ opacity: 0, y: 30, filter: 'blur(8px)' }}
                  animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }} transition={{ delay: (2.3 + i * 0.3) * d, duration: 0.6, ease: EASE }}>
                  {w}
                </motion.span>
              ))}
            </h2>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
