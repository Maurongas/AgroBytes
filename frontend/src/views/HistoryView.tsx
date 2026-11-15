import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { listAnalyses, getAnalysis } from '../api/client';
import type { AnalysisResponse, AnalysisSummary } from '../api/types';
import { useStore } from '../store/useStore';
import { cropName } from '../lib/crops';
import { formatoFecha, formatoUbicacion, PRIORITY_LABEL } from '../lib/etiquetas';
import { guardarAnalisis, guardarHistorial, leerAnalisis, leerHistorial } from '../lib/offline';

// Intenta la API; si falla y hay historial guardado, usa ese.
async function cargarHistorial(): Promise<{ filas: AnalysisSummary[]; guardado: boolean }> {
  try {
    const filas = await listAnalyses();
    guardarHistorial(filas);
    return { filas, guardado: false };
  } catch (error) {
    const filas = leerHistorial();
    if (filas) return { filas, guardado: true };
    throw error;
  }
}

export default function HistoryView() {
  const goTo = useStore((s) => s.goTo);
  const [abriendo, setAbriendo] = useState<string | null>(null);
  const [errorAbrir, setErrorAbrir] = useState<string | null>(null);
  const { data, isPending, isError, error, refetch } = useQuery({
    queryKey: ['historial'],
    queryFn: cargarHistorial,
    retry: 1,
  });

  async function abrir(fila: AnalysisSummary) {
    setAbriendo(fila.id);
    setErrorAbrir(null);
    try {
      let analysis: AnalysisResponse | null;
      try {
        analysis = await getAnalysis(fila.id);
        guardarAnalisis(analysis);
      } catch {
        analysis = leerAnalisis(fila.id); // sin red: usa la copia del dispositivo
      }
      if (!analysis) {
        setErrorAbrir('Este análisis no está guardado en el dispositivo y no hay conexión con el servidor.');
        return;
      }
      useStore.setState({ analysis, crop: fila.currentCrop, priority: fila.priority, view: 'diagnosis' });
    } finally {
      setAbriendo(null);
    }
  }

  return (
    <div className="h-full overflow-auto p-6">
      <h1 className="font-display text-3xl font-semibold">Historial</h1>
      <p className="mt-1 text-sm text-ink-500">Tus análisis anteriores. Abre uno para ver sus resultados.</p>

      {isPending && <p className="mt-6 text-ink-500" role="status">Cargando historial…</p>}

      {isError && (
        <div className="mt-6 rounded-card border border-danger/40 bg-danger/10 p-4 text-sm text-ink-900" role="alert">
          <p>{error.message}</p>
          <button onClick={() => refetch()} className="mt-2 rounded-full bg-leaf-600 px-4 py-1.5 text-paper hover:bg-leaf-700">
            Reintentar
          </button>
        </div>
      )}

      {errorAbrir && (
        <p className="mt-4 rounded-xl bg-clay-100 p-3 text-sm text-ink-900" role="alert">{errorAbrir}</p>
      )}

      {data?.guardado && (
        <p className="mt-4 rounded-xl bg-sun-100 p-3 text-sm text-ink-900">
          No se pudo conectar: mostrando el historial guardado en este dispositivo.
        </p>
      )}

      {data && data.filas.length === 0 && (
        <div className="mt-8 text-center">
          <p className="text-ink-700">Aún no has analizado ninguna parcela.</p>
          <button onClick={() => goTo('select')} className="mt-3 rounded-full bg-leaf-600 px-5 py-2 text-sm font-medium text-paper hover:bg-leaf-700">
            Analizar una parcela
          </button>
        </div>
      )}

      {data && data.filas.length > 0 && (
        <>
          {/* Pantallas anchas: tabla. Si aun así no cabe, se desplaza a los lados en vez de cortarse. */}
          <div className="mt-6 hidden overflow-x-auto rounded-card border border-line bg-surface-raised shadow-card xl:block">
            <table className="w-full min-w-[760px] text-left text-sm">
              <thead className="bg-surface-sunken text-xs uppercase tracking-widest text-ink-500">
                <tr>
                  <th className="px-4 py-3">Fecha</th><th className="px-4 py-3">Ubicación</th><th className="px-4 py-3">Área</th>
                  <th className="px-4 py-3">Cultivo actual</th><th className="px-4 py-3">Prioridad</th>
                  <th className="px-4 py-3">Rotación</th><th className="px-4 py-3"><span className="sr-only">Abrir</span></th>
                </tr>
              </thead>
              <tbody>
                {data.filas.map((f) => (
                  <tr key={f.id} className="border-t border-line-soft">
                    <td className="px-4 py-3">{formatoFecha(f.createdAt)}</td>
                    <td className="px-4 py-3 font-mono text-xs">{formatoUbicacion(f.location)}</td>
                    <td className="px-4 py-3">{f.areaHa.toFixed(1)} ha</td>
                    <td className="px-4 py-3">{cropName(f.currentCrop)}</td>
                    <td className="px-4 py-3">{PRIORITY_LABEL[f.priority]}</td>
                    <td className="px-4 py-3">{f.rotationCrops.map(cropName).join(' · ')}</td>
                    <td className="px-4 py-3 text-right">
                      <button onClick={() => abrir(f)} disabled={abriendo !== null}
                        className="rounded-full border border-leaf-600 px-3 py-1 text-leaf-700 hover:bg-leaf-50 disabled:opacity-50">
                        {abriendo === f.id ? 'Abriendo…' : 'Abrir'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Celular, tableta y ventanas angostas: tarjetas (dos columnas cuando hay espacio) */}
          <ul className="mt-6 grid gap-3 sm:grid-cols-2 xl:hidden">
            {data.filas.map((f) => (
              <li key={f.id} className="flex flex-col rounded-card border border-line bg-surface-raised p-4 shadow-card">
                <p className="text-xs text-ink-500">{formatoFecha(f.createdAt)}</p>
                <p className="mt-1 font-display text-lg font-semibold">{cropName(f.currentCrop)} · {f.areaHa.toFixed(1)} ha</p>
                <p className="text-sm text-ink-700">{PRIORITY_LABEL[f.priority]}</p>
                <p className="mt-1 text-sm text-ink-700">Rotación: {f.rotationCrops.map(cropName).join(' · ')}</p>
                <p className="mb-auto mt-1 font-mono text-xs text-ink-500">{formatoUbicacion(f.location)}</p>
                <button onClick={() => abrir(f)} disabled={abriendo !== null}
                  className="mt-3 w-full rounded-full bg-leaf-600 py-2 text-sm font-medium text-paper disabled:opacity-50">
                  {abriendo === f.id ? 'Abriendo…' : 'Abrir resultados'}
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
