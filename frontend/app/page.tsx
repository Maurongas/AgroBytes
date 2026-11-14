"use client";
import { useState } from "react";

export default function Home() {
  const [temp, setTemp] = useState("");
  const [rain, setRain] = useState("");
  const [soil, setSoil] = useState("arcilloso");
  const [resultado, setResultado] = useState([]); // Cambiamos a un arreglo vacío

  const obtenerRecomendacion = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const peticion = {
      avg_temp: parseFloat(temp),
      rainfall_mm: parseFloat(rain),
      soil_type: soil
    };

    try {
      const res = await fetch("http://localhost:8000/api/v1/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(peticion),
      });
      const data = await res.json();
      // ¡Aquí está la magia! Leemos la variable exacta que manda tu backend
      setResultado(data.recomendaciones || []);
    } catch (error) {
      console.error("Error conectando al backend:", error);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-8 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold text-blue-500 mb-8 mt-10">🚀 NASA Space Apps - IA Agrícola</h1>
      
      <form onSubmit={obtenerRecomendacion} className="flex flex-col gap-4 bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Temperatura Promedio (°C)</label>
          <input type="number" step="0.1" value={temp} onChange={(e) => setTemp(e.target.value)} required className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600 focus:border-blue-500 outline-none" />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Lluvia Anual (mm)</label>
          <input type="number" step="0.1" value={rain} onChange={(e) => setRain(e.target.value)} required className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600 focus:border-blue-500 outline-none" />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Tipo de Suelo</label>
          <select value={soil} onChange={(e) => setSoil(e.target.value)} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600 focus:border-blue-500 outline-none">
            <option value="Arcilloso">Arcilloso</option>
            <option value="Arenoso">Arenoso</option>
            <option value="Limoso">Limoso</option>
          </select>
        </div>
        <button type="submit" className="mt-4 bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition-colors">
          Obtener Recomendación
        </button>
      </form>

      {/* Sección de resultados dinámicos */}
      {resultado.length > 0 && (
        <div className="mt-8 bg-gray-800 border border-green-500 p-6 rounded-lg w-full max-w-md">
          <h2 className="text-xl text-green-400 font-bold mb-4 text-center">✅ Resultados del Análisis</h2>
          <ul className="space-y-4">
            {resultado.map((item: any, index: number) => (
              <li key={index} className="bg-gray-700 p-4 rounded-md border border-gray-600">
                <h3 className="text-lg font-bold text-blue-300">🌱 {item.cultivo}</h3>
                <p className="text-sm text-gray-300 mt-2">{item.razon}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}