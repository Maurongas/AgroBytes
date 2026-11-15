import type { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { ui } from '../content';

export const EASE = [0.22, 1, 0.36, 1] as const;

/** Etiqueta obligatoria para nitrógeno y salud del suelo (son estimaciones por reglas). */
export function Estimated({ className = '' }: { className?: string }) {
  return (
    <span className={`inline-flex items-center rounded-full border border-current/30 px-2 py-0.5 text-[11px] font-medium uppercase tracking-widest opacity-70 ${className}`}>
      {ui.estimated}
    </span>
  );
}

/** «01 · The challenge»: número en mono + etiqueta, con una rayita que crece. */
export function Eyebrow({ children, dark = false, className = '' }: { children: string; dark?: boolean; className?: string }) {
  const [num, ...rest] = children.split(' · ');
  const label = rest.length ? rest.join(' · ') : num;
  return (
    <p className={`flex items-center gap-3 text-base font-semibold uppercase tracking-[0.25em] ${dark ? 'text-leaf-300' : 'text-leaf-600'} ${className}`}>
      {rest.length > 0 && <span className="font-mono">{num}</span>}
      <motion.span className="h-0.5 w-10 origin-left rounded-full bg-current" initial={{ scaleX: 0 }} animate={{ scaleX: 1 }} transition={{ delay: 0.2, duration: 0.6, ease: EASE }} />
      {label}
    </p>
  );
}

export function Title({ children, sub, eyebrow, dark = false, className = '' }: { children: ReactNode; sub?: ReactNode; eyebrow?: string; dark?: boolean; className?: string }) {
  return (
    <motion.header className={className} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: EASE }}>
      {eyebrow && <Eyebrow dark={dark} className="mb-3">{eyebrow}</Eyebrow>}
      <h1 className={`font-display text-6xl font-semibold tracking-tight ${dark ? 'text-paper' : 'text-ink-900'}`}>{children}</h1>
      {sub && <p className={`mt-3 text-xl ${dark ? 'text-paper/70' : 'text-ink-500'}`}>{sub}</p>}
    </motion.header>
  );
}

/** Marca roja de NASA, igual que en la cabecera de diagnóstico de la app. */
export const NasaDot = ({ className = 'h-3 w-3' }: { className?: string }) => (
  <span className={`inline-block rounded-full bg-nasa-mark ${className}`} />
);

/** Ícono de cada cultivo: el mismo componente que usa la app. */
export { default as CropIcon } from '@app/components/CropIcon';
