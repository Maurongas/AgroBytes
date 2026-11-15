import { useEffect, useRef, useState } from 'react';
import { MotionConfig } from 'framer-motion';
import { ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react';
import { slides, notesUi, type Speaker } from './content';
import { fill } from './data';
import { SLIDE_COMPONENTS } from './slides';
import SlideBoundary from './SlideBoundary';
import Stage from './Stage';
import { CHANNEL, TOTAL, parseHash, type DeckState, type Msg } from './useDeck';

const fmt = (ms: number) => {
  const s = Math.max(0, Math.floor(ms / 1000));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
};
const SPEAKER_TONE: Record<Speaker, string> = {
  Mia: 'bg-sky-500 text-paper', Mauro: 'bg-leaf-600 text-paper', Both: 'bg-sun-500 text-ink-900',
};
const PLANNED_END = slides.reduce<number[]>((acc, s) => [...acc, (acc.at(-1) ?? 0) + s.seconds], []);

/** Guion con los [→] (momentos de avanzar) resaltados. */
function Script({ text }: { text: string }) {
  const parts = fill(text).split('[→]');
  return (
    <>
      {parts.map((p, i) => (
        <span key={i}>
          {p}
          {i < parts.length - 1 && <span className="mx-1 inline-flex -translate-y-0.5 items-center rounded bg-leaf-600 px-1.5 text-sm font-semibold text-paper">→</span>}
        </span>
      ))}
    </>
  );
}

function Preview({ index, step, label }: { index: number; step: number; label: string }) {
  const C = SLIDE_COMPONENTS[index];
  return (
    <div>
      <p className="mb-2 text-xs uppercase tracking-widest text-paper/50">{label}</p>
      <div className="aspect-video overflow-hidden rounded-xl border border-paper/15 bg-orbit">
        {C ? (
          <MotionConfig reducedMotion="always">
            <Stage><SlideBoundary key={`${index}-${step}`} title={slides[index].title}><C step={step} preview /></SlideBoundary></Stage>
          </MotionConfig>
        ) : (
          <div className="flex h-full items-center justify-center text-paper/40">{notesUi.end}</div>
        )}
      </div>
    </div>
  );
}

export default function Presenter() {
  const [st, setSt] = useState<DeckState>(() => ({ ...parseHash(), startedAt: null, slideStartedAt: Date.now() }));
  const [connected, setConnected] = useState(false);
  const [now, setNow] = useState(Date.now());
  const bc = useRef<BroadcastChannel | null>(null);

  useEffect(() => {
    document.title = `${notesUi.title} · Field Shift`;
    const ch = new BroadcastChannel(CHANNEL);
    bc.current = ch;
    ch.onmessage = (e: MessageEvent<Msg>) => {
      if (e.data.type === 'state') { const { type: _t, ...rest } = e.data; setSt(rest); setConnected(true); }
    };
    ch.postMessage({ type: 'hello' } satisfies Msg);
    const t = setInterval(() => setNow(Date.now()), 500);
    return () => { ch.close(); clearInterval(t); };
  }, []);

  const send = (m: Msg) => bc.current?.postMessage(m);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const k = e.key;
      if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(k)) { e.preventDefault(); send({ type: 'nav', action: 'next' }); }
      else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); send({ type: 'nav', action: 'prev' }); }
      else if (k === 'Home') send({ type: 'nav', action: 'first' });
      else if (k === 'End') send({ type: 'nav', action: 'last' });
      else if (k === 'r' || k === 'R') send({ type: 'resetTimer' });
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const s = slides[st.slide];
  const total = st.startedAt ? now - st.startedAt : 0;
  const perSlide = st.startedAt ? now - st.slideStartedAt : 0;
  const over = perSlide / 1000 > s.seconds;
  const plannedEnd = PLANNED_END[st.slide] * 1000;
  const behind = st.startedAt ? total - plannedEnd : 0; // >0: vamos tarde respecto al final previsto de esta diapositiva
  const nextIsBuild = st.step < s.builds;

  return (
    <div className="flex h-full flex-col gap-5 overflow-auto bg-orbit p-6 text-paper">
      <header className="flex flex-wrap items-center gap-4">
        <span className="font-display text-3xl font-semibold">{st.slide + 1} / {TOTAL} · {s.title}</span>
        <span className={`rounded-full px-2.5 py-1 text-xs ${connected ? 'bg-ok/20 text-ok' : 'bg-danger/20 text-danger'}`}>
          {connected ? notesUi.connected : notesUi.waiting}
        </span>
        <div className="ml-auto flex items-center gap-6 font-mono">
          <div><p className="text-xs uppercase tracking-widest text-paper/50">{notesUi.total}</p><p className="text-4xl">{fmt(total)}</p></div>
          <div>
            <p className="text-xs uppercase tracking-widest text-paper/50">{notesUi.slide} · {fmt(s.seconds * 1000)}</p>
            <p className={`text-4xl ${over ? 'text-warn' : ''}`}>{fmt(perSlide)}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-widest text-paper/50">{notesUi.pace}</p>
            <p className={`text-2xl ${behind > 5000 ? 'text-warn' : 'text-ok'}`}>{behind > 0 ? '+' : '−'}{fmt(Math.abs(behind))}</p>
          </div>
        </div>
      </header>

      <div className="grid flex-1 grid-cols-5 gap-6">
        <section className="col-span-3 space-y-4">
          {s.script.map((l, i) => (
            <div key={i} className="rounded-2xl bg-orbit-soft p-5">
              <span className={`rounded-full px-3 py-1 text-sm font-semibold ${SPEAKER_TONE[l.who]}`}>{l.who === 'Both' ? notesUi.both : l.who}</span>
              <p className="mt-3 text-2xl leading-relaxed"><Script text={l.text} /></p>
            </div>
          ))}
          {s.buildNotes && (
            <ol className="space-y-1 text-base">
              {s.buildNotes.map((b, i) => (
                <li key={i} className={`rounded-lg px-3 py-1.5 ${i + 1 === st.step ? 'bg-leaf-600 text-paper' : i + 1 < st.step ? 'text-paper/40 line-through' : 'text-paper/80'}`}>
                  {i + 1}. {fill(b)}
                </li>
              ))}
            </ol>
          )}
        </section>

        <aside className="col-span-2 space-y-5">
          <Preview index={st.slide} step={st.step} label={notesUi.now} />
          <Preview index={nextIsBuild ? st.slide : st.slide + 1} step={nextIsBuild ? st.step + 1 : slides[st.slide + 1]?.builds ?? 0}
            label={nextIsBuild ? `${notesUi.nextBuild}: ${fill(s.buildNotes?.[st.step] ?? '')}` : `${notesUi.next}: ${slides[st.slide + 1]?.title ?? notesUi.end}`} />
          <div className="flex gap-3">
            <button onClick={() => send({ type: 'nav', action: 'prev' })} className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-orbit-soft py-3 hover:bg-paper/10"><ChevronLeft /> {notesUi.prev}</button>
            <button onClick={() => send({ type: 'nav', action: 'next' })} className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-leaf-600 py-3 hover:bg-leaf-700">{notesUi.advance} <ChevronRight /></button>
            <button onClick={() => send({ type: 'resetTimer' })} title={notesUi.reset} className="rounded-xl bg-orbit-soft px-4 hover:bg-paper/10"><RotateCcw size={18} /></button>
          </div>
          <p className="text-xs text-paper/40">{notesUi.help}</p>
        </aside>
      </div>
    </div>
  );
}
