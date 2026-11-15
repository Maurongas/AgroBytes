import type { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Bean, Carrot, Cherry, CircleDashed, Cloud, Flower, Sprout, Wheat, type LucideIcon } from 'lucide-react';
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

export function Title({ children, sub, dark = false, className = '' }: { children: ReactNode; sub?: ReactNode; dark?: boolean; className?: string }) {
  return (
    <motion.header className={className} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: EASE }}>
      <h1 className={`font-display text-6xl font-semibold tracking-tight ${dark ? 'text-paper' : 'text-ink-900'}`}>{children}</h1>
      {sub && <p className={`mt-3 text-xl ${dark ? 'text-paper/70' : 'text-ink-500'}`}>{sub}</p>}
    </motion.header>
  );
}

/** Marca roja de NASA, igual que en la cabecera de diagnóstico de la app. */
export const NasaDot = ({ className = 'h-3 w-3' }: { className?: string }) => (
  <span className={`inline-block rounded-full bg-nasa-mark ${className}`} />
);

const CROP_ICON: Record<string, { icon: LucideIcon; tone: string }> = {
  maize: { icon: Wheat, tone: 'text-sun-500' }, sorghum: { icon: Wheat, tone: 'text-clay-500' },
  wheat: { icon: Wheat, tone: 'text-sun-700' }, barley: { icon: Wheat, tone: 'text-sun-700' },
  oat: { icon: Wheat, tone: 'text-leaf-500' }, bean: { icon: Bean, tone: 'text-nitro' },
  soy: { icon: Bean, tone: 'text-leaf-600' }, chickpea: { icon: Bean, tone: 'text-clay-500' },
  pea: { icon: Bean, tone: 'text-leaf-500' }, vetch: { icon: Sprout, tone: 'text-leaf-600' },
  canola: { icon: Flower, tone: 'text-sun-500' }, safflower: { icon: Flower, tone: 'text-sun-700' },
  cotton: { icon: Cloud, tone: 'text-ink-400' }, tomato: { icon: Cherry, tone: 'text-danger' },
  chile: { icon: Cherry, tone: 'text-danger' }, potato: { icon: Carrot, tone: 'text-clay-500' },
  onion: { icon: Carrot, tone: 'text-clay-300' }, squash: { icon: Carrot, tone: 'text-sun-500' },
  fallow: { icon: CircleDashed, tone: 'text-ink-400' },
};

export function CropIcon({ id, size = 22, className = '' }: { id: string; size?: number; className?: string }) {
  const c = CROP_ICON[id] ?? { icon: Sprout, tone: 'text-leaf-600' };
  const Icon = c.icon;
  return <Icon size={size} className={`${c.tone} ${className}`} aria-hidden />;
}
