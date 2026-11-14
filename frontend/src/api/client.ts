// Cliente único de la API: los componentes NO hacen fetch directo. Ver docs/ARQUITECTURA.md §5 y §9.
import type { AnalysisRequest, AnalysisResponse, AnalysisSummary } from './types';
import { mockAnalysis, mockHistory } from './mock';

const BASE = import.meta.env.VITE_API_URL as string | undefined;
// Si no hay API configurada (VITE_API_URL vacío) o VITE_USE_MOCK=true, usa datos de ejemplo.
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true' || !BASE;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...init?.headers },
    });
  } catch {
    throw new Error('No se pudo conectar con el servidor.');
  }
  if (!res.ok) {
    // El backend responde los errores como {"detail": "mensaje en español"}
    const body = await res.json().catch(() => null);
    const detail = typeof body?.detail === 'string' ? body.detail : `Error ${res.status}`;
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export async function createAnalysis(req: AnalysisRequest): Promise<AnalysisResponse> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 2600)); // simula la espera y deja ver la animación de escaneo
    return mockAnalysis;
  }
  return request<AnalysisResponse>('/api/v1/analyses', { method: 'POST', body: JSON.stringify(req) });
}

/** Historial (GET /api/v1/analyses). */
export async function listAnalyses(limit = 20): Promise<AnalysisSummary[]> {
  if (USE_MOCK) return mockHistory;
  return request<AnalysisSummary[]>(`/api/v1/analyses?limit=${limit}`);
}

/** Detalle de un análisis guardado (GET /api/v1/analyses/{id}). */
export async function getAnalysis(id: string): Promise<AnalysisResponse> {
  if (USE_MOCK) return mockAnalysis;
  return request<AnalysisResponse>(`/api/v1/analyses/${encodeURIComponent(id)}`);
}
