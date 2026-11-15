import { motion } from 'framer-motion';
import { slide } from '../content';
import { EASE } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('hook');
// Parcela en coordenadas del escenario (1600×900)
const FIELD = [[620, 520], [740, 160], [1120, 210], [1200, 470], [920, 600]];
const PATH = `M${FIELD.map((p) => p.join(' ')).join(' L')} Z`;

export default function S01Hook({ preview }: SlideProps) {
  const words = T.title.split(' ');
  const d = preview ? 0 : 1;
  return (
    <div className="absolute inset-0 overflow-hidden bg-orbit">
      <motion.div className="soil-texture absolute inset-0" initial={{ opacity: 0, scale: 1.08 }} animate={{ opacity: 0.55, scale: 1 }}
        transition={{ duration: 2.4 * d, ease: EASE }} />
      <div className="absolute inset-0 bg-gradient-to-t from-orbit via-orbit/40 to-orbit/70" />

      <svg viewBox="0 0 1600 900" className="absolute inset-0 h-full w-full">
        <motion.path d={PATH} fill="#4E9F3D" stroke="#FBF8F1" strokeWidth="5" strokeLinejoin="round"
          initial={{ pathLength: 0, fillOpacity: 0 }} animate={{ pathLength: 1, fillOpacity: 0.28 }}
          transition={{ pathLength: { duration: 2.2 * d, delay: 0.4 * d, ease: 'easeInOut' }, fillOpacity: { delay: 2.4 * d, duration: 0.8 * d } }} />
        {FIELD.map(([x, y], i) => (
          <motion.circle key={i} cx={x} cy={y} r="10" fill="#FBF8F1" stroke="#3F7D4A" strokeWidth="4"
            initial={{ scale: 0 }} animate={{ scale: 1 }}
            transition={{ delay: (0.4 + i * 0.44) * d, type: 'spring', stiffness: 500, damping: 16 }} />
        ))}
      </svg>

      <h1 className="absolute bottom-24 left-24 font-display text-8xl font-semibold tracking-tight text-paper">
        {words.map((w, i) => (
          <motion.span key={i} className="mr-[0.25em] inline-block" initial={{ opacity: 0, y: 30, filter: 'blur(8px)' }}
            animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }} transition={{ delay: (2.6 + i * 0.32) * d, duration: 0.6, ease: EASE }}>
            {w}
          </motion.span>
        ))}
      </h1>
    </div>
  );
}
