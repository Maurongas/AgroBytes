export const MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'] as const;

/**
 * Convierte una ventana como "Sep – Oct" o "Nov – Feb" en índices de mes (0 = enero).
 * Si el texto no se entiende devuelve [] y la vista solo muestra el texto.
 */
export function mesesDeVentana(ventana: string): number[] {
  const palabras = ventana.match(/[A-Za-zÁÉÍÓÚáéíóúñÑ]{3}/g) ?? [];
  const indices = palabras
    .map((p) => MESES.findIndex((m) => m.toLowerCase() === p.toLowerCase()))
    .filter((i) => i >= 0);
  if (indices.length === 0) return [];
  const inicio = indices[0];
  const fin = indices[indices.length - 1];
  const meses: number[] = [];
  for (let m = inicio; ; m = (m + 1) % 12) {   // da la vuelta al año si hace falta (Nov → Feb)
    meses.push(m);
    if (m === fin) break;
  }
  return meses;
}