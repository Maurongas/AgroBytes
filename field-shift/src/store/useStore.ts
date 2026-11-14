import { create } from 'zustand';
import * as turf from '@turf/turf';
import type { AnalysisResponse, Priority, Soil } from '../api/types';

export type LatLng = [number, number]; // Leaflet usa [latitud, longitud]

interface State {
  view: 'select' | 'diagnosis';
  drawing: boolean;
  points: LatLng[];
  geometry: GeoJSON.Polygon | null;
  areaHa: number | null;
  crop: string | null;
  priority: Priority | null;
  soil: Soil | null;
  analysis: AnalysisResponse | null;
  startDrawing: () => void;
  addPoint: (p: LatLng) => void;
  finishDrawing: () => void;
  clearParcel: () => void;
  setCrop: (c: string) => void;
  setPriority: (p: Priority) => void;
  setSoil: (s: Soil | null) => void;
  setAnalysis: (a: AnalysisResponse) => void;
  backToSelect: () => void;
}

export const useStore = create<State>((set, get) => ({
  view: 'select',
  drawing: false,
  points: [],
  geometry: null,
  areaHa: null,
  crop: null,
  priority: null,
  soil: null,
  analysis: null,

  startDrawing: () => set({ drawing: true, points: [], geometry: null, areaHa: null }),
  addPoint: (p) => set((s) => ({ points: [...s.points, p] })),

  finishDrawing: () => {
    const { points } = get();
    if (points.length < 3) return;
    // GeoJSON usa [longitud, latitud]: hay que invertir el orden
    const ring = points.map(([lat, lng]) => [lng, lat]);
    ring.push(ring[0]); // el polígono debe cerrarse
    const geometry: GeoJSON.Polygon = { type: 'Polygon', coordinates: [ring] };
    const areaHa = turf.area({ type: 'Feature', properties: {}, geometry }) / 10000;
    set({ drawing: false, geometry, areaHa });
  },

  clearParcel: () => set({ drawing: false, points: [], geometry: null, areaHa: null }),
  setCrop: (crop) => set({ crop }),
  setPriority: (priority) => set({ priority }),
  setSoil: (soil) => set({ soil }),
  setAnalysis: (analysis) => set({ analysis }),
  backToSelect: () => set({ view: 'select' }),
}));