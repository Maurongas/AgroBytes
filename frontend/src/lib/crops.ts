import type { Season } from '../api/types';
import { tr } from './i18n';

// Espejo de backend/app/data/crops.json (18 cultivos). Nombre en español e inglés (backend/app/core/i18n.py).
// 'fallow' no es un cultivo: es el paso de "descanso" de la rotación.
const CATALOG = [
  { id: 'maize', es: 'Maíz', en: 'Maize' },
  { id: 'sorghum', es: 'Sorgo', en: 'Sorghum' },
  { id: 'wheat', es: 'Trigo', en: 'Wheat' },
  { id: 'barley', es: 'Cebada', en: 'Barley' },
  { id: 'oat', es: 'Avena', en: 'Oat' },
  { id: 'bean', es: 'Frijol', en: 'Bean' },
  { id: 'soy', es: 'Soya', en: 'Soybean' },
  { id: 'chickpea', es: 'Garbanzo', en: 'Chickpea' },
  { id: 'pea', es: 'Chícharo', en: 'Pea' },
  { id: 'vetch', es: 'Veza (abono verde)', en: 'Vetch (green manure)' },
  { id: 'canola', es: 'Canola', en: 'Canola' },
  { id: 'safflower', es: 'Cártamo', en: 'Safflower' },
  { id: 'cotton', es: 'Algodón', en: 'Cotton' },
  { id: 'tomato', es: 'Jitomate', en: 'Tomato' },
  { id: 'chile', es: 'Chile', en: 'Chili pepper' },
  { id: 'potato', es: 'Papa', en: 'Potato' },
  { id: 'onion', es: 'Cebolla', en: 'Onion' },
  { id: 'squash', es: 'Calabaza', en: 'Squash' },
];

/** Lista de cultivos con el nombre en el idioma actual (llámala al renderizar). */
export const crops = () => CATALOG.map((c) => ({ id: c.id, name: tr(c.es, c.en) }));

export const FALLOW_ID = 'fallow';

export function cropName(id: string): string {
  if (id === FALLOW_ID) return tr('Descanso (barbecho)', 'Rest (fallow)');
  const c = CATALOG.find((x) => x.id === id);
  return c ? tr(c.es, c.en) : id;
}

const SEASON: Record<Season, [string, string]> = {
  autumn: ['Otoño', 'Autumn'], winter: ['Invierno', 'Winter'], spring: ['Primavera', 'Spring'], summer: ['Verano', 'Summer'],
};
export const seasonLabel = (s: Season) => tr(...SEASON[s]);

export const SEASON_BG: Record<Season, string> = {
  autumn: 'bg-clay-100', winter: 'bg-sky-50', spring: 'bg-leaf-50', summer: 'bg-sun-100',
};
