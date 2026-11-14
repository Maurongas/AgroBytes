import { AnimatePresence, motion } from 'framer-motion';
import { useStore } from './store/useStore';
import SelectView from './views/SelectView';
import DiagnosisView from './views/DiagnosisView';

export default function App() {
  const view = useStore((s) => s.view);
  return (
    <AnimatePresence mode="wait">
      <motion.main key={view} className="h-full" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
        exit={{ opacity: 0 }} transition={{ duration: 0.3 }}>
        {view === 'select' ? <SelectView /> : <DiagnosisView />}
      </motion.main>
    </AnimatePresence>
  );
}