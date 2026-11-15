import type { AnalysisResponse } from '../api/types';

type Mes = AnalysisResponse['climate'][number]; // { month, rain, temp }

export type RiesgoId = 'helada' | 'calor' | 'sequia' | 'lluvia';

export interface Riesgo {
  id: RiesgoId;
  titulo: string;
  detalle: string;      // la regla, en palabras
  nivel: 'medio' | 'alto';
  meses: string[];      // etiquetas tal como vienen en climate[].month
}

const REGLAS: { id: RiesgoId; titulo: string; detalle: string; test: (m: Mes) => boolean }[] = [
  { id: 'helada', titulo: 'Riesgo de heladas', detalle: 'Temperatura media del mes de 7 °C o menos.', test: (m) => m.temp <= 7 },
  { id: 'calor', titulo: 'Estrés por calor', detalle: 'Temperatura media del mes de 28 °C o más.', test: (m) => m.temp >= 28 },
  { id: 'sequia', titulo: 'Mes seco y cálido', detalle: 'Menos de 10 mm de lluvia con 22 °C o más.', test: (m) => m.rain < 10 && m.temp >= 22 },
  { id: 'lluvia', titulo: 'Lluvia abundante', detalle: '50 mm o más en el mes: encharcamiento y erosión.', test: (m) => m.rain >= 50 },
];

/** Riesgos típicos del año a partir del clima mensual histórico. NO es un pronóstico. */
export function calcularRiesgos(climate: Mes[]): Riesgo[] {
  const out: Riesgo[] = [];
  for (const r of REGLAS) {
    const meses = climate.filter(r.test).map((m) => m.month);
    if (meses.length > 0) {
      out.push({ id: r.id, titulo: r.titulo, detalle: r.detalle, meses, nivel: meses.length >= 3 ? 'alto' : 'medio' });
    }
  }
  return out.sort((a, b) => (a.nivel === b.nivel ? 0 : a.nivel === 'alto' ? -1 : 1));
}