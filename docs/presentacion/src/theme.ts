// Tema del pitch: claro por defecto (no sigue al sistema), T alterna. Usa los mismos tokens [data-theme] de la app.
const KEY = 'fieldshift:pitch-tema';

export function initTheme(fallback: 'light' | 'dark' = 'light') {
  let t: string | null = null;
  try { t = localStorage.getItem(KEY); } catch { /* sin almacenamiento: tema por defecto */ }
  document.documentElement.dataset.theme = t === 'dark' || t === 'light' ? t : fallback;
}

export function toggleTheme() {
  const t = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = t;
  try { localStorage.setItem(KEY, t); } catch { /* ignore */ }
}
