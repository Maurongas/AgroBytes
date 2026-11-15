import { motion } from 'framer-motion';
import { deck } from '../content';
import { EASE } from './ui';

/** Marca: una parcela dibujada + el punto rojo de NASA. */
export function Mark({ size = 96, draw = true }: { size?: number; draw?: boolean }) {
  return (
    <svg viewBox="0 0 64 64" width={size} height={size} aria-hidden>
      <rect width="64" height="64" rx="16" className="fill-orbit" />
      <motion.path d="M14 46 L24 16 L48 22 L44 48 Z" fill="#4E9F3D" fillOpacity={0.85} stroke="#FBF8F1" strokeWidth="3.5" strokeLinejoin="round"
        initial={draw ? { pathLength: 0, fillOpacity: 0 } : false} animate={{ pathLength: 1, fillOpacity: 0.85 }}
        transition={{ duration: 1.2, ease: EASE }} />
      <motion.circle cx="50" cy="13" r="6" fill="#E03C21" initial={draw ? { scale: 0 } : false} animate={{ scale: 1 }}
        transition={{ delay: 1, type: 'spring', stiffness: 400, damping: 14 }} />
    </svg>
  );
}

export default function Logo({ size = 'text-8xl', dark = false, mark = 112 }: { size?: string; dark?: boolean; mark?: number }) {
  return (
    <div className="flex items-center gap-6">
      <Mark size={mark} />
      <span className={`font-display font-semibold tracking-tight ${size} ${dark ? 'text-paper' : 'text-ink-900'}`}>{deck.name}</span>
    </div>
  );
}
