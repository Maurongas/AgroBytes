// Contrato de la API — espejo EXACTO de backend/app/schemas/ y de docs/ARQUITECTURA.md §5.
// Si cambias algo aquí, cambia también el backend y ARQUITECTURA.md en el mismo PR.

export type Priority = 'water' | 'nitrogen' | 'yield';
export type Season = 'autumn' | 'winter' | 'spring' | 'summer';
export type Status = 'ok' | 'warn' | 'danger';
export type SoilTexture = 'sandy' | 'loam' | 'clay';

export interface Soil {
  texture: SoilTexture;
  ph?: number;
  organicMatter?: 'low' | 'mid' | 'high';
}

// POST /api/v1/analyses — lo que el frontend envía
export interface AnalysisRequest {
  geometry: GeoJSON.Polygon; // coordenadas en orden [longitud, latitud]
  currentCrop: string;       // id del catálogo, ej. 'maize'
  priority: Priority;
  soil?: Soil;
}

// Todas las métricas salen de NASA POWER
export interface NasaMetric {
  id: 'soilMoisture' | 'rain90d' | 'tempMean' | 'solarRadiation';
  label: string;
  value: number;
  unit: string;
  status: Status;
  meaning: string;   // «Algo seco para maíz»
  series: number[];  // 12 valores mensuales para el sparkline
  source: string;    // «NASA POWER · 2015-2024»
}

export interface RotationStep {
  season: Season;
  cropId: string;
  score: number;            // 0-100
  reasons: string[];
  waterSavingPct: number;
  nitrogenDelta: number;    // kg/ha ESTIMADO por reglas, positivo = aporta
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

export interface Uncertainty {
  level: 'low' | 'medium' | 'high';
  reason: string;           // «La lluvia anual varía 38 % entre años»
}

// POST /api/v1/analyses y GET /api/v1/analyses/{id} — lo que el backend responde
export interface AnalysisResponse {
  id: string;
  createdAt: string;        // ISO 8601 UTC
  areaHa: number;
  location: { lat: number; lon: number }; // centroide de la parcela
  metrics: NasaMetric[];
  rotation: RotationStep[]; // ordenado por temporada del ciclo
  impact: ImpactItem[];
  soilHealth: { current: number; recommended: number }; // índice 0-100 ESTIMADO por reglas
  climate: { month: string; rain: number; temp: number }[]; // 12 meses
  uncertainty: Uncertainty;
}

// GET /api/v1/analyses — un renglón del historial
export interface AnalysisSummary {
  id: string;
  createdAt: string;
  location: { lat: number; lon: number };
  areaHa: number;
  currentCrop: string;
  priority: Priority;
  rotationCrops: string[];  // ids, ej. ['bean', 'oat', 'sorghum']
}
