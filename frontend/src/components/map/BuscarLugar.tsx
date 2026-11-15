import { useState, type FormEvent } from 'react';
import type L from 'leaflet';
import { LocateFixed, Search } from 'lucide-react';

interface Resultado { place_id: number; display_name: string; lat: string; lon: string }

/**
 * Buscar un lugar (Nominatim de OpenStreetMap: gratis y sin llave) y «Mi ubicación».
 * La política de Nominatim pide como máximo una búsqueda por segundo y solo cuando el usuario la manda:
 * por eso es un formulario con botón y no autocompletado.
 * Va fuera del <MapContainer> (en la columna de la barra de dibujo), así que los toques no llegan al mapa.
 */
export default function BuscarLugar({ map }: { map: L.Map | null }) {
  const [texto, setTexto] = useState('');
  const [resultados, setResultados] = useState<Resultado[]>([]);
  const [aviso, setAviso] = useState<string | null>(null);
  const [cargando, setCargando] = useState(false);
  const [ubicando, setUbicando] = useState(false);

  function ir(lat: number, lon: number) {
    map?.flyTo([lat, lon], 16, { duration: 1.2 });
    setResultados([]);
    setAviso(null);
  }

  async function buscar(e: FormEvent) {
    e.preventDefault();
    const q = texto.trim();
    if (q.length < 3) {
      setAviso('Escribe al menos 3 letras.');
      return;
    }
    setCargando(true);
    setAviso(null);
    try {
      // countrycodes: solo la región donde la app permite marcar parcelas (México, EE. UU. y Canadá).
      const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&limit=5&accept-language=es&countrycodes=mx,us,ca&q=${encodeURIComponent(q)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error();
      const datos = (await res.json()) as Resultado[];
      setResultados(datos);
      if (datos.length === 0) setAviso('No encontramos ese lugar en México, EE. UU. o Canadá. Prueba con otro nombre.');
    } catch {
      setAviso('No se pudo buscar ahora. Revisa tu conexión.');
    } finally {
      setCargando(false);
    }
  }

  function miUbicacion() {
    if (!('geolocation' in navigator)) {
      setAviso('Tu navegador no permite obtener la ubicación.');
      return;
    }
    setUbicando(true);
    navigator.geolocation.getCurrentPosition(
      (p) => {
        setUbicando(false);
        ir(p.coords.latitude, p.coords.longitude);
      },
      () => {
        setUbicando(false);
        setAviso('No pudimos obtener tu ubicación. Revisa el permiso del navegador.');
      },
      { enableHighAccuracy: true, timeout: 10000 },
    );
  }

  return (
    <div className="w-full max-w-sm">
      <form onSubmit={buscar} className="flex gap-2" role="search">
        <input value={texto} onChange={(e) => setTexto(e.target.value)} aria-label="Buscar lugar o dirección"
          placeholder="Buscar lugar o dirección" enterKeyHint="search"
          className="min-w-0 flex-1 rounded-full border border-line bg-surface-raised px-4 py-2 text-sm text-ink-900 shadow-card focus-visible:outline-2 focus-visible:outline-leaf-600" />
        <button type="submit" disabled={cargando} aria-label="Buscar"
          className="flex min-h-11 min-w-11 items-center justify-center rounded-full bg-leaf-600 text-paper hover:bg-leaf-700 disabled:opacity-50">
          <Search size={18} aria-hidden />
        </button>
        <button type="button" onClick={miUbicacion} disabled={ubicando} aria-label="Mi ubicación"
          className="flex min-h-11 min-w-11 items-center justify-center rounded-full border border-line bg-surface-raised text-ink-700 shadow-card hover:bg-surface-sunken disabled:opacity-50">
          <LocateFixed size={18} aria-hidden className={ubicando ? 'animate-pulse' : ''} />
        </button>
      </form>
      {aviso && <p className="mt-2 rounded-xl bg-surface-raised px-3 py-2 text-xs text-ink-700 shadow-card" role="status">{aviso}</p>}
      {resultados.length > 0 && (
        <ul className="mt-2 overflow-hidden rounded-2xl border border-line bg-surface-raised shadow-lift">
          {resultados.map((r) => (
            <li key={r.place_id}>
              <button type="button" onClick={() => ir(Number(r.lat), Number(r.lon))}
                className="block w-full px-4 py-2.5 text-left text-sm text-ink-900 hover:bg-leaf-50">
                {r.display_name}
              </button>
            </li>
          ))}
          <li className="px-4 py-1.5 text-[11px] text-ink-500">Búsqueda: Nominatim, © colaboradores de OpenStreetMap</li>
        </ul>
      )}
    </div>
  );
}
