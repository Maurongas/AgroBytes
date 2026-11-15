// «¿Y si…?» simulado en el cliente para el prototipo (sin backend).
// TODO: con backend, llamar previewAnalysis(...) de @app/api/client con climateShift { rainPct, tempC }
//       (contrato v2.2, guardar=false) y usar su `rotation`; este archivo deja de hacer falta.
import type { Season } from '@app/api/types';
import { analysis, recommended, strategies } from '../data';

export interface Shift { rainPct: number; tempC: number }
export interface ScenarioStep { season: Season; cropId: string; score: number; irrigationMm: number }

/** Puntaje y riego base de cada cultivo: los del mock (la recomendada manda); barley no está en el mock. */
const BASE: Record<string, { score: number; irrigationMm: number }> = {};
const ordered = [...strategies].sort((a, b) => Number(b.isRecommended) - Number(a.isRecommended));
for (const s of ordered) {
  for (const st of s.steps) {
    if (st.cropId !== 'fallow' && !BASE[st.cropId]) BASE[st.cropId] = { score: st.score, irrigationMm: st.irrigationMm };
  }
}
BASE.barley ??= { score: 80, irrigationMm: 70 };
BASE.pea ??= { score: 78, irrigationMm: 110 };

const clamp01 = (n: number) => Math.max(0, Math.min(1, n));

/**
 * 3 escenarios precalculados (normal · seco · caluroso) mezclados según los sliders:
 * el cultivo cambia al cruzar un umbral; puntaje y riego se interpolan.
 */
export function scenario({ rainPct, tempC }: Shift): ScenarioStep[] {
  const dry = clamp01(-rainPct / 60);
  const wet = clamp01(rainPct / 60);
  const hot = clamp01(tempC / 5);
  const cold = clamp01(-tempC / 3);
  const normal = recommended?.steps ?? analysis.rotation;

  return normal.map((st) => {
    let cropId = st.cropId;
    if (st.season === 'autumn') cropId = dry > 0.25 ? 'chickpea' : cold > 0.5 ? 'pea' : st.cropId;
    if (st.season === 'winter') cropId = hot > 0.25 ? 'barley' : wet > 0.4 ? 'wheat' : st.cropId;
    if (st.season === 'summer') cropId = dry > 0.6 && hot > 0.5 ? 'fallow' : wet > 0.4 ? 'maize' : st.cropId;
    if (cropId === 'fallow') return { season: st.season, cropId, score: 0, irrigationMm: 0 };
    const b = BASE[cropId] ?? { score: st.score, irrigationMm: st.irrigationMm };
    const score = Math.round(b.score * (1 - 0.16 * dry - 0.12 * hot - 0.08 * cold + 0.04 * wet));
    const irrigationMm = Math.round(b.irrigationMm * (1 + 0.9 * dry - 0.5 * wet + 0.06 * tempC));
    return { season: st.season, cropId, score, irrigationMm: Math.max(0, irrigationMm) };
  });
}

/** Clima de la parcela con el cambio aplicado (lluvia en %, temperatura en °C). */
export const shiftedClimate = ({ rainPct, tempC }: Shift) =>
  analysis.climate.map((c) => ({ ...c, rain: Math.round(c.rain * (1 + rainPct / 100)), temp: +(c.temp + tempC).toFixed(1) }));

export const RAIN_MAX = Math.ceil(Math.max(...analysis.climate.map((c) => c.rain)) * 1.6 / 10) * 10;
export const TEMP_RANGE: [number, number] = [
  Math.floor(Math.min(...analysis.climate.map((c) => c.temp)) - 4),
  Math.ceil(Math.max(...analysis.climate.map((c) => c.temp)) + 6),
];
