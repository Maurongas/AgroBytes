"use client";
import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function HistorialPage() {
  const [historial, setHistorial] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/history')
      .then(res => res.json())
      .then(data => setHistorial(data))
      .catch(err => console.error("Error cargando historial:", err));
  }, []);

  return (
    <div className="p-8 max-w-4xl mx-auto text-white min-h-screen">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-green-500">Historial de Consultas</h1>
        <Link href="/" className="bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded transition">
          &larr; Nueva Consulta
        </Link>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-1 shadow-2xl overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-800 text-gray-300">
            <tr>
              <th className="p-4 font-semibold">Fecha</th>
              <th className="p-4 font-semibold">Temp (°C)</th>
              <th className="p-4 font-semibold">Lluvia (mm)</th>
              <th className="p-4 font-semibold">Suelo</th>
              <th className="p-4 font-semibold">Recomendación</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {historial.map((item: any) => (
              <tr key={item.id} className="hover:bg-gray-800/50 transition">
                <td className="p-4 text-gray-400">
                  {new Date(item.fecha_consulta).toLocaleString()}
                </td>
                <td className="p-4">{item.temperatura}</td>
                <td className="p-4">{item.lluvia}</td>
                <td className="p-4 capitalize">{item.tipo_suelo}</td>
                <td className="p-4 text-green-400 font-medium">{item.resultado_cultivos}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {historial.length === 0 && (
          <div className="p-8 text-center text-gray-500">
            Aún no hay consultas registradas.
          </div>
        )}
      </div>
    </div>
  );
}