import { motion } from 'framer-motion';
import { Bean, CloudRain, Droplets, Leaf, Satellite, Sprout, Sun, Thermometer, Wheat, type LucideIcon } from 'lucide-react';
import { EASE } from './ui';

/**
 * Fondo animado de la portada y el cierre: iconos del campo que flotan, «polen» que sube
 * y un satélite que orbita. Todo en coordenadas del escenario (1600×900), sin interacción.
 * Con prefers-reduced-motion framer-motion quita los movimientos y deja solo los fundidos.
 */
const ICONS: { icon: LucideIcon; x: number; y: number; size: number; color: string }[] = [
  { icon: Wheat, x: 150, y: 150, size: 46, color: '#FFCF5C' },
  { icon: Droplets, x: 1380, y: 130, size: 40, color: '#7CC3EE' },
  { icon: Sprout, x: 1430, y: 560, size: 48, color: '#9CCB86' },
  { icon: Sun, x: 210, y: 560, size: 44, color: '#FFCF5C' },
  { icon: CloudRain, x: 1130, y: 70, size: 36, color: '#BFE0F5' },
  { icon: Bean, x: 420, y: 70, size: 34, color: '#9CCB86' },
  { icon: Leaf, x: 70, y: 360, size: 36, color: '#9CCB86' },
  { icon: Thermometer, x: 1510, y: 340, size: 34, color: '#F08A24' },
];

const DOTS = Array.from({ length: 34 }, (_, i) => ({
  x: (i * 397) % 1600,
  y: 120 + ((i * 211) % 760),
  r: 2 + (i % 4),
  dur: 6 + (i % 5) * 1.3,
  delay: (i * 0.37) % 6,
}));

// Órbita elíptica (inclinada) alrededor del título
const ORBIT = { cx: 800, cy: 400, rx: 660, ry: 190, tilt: -8 };
const ORBIT_PTS = (() => {
  const t = (ORBIT.tilt * Math.PI) / 180;
  return Array.from({ length: 61 }, (_, i) => {
    const a = (i / 60) * Math.PI * 2;
    const x = ORBIT.rx * Math.cos(a);
    const y = ORBIT.ry * Math.sin(a);
    return [ORBIT.cx + x * Math.cos(t) - y * Math.sin(t), ORBIT.cy + x * Math.sin(t) + y * Math.cos(t)];
  });
})();

export default function Floaters({ instant = false, orbit = true, dim = false }: { instant?: boolean; orbit?: boolean; dim?: boolean }) {
  const d = instant ? 0 : 1;
  return (
    <div className="pointer-events-none absolute inset-0" style={{ opacity: dim ? 0.5 : 1, transition: 'opacity .8s' }}>
      {/* Polen que sube */}
      {DOTS.map((p, i) => (
        <motion.span key={i} className="absolute rounded-full bg-sun-300"
          style={{ left: p.x, top: p.y, width: p.r * 2, height: p.r * 2 }}
          initial={{ opacity: 0, y: 0 }} animate={{ opacity: [0, 0.7, 0], y: -70 }}
          transition={{ duration: p.dur, delay: p.delay * d, repeat: Infinity, ease: 'easeOut' }} />
      ))}

      {/* Órbita + satélite */}
      {orbit && (
        <>
          <svg viewBox="0 0 1600 900" className="absolute inset-0 h-full w-full">
            <motion.ellipse cx={ORBIT.cx} cy={ORBIT.cy} rx={ORBIT.rx} ry={ORBIT.ry} fill="none" stroke="#FBF8F1" strokeOpacity={0.14}
              strokeWidth={1.5} strokeDasharray="4 10" transform={`rotate(${ORBIT.tilt} ${ORBIT.cx} ${ORBIT.cy})`}
              initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 2 * d, ease: 'easeInOut' }} />
          </svg>
          <motion.div className="absolute left-0 top-0" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 * d }}>
            <motion.div className="-ml-6 -mt-6 flex h-12 w-12 items-center justify-center rounded-full bg-orbit/70 text-paper shadow-[0_0_24px_4px_rgba(224,60,33,.35)] ring-1 ring-paper/20"
              animate={{ x: ORBIT_PTS.map((p) => p[0]), y: ORBIT_PTS.map((p) => p[1]) }}
              transition={{ duration: 22, repeat: Infinity, ease: 'linear' }}>
              <Satellite size={24} />
              <span className="absolute -right-0.5 -top-0.5 h-3 w-3 rounded-full bg-nasa-mark" />
            </motion.div>
          </motion.div>
        </>
      )}

      {/* Iconos que flotan */}
      {ICONS.map(({ icon: Icon, x, y, size, color }, i) => (
        <motion.div key={i} className="absolute" style={{ left: x, top: y }}
          initial={{ opacity: 0, scale: 0.4 }} animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: (0.6 + i * 0.15) * d, duration: 0.8, ease: EASE }}>
          <motion.div className="flex items-center justify-center rounded-full border border-paper/15 bg-paper/[0.07] p-4 backdrop-blur-sm"
            animate={{ y: [0, -18, 0], rotate: [-6, 6, -6] }}
            transition={{ duration: 5 + (i % 3) * 1.4, repeat: Infinity, ease: 'easeInOut', delay: i * 0.4 }}>
            <Icon size={size} color={color} strokeWidth={1.6} />
          </motion.div>
        </motion.div>
      ))}
    </div>
  );
}


/**
 * Título letra por letra: entra con desenfoque y luego cada letra flota en ola.
 * Desde la letra `accentAt` va en verde («Agro» + «Bytes»); por defecto, desde la 2.ª palabra.
 */
export function FloatingTitle({ text, className = '', delay = 0, instant = false, accentAt }: {
  text: string; className?: string; delay?: number; instant?: boolean; accentAt?: number;
}) {
  const d = instant ? 0 : 1;
  const accent = accentAt ?? (text.includes(' ') ? text.indexOf(' ') + 1 : Infinity);
  return (
    <h1 className={`whitespace-nowrap ${className}`} aria-label={text}>
      {[...text].map((ch, i) => (ch === ' ' ? <span key={i} className="inline-block w-[0.22em]" /> : (
        <motion.span key={i} className={`inline-block ${i >= accent ? 'text-leaf-300' : ''}`} aria-hidden
          initial={{ opacity: 0, y: 70, filter: 'blur(12px)' }} animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
          transition={{ delay: (delay + i * 0.07) * d, duration: 0.8, ease: EASE }}>
          <motion.span className="inline-block" animate={{ y: [0, -10, 0] }}
            transition={{ duration: 3.4, repeat: Infinity, ease: 'easeInOut', delay: 1.5 + i * 0.16 }}>
            {ch}
          </motion.span>
        </motion.span>
      )))}
    </h1>
  );
}
