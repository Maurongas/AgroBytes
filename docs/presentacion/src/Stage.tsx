import { useEffect, useRef, useState, type ReactNode } from 'react';

export const STAGE_W = 1600;
export const STAGE_H = 900;

/**
 * Lienzo fijo de 1600×900 escalado para caber en su contenedor (16:9, con bandas si hace falta).
 * Así se ve igual en 1920×1080, en una laptop 1366×768 o en la miniatura de las notas.
 */
export default function Stage({ children, className = '' }: { children: ReactNode; className?: string }) {
  const box = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0);
  useEffect(() => {
    const el = box.current;
    if (!el) return;
    const fit = () => setScale(Math.min(el.clientWidth / STAGE_W, el.clientHeight / STAGE_H));
    fit();
    const ro = new ResizeObserver(fit);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return (
    <div ref={box} className={`relative h-full w-full overflow-hidden ${className}`}>
      <div className="absolute left-1/2 top-1/2 overflow-hidden"
        style={{ width: STAGE_W, height: STAGE_H, transform: `translate(-50%, -50%) scale(${scale})`, visibility: scale ? 'visible' : 'hidden' }}>
        {children}
      </div>
    </div>
  );
}
