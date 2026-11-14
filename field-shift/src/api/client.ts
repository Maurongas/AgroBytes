import type { AnalysisRequest, AnalysisResponse } from './types';
import { mockAnalysis } from './mock';

const BASE = import.meta.env.VITE_API_URL as string | undefined;
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

export async function createAnalysis(req: AnalysisRequest): Promise<AnalysisResponse> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 2600)); // simula la espera y deja ver la animación de escaneo
    return mockAnalysis;
  }
  const res = await fetch(`${BASE}/api/analyses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.message ?? `Error ${res.status}`);
  }
  return res.json();
}