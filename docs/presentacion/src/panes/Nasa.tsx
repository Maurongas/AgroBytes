import { useEffect, useState } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import NasaMetricCard from '@app/components/NasaMetricCard';
import { panes } from '../content';
import { analysis, isLiveData, metricsEn } from '../data';
import { analyzeAgain } from '../live';
import PitchScan from '../components/PitchScan';
import { NasaDot, Title } from '../components/ui';
import type { SlideProps } from '../slides/types';

const T = panes.nasa;
const SCAN_MS = 2600;
const MIN_LIVE_MS = 1800;
const MAX_LIVE_MS = 12000;
const { lat, lon } = analysis.location;
const COORDS = `${Math.abs(lat).toFixed(3)}° ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lon).toFixed(3)}° ${lon >= 0 ? 'E' : 'W'}`;

export default function NasaPane({ preview }: SlideProps) {
  const reduce = useReducedMotion();
  const [scanning, setScanning] = useState(!preview && !reduce);
  // En vivo: vuelve a pedir el análisis al backend; el escaneo dura lo que tarda la respuesta real (mín. 1.8 s).
  useEffect(() => {
    if (preview) return;
    if (!isLiveData) {
      if (!scanning) return;
      const t = setTimeout(() => setScanning(false), SCAN_MS);
      return () => clearTimeout(t);
    }
    let alive = true;
    const min = new Promise((r) => setTimeout(r, reduce ? 0 : MIN_LIVE_MS));
    const req = analyzeAgain().catch(() => null);
    const cap = new Promise((r) => setTimeout(r, MAX_LIVE_MS));
    void Promise.race([Promise.all([min, req]), cap]).then(() => { if (alive) setScanning(false); });
    return () => { alive = false; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="absolute inset-0 overflow-hidden bg-orbit px-24 py-20">
      {/* rejilla tenue tipo «coordenadas» */}
      <div className="absolute inset-0 opacity-[0.07]"
        style={{ backgroundImage: 'linear-gradient(#FBF8F1 1px, transparent 1px), linear-gradient(90deg, #FBF8F1 1px, transparent 1px)', backgroundSize: '80px 80px' }} />
      <Title dark sub={<span className="flex items-center gap-3"><NasaDot /> {T.subtitle} · <span className="font-mono">{COORDS}</span></span>} className="relative">{T.title}</Title>

      {/* Tarjetas reales de la app (NasaMetricCard). Solo CSS por fuera: texto más grande para el escenario y
          vector-effect normal en el sparkline (con non-scaling-stroke el trazo animado por pathLength sale cortado). */}
      <motion.div className="relative mt-16 grid grid-cols-4 gap-6 [&_p.font-display]:text-5xl [&_p.text-sm]:text-lg [&_polyline]:[vector-effect:none] [&_polyline]:[stroke-width:1.2]"
        initial="hidden" animate={scanning ? 'hidden' : 'show'}
        variants={{ hidden: {}, show: { transition: { staggerChildren: 0.18 } } }}>
        {metricsEn.map((m) => (
          <motion.div key={m.id}
            variants={{ hidden: { opacity: 0, y: -60, rotate: -2 }, show: { opacity: 1, y: 0, rotate: 0, transition: { type: 'spring', stiffness: 220, damping: 18 } } }}>
            {!scanning && <NasaMetricCard m={m} />}
          </motion.div>
        ))}
      </motion.div>

      <AnimatePresence>{scanning && <PitchScan key="scan" live={isLiveData} />}</AnimatePresence>
    </div>
  );
}
