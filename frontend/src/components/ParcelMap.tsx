import { useEffect } from 'react';
import { MapContainer, TileLayer, Polygon, Polyline, CircleMarker, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { PenLine, Check, Trash2 } from 'lucide-react';
import { useStore } from '../store/useStore';

function ClickCapture() {
  const addPoint = useStore((s) => s.addPoint);
  const drawing = useStore((s) => s.drawing);
  useMapEvents({
    click(e) {
      if (drawing) addPoint([e.latlng.lat, e.latlng.lng]);
    },
  });
  return null;
}

function FlyToParcel() {
  const map = useMap();
  const geometry = useStore((s) => s.geometry);
  const points = useStore((s) => s.points);
  useEffect(() => {
    if (geometry && points.length >= 3) {
      map.flyToBounds(L.latLngBounds(points), { padding: [80, 80], duration: 1.1, easeLinearity: 0.2 });
    }
  }, [geometry]); // eslint-disable-line react-hooks/exhaustive-deps
  return null;
}

export default function ParcelMap() {
  const { drawing, points, geometry, areaHa, startDrawing, finishDrawing, clearParcel } = useStore();

  return (
    <div className={`relative h-full w-full ${drawing ? 'cursor-crosshair' : ''}`}>
      <MapContainer
        center={[31.8667, -116.5963]}
        zoom={13}
        doubleClickZoom={false}
        zoomControl={false}
        className="h-full w-full"
      >
        <TileLayer
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          attribution="Tiles © Esri"
        />
        <ClickCapture />
        <FlyToParcel />

        {drawing && points.length > 1 && (
          <Polyline positions={points} pathOptions={{ color: '#FFFFFF', weight: 2.5, dashArray: '6 6' }} />
        )}
        {drawing &&
          points.map((p, i) => (
            <CircleMarker key={i} center={p} radius={6}
              pathOptions={{ color: '#3F7D4A', weight: 2.5, fillColor: '#FFFFFF', fillOpacity: 1 }} />
          ))}
        {geometry && (
          <Polygon positions={points}
            pathOptions={{ color: '#FFFFFF', weight: 3, fillColor: '#3F7D4A', fillOpacity: 0.25 }} />
        )}
      </MapContainer>

      <div className="absolute left-4 top-4 z-[1000] flex gap-2 rounded-2xl border border-line bg-surface-raised p-1.5 shadow-card">
        <button onClick={startDrawing}
          className="flex items-center gap-2 rounded-xl bg-leaf-50 px-3 py-2 text-sm font-medium text-leaf-900 hover:bg-leaf-100">
          <PenLine size={16} /> {geometry ? 'Dibujar otra' : 'Dibujar parcela'}
        </button>
        {drawing && (
          <button onClick={finishDrawing} disabled={points.length < 3}
            className="flex items-center gap-2 rounded-xl bg-leaf-600 px-3 py-2 text-sm font-medium text-paper hover:bg-leaf-700 disabled:opacity-40">
            <Check size={16} /> Terminar
          </button>
        )}
        {(geometry || points.length > 0) && (
          <button onClick={clearParcel} aria-label="Borrar parcela"
            className="rounded-xl px-3 py-2 text-ink-500 hover:bg-canvas-subtle">
            <Trash2 size={16} />
          </button>
        )}
      </div>

      {drawing && (
        <div className="absolute bottom-6 left-1/2 z-[1000] -translate-x-1/2 rounded-full bg-orbit/80 px-4 py-2 text-sm text-paper">
          Haz clic en el mapa para marcar las esquinas ({points.length}) y pulsa «Terminar»
        </div>
      )}
      {geometry && areaHa && (
        <div className="absolute bottom-6 left-4 z-[1000] rounded-lg bg-orbit/80 px-3 py-1.5 font-mono text-xs text-paper">
          {areaHa.toFixed(1)} ha
        </div>
      )}
    </div>
  );
}