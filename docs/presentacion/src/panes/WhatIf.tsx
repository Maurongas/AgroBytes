import { useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, LayoutGroup, animate, motion, useReducedMotion } from 'framer-motion';
import { CloudRain, Thermometer } from 'lucide-react';
import { panes, ui, whatIfTarget } from '../content';
import { SEASON_EN, cropEn } from '../i18n';
import ClimateChart from '../components/ClimateChart';
import { RAIN_MAX, TEMP_RANGE, scenario, shiftedClimate, type ScenarioStep, type Shift } from '../components/scenario';
import { analysis, isLiveData } from '../data';
import { whatIf } from '../live';
import { CropIcon, Title } from '../components/ui';
import type { SlideProps } from '../slides/types';

const T = panes.whatif;
const ZERO: Shift = { rainPct: 0, tempC: 0 };
const toSteps = (rot: typeof analysis.rotation): ScenarioStep[] =>
  rot.map((s) => ({ season: s.season, cropId: s.cropId, score: s.score, irrigationMm: Math.round(s.irrigationMm ?? 0) }));
const BASE_PLAN = toSteps(analysis.rotation);
const SEASON_TONE = { autumn: 'bg-clay-100', winter: 'bg-sky-50', spring: 'bg-leaf-50', summer: 'bg-sun-100' } as const;

function Slider({ icon: Icon, label, value, min, max, step, unit, onChange, tone }: {
  icon: typeof CloudRain; label: string; value: number; min: number; max: number; step: number; unit: string; tone: string;
  onChange: (v: number) => void;
}) {
  const shown = unit === '%' ? Math.round(value) : value.toFixed(1);
  return (
    <label data-interactive className="block rounded-panel border border-line bg-surface-raised p-6 shadow-card">
      <span className="flex items-center justify-between">
        <span className="flex items-center gap-3 text-2xl font-medium"><Icon size={28} className={tone} /> {label}</span>
        <span className={`font-mono text-3xl font-medium ${value === 0 ? 'text-ink-400' : tone}`}>{value > 0 ? '+' : ''}{shown}{unit === '%' ? ' %' : ` ${unit}`}</span>
      </span>
      <input type="range" className="pitch-range mt-4 w-full" min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(Number(e.target.value))} />
      <span className="flex justify-between text-sm text-ink-400"><span>{min}{unit === '%' ? '%' : ''}</span><span>+{max}{unit === '%' ? '%' : ''}</span></span>
    </label>
  );
}

export default function WhatIfPane({ step, preview }: SlideProps) {
  const reduce = useReducedMotion();
  const [shift, setShift] = useState<Shift>(preview && step >= 1 ? whatIfTarget : ZERO);
  const live = useRef(shift);
  live.current = shift;

  // El build mueve los sliders solos hasta lo que dice el guion (o los regresa a 0)
  useEffect(() => {
    const to = step >= 1 ? whatIfTarget : ZERO;
    if (preview || reduce) { setShift(to); return; }
    const from = live.current;
    const c = animate(0, 1, {
      duration: 1.6, ease: [0.22, 1, 0.36, 1],
      onUpdate: (t) => setShift({
        rainPct: from.rainPct + (to.rainPct - from.rainPct) * t,
        tempC: +(from.tempC + (to.tempC - from.tempC) * t).toFixed(2),
      }),
    });
    return () => c.stop();
  }, [step, preview, reduce]);

  const rounded = { rainPct: Math.round(shift.rainPct), tempC: Math.round(shift.tempC * 10) / 10 };
  const climate = useMemo(() => shiftedClimate(rounded), [rounded.rainPct, rounded.tempC]); // eslint-disable-line react-hooks/exhaustive-deps
  // En vivo: el backend recalcula la rotación con climateShift (POST /analyses?guardar=false). Se pide 450 ms
  // después de que el slider se detiene; las respuestas viejas se ignoran. Sin backend: escenarios precalculados.
  const [livePlan, setLivePlan] = useState<ScenarioStep[] | null>(null);
  const reqId = useRef(0);
  useEffect(() => {
    if (!isLiveData || preview) return;
    if (rounded.rainPct === 0 && rounded.tempC === 0) { reqId.current++; setLivePlan(null); return; }
    const t = setTimeout(() => {
      const id = ++reqId.current;
      whatIf(rounded).then((r) => { if (id === reqId.current) setLivePlan(toSteps(r.rotation)); }).catch(() => {});
    }, 450);
    return () => clearTimeout(t);
  }, [rounded.rainPct, rounded.tempC, preview]); // eslint-disable-line react-hooks/exhaustive-deps
  const plan = isLiveData ? (livePlan ?? BASE_PLAN) : scenario(rounded);
  const irrigation = plan.reduce((s, p) => s + p.irrigationMm, 0);
  const baseIrrigation = (isLiveData ? BASE_PLAN : scenario(ZERO)).reduce((s, p) => s + p.irrigationMm, 0);
  const diff = irrigation - baseIrrigation;

  return (
    <div className="absolute inset-0 flex flex-col bg-canvas px-20 py-16">
      <div className="flex items-end justify-between">
        <Title>{T.title}</Title>
        <p className={`text-sm uppercase tracking-widest ${isLiveData ? 'font-semibold text-danger' : 'text-ink-400'}`}>{isLiveData ? ui.liveWhatIf : ui.simulated}</p>
      </div>

      <div className="mt-10 grid flex-1 grid-cols-5 gap-8">
        <div className="col-span-2 flex flex-col gap-6">
          <Slider icon={CloudRain} label={ui.rain} value={rounded.rainPct} min={-60} max={60} step={1} unit="%" tone="text-sky-500"
            onChange={(v) => setShift((s) => ({ ...s, rainPct: v }))} />
          <Slider icon={Thermometer} label={ui.temperature} value={rounded.tempC} min={-3} max={5} step={0.1} unit={ui.tempUnit} tone="text-sun-700"
            onChange={(v) => setShift((s) => ({ ...s, tempC: v }))} />
          <div className="mt-auto rounded-panel bg-orbit p-6 text-paper">
            <p className="text-sm uppercase tracking-widest text-paper/60">{ui.irrigation3}</p>
            <p className="font-display text-5xl font-semibold">{irrigation} <span className="font-sans text-2xl text-paper/60">mm</span>
              {diff !== 0 && <span className={`ml-4 rounded-full px-3 py-1 font-mono text-xl ${diff > 0 ? "bg-danger/25 text-sun-300" : "bg-ok/25 text-leaf-300"}`}>{diff > 0 ? "+" : ""}{diff} mm</span>}</p>
          </div>
        </div>

        <div className="col-span-3 flex flex-col gap-6">
          <div className="h-[330px] rounded-panel border border-line bg-surface-raised p-5 shadow-card">
            <ClimateChart data={climate} rainMax={RAIN_MAX} tempRange={TEMP_RANGE} />
          </div>
          <LayoutGroup>
            <div className="grid flex-1 grid-cols-3 gap-4">
              {plan.map((p) => (
                <motion.div layout key={p.season} className={`flex flex-col overflow-hidden rounded-panel p-5 ${SEASON_TONE[p.season]}`}>
                  <p className="text-sm uppercase tracking-widest text-ink-500">{SEASON_EN[p.season]}</p>
                  <AnimatePresence mode="popLayout" initial={false}>
                    <motion.div key={p.cropId} className="mt-2 flex items-center gap-3"
                      initial={{ opacity: 0, y: 24, scale: 0.9 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: -24, scale: 0.9 }}
                      transition={{ type: 'spring', stiffness: 320, damping: 24 }}>
                      <CropIcon id={p.cropId} size={36} />
                      <span className={`font-display text-3xl font-semibold ${p.cropId === 'fallow' ? 'text-ink-400' : ''}`}>{cropEn(p.cropId)}</span>
                    </motion.div>
                  </AnimatePresence>
                  <p className="mt-auto font-mono text-base text-ink-500">{p.cropId === 'fallow' ? '—' : `${p.score} · ${p.irrigationMm} mm`}</p>
                </motion.div>
              ))}
            </div>
          </LayoutGroup>
        </div>
      </div>
    </div>
  );
}
