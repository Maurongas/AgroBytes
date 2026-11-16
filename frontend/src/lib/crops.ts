import type { Season } from '../api/types';

// Espejo de backend/app/data/crops.json (18 cultivos). Mejor aún: leerlo de GET /api/v1/crops.
// 'fallow' no es un cultivo: es el paso de "descanso" de la rotación.
export const CROPS = [
  { id: 'maize', name: 'Maíz' },
  { id: 'sorghum', name: 'Sorgo' },
  { id: 'wheat', name: 'Trigo' },
  { id: 'barley', name: 'Cebada' },
  { id: 'oat', name: 'Avena' },
  { id: 'bean', name: 'Frijol' },
  { id: 'soy', name: 'Soya' },
  { id: 'chickpea', name: 'Garbanzo' },
  { id: 'pea', name: 'Chícharo' },
  { id: 'vetch', name: 'Veza (abono verde)' },
  { id: 'canola', name: 'Canola' },
  { id: 'safflower', name: 'Cártamo' },
  { id: 'cotton', name: 'Algodón' },
  { id: 'tomato', name: 'Jitomate' },
  { id: 'chile', name: 'Chile' },
  { id: 'potato', name: 'Papa' },
  { id: 'onion', name: 'Cebolla' },
  { id: 'squash', name: 'Calabaza' },
];

export const FALLOW_ID = 'fallow';

export const cropName = (id: string) =>
  id === FALLOW_ID ? 'Descanso (barbecho)' : CROPS.find((c) => c.id === id)?.name ?? id;

export const SEASON_LABEL: Record<Season, string> = {
  autumn: 'Otoño', winter: 'Invierno', spring: 'Primavera', summer: 'Verano',
};

export const SEASON_BG: Record<Season, string> = {
  autumn: 'bg-clay-100', winter: 'bg-sky-50', spring: 'bg-leaf-50', summer: 'bg-sun-100',
};