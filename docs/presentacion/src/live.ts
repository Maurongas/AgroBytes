// Conexión EN VIVO con el backend de AgroBytes durante la presentación.
// - boot(): al abrir el deck pide GET /health y POST /api/v1/analyses?guardar=false con la parcela de la
//   presentación. Si responde, TODAS las diapositivas usan esa respuesta real (data.ts). Si no, usan el mock.
// - Cada petición queda en un registro (método, ruta, estado, ms, kB) que se ve en la ventana del prototipo.
// - whatIf(): el «¿Y si…?» llama a la API real con climateShift.
// URL del backend: VITE_PITCH_API o http://localhost:8000 (el backend debe permitir el origen :3001 en CORS).
import { useSyncExternalStore } from 'react';
import type { AnalysisRequest, AnalysisResponse, ClimateShift } from '@app/api/types';
import { FIELD } from './components/FieldMap';

export const API = (import.meta.env.VITE_PITCH_API as string | undefined) ?? 'http://localhost:8000';
export const API_HOST = API.replace(/^https?:\/\//, '');

export interface LogEntry {
  id: number;
  method: 'GET' | 'POST';
  path: string;
  status: number | 'ERR' | '…';
  ms?: number;
  kb?: number;
  note?: string;
}

let log: LogEntry[] = [];
let seq = 0;
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());
const update = (id: number, patch: Partial<LogEntry>) => {
  log = log.map((e) => (e.id === id ? { ...e, ...patch } : e));
  emit();
};

/** Registro de peticiones (más reciente al final), para React. */
export function useApiLog(): LogEntry[] {
  return useSyncExternalStore((cb) => { listeners.add(cb); return () => listeners.delete(cb); }, () => log);
}

/** fetch con cronómetro y registro. Lanza si falla o tarda más de `timeoutMs`. */
export async function call<T>(method: LogEntry['method'], path: string, body?: unknown, note?: string, timeoutMs = 25000): Promise<T> {
  const id = ++seq;
  log = [...log.slice(-30), { id, method, path, status: '…', note }];
  emit();
  const t0 = performance.now();
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(API + path, {
      method, signal: ctrl.signal,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
    const text = await res.text();
    update(id, { status: res.status, ms: Math.round(performance.now() - t0), kb: +(text.length / 1024).toFixed(1) });
    if (!res.ok) throw new Error(`${res.status}`);
    return JSON.parse(text) as T;
  } catch (e) {
    update(id, { status: 'ERR', ms: Math.round(performance.now() - t0) });
    throw e;
  } finally {
    clearTimeout(timer);
  }
}

/** La misma parcela que se dibuja en la diapositiva (valle de Mexicali), en GeoJSON [lon, lat]. */
const RING = [...FIELD, FIELD[0]].map(([lat, lon]) => [lon, lat]);
export const REQUEST: AnalysisRequest = {
  geometry: { type: 'Polygon', coordinates: [RING] },
  currentCrop: 'maize',
  priority: 'water',
} as AnalysisRequest;

const ANALYZE = '/api/v1/analyses?guardar=false';

/** Respuesta real del arranque (null = backend no disponible → mock). */
export let liveAnalysis: AnalysisResponse | null = null;

export async function boot(): Promise<AnalysisResponse | null> {
  try {
    await call('GET', '/health', undefined, 'API + PostgreSQL', 4000);
    liveAnalysis = await call<AnalysisResponse>('POST', ANALYZE, REQUEST, 'NASA POWER + SoilGrids', 25000);
  } catch {
    liveAnalysis = null;
  }
  return liveAnalysis;
}

/** Vuelve a analizar la parcela (pestaña NASA data): muestra que la llamada es real y cuánto tarda. */
export const analyzeAgain = () => call<AnalysisResponse>('POST', ANALYZE, REQUEST, 'NASA POWER + SoilGrids');

/** «¿Y si…?» real: el backend recalcula la rotación con el clima modificado. */
export const whatIf = (shift: ClimateShift) =>
  call<AnalysisResponse>('POST', ANALYZE, { ...REQUEST, climateShift: shift }, `climateShift ${shift.rainPct > 0 ? '+' : ''}${shift.rainPct}% · ${shift.tempC > 0 ? '+' : ''}${shift.tempC} °C`);

export const isLive = () => liveAnalysis !== null;
