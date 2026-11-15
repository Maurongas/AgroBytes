import { useSyncExternalStore } from 'react';
import type { AnalysisResponse, AnalysisSummary, Priority } from '../api/types';

const K_ULTIMA = 'fieldshift:ultima';
const K_HISTORIAL = 'fieldshift:historial';
const K_ANALISIS = 'fieldshift:analisis';
const MAX_ANALISIS = 5; // cuántos análisis completos se guardan

export interface Ultima {
  analysis: AnalysisResponse;
  crop: string | null;
  priority: Priority | null;
  guardadoEn: string;
}

// localStorage puede fallar (modo privado, sin espacio): todo va en try/catch y la app funciona igual.
function leer<T>(clave: string): T | null {
  try {
    const crudo = localStorage.getItem(clave);
    return crudo ? (JSON.parse(crudo) as T) : null;
  } catch {
    return null;
  }
}

function guardar(clave: string, valor: unknown): void {
  try {
    localStorage.setItem(clave, JSON.stringify(valor));
  } catch {
    /* sin espacio o bloqueado: se ignora */
  }
}

export function guardarUltima(u: Omit<Ultima, 'guardadoEn'>): void {
  guardar(K_ULTIMA, { ...u, guardadoEn: new Date().toISOString() });
}
export const leerUltima = () => leer<Ultima>(K_ULTIMA);

export function guardarHistorial(filas: AnalysisSummary[]): void {
  guardar(K_HISTORIAL, filas);
}
export const leerHistorial = () => leer<AnalysisSummary[]>(K_HISTORIAL);

/** Guarda un análisis completo por id y conserva solo los últimos MAX_ANALISIS. */
export function guardarAnalisis(a: AnalysisResponse): void {
  const todos = leer<Record<string, AnalysisResponse>>(K_ANALISIS) ?? {};
  delete todos[a.id]; // se vuelve a insertar al final = el más reciente
  todos[a.id] = a;
  const ids = Object.keys(todos);
  for (const viejo of ids.slice(0, Math.max(0, ids.length - MAX_ANALISIS))) delete todos[viejo];
  guardar(K_ANALISIS, todos);
}
export const leerAnalisis = (id: string) => leer<Record<string, AnalysisResponse>>(K_ANALISIS)?.[id] ?? null;

// --- ¿hay red? ---
function suscribir(avisar: () => void) {
  window.addEventListener('online', avisar);
  window.addEventListener('offline', avisar);
  return () => {
    window.removeEventListener('online', avisar);
    window.removeEventListener('offline', avisar);
  };
}

/** true si el navegador cree tener red. (No garantiza que el servidor responda: eso lo avisa el cliente de la API.) */
export function useOnline(): boolean {
  return useSyncExternalStore(suscribir, () => navigator.onLine, () => true);
}
