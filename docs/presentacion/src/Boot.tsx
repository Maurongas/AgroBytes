import { motion } from 'framer-motion';
import { API_HOST, useApiLog } from './live';
import { deck } from './content';
import { Mark } from './components/Logo';

/** Pantalla de arranque: muestra en vivo las peticiones al backend mientras llega el análisis real. */
export default function Boot({ failed = false }: { failed?: boolean }) {
  const log = useApiLog();
  return (
    <div className="flex h-full flex-col items-center justify-center gap-8 bg-orbit text-paper">
      <div className="flex items-center gap-5">
        <Mark size={72} />
        <span className="font-display text-6xl font-semibold">Agro<span className="text-leaf-300">Bytes</span></span>
      </div>
      <div className="w-[min(640px,90vw)] rounded-2xl border border-paper/15 bg-black/30 p-5 font-mono text-sm">
        <p className="mb-3 text-paper/50">→ {API_HOST}</p>
        {log.map((e) => (
          <motion.p key={e.id} className="flex gap-3" initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }}>
            <span className="text-sky-300">{e.method}</span>
            <span className="flex-1 truncate">{e.path}</span>
            <span className={e.status === 'ERR' ? 'text-danger' : e.status === '…' ? 'animate-blink text-sun-300' : 'text-leaf-300'}>
              {e.status === '…' ? 'waiting…' : e.status}
            </span>
            {e.ms != null && <span className="w-16 text-right text-paper/60">{(e.ms / 1000).toFixed(1)} s</span>}
          </motion.p>
        ))}
        {failed && <p className="mt-3 text-sun-300">Backend not reachable → using sample data</p>}
      </div>
      <p className="text-sm text-paper/40">{deck.tagline}</p>
    </div>
  );
}
