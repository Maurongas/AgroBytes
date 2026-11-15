import { useCallback, useEffect, useRef, useState } from 'react';
import { slides } from './content';

/** Canal entre la presentación y la ventana de notas (misma origin, misma máquina). */
export const CHANNEL = 'agrobytes-pitch';

export interface Pos { slide: number; step: number }
export interface DeckState extends Pos {
  /** ms epoch en que empezó la charla (primer avance); null = cronómetro en 0 */
  startedAt: number | null;
  slideStartedAt: number;
}
export type Msg =
  | ({ type: 'state' } & DeckState)
  | { type: 'hello' }
  | { type: 'nav'; action: 'next' | 'prev' | 'first' | 'last' }
  | { type: 'goto'; slide: number }
  | { type: 'resetTimer' };

export const TOTAL = slides.length;
const buildsOf = (i: number) => slides[i]?.builds ?? 0;
const clamp = (n: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, n));

/** #/4 o #/4/2 (diapositiva 1-based, paso opcional). */
export function parseHash(hash = location.hash): Pos {
  const m = hash.match(/^#\/(\d+)(?:\/(\d+))?/);
  if (!m) return { slide: 0, step: 0 };
  const slide = clamp(Number(m[1]) - 1, 0, TOTAL - 1);
  return { slide, step: clamp(Number(m[2] ?? 0), 0, buildsOf(slide)) };
}
const toHash = ({ slide, step }: Pos) => `#/${slide + 1}${step ? `/${step}` : ''}`;

export function isTyping(t: EventTarget | null) {
  const el = t as HTMLElement | null;
  return !!el && (['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName) || el.isContentEditable);
}

export function useDeck() {
  const [pos, setPos] = useState<Pos>(() => parseHash());
  const [dir, setDir] = useState(1);
  const [startedAt, setStartedAt] = useState<number | null>(null);
  const [slideStartedAt, setSlideStartedAt] = useState(() => Date.now());
  const bc = useRef<BroadcastChannel | null>(null);

  const posRef = useRef(pos);

  /** Única forma de moverse: actualiza la posición (y el cronómetro de la diapositiva si cambia). */
  const go = useCallback((next: Pos, d: number) => {
    const prev = posRef.current;
    if (prev.slide === next.slide && prev.step === next.step) return;
    posRef.current = next;
    if (prev.slide !== next.slide) setSlideStartedAt(Date.now());
    setPos(next);
    setDir(d);
  }, []);

  const next = useCallback(() => {
    setStartedAt((s) => s ?? Date.now());
    const p = posRef.current;
    if (p.step < buildsOf(p.slide)) go({ ...p, step: p.step + 1 }, 1);
    else if (p.slide < TOTAL - 1) go({ slide: p.slide + 1, step: 0 }, 1);
  }, [go]);

  const prev = useCallback(() => {
    const p = posRef.current;
    if (p.step > 0) go({ ...p, step: p.step - 1 }, -1);
    else if (p.slide > 0) go({ slide: p.slide - 1, step: buildsOf(p.slide - 1) }, -1); // vuelve a la anterior ya construida
  }, [go]);

  const goto = useCallback((slide: number) => {
    const s = clamp(slide, 0, TOTAL - 1);
    go({ slide: s, step: 0 }, s >= posRef.current.slide ? 1 : -1);
  }, [go]);

  // URL ↔ posición
  useEffect(() => {
    const h = toHash(pos);
    if (location.hash !== h) history.replaceState(null, '', h);
  }, [pos]);
  useEffect(() => {
    const onHash = () => go(parseHash(), 1);
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, [go]);

  // Ventana de notas
  const api = useRef({ next, prev, goto });
  api.current = { next, prev, goto };
  useEffect(() => {
    if (typeof BroadcastChannel === 'undefined') return;
    const ch = new BroadcastChannel(CHANNEL);
    bc.current = ch;
    ch.onmessage = (e: MessageEvent<Msg>) => {
      const m = e.data;
      if (m.type === 'nav') {
        if (m.action === 'next') api.current.next();
        else if (m.action === 'prev') api.current.prev();
        else api.current.goto(m.action === 'first' ? 0 : TOTAL - 1);
      } else if (m.type === 'goto') api.current.goto(m.slide);
      else if (m.type === 'resetTimer') { setStartedAt(null); setSlideStartedAt(Date.now()); }
      else if (m.type === 'hello') ch.postMessage(stateRef.current);
    };
    return () => { ch.close(); bc.current = null; };
  }, []);
  const state: Msg = { type: 'state', ...pos, startedAt, slideStartedAt };
  const stateRef = useRef(state);
  stateRef.current = state;
  useEffect(() => {
    bc.current?.postMessage(stateRef.current);
  }, [pos, startedAt, slideStartedAt]);

  return { ...pos, dir, next, prev, goto, startedAt };
}
