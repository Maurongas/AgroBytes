import type { Priority, SoilTexture } from '../api/types';

export const PRIORITY_LABEL: Record<Priority, string> = {
  water: 'Ahorrar agua',
  nitrogen: 'Regenerar nitrógeno',
  yield: 'Maximizar rendimiento',
};

export const formatoFecha = (iso: string) =>
  new Date(iso).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' });

export const formatoUbicacion = (l: { lat: number; lon: number }) => `${l.lat.toFixed(3)}, ${l.lon.toFixed(3)}`;

export const TEXTURA_LABEL: Record<SoilTexture, string> = {
  sandy: 'Arenoso',
  loam: 'Franco',
  clay: 'Arcilloso',
};
