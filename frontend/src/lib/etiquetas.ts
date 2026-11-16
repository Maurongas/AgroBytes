import type { Priority, SoilTexture } from '../api/types';
import { locale, tr } from './i18n';

const PRIORITY: Record<Priority, [string, string]> = {
  water: ['Ahorrar agua', 'Save water'],
  nitrogen: ['Regenerar nitrógeno', 'Restore nitrogen'],
  yield: ['Maximizar rendimiento', 'Maximize yield'],
};
export const priorityLabel = (p: Priority) => tr(...PRIORITY[p]);

export const formatoFecha = (iso: string) =>
  new Date(iso).toLocaleString(locale(), { dateStyle: 'medium', timeStyle: 'short' });

export const formatoUbicacion = (l: { lat: number; lon: number }) => `${l.lat.toFixed(3)}, ${l.lon.toFixed(3)}`;

const TEXTURA: Record<SoilTexture, [string, string]> = {
  sandy: ['Arenoso', 'Sandy'],
  loam: ['Franco', 'Loam'],
  clay: ['Arcilloso', 'Clay'],
};
export const texturaLabel = (s: SoilTexture) => tr(...TEXTURA[s]);
