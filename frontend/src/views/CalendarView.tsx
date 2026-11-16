import { useStore } from '../store/useStore';
import CropIcon from '../components/CropIcon';
import { cropName, seasonLabel } from '../lib/crops';
import { meses, mesesDeVentana } from '../lib/calendario';
import SinAnalisis from '../components/SinAnalisis';

const COLUMNAS = 'grid-cols-[150px_repeat(12,minmax(44px,1fr))]';

export default function CalendarView() {
  const analysis = useStore((s) => s.analysis);
  if (!analysis) return <SinAnalisis titulo="Calendario agrícola" />;

  const mesActual = new Date().getMonth();
  const colMes = (i: number) => (i === mesActual ? 'bg-sun-100/60' : '');

  return (
    <div className="h-full overflow-auto p-6">
      <h1 className="font-display text-3xl font-semibold">Calendario agrícola</h1>
      <p className="mt-1 max-w-2xl text-sm text-ink-500">
        Ventanas de siembra recomendadas para tu rotación, junto al clima mensual de la parcela (NASA POWER). El mes actual está resaltado.
      </p>

      <div className="mt-6 overflow-x-auto rounded-card border border-line bg-surface-raised shadow-card">
        <div className="min-w-[760px] p-3">
          <div className={`grid ${COLUMNAS} items-center gap-y-1 text-center text-xs text-ink-500`}>
            <span />
            {meses().map((m, i) => <span key={m} className={`rounded-md py-1 font-medium ${colMes(i)}`}>{m}</span>)}

            {analysis.rotation.map((step) => {
              const meses = mesesDeVentana(step.plantingWindow);
              return (
                <div key={step.season} className="contents">
                  <div className="pr-2 text-left">
                    <p className="flex items-center gap-1.5 text-sm font-semibold text-ink-900"><CropIcon id={step.cropId} size={15} />{cropName(step.cropId)}</p>
                    <p className="text-[11px] text-ink-500">{seasonLabel(step.season)} · {step.plantingWindow}</p>
                  </div>
                  {meses().map((m, i) => (
                    <span key={m} className={`flex h-9 items-center justify-center ${colMes(i)}`}>
                      {meses.includes(i) && (
                        <span className="h-5 w-full bg-leaf-500" aria-label={`Siembra de ${cropName(step.cropId)} en ${m}`} />
                      )}
                    </span>
                  ))}
                </div>
              );
            })}

            <div className="contents">
              <span className="pr-2 text-left text-sm font-medium text-sky-700">Lluvia (mm)</span>
              {analysis.climate.map((c, i) => <span key={c.month} className={`py-1 text-ink-900 ${colMes(i)}`}>{Math.round(c.rain)}</span>)}
            </div>
            <div className="contents">
              <span className="pr-2 text-left text-sm font-medium text-sun-700">Temp. (°C)</span>
              {analysis.climate.map((c, i) => <span key={c.month} className={`py-1 text-ink-900 ${colMes(i)}`}>{Math.round(c.temp)}</span>)}
            </div>
          </div>
        </div>
      </div>

      <p className="mt-4 text-xs text-ink-500">Las ventanas vienen de las reglas agronómicas del análisis; el clima es el promedio histórico de cada mes.</p>
    </div>
  );
}