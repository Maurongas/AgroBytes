import { motion } from 'framer-motion';
import CropIcon from '../components/CropIcon';
import { CloudRain, ShieldCheck, Snowflake, Sun, Thermometer } from 'lucide-react';
import { useStore } from '../store/useStore';
import { cropName, SEASON_LABEL } from '../lib/crops';
import { calcularRiesgos, type RiesgoId } from '../lib/riesgos';
import SinAnalisis from '../components/SinAnalisis';

const ICONOS = { helada: Snowflake, calor: Thermometer, sequia: Sun, lluvia: CloudRain } as const satisfies Record<RiesgoId, unknown>;
const NIVEL = {
  alto: { texto: 'Alto', clase: 'border-danger/40 bg-danger/10' },
  medio: { texto: 'Medio', clase: 'border-warn/40 bg-warn/10' },
} as const;
const INCERTIDUMBRE = { low: 'baja', medium: 'media', high: 'alta' } as const;

export default function AlertsView() {
  const analysis = useStore((s) => s.analysis);
  if (!analysis) return <SinAnalisis titulo="Alertas climáticas" />;

  const riesgos = calcularRiesgos(analysis.climate);
  const { uncertainty } = analysis;

  return (
    <div className="h-full overflow-auto p-6">
      <h1 className="font-display text-3xl font-semibold">Alertas climáticas</h1>
      <p className="mt-1 max-w-2xl text-sm text-ink-500">
        Se calculan con el clima mensual histórico de tu parcela (NASA POWER). Son riesgos típicos del año, no un pronóstico.
      </p>
      <p className="mt-3 max-w-2xl rounded-xl border border-line bg-surface-raised p-3 text-sm text-ink-700">
        Incertidumbre {INCERTIDUMBRE[uncertainty.level]}: {uncertainty.reason}.
      </p>

      {riesgos.length === 0 ? (
        <div className="mt-6 flex items-center gap-3 rounded-card border border-line bg-leaf-50 p-5 text-leaf-900">
          <ShieldCheck size={22} /> No se detectan meses de riesgo con las reglas actuales.
        </div>
      ) : (
        <motion.ul className="mt-6 grid gap-4 md:grid-cols-2" initial="hidden" animate="show"
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.07 } } }}>
          {riesgos.map((r) => {
            const Icon = ICONOS[r.id];
            const nivel = NIVEL[r.nivel];
            return (
              <motion.li key={r.id} variants={{ hidden: { opacity: 0, y: 12 }, show: { opacity: 1, y: 0 } }}
                className={`rounded-card border p-5 ${nivel.clase}`}>
                <div className="flex items-center justify-between gap-3">
                  <span className="flex items-center gap-2 font-display text-lg font-semibold text-ink-900">
                    <Icon size={20} /> {r.titulo}
                  </span>
                  <span className="rounded-full bg-surface-raised px-3 py-1 text-xs font-medium text-ink-900">{nivel.texto}</span>
                </div>
                <p className="mt-2 text-sm text-ink-700">{r.detalle}</p>
                <p className="mt-2 text-sm text-ink-900"><strong>Meses:</strong> {r.meses.join(', ')}</p>
              </motion.li>
            );
          })}
        </motion.ul>
      )}

      <h2 className="mt-10 font-display text-2xl font-semibold">Riesgos de cada cultivo de la rotación</h2>
      <ul className="mt-4 grid gap-3 md:grid-cols-3">
        {analysis.rotation.map((step) => (
          <li key={step.season} className="rounded-card border border-line bg-surface-raised p-4">
            <p className="text-xs uppercase tracking-widest text-ink-500">{SEASON_LABEL[step.season]}</p>
            <p className="flex items-center gap-2 font-display text-lg font-semibold"><CropIcon id={step.cropId} size={20} />{cropName(step.cropId)}</p>
            {step.risks.length > 0 ? (
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink-700">
                {step.risks.map((risk) => <li key={risk}>{risk}</li>)}
              </ul>
            ) : (
              <p className="mt-2 text-sm text-ink-500">Sin riesgos registrados.</p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}