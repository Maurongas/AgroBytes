import { AnimatePresence, motion } from 'framer-motion';
import type { ComponentType } from 'react';
import { useStore, type ViewId } from './store/useStore';
import AppShell from './components/AppShell';
import SelectView from './views/SelectView';
import DiagnosisView from './views/DiagnosisView';
import HistoryView from './views/HistoryView';
import AlertsView from './views/AlertsView';
import CalendarView from './views/CalendarView';
import CompareView from './views/CompareView';
import AccountView from './views/AccountView';

const VIEWS: Record<ViewId, ComponentType> = {
  select: SelectView,
  diagnosis: DiagnosisView,
  history: HistoryView,
  alerts: AlertsView,
  calendar: CalendarView,
  compare: CompareView,
  account: AccountView,
};

export default function App() {
  const view = useStore((s) => s.view);
  const View = VIEWS[view];
  return (
    <AppShell>
      <AnimatePresence mode="wait">
        <motion.main key={view} className="h-full" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          exit={{ opacity: 0 }} transition={{ duration: 0.3 }}>
          <View />
        </motion.main>
      </AnimatePresence>
    </AppShell>
  );
}
