"use client";
import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Historial() {
  const [historial, setHistorial] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/history')
      .then(res => res.json())
      .then(data => {
        setHistorial(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-green-500">Historial de Consultas DSS</h1>
          <Link href="/" className="bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded transition border border-gray-600">
            ← Nueva Consulta
          </Link>
        </div>

        {loading ? (
          <p className="text-gray-400">Cargando datos de satélite...</p>
        ) : (
          <div className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-900/50 border-b border-gray-700 text-sm text-gray-400 uppercase">
                  <th className="p-4">Fecha</th>
                  <th className="p-4">Ubicación</th>
                  <th className="p-4">Temp (°C)</th>
                  <th className="p-4">Lluvia (mm)</th>
                  <th className="p-4 text-blue-400">Humedad (%)</th>
                  <th className="p-4">Suelo</th>
                  <th className="p-4">Recomendación Proyectada</th>
                </tr>
              </thead>
              <tbody>
                {historial.map((item: any) => (
                  <tr key={item.id} className="border-b border-gray-700/50 hover:bg-gray-700/30 transition text-sm">
                    <td className="p-4 text-gray-400">
                      {new Date(item.fecha_consulta).toLocaleString()}
                    </td>
                    <td className="p-4 text-gray-300 font-medium">{item.ubicacion}</td>
                    <td className="p-4 text-center">{item.temperatura}</td>
                    <td className="p-4 text-center">{item.lluvia}</td>
                    <td className="p-4 text-center text-blue-300 font-bold">{item.humedad_suelo}</td>
                    <td className="p-4 capitalize">{item.tipo_suelo}</td>
                    <td className="p-4 text-green-400">{item.resultado_cultivos}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {historial.length === 0 && (
              <div className="p-8 text-center text-gray-500">
                Aún no hay registros en la base de datos.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}