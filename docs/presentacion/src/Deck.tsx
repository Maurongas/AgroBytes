import { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { slides, ui } from './content';
import { SLIDE_COMPONENTS } from './slides';
import SlideBoundary from './SlideBoundary';
import Stage from './Stage';
import { TOTAL, isTyping, useDeck } from './useDeck';
import { toggleTheme } from './theme';

/** ?still: cada diapositiva en su estado final, sin animaciones (capturas, respaldo en PDF). */
const STILL = new URLSearchParams(location.search).has('still');
const INTERACTIVE = '[data-interactive], button, a, input, select, textarea, label, .leaflet-control';

export default function Deck() {
  const { slide, step, dir, next, prev, goto } = useDeck();
  const [jump, setJump] = useState('');
  const [hint, setHint] = useState(!STILL);
  const touch = useRef<{ x: number; y: number } | null>(null);
  const Slide = SLIDE_COMPONENTS[slide];
  const builds = slides[slide].builds;

  useEffect(() => {
    const t = setTimeout(() => setHint(false), 4000);
    return () => clearTimeout(t);
  }, []);

  // Teclado (como PowerPoint)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      const onRange = t instanceof HTMLInputElement && t.type === 'range';
      if (isTyping(t) && !(onRange && !e.key.startsWith('Arrow'))) return; // las flechas mueven el slider enfocado
      const k = e.key;
      if (/^\d$/.test(k)) { setJump((j) => (j + k).slice(-2)); return; }
      if (k === 'Enter' && jump) { goto(Number(jump) - 1); setJump(''); e.preventDefault(); return; }
      if (k === 'Escape') { setJump(''); return; }
      if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(k)) { e.preventDefault(); next(); }
      else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); prev(); }
      else if (k === 'Home') goto(0);
      else if (k === 'End') goto(TOTAL - 1);
      else if (k === 's' || k === 'S') window.open(`${location.pathname}?presenter${location.hash}`, 'agrobytes-notes', 'width=1180,height=760');
      else if (k === 'f' || k === 'F') {
        if (document.fullscreenElement) void document.exitFullscreen();
        else void document.documentElement.requestFullscreen?.();
      } else if (k === 't' || k === 'T') toggleTheme();
      else return;
      setHint(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [jump, next, prev, goto]);

  useEffect(() => {
    if (!jump) return;
    const t = setTimeout(() => setJump(''), 2500);
    return () => clearTimeout(t);
  }, [jump]);

  const onClick = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest(INTERACTIVE)) return;
    if (e.clientX < window.innerWidth / 2) prev(); else next();
    setHint(false);
  };
  const onTouchStart = (e: React.TouchEvent) => { touch.current = { x: e.touches[0].clientX, y: e.touches[0].clientY }; };
  const onTouchEnd = (e: React.TouchEvent) => {
    const s = touch.current;
    touch.current = null;
    if (!s) return;
    const dx = e.changedTouches[0].clientX - s.x;
    const dy = e.changedTouches[0].clientY - s.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
      if (dx < 0) next(); else prev();
    }
  };

  const progress = (slide + step / (builds + 1)) / TOTAL;

  return (
    <div className="relative h-full w-full select-none bg-orbit" onClick={onClick} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}
      onDragStart={(e) => e.preventDefault()}>
      <Stage>
        <AnimatePresence mode="wait" custom={dir} initial={false}>
          <motion.div key={slide} className="absolute inset-0" custom={dir}
            variants={{
              enter: (d: number) => ({ opacity: 0, x: d * 60 }),
              center: { opacity: 1, x: 0 },
              exit: (d: number) => ({ opacity: 0, x: d * -60 }),
            }}
            initial="enter" animate="center" exit="exit" transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}>
            <SlideBoundary title={slides[slide].title}><Slide step={step} preview={STILL} /></SlideBoundary>
          </motion.div>
        </AnimatePresence>
      </Stage>

      {/* Barra de progreso + indicador */}
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-1 bg-ink-900/10">
        <motion.div className="h-full bg-leaf-500" animate={{ width: `${progress * 100}%` }} transition={{ duration: 0.4 }} />
      </div>
      <div className="pointer-events-none absolute bottom-3 right-4 rounded-full bg-orbit/60 px-3 py-1 font-mono text-xs text-paper/80 backdrop-blur">
        {jump ? `→ ${jump}` : `${slide + 1} / ${TOTAL}`}
      </div>
      <AnimatePresence>
        {hint && (
          <motion.div className="pointer-events-none absolute bottom-3 left-1/2 -translate-x-1/2 rounded-full bg-orbit/70 px-4 py-1.5 text-xs text-paper/80 backdrop-blur"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            {ui.keysHint}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
