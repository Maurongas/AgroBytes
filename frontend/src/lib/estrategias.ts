import type { ImpactItem, Strategy } from '../api/types';
import { tr } from './i18n';

/** La estrategia que se muestra al abrir: la recomendada; si no hay, la primera que no sea "seguir como hoy". */
export function estrategiaInicial(lista: Strategy[]): string | null {
  return (lista.find((s) => s.isRecommended) ?? lista.find((s) => !s.isCurrent) ?? lista[0])?.id ?? null;
}

/** Las barras de impacto de una estrategia contra "seguir como hoy" (mismas etiquetas que el backend). */
export function impactoContra(base: Strategy, s: Strategy): ImpactItem[] {
  return [
    { label: tr('Agua total del cultivo', 'Total crop water'), unit: 'mm', current: base.waterMm, recommended: s.waterMm, betterWhen: 'lower' },
    { label: tr('Riego necesario', 'Irrigation needed'), unit: 'mm', current: base.irrigationMm, recommended: s.irrigationMm, betterWhen: 'lower' },
    { label: tr('Balance de nitrógeno (estimado)', 'Nitrogen balance (estimated)'), unit: 'kg/ha', current: base.nitrogenKgHa, recommended: s.nitrogenKgHa, betterWhen: 'higher' },
  ];
}
