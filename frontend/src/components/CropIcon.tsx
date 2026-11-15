import { Bean, Carrot, Cherry, CircleDashed, Cloud, Flower, Sprout, Wheat, type LucideIcon } from 'lucide-react';

/** Ícono y color de cada cultivo del catálogo (mismos ids que lib/crops.ts). 'fallow' = descanso. */
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

export default function CropIcon({ id, size = 18, className = '' }: { id: string; size?: number; className?: string }) {
  const c = CROP_ICON[id] ?? { icon: Sprout, tone: 'text-leaf-600' };
  const Icon = c.icon;
  return <Icon size={size} className={`inline-block shrink-0 ${c.tone} ${className}`} aria-hidden />;
}
