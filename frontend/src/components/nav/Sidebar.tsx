import { motion } from 'framer-motion';
import { useStore } from '../../store/useStore';
import { useSession } from '../../lib/session';
import ThemeToggle from '../ThemeToggle';
import BrandMark from '../BrandMark';
import { ACCOUNT_ITEM, NAV_ITEMS, type NavItem } from './navItems';

function Item({ item, label }: { item: NavItem; label?: string }) {
  const view = useStore((s) => s.view);
  const goTo = useStore((s) => s.goTo);
  const hasAnalysis = useStore((s) => s.analysis !== null);
  const disabled = !!item.needsAnalysis && !hasAnalysis;
  const active = view === item.id;
  const Icon = item.icon;
  return (
    <button
      onClick={() => goTo(item.id)}
      disabled={disabled}
      aria-current={active ? 'page' : undefined}
      title={disabled ? 'Primero analiza una parcela' : undefined}
      className="relative flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm font-medium text-ink-700 transition-colors hover:bg-surface-sunken focus-visible:outline-2 focus-visible:outline-leaf-600 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-transparent"
    >
      {active && (
        <motion.span layoutId="nav-pill" className="absolute inset-0 rounded-xl bg-leaf-100"
          transition={{ type: 'spring', stiffness: 380, damping: 30 }} />
      )}
      <Icon size={18} className="relative" />
      <span className="relative truncate">{label ?? item.label}</span>
    </button>
  );
}

export default function Sidebar() {
  const { usuario } = useSession();
  return (
    <aside aria-label="Menú principal"
      className="hidden w-60 shrink-0 flex-col border-r border-line-soft bg-surface-raised p-4 md:flex">
      <div className="mb-6 flex items-center gap-2 px-2">
        <BrandMark size={30} />
        <span className="font-display text-xl font-semibold text-ink-900">Agro<span className="text-leaf-600">Bytes</span></span>
      </div>

      <nav className="flex flex-1 flex-col gap-1">
        {NAV_ITEMS.map((item) => <Item key={item.id} item={item} />)}
      </nav>

      <div className="mt-4 space-y-1 border-t border-line-soft pt-4">
        <Item item={ACCOUNT_ITEM} label={usuario ? usuario.nombre : 'Iniciar sesión'} />
        <ThemeToggle className="w-full" />
      </div>
    </aside>
  );
}