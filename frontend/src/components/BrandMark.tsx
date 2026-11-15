import { motion } from 'framer-motion';

/** Logo de AgroBytes: una parcela dibujada + el punto rojo de NASA (igual que favicon.svg). */
export default function BrandMark({ size = 32, draw = false, className = '' }: { size?: number; draw?: boolean; className?: string }) {
  return (
    <svg viewBox="0 0 64 64" width={size} height={size} className={className} aria-hidden>
      <rect width="64" height="64" rx="16" fill="#12261F" />
      <motion.path d="M14 46 L24 16 L48 22 L44 48 Z" fill="#4E9F3D" fillOpacity={0.85} stroke="#FBF8F1" strokeWidth="3.5" strokeLinejoin="round"
        initial={draw ? { pathLength: 0, fillOpacity: 0 } : false} animate={{ pathLength: 1, fillOpacity: 0.85 }}
        transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }} />
      <motion.circle cx="50" cy="13" r="6" fill="#E03C21" initial={draw ? { scale: 0 } : false} animate={{ scale: 1 }}
        transition={{ delay: draw ? 1 : 0, type: 'spring', stiffness: 400, damping: 14 }} />
    </svg>
  );
}
