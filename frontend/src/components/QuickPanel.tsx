import { useEffect, useMemo, useRef, useState, useSyncExternalStore, type CSSProperties, type PointerEvent, type ReactNode } from 'react';
import CropIcon from './CropIcon';
import { useQuery } from '@tanstack/react-query';
import * as turf from '@turf/turf';
import { motion } from 'framer-motion';
import { Droplets, Sprout, TrendingUp, ArrowRight, Check } from 'lucide-react';
import { useStore } from '../store/useStore';
import { getSoil } from '../api/client';
import { crops } from '../lib/crops';
import { texturaLabel } from '../lib/etiquetas';
import { useT } from '../lib/i18n';
import type { Priority, SoilTexture } from '../api/types';

const PRIORITIES: { id: Priority; title: [string, string]; text: [string, string]; icon: typeof Droplets; tone: string }[] = [
  { id: 'water', title: ['Ahorrar agua', 'Save water'], text: ['Menos riego, más retención', 'Less irrigation, more retention'], icon: Droplets, tone: 'text-sky-500' },
  { id: 'nitrogen', title: ['Regenerar nitrógeno', 'Restore nitrogen'], text: ['Suelo más fértil con leguminosas', 'More fertile soil with legumes'], icon: Sprout, tone: 'text-nitro' },
  { id: 'yield', title: ['Maximizar rendimiento', 'Maximize yield'], text: ['Mayor producción por hectárea', 'Higher production per hectare'], icon: TrendingUp, tone: 'text-leaf-500' },
];

const TEXTURAS: SoilTexture[] = ['sandy', 'loam', 'clay'];

/** Devuelve `valor` pero solo después de que deja de cambiar `ms` milisegundos (evita pedir suelo en cada arrastre). */
function useRetardo<T>(valor: T, ms: number): T {
  const [v, setV] = useState(valor);
  useEffect(() => {
    const t = setTimeout(() => setV(valor), ms);
    return () => clearTimeout(t);
  }, [valor, ms]);
  return v;
}

function Chip({ activo, onClick, children }: { activo: boolean; onClick: () => void; children: ReactNode }) {
  return (
    <button type="button" aria-pressed={activo} onClick={onClick}
      className={`rounded-full border px-4 py-2 text-sm transition-colors ${
        activo ? 'border-leaf-600 bg-leaf-50 font-medium text-leaf-900' : 'border-line bg-surface-raised text-ink-700 hover:border-leaf-300'}`}>
      {children}
    </button>
  );
}

/**
 * En celular el panel es una hoja inferior con cuatro alturas:
 *  - oculto: solo el asa y una línea de estado (el mapa queda libre casi por completo)
 *  - recogido: título, estado y botón «Analizar»
 *  - medio: la mitad de la pantalla
 *  - completo: casi toda la pantalla
 * Se arrastra desde la cabecera o se toca el asa para abrir/recoger. En pantallas de 1024 px o más es un panel lateral fijo (con el menú lateral no cabe antes).
 */
type Posicion = 'oculto' | 'recogido' | 'medio' | 'completo';
const ORDEN: Posicion[] = ['oculto', 'recogido', 'medio', 'completo'];
const ES_ESCRITORIO = '(min-width: 1024px)'; // igual que el prefijo lg: de Tailwind

const suscribirAncho = (avisar: () => void) => {
  const mq = window.matchMedia(ES_ESCRITORIO);
  mq.addEventListener('change', avisar);
  return () => mq.removeEventListener('change', avisar);
};
const useEsEscritorio = () => useSyncExternalStore(suscribirAncho, () => window.matchMedia(ES_ESCRITORIO).matches, () => true);

interface Props {
  onAnalyze: () => void;
  pending: boolean;
  error?: string | null;
}

export default function QuickPanel({ onAnalyze, pending, error }: Props) {
  const t = useT();
  const { geometry, areaHa, parcelError, crop, priority, soil, irrigated, setCrop, setPriority, setSoil, setIrrigated } = useStore();

  // Suelo estimado en el centro de la parcela (GeoJSON es [lon, lat]). El retardo evita una consulta por cada arrastre de punto.
  const centro = useMemo(() => (geometry ? turf.centroid(geometry).geometry.coordinates : null), [geometry]);
  const centroQuieto = useRetardo(centro, 800);
  const detectado = useQuery({
    queryKey: ['soil', centroQuieto?.[1].toFixed(3), centroQuieto?.[0].toFixed(3)],
    queryFn: () => getSoil(centroQuieto![1], centroQuieto![0]),
    enabled: centroQuieto !== null,
    staleTime: Infinity,
    retry: false,
  });
  const ready = !!geometry && !!crop && !!priority;
  const missing = !geometry ? t('Dibuja tu parcela en el mapa', 'Draw your field on the map')
    : !crop ? t('Elige tu cultivo actual', 'Choose your current crop')
    : !priority ? t('Elige tu prioridad', 'Choose your priority') : '';
  const estado = parcelError ?? (ready && areaHa ? t(`${areaHa.toFixed(1)} ha · listo para analizar`, `${areaHa.toFixed(1)} ha · ready to analyze`) : missing);
  const escritorio = useEsEscritorio();

  const [posicion, setPosicion] = useState<Posicion>(() => (useStore.getState().geometry ? 'medio' : 'recogido'));
  // En celular, con el panel oculto, sus botones no deben recibir foco ni clics.
  const oculto = !escritorio && posicion === 'oculto';
  const [arrastre, setArrastre] = useState<number | null>(null); // altura mientras el dedo arrastra
  const [medidas, setMedidas] = useState({ contenedor: 0, oculto: 48, recogido: 140 });

  const panelRef = useRef<HTMLElement>(null);
  const cabeceraRef = useRef<HTMLDivElement>(null);
  const asaRef = useRef<HTMLButtonElement>(null);
  const pieRef = useRef<HTMLDivElement>(null);
  const gesto = useRef<{ y: number; alto: number; movio: boolean } | null>(null);
  const finArrastre = useRef(0); // momento en que terminó el último arrastre (para ignorar el clic que lo sigue)

  // Mide el espacio disponible, el asa (versión oculta) y cabecera + botón (versión recogida).
  useEffect(() => {
    const padre = panelRef.current?.parentElement;
    const cabecera = cabeceraRef.current;
    const asa = asaRef.current;
    const pie = pieRef.current;
    if (!padre || !cabecera || !asa || !pie) return;
    const ro = new ResizeObserver(() =>
      setMedidas({
        contenedor: padre.clientHeight,
        oculto: asa.offsetHeight + 2, // + borde del panel
        recogido: cabecera.offsetHeight + pie.offsetHeight,
      }));
    [padre, cabecera, asa, pie].forEach((el) => ro.observe(el));
    return () => ro.disconnect();
  }, []);

  // Al empezar a dibujar se oculta para dejar libre el mapa; al terminar la parcela se abre para elegir cultivo.
  useEffect(
    () =>
      useStore.subscribe((s, antes) => {
        if (s.drawing && !antes.drawing) setPosicion('oculto');
        else if (s.geometry && !antes.geometry) setPosicion('medio');
      }),
    [],
  );

  const altos: Record<Posicion, number> = {
    oculto: medidas.oculto,
    recogido: medidas.recogido,
    medio: Math.max(medidas.recogido, Math.round(medidas.contenedor * 0.5)),
    completo: Math.max(medidas.recogido, Math.round(medidas.contenedor * 0.88)),
  };
  const alto = arrastre ?? altos[posicion];
  const limitar = (h: number) => Math.min(Math.max(h, altos.oculto), altos.completo);

  const alBajar = (e: PointerEvent<HTMLDivElement>) => {
    if (window.matchMedia(ES_ESCRITORIO).matches) return;
    gesto.current = { y: e.clientY, alto, movio: false };
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const alMover = (e: PointerEvent<HTMLDivElement>) => {
    const g = gesto.current;
    if (!g) return;
    const dy = g.y - e.clientY; // positivo = hacia arriba
    if (!g.movio && Math.abs(dy) < 6) return;
    g.movio = true;
    setArrastre(limitar(g.alto + dy));
  };

  const alSoltar = (e: PointerEvent<HTMLDivElement>) => {
    const g = gesto.current;
    gesto.current = null;
    if (!g?.movio) return; // fue un toque: lo resuelve el clic del asa
    finArrastre.current = Date.now();
    const final = limitar(g.alto + g.y - e.clientY);
    let destino = ORDEN.reduce((a, b) => (Math.abs(altos[b] - final) < Math.abs(altos[a] - final) ? b : a));
    // Un deslizamiento corto pero claro también cambia de altura.
    const movido = final - g.alto;
    if (destino === posicion && Math.abs(movido) > 40) {
      destino = ORDEN[Math.min(ORDEN.length - 1, Math.max(0, ORDEN.indexOf(posicion) + Math.sign(movido)))];
    }
    setPosicion(destino);
    setArrastre(null);
  };

  const alCancelar = () => {
    gesto.current = null;
    setArrastre(null);
  };

  const alTocarAsa = () => {
    if (Date.now() - finArrastre.current < 350) return; // el clic que sigue a un arrastre no cuenta como toque
    setPosicion((p) => (p === 'oculto' ? 'medio' : 'oculto'));
  };

  return (
    <aside ref={panelRef} style={{ '--alto': `${alto}px` } as CSSProperties}
      className={`absolute inset-x-0 bottom-0 z-[1100] flex h-(--alto) flex-col overflow-hidden rounded-t-panel border border-line bg-surface-raised/95 shadow-lift backdrop-blur
        lg:inset-x-auto lg:bottom-4 lg:right-4 lg:top-4 lg:h-auto lg:w-[360px] lg:rounded-panel xl:w-[400px]
        ${arrastre === null ? 'transition-[height] duration-300 ease-out' : ''}`}>

      {/* Cabecera: en celular se arrastra para subir o bajar el panel */}
      <div ref={cabeceraRef} onPointerDown={alBajar} onPointerMove={alMover} onPointerUp={alSoltar} onPointerCancel={alCancelar}
        className="shrink-0 touch-none select-none px-5 pb-3 lg:touch-auto lg:select-auto lg:pt-5">
        <button ref={asaRef} type="button" onClick={alTocarAsa} aria-expanded={posicion !== 'oculto'}
          aria-label={posicion === 'oculto' ? t('Mostrar el panel de la parcela', 'Show the field panel') : t('Ocultar el panel y ver el mapa', 'Hide the panel and see the map')}
          className="flex min-h-11 w-full flex-col items-center justify-center gap-1 py-2 lg:hidden">
          <span className="h-1.5 w-10 rounded-full bg-line-strong" />
          {posicion === 'oculto' && (
            <span className={`text-xs font-medium ${parcelError ? 'text-danger' : 'text-ink-700'}`}>{t('Tu parcela', 'Your field')} · {estado || t('listo', 'ready')}</span>
          )}
        </button>
        <h1 className="font-display text-2xl font-semibold">{t('Tu parcela', 'Your field')}</h1>
        <p aria-live="polite" className={`mt-0.5 text-sm ${parcelError ? 'text-danger' : ready ? 'text-leaf-700' : 'text-ink-500'}`}>{estado}</p>
      </div>

      {/* Opciones: se desplazan hacia arriba o abajo cuando no caben */}
      <div inert={oculto} className="min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 pb-2">
        <section className="mt-2">
          <p className="text-xs font-semibold uppercase tracking-widest text-ink-500">1 · {t('Terreno', 'Field')}</p>
          <div className="mt-2 flex items-center gap-2 text-sm">
            <span className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full ${geometry ? 'bg-leaf-600 text-paper' : 'bg-surface-sunken text-ink-400'}`}>
              {geometry && <Check size={13} />}
            </span>
            <span className={parcelError ? 'text-danger' : 'text-ink-700'}>
              {parcelError ?? (geometry && areaHa
                ? t(`${areaHa.toFixed(1)} hectáreas marcadas`, `${areaHa.toFixed(1)} hectares marked`)
                : t('Aún no has dibujado tu parcela', 'You have not drawn your field yet'))}
            </span>
          </div>
        </section>

        <section className="mt-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-ink-500">2 · {t('Cultivo actual', 'Current crop')}</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {crops().map((c) => (
              <motion.button key={c.id} whileTap={{ scale: 0.96 }} onClick={() => setCrop(c.id)}
                className={`inline-flex items-center gap-1.5 rounded-full border px-4 py-2 text-sm transition-colors ${
                  crop === c.id ? 'border-leaf-600 bg-leaf-50 font-medium text-leaf-900' : 'border-line bg-surface-raised text-ink-700 hover:border-leaf-300'}`}>
                <CropIcon id={c.id} size={16} /> {c.name}
              </motion.button>
            ))}
          </div>
        </section>

        <section className="mt-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-ink-500">3 · {t('Tu prioridad', 'Your priority')}</p>
          <div className="mt-2 flex flex-col gap-2">
            {PRIORITIES.map(({ id, title, text, icon: Icon, tone }) => (
              <motion.button key={id} whileHover={{ y: -2 }} whileTap={{ scale: 0.98 }} onClick={() => setPriority(id)}
                className={`flex items-center gap-3 rounded-2xl border p-3 text-left transition-colors ${
                  priority === id ? 'border-leaf-600 bg-leaf-50' : 'border-line bg-surface-raised hover:border-leaf-300'}`}>
                <Icon size={22} className={`shrink-0 ${tone}`} />
                <span>
                  <span className="block text-sm font-medium">{t(...title)}</span>
                  <span className="block text-xs text-ink-500">{t(...text)}</span>
                </span>
              </motion.button>
            ))}
          </div>
        </section>

        {/* Plegable para no alargar el panel en el celular */}
        <details className="mt-5 rounded-2xl border border-line p-3">
          <summary className="cursor-pointer text-xs font-semibold uppercase tracking-widest text-ink-500">
            4 · {t('Suelo y riego (opcional)', 'Soil and irrigation (optional)')}
          </summary>
          <div className="mt-3 space-y-4">
            <div>
              <p className="text-sm font-medium">{t('Tipo de suelo', 'Soil type')}</p>
              <p className="mt-1 text-xs text-ink-500" role="status">
                {!geometry
                  ? t('Dibuja tu parcela para estimarlo.', 'Draw your field to estimate it.')
                  : detectado.isPending || detectado.isFetching // isPending: también durante el retardo previo a la consulta
                    ? t('Estimando con ISRIC SoilGrids…', 'Estimating with ISRIC SoilGrids…')
                    : detectado.data
                      ? t(`Estimado: ${texturaLabel(detectado.data.texture)} (arcilla ${Math.round(detectado.data.clayPct)} %, arena ${Math.round(detectado.data.sandPct)} %)`,
                        `Estimated: ${texturaLabel(detectado.data.texture)} (clay ${Math.round(detectado.data.clayPct)} %, sand ${Math.round(detectado.data.sandPct)} %)`)
                      : t('No hay dato para este punto; elige el tipo tú.', 'No data for this point; choose the type yourself.')}
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                <Chip activo={soil === null} onClick={() => setSoil(null)}>{t('Automático', 'Automatic')}</Chip>
                {TEXTURAS.map((x) => (
                  <Chip key={x} activo={soil?.texture === x} onClick={() => setSoil({ texture: x })}>{texturaLabel(x)}</Chip>
                ))}
              </div>
            </div>
            <div>
              <p className="text-sm font-medium">{t('¿Tiene riego?', 'Is it irrigated?')}</p>
              <div className="mt-2 flex flex-wrap gap-2">
                <Chip activo={!irrigated} onClick={() => setIrrigated(false)}>{t('Temporal (solo lluvia)', 'Rainfed (rain only)')}</Chip>
                <Chip activo={irrigated} onClick={() => setIrrigated(true)}>{t('Con riego', 'Irrigated')}</Chip>
              </div>
            </div>
          </div>
        </details>
      </div>

      {/* Pie: el botón siempre queda visible, también con el panel recogido */}
      <div ref={pieRef} inert={oculto} className="shrink-0 border-t border-line-soft px-5 pb-4 pt-3 lg:pb-5">
        {error && <p role="alert" className="mb-3 rounded-xl bg-danger/10 p-3 text-sm text-danger">{error}</p>}
        <button onClick={onAnalyze} disabled={!ready || pending}
          className="flex w-full items-center justify-center gap-2 rounded-2xl bg-leaf-600 px-4 py-3 font-medium text-paper transition-colors hover:bg-leaf-700 disabled:opacity-50">
          {pending ? t('Analizando…', 'Analyzing…') : t('Analizar parcela', 'Analyze field')} {!pending && <ArrowRight size={18} />}
        </button>
      </div>
    </aside>
  );
}
