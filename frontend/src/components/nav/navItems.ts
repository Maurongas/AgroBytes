import { CalendarDays, CloudRain, GitCompare, History, MapPin, Sprout, User, type LucideIcon } from 'lucide-react';
import type { ViewId } from '../../store/useStore';
import { tr } from '../../lib/i18n';

export interface NavItem {
  id: ViewId;
  label: [string, string]; // [español, inglés]
  icon: LucideIcon;
  needsAnalysis?: boolean; // desactivado hasta que exista un análisis
}

export const NAV_ITEMS: NavItem[] = [
  { id: 'select', label: ['Analizar', 'Analyze'], icon: MapPin },
  { id: 'diagnosis', label: ['Resultados', 'Results'], icon: Sprout, needsAnalysis: true },
  { id: 'history', label: ['Historial', 'History'], icon: History },
  { id: 'alerts', label: ['Alertas', 'Alerts'], icon: CloudRain, needsAnalysis: true },
  { id: 'calendar', label: ['Calendario', 'Calendar'], icon: CalendarDays, needsAnalysis: true },
  { id: 'compare', label: ['Comparar', 'Compare'], icon: GitCompare, needsAnalysis: true },
];

export const ACCOUNT_ITEM: NavItem = { id: 'account', label: ['Cuenta', 'Account'], icon: User };

/** Texto del elemento en el idioma actual. */
export const navLabel = (item: NavItem) => tr(...item.label);