import { useEffect, useState } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import { Polygon, useMap } from 'react-leaflet';
import { REGION_LATLNGS } from '@app/lib/region';
import { deck, school, slide, team, ui } from '../content';
import FieldMap, { FIELD, FIELD_CENTER } from '../components/FieldMap';
import Floaters, { FloatingTitle } from '../components/Floaters';
import { Mark } from '../components/Logo';
import { EASE, NasaDot } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('close');
const WORLD: [number, number][] = [[-89, -540], [-89, 540], [89, 540], [89, -540]]; // más ancho que el mundo: sin franjas sin máscara
const NORTH_AMERICA: [number, number] = [47, -100];
const ZOOM_OUT_S = 2.8;

/** Vuela de la parcela a Norteamérica (México, EE. UU. y Canadá iluminados, como la máscara de la app). */
function ZoomOut({ instant, onDone }: { instant: boolean; onDone: () => void }) {
  const map = useMap();
  useEffect(() => {
    if (instant) { map.setView(NORTH_AMERICA, 3.2, { animate: false }); onDone(); return; }
    const t = setTimeout(() => {
      map.flyTo(NORTH_AMERICA, 3.2, { duration: ZOOM_OUT_S, easeLinearity: 0.15 });
      map.once('moveend', onDone);
    }, 500);
    return () => {
      clearTimeout(t);
      // Al salir de la diapositiva el mapa puede estar ya desmontado: detenerlo entonces lanza en Leaflet
      try { map.off('moveend', onDone); map.stop(); } catch { /* mapa ya destruido */ }
    };
  }, [map, instant, onDone]);
  return null;
}

/**
 * Cierre «como la portada»: la parcela se aleja hasta Norteamérica y encima aparece la portada
 * (iconos flotando, título letra por letra), el equipo y, discretos abajo, los logos de UABC y FIAD.
 */
export default function S06Close({ preview }: SlideProps) {
  const reduce = useReducedMotion();
  const instant = !!preview || !!reduce;
  const d = preview ? 0 : 1;
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
          <motion.div key="end" className="absolute inset-0 z-[1100] overflow-hidden text-paper"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.9 }}>
            <div className="absolute inset-0 bg-gradient-to-t from-orbit via-orbit/90 to-orbit/75" />
            <motion.div className="absolute left-1/2 top-[360px] h-[640px] w-[1100px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-leaf-500/20 blur-[120px]"
              animate={{ scale: [1, 1.1, 1] }} transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }} />
            <Floaters instant={!!preview} />

            <div className="absolute inset-x-0 top-[150px] flex flex-col items-center text-center">
              <motion.div initial={{ opacity: 0, scale: 0.6 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 * d, duration: 0.7, ease: EASE }}>
                <Mark size={92} draw={!preview} />
              </motion.div>
              <FloatingTitle text={T.title} accentAt={4} instant={!!preview} delay={0.3}
                className="mt-4 font-display text-[170px] font-semibold leading-[0.95] tracking-tight text-paper drop-shadow-[0_8px_40px_rgba(0,0,0,.45)]" />
              <motion.p className="mt-12 font-display text-5xl font-semibold" initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1.2 * d, duration: 0.6 }}>
                {T.subtitle}
              </motion.p>
              <motion.p className="mt-3 flex items-center gap-3 text-2xl text-paper/70" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 * d }}>
                <NasaDot /> {deck.tagline}
              </motion.p>
              {ui.qrImage && (
                <motion.div className="mt-6 flex items-center gap-5 rounded-panel bg-paper p-3 text-ink-900" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1.7 * d }}>
                  <img src={ui.qrImage} alt={ui.demo} className="h-24 w-24" />
                  <div className="text-left"><p className="text-lg text-ink-500">{ui.demo}</p><p className="font-mono text-xl">{ui.demoUrl}</p></div>
                </motion.div>
              )}
            </div>

            {/* Equipo */}
            <motion.div className="absolute inset-x-0 bottom-[150px] flex flex-wrap justify-center gap-3"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.8 * d }}>
              {team.map((n, i) => (
                <motion.span key={n} className="rounded-full border border-paper/15 bg-paper/[0.08] px-5 py-2 text-xl text-paper/90 backdrop-blur"
                  initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: [0, -5, 0] }}
                  transition={{ opacity: { delay: (1.9 + i * 0.12) * d }, y: { duration: 4, repeat: Infinity, ease: 'easeInOut', delay: i * 0.3 } }}>
                  {n}
                </motion.span>
              ))}
            </motion.div>

            {/* Pie discreto: logos + reto */}
            <motion.div className="absolute inset-x-16 bottom-10 flex items-center justify-between gap-6"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.4 * d, duration: 0.8 }}>
              <div className="flex items-center gap-4 opacity-80">
                {school.logos.map((l) => (
                  <span key={l.src} className="flex h-[72px] w-16 items-center justify-center rounded-xl bg-paper/95 p-1.5 shadow-card">
                    <img src={l.src} alt={l.alt} className="max-h-full max-w-full object-contain" />
                  </span>
                ))}
                <span className="max-w-[440px] text-sm leading-snug text-paper/55">{school.line}</span>
              </div>
              <p className="text-right text-sm leading-snug text-paper/55">{deck.event}<br />{deck.challenge}</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
