import { useEffect, useState } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import NasaMetricCard from '@app/components/NasaMetricCard';
import { slide } from '../content';
import { metricsEn } from '../data';
import PitchScan from '../components/PitchScan';
import { NasaDot, Title } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('nasa');
const SCAN_MS = 2600;

export default function S05Nasa({ preview }: SlideProps) {
  const reduce = useReducedMotion();
  const [scanning, setScanning] = useState(!preview && !reduce);
  useEffect(() => {
    if (!scanning) return;
    const t = setTimeout(() => setScanning(false), SCAN_MS);
    return () => clearTimeout(t);
  }, [scanning]);

  return (
    <div className="absolute inset-0 overflow-hidden bg-orbit px-24 py-20">
      {/* rejilla tenue tipo «coordenadas» */}
      <div className="absolute inset-0 opacity-[0.07]"
        style={{ backgroundImage: 'linear-gradient(#FBF8F1 1px, transparent 1px), linear-gradient(90deg, #FBF8F1 1px, transparent 1px)', backgroundSize: '80px 80px' }} />
      <Title dark sub={<span className="flex items-center gap-3"><NasaDot /> {T.subtitle}</span>} className="relative">{T.title}</Title>

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

      <AnimatePresence>{scanning && <PitchScan key="scan" />}</AnimatePresence>
    </div>
  );
}
