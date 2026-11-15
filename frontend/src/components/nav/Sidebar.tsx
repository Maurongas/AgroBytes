import { useState, useSyncExternalStore } from 'react';
import { motion } from 'framer-motion';
import { PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import { useStore } from '../../store/useStore';
import { useSession } from '../../lib/session';
import ThemeToggle from '../ThemeToggle';
import { ACCOUNT_ITEM, NAV_ITEMS, type NavItem } from './navItems';

/*
 * Menú lateral plegable (desde md). Plegado muestra solo los íconos (w-16) y deja más espacio a la vista.
 * Si la persona no lo ha tocado, empieza plegado entre 768 y 1023 px y abierto desde 1024 px.
 * Su elección se recuerda en este navegador.
 */
const CLAVE = 'fieldshift:menu';
type Preferencia = 'abierto' | 'plegado' | null;

function leerPreferencia(): Preferencia {
  try {
    const v = localStorage.getItem(CLAVE);
    return v === 'abierto' || v === 'plegado' ? v : null;
  } catch {
    return null;
  }
}

const ANCHO_GRANDE = '(min-width: 1024px)';
const suscribirAncho = (avisar: () => void) => {
  const mq = window.matchMedia(ANCHO_GRANDE);
  mq.addEventListener('change', avisar);
  return () => mq.removeEventListener('change', avisar);
};
const useAnchoGrande = () => useSyncExternalStore(suscribirAncho, () => window.matchMedia(ANCHO_GRANDE).matches, () => true);

function Item({ item, label, plegado }: { item: NavItem; label?: string; plegado: boolean }) {
  const view = useStore((s) => s.view);
  const goTo = useStore((s) => s.goTo);
  const hasAnalysis = useStore((s) => s.analysis !== null);
  const disabled = !!item.needsAnalysis && !hasAnalysis;
  const active = view === item.id;
  const Icon = item.icon;
  const texto = label ?? item.label;
  return (
    <button
      onClick={() => goTo(item.id)}
      disabled={disabled}
      aria-current={active ? 'page' : undefined}
      aria-label={plegado ? texto : undefined}
      title={disabled ? 'Primero analiza una parcela' : plegado ? texto : undefined}
      className={`relative flex w-full items-center gap-3 rounded-xl py-2.5 text-left text-sm font-medium text-ink-700 transition-colors hover:bg-surface-sunken focus-visible:outline-2 focus-visible:outline-leaf-600 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-transparent ${
        plegado ? 'justify-center px-0' : 'px-3'}`}
    >
      {active && (
        <motion.span layoutId="nav-pill" className="absolute inset-0 rounded-xl bg-leaf-100"
          transition={{ type: 'spring', stiffness: 380, damping: 30 }} />
      )}
      <Icon size={18} className="relative shrink-0" />
      {!plegado && <span className="relative truncate">{texto}</span>}
    </button>
  );
}

export default function Sidebar() {
  const { usuario } = useSession();
  const grande = useAnchoGrande();
  const [preferencia, setPreferencia] = useState<Preferencia>(leerPreferencia);
  const plegado = preferencia ? preferencia === 'plegado' : !grande;

  const alternar = () => {
    const nueva = plegado ? 'abierto' : 'plegado';
    setPreferencia(nueva);
    try {
      localStorage.setItem(CLAVE, nueva);
    } catch {
      /* modo privado: vale solo en esta sesión */
    }
  };

  return (
    <aside aria-label="Menú principal"
      className={`hidden shrink-0 flex-col overflow-y-auto overflow-x-hidden border-r border-line-soft bg-surface-raised transition-[width] duration-200 md:flex ${
        plegado ? 'w-16 p-2' : 'w-60 p-4'}`}>
      <div className={`mb-6 flex items-center gap-2 ${plegado ? 'flex-col' : 'px-2'}`}>
        <span className="h-3 w-3 shrink-0 rounded-full bg-leaf-600" aria-hidden />
        {!plegado && <span className="flex-1 truncate font-display text-xl font-semibold text-ink-900">Field Shift</span>}
        <button onClick={alternar} aria-expanded={!plegado}
          aria-label={plegado ? 'Desplegar menú' : 'Plegar menú'} title={plegado ? 'Desplegar menú' : 'Plegar menú'}
          className="flex min-h-9 min-w-9 items-center justify-center rounded-lg text-ink-500 hover:bg-surface-sunken focus-visible:outline-2 focus-visible:outline-leaf-600">
          {plegado ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
        </button>
      </div>

      <nav className="flex flex-1 flex-col gap-1">
        {NAV_ITEMS.map((item) => <Item key={item.id} item={item} plegado={plegado} />)}
      </nav>

      <div className="mt-4 space-y-1 border-t border-line-soft pt-4">
        <Item item={ACCOUNT_ITEM} label={usuario ? usuario.nombre : 'Iniciar sesión'} plegado={plegado} />
        <ThemeToggle className="w-full" compacto={plegado} />
      </div>
    </aside>
  );
}
