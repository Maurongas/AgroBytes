import { useEffect, useRef } from 'react';
import { animate } from 'framer-motion';

export default function CountUp({ value, decimals = 0 }: { value: number; decimals?: number }) {
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    const controls = animate(0, value, {
      duration: 1.2,
      ease: [0.22, 1, 0.36, 1],
      onUpdate: (v) => { if (ref.current) ref.current.textContent = v.toFixed(decimals); },
    });
    return () => controls.stop();
  }, [value, decimals]);
  return <span ref={ref}>0</span>;
}