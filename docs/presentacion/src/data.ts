// Todo número que sale en pantalla o en el guion se calcula aquí a partir de mockAnalysis.
// Si el mock cambia, la presentación y las notas del orador cambian con él.
import { mockAnalysis } from '@app/api/mock';
import { liveAnalysis } from './live';
import type { NasaMetric, Strategy, StrategyId } from '@app/api/types';
import { METRIC_EN, SOIL_EN, STRATEGY_EN, STRATEGY_WHY_EN, UNCERTAINTY_EN, en, impactLabelEn } from './i18n';

/** Respuesta REAL del backend si respondió al abrir el deck (live.ts); si no, el mock de la app. */
export const analysis = liveAnalysis ?? mockAnalysis;
export const isLiveData = liveAnalysis !== null;

const STRATEGY_ORDER: StrategyId[] = ['current', 'water', 'nitrogen', 'yield'];
export const strategies: Strategy[] = [...(analysis.strategies ?? [])].sort(
  (a, b) => STRATEGY_ORDER.indexOf(a.id) - STRATEGY_ORDER.indexOf(b.id),
);
export const current = strategies.find((s) => s.isCurrent);
export const recommended = strategies.find((s) => s.isRecommended);

/** Puntaje de una estrategia = promedio de sus temporadas (igual que CompareView de la app). */
export const strategyScore = (s: Strategy) =>
  Math.round(s.steps.reduce((sum, r) => sum + r.score, 0) / (s.steps.length || 1));

/** Beneficios en inglés, calculados con los números (no traduciendo el texto). */
export function benefitsEn(s: Strategy): string[] {
  if (s.isCurrent || !current) return s.benefits.map(en);
  const out: string[] = [];
  const irr = current.irrigationMm - s.irrigationMm;
  if (irr > 0) out.push(`${irr} mm less irrigation`);
  const n = s.nitrogenKgHa - current.nitrogenKgHa;
  if (n > 0) out.push(`+${n} kg/ha nitrogen (estimated)`);
  if (s.soilHealth > current.soilHealth) out.push(`Soil health ${current.soilHealth} → ${s.soilHealth} (estimated)`);
  if (s.bareSeasons < current.bareSeasons) out.push('No bare seasons');
  return out;
}

export const strategyEn = (s: Strategy) => ({
  title: STRATEGY_EN[s.id] ?? s.title,
  why: STRATEGY_WHY_EN[s.id] ?? s.why,
  evidence: s.evidence.map(en),
  benefits: benefitsEn(s),
  risks: s.tradeoffs.map(en),
  score: strategyScore(s),
});

/** Métricas con etiquetas en inglés, listas para el NasaMetricCard real de la app. */
export const metricsEn: NasaMetric[] = analysis.metrics.map((m) => ({
  ...m,
  label: METRIC_EN[m.id] ?? m.label,
  meaning: en(m.meaning),
  unit: m.unit.replace('día', 'day'),
  source: m.source.replace('· demo', '· sample data'),
}));

export const impactEn = analysis.impact.map((i) => ({
  ...i,
  label: impactLabelEn(i.label, i.unit),
  estimated: /estimad/i.test(i.label),
}));

export const soil = analysis.soilDetected
  ? `${SOIL_EN[analysis.soilDetected.texture]}${analysis.soilDetected.ph != null ? ` · pH ${analysis.soilDetected.ph}` : ''}`
  : null;

export const uncertaintyEn = UNCERTAINTY_EN[analysis.uncertainty.level];

const nitroItem = analysis.impact.find((i) => /nitr/i.test(i.label));
const nitroDelta = nitroItem ? nitroItem.recommended - nitroItem.current : 0;
// Riego POR CICLO de cultivo: la rotación puede tener más ciclos que «seguir como hoy» (que deja temporadas sin
// cultivo), así que comparar el total confunde. El signo decide la palabra: nunca se dice "menos" si es "más".
const cycles = (s?: Strategy) => (s ? s.steps.filter((p) => p.cropId !== 'fallow').length : 0);
const perCycle = (s?: Strategy) => (s && cycles(s) > 0 ? s.irrigationMm / cycles(s) : 0);
const waterDelta = perCycle(current) > 0 ? Math.round((1 - perCycle(recommended) / perCycle(current)) * 100) : 0;

/** Valores que el guion puede citar ({{clave}} en content.ts). */
export const facts: Record<string, string | number> = {
  area: analysis.areaHa,
  soil: soil ?? 'unknown',
  soilNow: analysis.soilHealth.current,
  soilNew: analysis.soilHealth.recommended,
  waterPct: Math.abs(waterDelta),
  waterWord: waterDelta >= 0 ? 'less' : 'more',
  nitroGain: Math.abs(nitroDelta),
  nitroWord: nitroDelta >= 0 ? 'better' : 'worse',
  strategies: strategies.length,
  uncertainty: uncertaintyEn,
  checks: analysis.localChecks?.length ?? 0,
};

export const fill = (text: string) => text.replace(/\{\{(\w+)\}\}/g, (_, k: string) => String(facts[k] ?? `{{${k}}}`));
