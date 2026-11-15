import * as turf from '@turf/turf';
import type { LatLng } from '../store/useStore';

/** Rectángulo a partir de dos esquinas opuestas. Devuelve 4 puntos [lat, lng]. */
export function rectanguloDesdeEsquinas(a: LatLng, b: LatLng): LatLng[] {
  return [a, [a[0], b[1]], b, [b[0], a[1]]];
}

/** true si los lados del polígono se cruzan entre sí. */
export function seCruza(puntos: LatLng[]): boolean {
  if (puntos.length < 4) return false; // un triángulo no puede cruzarse
  const anillo = puntos.map(([lat, lng]) => [lng, lat]);
  anillo.push(anillo[0]);
  return turf.kinks(turf.polygon([anillo])).features.length > 0;
}
