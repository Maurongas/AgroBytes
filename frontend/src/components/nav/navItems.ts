import { CalendarDays, CloudRain, GitCompare, History, MapPin, Sprout, User, type LucideIcon } from 'lucide-react';
import type { ViewId } from '../../store/useStore';

export interface NavItem {
  id: ViewId;
  label: string;
  icon: LucideIcon;
  needsAnalysis?: boolean; // desactivado hasta que exista un análisis
}

export const NAV_ITEMS: NavItem[] = [
  { id: 'select', label: 'Analizar', icon: MapPin },
  { id: 'diagnosis', label: 'Resultados', icon: Sprout, needsAnalysis: true },
  { id: 'history', label: 'Historial', icon: History },
  { id: 'alerts', label: 'Alertas', icon: CloudRain, needsAnalysis: true },
  { id: 'calendar', label: 'Calendario', icon: CalendarDays, needsAnalysis: true },
  { id: 'compare', label: 'Comparar', icon: GitCompare, needsAnalysis: true },
];

export const ACCOUNT_ITEM: NavItem = { id: 'account', label: 'Cuenta', icon: User };