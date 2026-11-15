// Región de trabajo (México, EE. UU. y Canadá) y tamaño permitido de la parcela.
// Espejo exacto de backend/app/services/region.py: mismo contorno (src/data/region.json, lo genera
// backend/research/build_region.py) y mismas constantes. El backend vuelve a validar y responde 422.
import type { LatLng } from '../store/useStore';
import type { CountryCode } from '../api/types';
import regionData from '../data/region.json';

export const REGION_NAME = 'México, Estados Unidos o Canadá';
export const MIN_AREA_HA = 0.1; // 1 000 m²
export const MAX_AREA_HA = 500; // 5 km²: más grande ya no comparte un solo clima/suelo
const EDGE_TOLERANCE_DEG = 0.05; // ~5 km: compensa la simplificación de la costa

type Ring = [number, number][]; // [longitud, latitud]
interface Country { code: CountryCode; name: string; rings: Ring[]; bboxes: [number, number, number, number][] }

const COUNTRIES: Country[] = Object.entries(regionData.countries).map(([code, c]) => {
  const rings = c.rings as Ring[];
  const bboxes = rings.map((r) => {
    const lons = r.map((p) => p[0]);
    const lats = r.map((p) => p[1]);
    return [Math.min(...lons), Math.min(...lats), Math.max(...lons), Math.max(...lats)] as [number, number, number, number];
  });
  return { code: code as CountryCode, name: c.name, rings, bboxes };
});

export const COUNTRY_NAME: Record<CountryCode, string> = { MX: 'México', US: 'Estados Unidos', CA: 'Canadá' };

/** Contornos de los países en formato Leaflet ([lat, lng]); para la máscara del mapa. */
export const REGION_LATLNGS: LatLng[][] = COUNTRIES.flatMap((c) => c.rings.map((r) => r.map(([lon, lat]) => [lat, lon] as LatLng)));

/** Límites para no sacar el mapa de Norteamérica (con margen). */
export const REGION_BOUNDS: [LatLng, LatLng] = [
  [12, -172],
  [84, -48],
];

function inRing(lon: number, lat: number, ring: Ring): boolean {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [x1, y1] = ring[j];
    const [x2, y2] = ring[i];
    if (y1 > lat !== y2 > lat && lon < x1 + ((lat - y1) * (x2 - x1)) / (y2 - y1)) inside = !inside;
  }
  return inside;
}

function distanceToRing(lon: number, lat: number, ring: Ring): number {
  let best = Infinity;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [x1, y1] = ring[j];
    const [x2, y2] = ring[i];
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len2 = dx * dx + dy * dy;
    const t = len2 === 0 ? 0 : Math.max(0, Math.min(1, ((lon - x1) * dx + (lat - y1) * dy) / len2));
    best = Math.min(best, Math.hypot(lon - (x1 + t * dx), lat - (y1 + t * dy)));
  }
  return best;
}

/** País que contiene el punto [lat, lng] (o el más cercano a menos de ~5 km). null = fuera de la región. */
export function countryOf([lat, lon]: LatLng): CountryCode | null {
  let nearest: CountryCode | null = null;
  let nearestD = EDGE_TOLERANCE_DEG;
  const t = EDGE_TOLERANCE_DEG;
  for (const c of COUNTRIES) {
    for (let k = 0; k < c.rings.length; k++) {
      const [x0, y0, x1, y1] = c.bboxes[k];
      if (lon < x0 - t || lon > x1 + t || lat < y0 - t || lat > y1 + t) continue;
      if (inRing(lon, lat, c.rings[k])) return c.code;
      const d = distanceToRing(lon, lat, c.rings[k]);
      if (d <= nearestD) {
        nearest = c.code;
        nearestD = d;
      }
    }
  }
  return nearest;
}

export const pointInRegion = (p: LatLng): boolean => countryOf(p) !== null;

/** Mensaje de error para el usuario, o null si la parcela es válida. */
export function validateParcel(points: LatLng[], areaHa: number): string | null {
  if (!points.every(pointInRegion)) return `La parcela debe estar completamente dentro de ${REGION_NAME}`;
  if (areaHa < MIN_AREA_HA) return `La parcela es muy pequeña (${areaHa.toFixed(2)} ha); el mínimo es ${MIN_AREA_HA} ha`;
  if (areaHa > MAX_AREA_HA)
    return `La parcela es muy grande (${Math.round(areaHa).toLocaleString('es-MX')} ha); el máximo es ${MAX_AREA_HA} ha. Divídela en parcelas más pequeñas`;
  return null;
}
