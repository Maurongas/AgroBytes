import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { MotionConfig } from 'framer-motion';
import './pitch.css';
import Boot from './Boot';
import { boot } from './live';
import { initTheme } from './theme';

const isPresenter = new URLSearchParams(location.search).has('presenter');
if (isPresenter) document.documentElement.dataset.theme = 'dark';
else initTheme('light');

const root = createRoot(document.getElementById('root')!);
root.render(<Boot />);

// 1) Pide el análisis REAL al backend (live.ts). 2) Solo entonces carga el deck: data.ts lee esa respuesta.
const live = await boot();
if (!live) {
  root.render(<Boot failed />);
  await new Promise((r) => setTimeout(r, 1500));
}
const [{ default: Deck }, { default: Presenter }] = await Promise.all([import('./Deck'), import('./Presenter')]);

root.render(
  <StrictMode>
    {/* prefers-reduced-motion: framer-motion cambia los movimientos por fundidos */}
    <MotionConfig reducedMotion={new URLSearchParams(location.search).has('still') ? 'always' : 'user'}>
      {isPresenter ? <Presenter /> : <Deck />}
    </MotionConfig>
  </StrictMode>,
);
