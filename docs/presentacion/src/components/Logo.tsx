import BrandMark from '@app/components/BrandMark';
import { deck } from '../content';

/** Marca: el mismo logo que la app (frontend/src/components/BrandMark.tsx). */
export function Mark({ size = 96, draw = true }: { size?: number; draw?: boolean }) {
  return <BrandMark size={size} draw={draw} />;
}

/** «Agro» + «Bytes» en verde, como en la barra lateral de la app. */
export function Wordmark({ className = '', dark = false }: { className?: string; dark?: boolean }) {
  const [a, b] = [deck.name.slice(0, 4), deck.name.slice(4)];
  return (
    <span className={`font-display font-semibold tracking-tight ${dark ? 'text-paper' : 'text-ink-900'} ${className}`}>
      {a}<span className={dark ? 'text-leaf-300' : 'text-leaf-600'}>{b}</span>
    </span>
  );
}

export default function Logo({ size = 'text-8xl', dark = false, mark = 112 }: { size?: string; dark?: boolean; mark?: number }) {
  return (
    <div className="flex items-center gap-6">
      <Mark size={mark} />
      <Wordmark className={size} dark={dark} />
    </div>
  );
}
