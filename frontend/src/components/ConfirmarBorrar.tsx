import { useEffect, useRef } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Trash2 } from 'lucide-react';
import type { AnalysisSummary } from '../api/types';
import { cropName } from '../lib/crops';
import { formatoFecha, PRIORITY_LABEL } from '../lib/etiquetas';

/** Ventana para confirmar el borrado de un análisis. `fila = null` la oculta. */
export default function ConfirmarBorrar({ fila, onCancelar, onConfirmar }: {
  fila: AnalysisSummary | null;
  onCancelar: () => void;
  onConfirmar: (fila: AnalysisSummary) => void;
}) {
  const cancelarRef = useRef<HTMLButtonElement>(null);

  // Al abrir: foco en "Cancelar" (la opción segura) y Esc para cerrar.
  useEffect(() => {
    if (!fila) return;
    const previo = document.activeElement as HTMLElement | null;
    cancelarRef.current?.focus();
    const alTeclear = (e: KeyboardEvent) => { if (e.key === 'Escape') onCancelar(); };
    window.addEventListener('keydown', alTeclear);
    return () => {
      window.removeEventListener('keydown', alTeclear);
      previo?.focus();
    };
  }, [fila, onCancelar]);

  return (
    <AnimatePresence>
      {fila && (
        <motion.div className="fixed inset-0 z-50 flex items-end justify-center bg-black/50 p-4 backdrop-blur-sm sm:items-center"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onCancelar}>
          <motion.div role="alertdialog" aria-modal="true" aria-labelledby="borrar-titulo" aria-describedby="borrar-texto"
            className="w-full max-w-sm rounded-card border border-line bg-surface-raised p-6 shadow-card"
            initial={{ opacity: 0, y: 24, scale: 0.96 }} animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 24, scale: 0.96 }} transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
            onClick={(e) => e.stopPropagation()}>
            <span className="flex h-12 w-12 items-center justify-center rounded-full bg-danger/10 text-danger">
              <Trash2 size={22} aria-hidden />
            </span>
            <h2 id="borrar-titulo" className="mt-4 font-display text-xl font-semibold">¿Borrar este análisis?</h2>
            <div className="mt-3 rounded-xl bg-surface-sunken p-3 text-sm">
              <p className="font-medium text-ink-900">{cropName(fila.currentCrop)} · {fila.areaHa.toFixed(1)} ha</p>
              <p className="text-ink-700">{PRIORITY_LABEL[fila.priority]} · {formatoFecha(fila.createdAt)}</p>
            </div>
            <p id="borrar-texto" className="mt-3 text-sm text-ink-700">
              Se quitará de tu historial y de este dispositivo. Esta acción no se puede deshacer.
            </p>
            <div className="mt-6 flex gap-3">
              <button ref={cancelarRef} onClick={onCancelar}
                className="flex-1 rounded-full border border-line py-2 text-sm font-medium text-ink-900 hover:bg-surface-sunken">
                Cancelar
              </button>
              <button onClick={() => onConfirmar(fila)}
                className="flex flex-1 items-center justify-center gap-1.5 rounded-full bg-danger py-2 text-sm font-medium text-paper hover:opacity-90">
                <Trash2 size={16} aria-hidden /> Borrar
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
