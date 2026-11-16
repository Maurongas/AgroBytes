import { Languages } from 'lucide-react';
import { toggleLang, useLang } from '../lib/i18n';

/** Cambia el idioma de la interfaz entre inglés y español. `compacto`: solo el código del idioma. */
export default function LangToggle({ className = '', compacto = false }: { className?: string; compacto?: boolean }) {
  const lang = useLang();
  const texto = lang === 'en' ? 'Cambiar a español' : 'Switch to English';
  return (
    <button onClick={toggleLang} aria-label={texto} title={texto}
      className={`flex items-center justify-center gap-2 rounded-xl border border-line px-3 py-2 text-sm font-medium text-ink-700 hover:bg-surface-sunken focus-visible:outline-2 focus-visible:outline-leaf-600 ${className}`}>
      <Languages size={16} aria-hidden />
      {compacto ? (
        <span className="text-xs font-semibold">{lang === 'en' ? 'ES' : 'EN'}</span>
      ) : (
        <span>
          <span className={lang === 'en' ? 'font-semibold text-leaf-700' : 'text-ink-400'}>EN</span>
          <span className="text-ink-400"> / </span>
          <span className={lang === 'es' ? 'font-semibold text-leaf-700' : 'text-ink-400'}>ES</span>
        </span>
      )}
    </button>
  );
}
