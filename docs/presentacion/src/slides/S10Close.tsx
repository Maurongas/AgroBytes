import { useEffect, useState } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import { Polygon, useMap } from 'react-leaflet';
import { REGION_LATLNGS } from '@app/lib/region';
import { deck, slide, ui } from '../content';
import FieldMap, { FIELD, FIELD_CENTER } from '../components/FieldMap';
import Logo from '../components/Logo';
import { EASE, NasaDot } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('close');
const WORLD: [number, number][] = [[-89, -540], [-89, 540], [89, 540], [89, -540]]; // más ancho que el mundo: sin franjas sin máscara
const NORTH_AMERICA: [number, number] = [47, -100];
const ZOOM_OUT_S = 3.6;

/** Vuela de la parcela a Norteamérica (México, EE. UU. y Canadá iluminados, como la máscara de la app). */
function ZoomOut({ instant, onDone }: { instant: boolean; onDone: () => void }) {
  const map = useMap();
  useEffect(() => {
    if (instant) { map.setView(NORTH_AMERICA, 3.2, { animate: false }); onDone(); return; }
    const t = setTimeout(() => {
      map.flyTo(NORTH_AMERICA, 3.2, { duration: ZOOM_OUT_S, easeLinearity: 0.15 });
      map.once('moveend', onDone);
    }, 700);
    return () => {
      clearTimeout(t);
      // Al salir de la diapositiva el mapa puede estar ya desmontado: detenerlo entonces lanza en Leaflet
      try { map.off('moveend', onDone); map.stop(); } catch { /* mapa ya destruido */ }
    };
  }, [map, instant, onDone]);
  return null;
}

export default function S10Close({ preview }: SlideProps) {
  const reduce = useReducedMotion();
  const instant = !!preview || !!reduce;
  const [done, setDone] = useState(false);
  const [onDone] = useState(() => () => setDone(true));

  return (
    <div className="absolute inset-0 bg-orbit">
      <FieldMap center={FIELD_CENTER} zoom={16}>
        <Polygon positions={[WORLD, ...REGION_LATLNGS]} interactive={false} pathOptions={{ stroke: false, fillColor: '#0B1220', fillOpacity: 0.6 }} />
        <Polygon positions={REGION_LATLNGS} interactive={false} pathOptions={{ color: '#9CCB86', weight: 2, fillColor: '#4E9F3D', fillOpacity: 0.18 }} />
        <Polygon positions={FIELD} interactive={false} pathOptions={{ color: '#FFFFFF', weight: 3, fillColor: '#3F7D4A', fillOpacity: 0.35 }} />
        <ZoomOut instant={instant} onDone={onDone} />
      </FieldMap>

      <AnimatePresence>
        {done && (
          <motion.div key="end" className="absolute inset-0 z-[1100] flex flex-col items-center justify-center bg-gradient-to-t from-orbit via-orbit/75 to-orbit/40 text-paper"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.9 }}>
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2, duration: 0.8, ease: EASE }}>
              <Logo dark />
            </motion.div>
            <motion.p className="mt-8 font-display text-5xl font-semibold" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.8 }}>
              {T.subtitle}
            </motion.p>
            <motion.p className="mt-4 flex items-center gap-3 text-2xl text-paper/70" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}>
              <NasaDot /> {deck.tagline}
            </motion.p>
            {ui.qrImage && (
              <motion.div className="mt-10 flex items-center gap-5 rounded-panel bg-paper p-4 text-ink-900" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1.6 }}>
                <img src={ui.qrImage} alt={ui.demo} className="h-32 w-32" />
                <div><p className="text-lg text-ink-500">{ui.demo}</p><p className="font-mono text-xl">{ui.demoUrl}</p></div>
              </motion.div>
            )}
            <p className="absolute bottom-10 text-base text-paper/50">{deck.challenge}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
