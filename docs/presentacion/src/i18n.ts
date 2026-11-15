// Traducción al inglés de lo que viene en español en mock.ts / lib/crops.ts.
// Regla: si falta una traducción se muestra el texto original (nunca se rompe la diapositiva).
// Si el mock cambia de textos, añade la frase aquí o crea un patrón en PATTERNS.
import type { NasaMetric, Season, SoilTexture, StrategyId } from '@app/api/types';

export const CROP_EN: Record<string, string> = {
  maize: 'Maize', sorghum: 'Sorghum', wheat: 'Wheat', barley: 'Barley', oat: 'Oat', bean: 'Bean',
  soy: 'Soy', chickpea: 'Chickpea', pea: 'Pea', vetch: 'Vetch', canola: 'Canola', safflower: 'Safflower',
  cotton: 'Cotton', tomato: 'Tomato', chile: 'Chili', potato: 'Potato', onion: 'Onion', squash: 'Squash',
  fallow: 'Bare soil',
};
export const cropEn = (id: string) => CROP_EN[id] ?? id;

const CROP_ES_TO_ID: Record<string, string> = {
  'maíz': 'maize', sorgo: 'sorghum', trigo: 'wheat', cebada: 'barley', avena: 'oat', frijol: 'bean',
  soya: 'soy', garbanzo: 'chickpea', 'chícharo': 'pea', veza: 'vetch', canola: 'canola', 'cártamo': 'safflower',
  'algodón': 'cotton', jitomate: 'tomato', chile: 'chile', papa: 'potato', cebolla: 'onion', calabaza: 'squash',
};

export const SEASON_EN: Record<Season, string> = {
  autumn: 'Autumn', winter: 'Winter', spring: 'Spring', summer: 'Summer',
};
const SEASON_ES: Record<string, string> = { 'otoño': 'autumn', invierno: 'winter', primavera: 'spring', verano: 'summer' };

/** Meses (0 = enero) de cada temporada del ciclo — misma convención que el calendario de la app. */
export const SEASON_MONTHS: Record<Season, number[]> = {
  autumn: [8, 9, 10], winter: [11, 0, 1], spring: [2, 3, 4], summer: [5, 6, 7],
};
export const MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export const SOIL_EN: Record<SoilTexture, string> = { sandy: 'sandy', loam: 'loam', clay: 'clay' };

export const STRATEGY_EN: Record<StrategyId, string> = {
  current: 'Keep as today', water: 'Save water', nitrogen: 'Regenerate soil', yield: 'Boost yield',
};
export const STRATEGY_WHY_EN: Record<StrategyId, string> = {
  current: 'Your current crop where the climate allows it; rest in the other seasons.',
  water: 'Each season, the crop that needs the least water among those the climate allows.',
  nitrogen: 'More legumes and cover crops, which return nitrogen and protect the soil.',
  yield: 'More weight to the highest-value crops the climate allows.',
};

export const METRIC_EN: Record<NasaMetric['id'], string> = {
  soilMoisture: 'Soil moisture', rain90d: 'Rain · 90 days', tempMean: 'Temperature', solarRadiation: 'Sunlight',
};

export const UNCERTAINTY_EN = { low: 'low', medium: 'medium', high: 'high' } as const;

const PHRASES: Record<string, string> = {
  'Algo seco para maíz': 'A bit dry for corn',
  'Excelente para cultivos de sol': 'Great for sun-loving crops',
  'Sensible a heladas tempranas': 'Sensitive to early frost',
  'Requiere control de maleza temprano': 'Needs early weed control',
  'Rendimiento menor si falta lluvia en enero': 'Lower yield if January is dry',
  'Misma familia que el cultivo anterior (más riesgo de plagas)': 'Same family as last crop (more pest risk)',
  'Repite familia botánica: plagas y enfermedades se acumulan': 'Same crop family again: pests and diseases build up',
  '1 temporada sin cultivo: deja rastrojo o una cobertura para evitar erosión': '1 bare season: leave residue or a cover crop',
  'El garbanzo y la veza tienen menos mercado que el maíz en la zona': 'Chickpea and vetch have a smaller local market',
  'Usa casi la misma agua que hoy: depende del riego en verano': 'Almost the same water as today: relies on summer irrigation',
  'Ya conoces el cultivo, tienes el equipo y sabes dónde venderlo': 'You know the crop, have the gear and the buyers',
};

const PATTERNS: [RegExp, (...m: string[]) => string][] = [
  [/^(\d+(?:\.\d+)?) % menos que el promedio$/, (n) => `${n}% below average`],
  [/^(\d+(?:\.\d+)?) °C sobre lo normal$/, (n) => `${n} °C above normal`],
  [/^Requiere riego: la lluvia cubre ~(\d+) % de lo que necesita$/, (n) => `Needs irrigation: rain covers ~${n}%`],
  [/^(.+?), (otoño|invierno|primavera|verano): necesita ~(\d+) mm y la lluvia aporta ~(\d+) mm \(FAO-56 con clima de NASA POWER\)$/,
    (crop, season, need, rain) => {
      const id = CROP_ES_TO_ID[crop.toLowerCase()];
      const s = SEASON_ES[season] as Season | undefined;
      return `${id ? cropEn(id) : crop}, ${s ? SEASON_EN[s].toLowerCase() : season}: needs ~${need} mm, rain gives ~${rain} mm (FAO-56 · NASA POWER)`;
    }],
];

/** Traduce una frase del mock; si no la conoce, la devuelve tal cual. */
export function en(text: string): string {
  if (PHRASES[text]) return PHRASES[text];
  for (const [re, fn] of PATTERNS) {
    const m = text.match(re);
    if (m) return fn(...m.slice(1));
  }
  return text;
}

/** Etiqueta en inglés de cada indicador de impacto (por su unidad/sentido; el texto del mock puede cambiar). */
export function impactLabelEn(label: string, unit: string): string {
  const l = label.toLowerCase();
  if (l.includes('nitr')) return 'Nitrogen balance';
  if (l.includes('riego')) return 'Irrigation needed';
  if (l.includes('agua')) return 'Crop water use';
  return `${label} (${unit})`;
}
