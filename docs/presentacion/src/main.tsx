import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { MotionConfig } from 'framer-motion';
import './pitch.css';
import Deck from './Deck';
import Presenter from './Presenter';
import { initTheme } from './theme';

const isPresenter = new URLSearchParams(location.search).has('presenter');
if (isPresenter) document.documentElement.dataset.theme = 'dark';
else initTheme('light');

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {/* prefers-reduced-motion: framer-motion cambia los movimientos por fundidos */}
    <MotionConfig reducedMotion="user">
      {isPresenter ? <Presenter /> : <Deck />}
    </MotionConfig>
  </StrictMode>,
);
