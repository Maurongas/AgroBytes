import { useEffect, useState } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import { CircleMarker, Polyline, useMap } from 'react-leaflet';
import { Check, Droplets, Layers, MousePointer2, Sprout, TrendingUp, type LucideIcon } from 'lucide-react';
import CountUp from '@app/components/CountUp';
import EditableParcel from '@app/components/map/EditableParcel';
import { useStore } from '@app/store/useStore';
import type { Priority } from '@app/api/types';
import { slide, ui } from '../content';
import { analysis, current, recommended, soil } from '../data';
import { cropEn } from '../i18n';
import FieldMap, { FIELD, FIELD_CENTER } from '../components/FieldMap';
import { CropIcon, EASE } from '../components/ui';
import type { SlideProps } from './types';

const T = slide('draw');
const STEP_MS = 520;
const noop = () => {};
// Parcela a la izquierda: el panel ocupa la derecha
const CENTER: [number, number] = [FIELD_CENTER[0], FIELD_CENTER[1] + 0.0017];

const CURRENT_CROP = current?.steps.find((s) => s.cropId !== 'fallow')?.cropId ?? 'maize';
const PRIORITY: Priority = recommended && recommended.id !== 'current' ? recommended.id : 'water';
const CROP_CHOICES = Array.from(new Set([CURRENT_CROP, 'wheat', 'bean', 'sorghum']));
const PRIORITY_ICON: Record<Priority, { icon: LucideIcon; tone: string }> = {
  water: { icon: Droplets, tone: 'text-sky-500' },
  nitrogen: { icon: Sprout, tone: 'text-nitro' },
  yield: { icon: TrendingUp, tone: 'text-leaf-500' },
};

/** Cursor animado en coordenadas del mapa (va de vértice en vértice). */
function Cursor({ index }: { index: number }) {
  const map = useMap();
  const target = FIELD[Math.min(index, FIELD.length - 1)];
  const p = map.latLngToContainerPoint(target);
  return (
    <motion.div className="pointer-events-none absolute left-0 top-0 z-[1000] text-paper drop-shadow-[0_2px_6px_rgba(0,0,0,.6)]"
      initial={{ x: p.x + 220, y: p.y + 160, opacity: 0 }} animate={{ x: p.x - 4, y: p.y - 2, opacity: 1 }}
      transition={{ duration: STEP_MS / 1000 * 0.8, ease: EASE }}>
      <MousePointer2 size={40} fill="#12261F" />
    </motion.div>
  );
}

/** Igual que ParcelMap mientras se dibuja: línea punteada blanca + vértices. Al cerrar, EditableParcel de la app. */
function Drawing({ count }: { count: number }) {
  const points = FIELD.slice(0, count);
  const done = count >= FIELD.length;
  return (
    <>
      {!done && points.length > 1 && <Polyline positions={points} pathOptions={{ color: '#FFFFFF', weight: 3, dashArray: '6 6' }} />}
      {!done && points.map((p, i) => (
        <CircleMarker key={i} center={p} radius={8} pathOptions={{ color: '#3F7D4A', weight: 3, fillColor: '#FFFFFF', fillOpacity: 1 }} />
      ))}
      {done && <EditableParcel editando={false} borrarPunto={false} onCambio={noop} onAviso={noop} />}
    </>
  );
}

function Panel({ animate }: { animate: boolean }) {
  const [phase, setPhase] = useState(animate ? 0 : 2);
  useEffect(() => {
    if (!animate) return;
    const a = setTimeout(() => setPhase(1), 900);
    const b = setTimeout(() => setPhase(2), 1900);
    return () => { clearTimeout(a); clearTimeout(b); };
  }, [animate]);
  return (
    <motion.aside className="absolute bottom-8 right-8 top-8 z-[1100] w-[440px] rounded-panel border border-line bg-surface-raised/95 p-8 shadow-lift backdrop-blur"
      initial={{ x: 480, opacity: 0 }} animate={{ x: 0, opacity: 1 }} exit={{ x: 480, opacity: 0 }} transition={{ duration: 0.6, ease: EASE }}>
      <h2 className="font-display text-4xl font-semibold">{ui.yourField}</h2>
      <p className="mt-2 flex items-center gap-2 text-lg text-ink-700">
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-leaf-600 text-paper"><Check size={15} /></span>
        {analysis.areaHa.toFixed(1)} ha
      </p>

      <p className="mt-8 text-sm font-semibold uppercase tracking-widest text-ink-500">{ui.currentCrop}</p>
      <div className="mt-3 grid grid-cols-2 gap-3">
        {CROP_CHOICES.map((id) => {
          const on = phase >= 1 && id === CURRENT_CROP;
          return (
            <motion.div key={id} animate={on ? { scale: [1, 1.08, 1] } : {}} transition={{ duration: 0.4 }}
              className={`flex items-center gap-2 rounded-xl border-2 px-4 py-3 text-lg transition-colors ${on ? 'border-leaf-600 bg-leaf-50 font-semibold text-leaf-900' : 'border-line text-ink-700'}`}>
              <CropIcon id={id} /> {cropEn(id)}
            </motion.div>
          );
        })}
      </div>

      <p className="mt-8 text-sm font-semibold uppercase tracking-widest text-ink-500">{ui.priority}</p>
      <div className="mt-3 space-y-3">
        {(Object.keys(ui.priorities) as Priority[]).map((id) => {
          const on = phase >= 2 && id === PRIORITY;
          const { icon: Icon, tone } = PRIORITY_ICON[id];
          return (
            <motion.div key={id} animate={on ? { scale: [1, 1.05, 1] } : {}} transition={{ duration: 0.4 }}
              className={`flex items-center gap-3 rounded-xl border-2 px-4 py-3 text-lg transition-colors ${on ? 'border-leaf-600 bg-leaf-50 font-semibold text-leaf-900' : 'border-line text-ink-700'}`}>
              <Icon size={24} className={tone} /> {ui.priorities[id]}
              {on && <Check size={20} className="ml-auto text-leaf-600" />}
            </motion.div>
          );
        })}
      </div>

      <div className={`mt-8 rounded-full px-6 py-4 text-center text-lg font-medium transition-colors ${phase >= 2 ? 'bg-leaf-600 text-paper' : 'bg-surface-sunken text-ink-400'}`}>
        {ui.analyze}
      </div>
    </motion.aside>
  );
}

export default function S04Draw({ step, preview }: SlideProps) {
  const reduce = useReducedMotion();
  const instant = !!preview || !!reduce;
  // Si se entra ya con el paso 1 o más (al retroceder), la parcela aparece completa
  const [animateDraw] = useState(() => step === 0 && !instant);
  const [count, setCount] = useState(step >= 1 && !animateDraw ? FIELD.length : 0);
  const [panelAnimates] = useState(() => step < 3 && !instant);

  const drawing = step >= 1; // solo el paso 0→1 dibuja; los pasos 2 y 3 no reinician el dibujo
  useEffect(() => {
    if (!drawing) { setCount(0); return; }
    if (!animateDraw) { setCount(FIELD.length); return; }
    setCount(0);
    const timers = FIELD.map((_, i) => setTimeout(() => setCount(i + 1), STEP_MS * (i + 1)));
    return () => timers.forEach(clearTimeout);
  }, [drawing, animateDraw]);

  // EditableParcel lee los puntos del store de la app
  useEffect(() => {
    useStore.setState({ points: count >= FIELD.length ? FIELD : [] });
  }, [count]);
  useEffect(() => () => useStore.setState({ points: [], geometry: null, areaHa: null }), []);

  const done = count >= FIELD.length;
  return (
    <div className="absolute inset-0 bg-orbit">
      <FieldMap center={CENTER} zoom={17.2}>
        {step >= 1 && <Drawing count={count} />}
        {step >= 1 && !done && <Cursor index={count} />}
      </FieldMap>

      <motion.div className="absolute left-8 top-8 z-[1000] rounded-full bg-orbit/85 px-7 py-3 font-display text-4xl font-semibold text-paper backdrop-blur"
        initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }}>
        {T.title}
      </motion.div>

      <div className="absolute bottom-10 left-8 z-[1000] flex flex-col items-start gap-4">
        <AnimatePresence>
          {done && (
            <motion.div key="area" className="rounded-card bg-orbit/85 px-7 py-4 text-paper backdrop-blur"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              <span className="font-display text-7xl font-semibold"><CountUp value={analysis.areaHa} decimals={1} /></span>
              <span className="ml-2 text-3xl text-paper/70">ha</span>
            </motion.div>
          )}
          {step >= 2 && soil && (
            <motion.div key="soil" className="flex items-center gap-3 rounded-full bg-surface-raised px-6 py-3 text-xl shadow-lift"
              initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0 }} transition={{ type: 'spring', stiffness: 300, damping: 22 }}>
              <Layers size={24} className="text-clay-500" />
              <span className="text-ink-500">{ui.soilDetected}:</span> <strong>{soil}</strong>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <AnimatePresence>{step >= 3 && <Panel key="panel" animate={panelAnimates} />}</AnimatePresence>
    </div>
  );
}
