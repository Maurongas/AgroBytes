"use client";
import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [formData, setFormData] = useState({
    ubicacion: '', // NUEVO CAMPO: Ubicación
    avg_temp: '',
    rainfall_mm: '',
    humedad_suelo_pct: '50',
    soil_type: 'arcilloso',
    cultivo_actual: '',
    disponibilidad_agua: 'media',
    prioridad_agricultor: 'conservar_agua'
  });
  const [resultado, setResultado] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          // Nota: Aún no enviamos 'ubicacion' al backend hasta actualizar los esquemas en el próximo paso
          avg_temp: parseFloat(formData.avg_temp),
          rainfall_mm: parseFloat(formData.rainfall_mm),
          humedad_suelo_pct: parseFloat(formData.humedad_suelo_pct),
          soil_type: formData.soil_type,
          cultivo_actual: formData.cultivo_actual || "ninguno",
          disponibilidad_agua: formData.disponibilidad_agua,
          prioridad_agricultor: formData.prioridad_agricultor
        })
      });
      const data = await res.json();
      setResultado(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-green-500">Sistema de Apoyo a la Decisión (DSS)</h1>
          <Link href="/historial" className="bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded transition border border-gray-600">
            Ver Historial
          </Link>
        </div>

        <form onSubmit={handleSubmit} className="bg-gray-800 p-6 rounded-xl shadow-lg grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 border border-gray-700">
          
          {/* NUEVA FILA: Ubicación Geoespacial */}
          <div className="md:col-span-3">
            <label className="block mb-2 text-sm text-gray-400">Ubicación / Coordenadas (Lat, Lon)</label>
            <input type="text" placeholder="Ej. Lat: 31.86, Lon: -116.60 (Ensenada, B.C.)" className="w-full p-2.5 rounded bg-gray-900 border border-gray-600 focus:border-green-500 outline-none text-blue-300 placeholder-gray-600"
              value={formData.ubicacion} onChange={e => setFormData({...formData, ubicacion: e.target.value})} />
          </div>

          {/* Fila 1: Datos Climáticos y Humedad */}
          <div>
            <label className="block mb-2 text-sm text-gray-400">Temp. Promedio (°C)</label>
            <input type="number" required className="w-full p-2.5 rounded bg-gray-900 border border-gray-600 focus:border-green-500 outline-none"
              value={formData.avg_temp} onChange={e => setFormData({...formData, avg_temp: e.target.value})} />
          </div>
          <div>
            <label className="block mb-2 text-sm text-gray-400">Lluvia Acumulada (mm)</label>
            <input type="number" required className="w-full p-2.5 rounded bg-gray-900 border border-gray-600 focus:border-green-500 outline-none"
              value={formData.rainfall_mm} onChange={e => setFormData({...formData, rainfall_mm: e.target.value})} />
          </div>
          <div>
            <label className="block mb-2 text-sm text-blue-400 font-semibold">Humedad del Suelo (%)</label>
            <input type="number" required className="w-full p-2.5 rounded bg-gray-900 border border-blue-500/50 focus:border-blue-400 outline-none"
              value={formData.humedad_suelo_pct} onChange={e => setFormData({...formData, humedad_suelo_pct: e.target.value})} />
          </div>

          {/* Fila 2: Suelo y Cultivo */}
          <div>
            <label className="block mb-2 text-sm text-gray-400">Tipo de Suelo</label>
            <select className="w-full p-2.5 rounded bg-gray-900 border border-gray-600 focus:border-green-500 outline-none"
              value={formData.soil_type} onChange={e => setFormData({...formData, soil_type: e.target.value})}>
              <option value="arcilloso">Arcilloso</option>
              <option value="arenoso">Arenoso</option>
              <option value="limoso">Limoso</option>
            </select>
          </div>
          <div className="md:col-span-2">
            <label className="block mb-2 text-sm text-gray-400">Cultivo Actual</label>
            <input type="text" required placeholder="Ej. Maíz, Trigo..." className="w-full p-2.5 rounded bg-gray-900 border border-gray-600 focus:border-green-500 outline-none"
              value={formData.cultivo_actual} onChange={e => setFormData({...formData, cultivo_actual: e.target.value})} />
          </div>

          {/* Fila 3: Restricciones */}
          <div>
            <label className="block mb-2 text-sm text-gray-400">Disponibilidad de Agua</label>
            <select className="w-full p-2.5 rounded bg-gray-900 border border-gray-600 focus:border-green-500 outline-none"
              value={formData.disponibilidad_agua} onChange={e => setFormData({...formData, disponibilidad_agua: e.target.value})}>
              <option value="alta">Alta (Riego abundante)</option>
              <option value="media">Media (Riego moderado)</option>
              <option value="baja">Baja (Escasa / Temporal)</option>
            </select>
          </div>
          <div className="md:col-span-2">
            <label className="block mb-2 text-sm text-gray-400">Prioridad Principal</label>
            <select className="w-full p-2.5 rounded bg-gray-900 border border-gray-600 focus:border-green-500 outline-none"
              value={formData.prioridad_agricultor} onChange={e => setFormData({...formData, prioridad_agricultor: e.target.value})}>
              <option value="conservar_agua">Conservar Agua</option>
              <option value="mejorar_suelo">Mejorar Salud del Suelo</option>
              <option value="ingresos_extra">Generar Ingresos Extra</option>
            </select>
          </div>

          {/* Botón y Créditos NASA */}
          <div className="md:col-span-3 mt-4">
            <p className="text-center text-xs text-gray-400 mb-4 tracking-wide">
              🛰️ Datos analizados basados en métricas de satélites de la NASA: <strong>SMAP</strong> (Humedad del Suelo) y <strong>GPM</strong> (Precipitación Global).
            </p>
            <button type="submit" disabled={loading} className="w-full bg-green-600 hover:bg-green-500 py-3.5 rounded font-bold text-lg transition shadow-lg flex justify-center items-center">
              {loading ? "Procesando Modelo Predictivo SI..." : "Ejecutar Análisis DSS"}
            </button>
          </div>
        </form>

        {/* Resultados */}
        {resultado && (
          <div className="space-y-6">
            
            <div className="bg-gray-800 border border-blue-900/50 p-5 rounded-xl flex flex-col md:flex-row justify-around items-center text-sm shadow-md">
              <div className="text-center mb-4 md:mb-0">
                <span className="text-gray-400 block mb-1">Confianza del Modelo (ML)</span>
                <span className="text-blue-400 font-bold text-2xl">{resultado.confianza_modelo_ml}</span>
              </div>
              <div className="hidden md:block w-px h-12 bg-gray-700"></div>
              <div className="text-center">
                <span className="text-gray-400 block mb-1">Margen de Incertidumbre</span>
                <span className="text-purple-400 font-bold text-2xl">{resultado.margen_incertidumbre}</span>
              </div>
            </div>
            
            <div className="flex flex-col items-center mb-6 text-center">
              <h2 className="text-2xl font-bold text-green-400">Escenarios de Rotación Proyectados</h2>
              {/* Refuerzo de la Ubicación en el resultado */}
              {formData.ubicacion && (
                <p className="text-blue-400 font-semibold mt-1">📍 Análisis para: {formData.ubicacion}</p>
              )}
              <p className="text-gray-400 text-sm mt-2 max-w-2xl italic">
                * Sistema DSS basado en evaluación de riesgos e incertidumbre de la humedad subsuperficial.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {resultado.recomendaciones.map((item: any, idx: number) => (
                <div key={idx} className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-md flex flex-col hover:border-gray-500 transition">
                  <span className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Estrategia {idx + 1}</span>
                  <h3 className="text-lg font-bold text-white mb-2 leading-tight">{item.estrategia}</h3>
                  <div className="mb-4">
                    <span className="bg-green-900/50 border border-green-500/50 text-green-300 text-sm font-medium px-3 py-1 rounded-full">
                      Cultivo: {item.cultivo}
                    </span>
                  </div>
                  <div className="flex-1 space-y-3 text-sm">
                    <p className="text-gray-300"><strong>Justificación:</strong> {item.justificacion}</p>
                    <p className="text-gray-300"><strong>Beneficios:</strong> {item.beneficios}</p>
                  </div>
                  <div className="mt-4 pt-4 border-t border-gray-700 space-y-3">
                    <p className="text-amber-400 text-sm"><strong>⚠️ Riesgos:</strong> {item.riesgos}</p>
                    <div className="bg-blue-900/20 border border-blue-800/50 p-3 rounded text-blue-300 text-sm">
                      <strong className="block mb-1">⚖️ Tradeoff (Compensación):</strong>
                      {item.tradeoff.split(': ')[1]}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}