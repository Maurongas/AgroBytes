import type { ReactNode } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import type { LatLng } from '@app/store/useStore';

/**
 * Parcela de ejemplo (~8.4 ha). Las coordenadas del mock caen en la zona urbana de Ensenada, así que la
 * imagen usa campos de cultivo del valle de Mexicali (como el 2.º análisis de mockHistory). Los datos que se muestran
 * (área, clima, suelo) siguen saliendo de mockAnalysis; cambia SPOT si quieres otra vista.
 */
const SPOT = { lat: 32.55, lon: -115.25 };
const { lat, lon } = SPOT;
const OFFSETS: [number, number][] = [
  [0.001221, -0.00176], [0.001346, 0.001449], [-0.000414, 0.001863], [-0.001242, 0.000103], [-0.000983, -0.001915],
];
export const FIELD: LatLng[] = OFFSETS.map(([dy, dx]) => [lat + dy, lon + dx]);
export const FIELD_CENTER: LatLng = [lat, lon];

/** Mismas teselas que ParcelMap de la app (Esri World Imagery). Sin internet se ve el fondo de respaldo. */
export const TILE_URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';

export default function FieldMap({ center = FIELD_CENTER, zoom = 16, children }: { center?: LatLng; zoom?: number; children?: ReactNode }) {
  return (
    <div className="map-fallback absolute inset-0">
      <MapContainer center={center} zoom={zoom} zoomControl={false} dragging={false} scrollWheelZoom={false}
        doubleClickZoom={false} touchZoom={false} keyboard={false} boxZoom={false} zoomSnap={0}
        className="h-full w-full">
        <TileLayer url={TILE_URL} attribution="Tiles © Esri" />
        {children}
      </MapContainer>
    </div>
  );
}
