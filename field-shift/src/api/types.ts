export type Priority = 'water' | 'nitrogen' | 'yield';
export type Season = 'autumn' | 'winter' | 'spring' | 'summer';
export type Status = 'ok' | 'warn' | 'danger';

export interface Soil {
  texture: 'sandy' | 'loam' | 'clay';
  ph?: number;
  organicMatter?: 'low' | 'mid' | 'high';
}

// Lo que el frontend envía
export interface AnalysisRequest {
  geometry: GeoJSON.Polygon; // coordenadas en orden [longitud, latitud]
  currentCrop: string;       // id del catálogo, ej. 'maize'
  priority: Priority;
  soil?: Soil;
}

export interface NasaMetric {
  id: 'soilMoisture' | 'rain90d' | 'tempMean' | 'solarRadiation' | 'ndvi';
  label: string;
  value: number;
  unit: string;
  status: Status;
  meaning: string;   // «Algo seco para maíz»
  series: number[];  // 12 valores mensuales para el sparkline
  source: string;    // «NASA POWER · 2026-11-12»
}

export interface RotationStep {
  season: Season;
  cropId: string;
  score: number;            // 0-100
  reasons: string[];
  waterSavingPct: number;
  nitrogenDelta: number;    // kg/ha, positivo = aporta
  risks: string[];
  plantingWindow: string;   // «Sep – Oct»
}

export interface ImpactItem {
  label: string;
  unit: string;
  current: number;
  recommended: number;
  betterWhen: 'higher' | 'lower';
}

// Lo que el backend responde
export interface AnalysisResponse {
  id: string;
  areaHa: number;
  metrics: NasaMetric[];
  rotation: RotationStep[]; // ordenado por temporada del ciclo
  impact: ImpactItem[];
  soilHealth: { current: number; recommended: number }; // 0-100
  climate: { month: string; rain: number; temp: number }[]; // 12 meses
}