import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Ellipsis } from 'lucide-react';
import { useStore } from '../../store/useStore';
import { useSession } from '../../lib/session';
import ThemeToggle from '../ThemeToggle';
import { ACCOUNT_ITEM, NAV_ITEMS, type NavItem } from './navItems';

const MAIN = NAV_ITEMS.slice(0, 3);                       // Analizar, Resultados, Historial
const MORE = [...NAV_ITEMS.slice(3), ACCOUNT_ITEM];       // Alertas, Calendario, Comparar, Cuenta

export default function BottomBar() {
  const [more, setMore] = useState(false);
  const view = useStore((s) => s.view);
  const goTo = useStore((s) => s.goTo);
  const hasAnalysis = useStore((s) => s.analysis !== null);
  const { usuario } = useSession();
  const moreActive = MORE.some((i) => i.id === view);

  const go = (item: NavItem) => { goTo(item.id); setMore(false); };
  const isDisabled = (item: NavItem) => !!item.needsAnalysis && !hasAnalysis;

  return (
    <nav aria-label="Menú principal" className="relative z-[1200] flex border-t border-line-soft bg-surface-raised md:hidden">
      <AnimatePresence>
        {more && (
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 12 }}
            className="absolute inset-x-0 bottom-full grid grid-cols-2 gap-2 rounded-t-panel border border-line bg-surface-raised p-4 shadow-lift">
            {MORE.map((item) => {
              const Icon = item.icon;
              return (
                <button key={item.id} onClick={() => go(item)} disabled={isDisabled(item)}
                  className="flex items-center gap-2 rounded-xl border border-line px-3 py-3 text-sm text-ink-700 disabled:opacity-40">
                  <Icon size={18} />
                  {item.id === 'account' ? (usuario ? usuario.nombre : 'Iniciar sesión') : item.label}
                </button>
              );
            })}
            <ThemeToggle className="col-span-2" />
          </motion.div>
        )}
      </AnimatePresence>

      {MAIN.map((item) => {
        const Icon = item.icon;
        const active = view === item.id;
        return (
          <button key={item.id} onClick={() => go(item)} disabled={isDisabled(item)} aria-label={item.label}
            aria-current={active ? 'page' : undefined}
            className={`flex flex-1 flex-col items-center gap-0.5 py-2 text-xs disabled:opacity-40 ${active ? 'font-semibold text-leaf-700' : 'text-ink-500'}`}>
            <Icon size={20} />{item.label}
          </button>
        );
      })}

      <button onClick={() => setMore(!more)} aria-label="Más opciones" aria-expanded={more}
        className={`flex flex-1 flex-col items-center gap-0.5 py-2 text-xs ${moreActive || more ? 'font-semibold text-leaf-700' : 'text-ink-500'}`}>
        <Ellipsis size={20} />Más
      </button>
    </nav>
  );
}