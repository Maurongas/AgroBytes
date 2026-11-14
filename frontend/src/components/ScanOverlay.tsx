import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';

const MESSAGES = [
  'Consultando NASA POWER…',
  'Leyendo humedad del suelo…',
  'Calculando balance hídrico…',
  'Buscando la mejor rotación…',
];

export default function ScanOverlay() {
  const [i, setI] = useState(0);
  useEffect(() => {
    const t = setInterval(() => setI((n) => (n + 1) % MESSAGES.length), 700);
    return () => clearInterval(t);
  }, []);

  return (
    <motion.div className="pointer-events-none absolute inset-0 z-[1050] bg-orbit/30"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <div className="absolute inset-y-0 w-0.5 bg-sky-300 shadow-[0_0_24px_6px_rgba(124,195,238,0.6)]"
        style={{ animation: 'scan 1.4s linear infinite' }} />
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 rounded-full bg-orbit px-5 py-2.5 text-sm text-canvas">
        <AnimatePresence mode="wait">
          <motion.span key={i} className="block" initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -6 }}>
            {MESSAGES[i]}
          </motion.span>
        </AnimatePresence>
      </div>
    </motion.div>
  );
}