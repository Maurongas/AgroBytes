import { tr } from './i18n';

const MESES_ES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
const MESES_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** Abreviaturas de los meses en el idioma actual. */
export const meses = () => tr(MESES_ES.join(','), MESES_EN.join(',')).split(',');

/**
 * Convierte una ventana como "Sep – Oct" o "Nov – Feb" (en español o inglés) en índices de mes (0 = enero).
 * Si el texto no se entiende devuelve [] y la vista solo muestra el texto.
 */
export function mesesDeVentana(ventana: string): number[] {
  const palabras = ventana.match(/[A-Za-zÁÉÍÓÚáéíóúñÑ]{3}/g) ?? [];
  const indice = (p: string) => {
    const l = p.toLowerCase();
    const i = MESES_ES.findIndex((m) => m.toLowerCase() === l);
    return i >= 0 ? i : MESES_EN.findIndex((m) => m.toLowerCase() === l);
  };
  const indices = palabras.map(indice).filter((i) => i >= 0);
  if (indices.length === 0) return [];
  const inicio = indices[0];
  const fin = indices[indices.length - 1];
  const out: number[] = [];
  for (let m = inicio; ; m = (m + 1) % 12) {   // da la vuelta al año si hace falta (Nov → Feb)
    out.push(m);
    if (m === fin) break;
  }
  return out;
}
