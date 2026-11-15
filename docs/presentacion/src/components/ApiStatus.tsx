import { AnimatePresence, motion } from 'framer-motion';
import { ExternalLink } from 'lucide-react';
import { ui } from '../content';
import { isLiveData } from '../data';
import { API, API_HOST, useApiLog, type LogEntry } from '../live';

const shortPath = (p: string) => p.replace('/api/v1', '').replace('?guardar=false', '');
const statusTone = (s: LogEntry['status']) =>
  s === 'ERR' ? 'text-danger' : s === '…' ? 'text-sun-700' : typeof s === 'number' && s < 300 ? 'text-ok' : 'text-warn';

/** Última petición real al backend (barra de la ventana de la app). */
export function ApiTicker() {
  const log = useApiLog();
  const last = log.at(-1);
  if (!isLiveData || !last) {
    return <span className="ml-auto font-mono text-sm text-ink-400">{ui.sampleData}</span>;
  }
  return (
    <span className="ml-auto flex min-w-0 items-center gap-2 font-mono text-sm text-ink-500" title={API_HOST}>
      <motion.span className="h-2.5 w-2.5 shrink-0 rounded-full bg-ok" animate={{ opacity: [1, 0.3, 1] }} transition={{ duration: 1.2, repeat: Infinity }} />
      <AnimatePresence mode="wait">
        <motion.span key={`${last.id}-${last.status}`} className="flex min-w-0 items-center gap-2"
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.2 }}>
          <span className="text-sky-700">{last.method}</span>
          <span className="truncate text-ink-700">{shortPath(last.path)}</span>
          <span className={`font-semibold ${statusTone(last.status)}`}>{last.status === '…' ? '…' : last.status}</span>
          {last.ms != null && <span>{last.ms} ms</span>}
          {last.kb != null && <span className="text-ink-400">{last.kb} kB</span>}
        </motion.span>
      </AnimatePresence>
    </span>
  );
}

/** Insignia del encabezado: EN VIVO (con enlace a la documentación de la API) o datos de ejemplo. */
export function LiveBadge() {
  if (!isLiveData) {
    return <span className="ml-auto rounded-full border border-line bg-surface-raised px-4 py-1.5 text-base text-ink-500">{ui.sampleData}</span>;
  }
  return (
    <span className="ml-auto flex items-center gap-3">
      <span className="flex items-center gap-2 rounded-full bg-danger px-4 py-1.5 text-base font-semibold tracking-wide text-paper shadow-card">
        <motion.span className="h-2.5 w-2.5 rounded-full bg-paper" animate={{ opacity: [1, 0.2, 1] }} transition={{ duration: 1.2, repeat: Infinity }} />
        {ui.live}
      </span>
      <a href={`${API}/docs`} target="_blank" rel="noreferrer" data-interactive
        className="flex items-center gap-1.5 rounded-full border border-line bg-surface-raised px-4 py-1.5 text-base text-ink-700 hover:border-leaf-300">
        {ui.apiDocs} <ExternalLink size={15} />
      </a>
    </span>
  );
}

/** Líneas del registro para el escaneo de la pestaña NASA data. */
export function LogLines({ n = 3 }: { n?: number }) {
  const log = useApiLog();
  return (
    <div className="space-y-1 font-mono text-base">
      {log.slice(-n).map((e) => (
        <p key={e.id} className="flex gap-3">
          <span className="text-sky-300">{e.method}</span>
          <span className="flex-1 truncate">{shortPath(e.path)}{e.note ? <span className="text-paper/50"> · {e.note}</span> : null}</span>
          <span className={e.status === '…' ? 'animate-blink text-sun-300' : e.status === 'ERR' ? 'text-danger' : 'text-leaf-300'}>{e.status}</span>
          {e.ms != null && <span className="w-20 text-right text-paper/60">{e.ms} ms</span>}
        </p>
      ))}
    </div>
  );
}
