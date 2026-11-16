import { Moon, Sun } from 'lucide-react';
import { alternarTema, useTema } from '../lib/tema';
import { useT } from '../lib/i18n';

/** `compacto`: solo el ícono (para el menú lateral plegado); el texto queda en aria-label y title. */
export default function ThemeToggle({ className = '', compacto = false }: { className?: string; compacto?: boolean }) {
  const oscuro = useTema() === 'dark';
  const t = useT();
  const texto = oscuro ? t('Modo claro', 'Light mode') : t('Modo oscuro', 'Dark mode');
  return (
    <button onClick={alternarTema} aria-pressed={oscuro} aria-label={compacto ? texto : undefined} title={compacto ? texto : undefined}
      className={`flex items-center justify-center gap-2 rounded-xl border border-line px-3 py-2 text-sm font-medium text-ink-700 hover:bg-surface-sunken focus-visible:outline-2 focus-visible:outline-leaf-600 ${className}`}>
      {oscuro ? <Sun size={16} /> : <Moon size={16} />}
      {!compacto && texto}
    </button>
  );
}
