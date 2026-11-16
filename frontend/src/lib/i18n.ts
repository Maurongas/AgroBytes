import { useSyncExternalStore } from 'react';

/**
 * Idioma de la interfaz: inglés por defecto, español con el botón EN/ES. La elección se recuerda en este navegador.
 * Los textos se escriben en pares junto a donde se usan: `t('Analizar', 'Analyze')` (primero español, luego inglés).
 * El backend recibe el mismo idioma (`?lang=`) y devuelve en ese idioma las razones, riesgos y métricas.
 */
export type Lang = 'en' | 'es';

const CLAVE = 'agrobytes:idioma';
const oyentes = new Set<() => void>();

function leer(): Lang {
  try {
    const v = localStorage.getItem(CLAVE);
    return v === 'es' || v === 'en' ? v : 'en';
  } catch {
    return 'en';
  }
}

let actual: Lang = leer();
document.documentElement.lang = actual;

export const getLang = (): Lang => actual;

export function setLang(l: Lang): void {
  if (l === actual) return;
  actual = l;
  document.documentElement.lang = l;
  try {
    localStorage.setItem(CLAVE, l);
  } catch {
    /* modo privado: vale solo en esta sesión */
  }
  oyentes.forEach((avisar) => avisar());
}

export const toggleLang = () => setLang(actual === 'en' ? 'es' : 'en');

/** Fuera de componentes (PDF, mensajes del store): usa el idioma actual. */
export const tr = (es: string, en: string): string => (actual === 'en' ? en : es);

/** Locale para fechas y números. */
export const locale = (): string => (actual === 'en' ? 'en-US' : 'es-MX');

function suscribir(avisar: () => void) {
  oyentes.add(avisar);
  return () => {
    oyentes.delete(avisar);
  };
}

export function useLang(): Lang {
  return useSyncExternalStore(suscribir, getLang, () => 'en');
}

/** En componentes: re-renderiza al cambiar de idioma. `const t = useT(); t('Hola', 'Hello')`. */
export function useT(): (es: string, en: string) => string {
  const lang = useLang();
  return (es, en) => (lang === 'en' ? en : es);
}

export function onLangChange(f: () => void): () => void {
  return suscribir(f);
}
