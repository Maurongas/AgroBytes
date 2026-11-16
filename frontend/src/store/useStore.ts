import { create } from 'zustand';
import * as turf from '@turf/turf';
import type { AnalysisResponse, Priority, Soil } from '../api/types';
import { regionName, pointInRegion, validateParcel } from '../lib/region';
import { tr } from '../lib/i18n';

export type LatLng = [number, number]; // Leaflet usa [latitud, longitud]

function toPolygon(points: LatLng[]): GeoJSON.Polygon {
  // GeoJSON usa [longitud, latitud]: hay que invertir el orden
  const ring = points.map(([lat, lng]) => [lng, lat]);
  ring.push(ring[0]); // el polígono debe cerrarse
  return { type: 'Polygon', coordinates: [ring] };
}

/** Área en hectáreas de los puntos marcados (≥ 3). */
export function polygonAreaHa(points: LatLng[]): number {
  return turf.area({ type: 'Feature', properties: {}, geometry: toPolygon(points) }) / 10000;
}
export type ViewId = 'select' | 'diagnosis' | 'history' | 'alerts' | 'calendar' | 'compare' | 'account';

interface State {
  view: ViewId;
  goTo: (v: ViewId) => void;
  drawing: boolean;
  points: LatLng[];
  geometry: GeoJSON.Polygon | null;
  areaHa: number | null;
  /** Por qué la parcela dibujada no se acepta (fuera de la región, muy grande o muy pequeña). */
  parcelError: string | null;
  crop: string | null;
  priority: Priority | null;
  soil: Soil | null;
  irrigated: boolean;
  analysis: AnalysisResponse | null;
  startDrawing: () => void;
  addPoint: (p: LatLng) => void;
  finishDrawing: () => void;
  clearParcel: () => void;
  setCrop: (c: string) => void;
  setPriority: (p: Priority) => void;
  setSoil: (s: Soil | null) => void;
  setIrrigated: (v: boolean) => void;
  setAnalysis: (a: AnalysisResponse) => void;
  backToSelect: () => void;
}

export const useStore = create<State>((set, get) => ({
  view: 'select',
  goTo: (view) => set({ view }),
  drawing: false,
  points: [],
  geometry: null,
  areaHa: null,
  parcelError: null,
  crop: null,
  priority: null,
  soil: null,
  irrigated: false,
  analysis: null,

  startDrawing: () => set({ drawing: true, points: [], geometry: null, areaHa: null, parcelError: null }),
  addPoint: (p) => {
    if (!pointInRegion(p)) {
      set({ parcelError: tr(`Solo puedes marcar puntos dentro de ${regionName()}`, `You can only place points within ${regionName()}`) });
      return;
    }
    set((s) => ({ points: [...s.points, p], parcelError: null }));
  },

  finishDrawing: () => {
    const { points } = get();
    if (points.length < 3) return;
    const geometry = toPolygon(points);
    const areaHa = polygonAreaHa(points);
    const parcelError = validateParcel(points, areaHa);
    // Si no es válida se deja dibujada (en rojo) pero sin geometry, para que no se pueda analizar
    set({ drawing: false, geometry: parcelError ? null : geometry, areaHa, parcelError });
  },

  clearParcel: () => set({ drawing: false, points: [], geometry: null, areaHa: null, parcelError: null }),
  setCrop: (crop) => set({ crop }),
  setPriority: (priority) => set({ priority }),
  setSoil: (soil) => set({ soil }),
  setIrrigated: (irrigated) => set({ irrigated }),
  setAnalysis: (analysis) => set({ analysis }),
  backToSelect: () => set({ view: 'select' }),
}));