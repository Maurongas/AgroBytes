import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ui } from '../content';

/**
 * Copia visual de frontend/src/components/ScanOverlay.tsx (misma línea de barrido y la misma animación
 * `scan` de index.css) con mensajes en inglés. Si cambias ScanOverlay, revisa este archivo.
 */
export default function PitchScan({ interval = 600 }: { interval?: number }) {
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI((n) => (n + 1) % ui.scanMessages.length), interval);
    return () => clearInterval(t);
  }, [interval]);

  return (
    <motion.div className="pointer-events-none absolute inset-0 z-[1050] bg-orbit/30"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <div className="absolute inset-y-0 w-0.5 bg-sky-300 shadow-[0_0_24px_6px_rgba(124,195,238,0.6)]"
        style={{ animation: 'scan 1.4s linear infinite' }} />
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 rounded-full bg-orbit px-6 py-3 text-lg text-paper">
        <AnimatePresence mode="wait">
          <motion.span key={i} className="block" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -6 }}>
            {ui.scanMessages[i]}
          </motion.span>
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
