import { useEffect, useState, type ReactNode } from 'react';
import { Check, Eraser, Hexagon, Move, PenLine, Square, Trash2, Undo2 } from 'lucide-react';
import { useStore } from '../../store/useStore';

export type Herramienta = 'poligono' | 'rectangulo';

const TONO = {
  normal: 'text-ink-700 hover:bg-surface-sunken',
  activo: 'bg-leaf-100 text-leaf-900',
  primario: 'bg-leaf-600 text-paper hover:bg-leaf-700',
  peligro: 'text-danger hover:bg-danger/10',
} as const;

interface BotonProps {
  onClick: () => void;
  label: string;
  tono?: keyof typeof TONO;
  disabled?: boolean;
  pressed?: boolean;
  children: ReactNode;
}

function Boton({ onClick, label, tono = 'normal', disabled, pressed, children }: BotonProps) {
  return (
    <button type="button" onClick={onClick} disabled={disabled} aria-label={label} aria-pressed={pressed}
      className={`flex min-h-11 min-w-11 items-center justify-center gap-2 rounded-xl px-3 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-leaf-600 disabled:opacity-40 ${TONO[tono]}`}>
      {children}
    </button>
  );
}

// Texto que se oculta en pantallas chicas (el aria-label del botón sigue ahí).
const Texto = ({ children }: { children: ReactNode }) => <span className="hidden sm:inline">{children}</span>;

interface Props {
  herramienta: Herramienta;
  onHerramienta: (h: Herramienta) => void;
  editando: boolean;
  onEditando: (v: boolean) => void;
  borrarPunto: boolean;
  onBorrarPunto: (v: boolean) => void;
  puedeDeshacer: boolean;
  onDeshacer: () => void;
  onIniciar: () => void;
  onTerminar: () => void;
  onBorrarTodo: () => void;
}

export default function DrawToolbar(p: Props) {
  const drawing = useStore((s) => s.drawing);
  const geometry = useStore((s) => s.geometry);
  const nPuntos = useStore((s) => s.points.length);
  const [confirmar, setConfirmar] = useState(false);

  useEffect(() => {
    if (!confirmar) return;
    const t = setTimeout(() => setConfirmar(false), 3000);
    return () => clearTimeout(t);
  }, [confirmar]);

  const hayAlgo = !!geometry || nPuntos > 0;
  const borrar = () => {
    if (!confirmar) { setConfirmar(true); return; }
    setConfirmar(false);
    p.onBorrarTodo();
  };

  return (
    <div role="toolbar" aria-label="Herramientas de dibujo"
      className="flex flex-wrap items-center gap-1 rounded-2xl border border-line bg-surface-raised p-1.5 shadow-card">
      {/* Forma */}
      <div role="group" aria-label="Forma de la parcela" className="flex rounded-xl bg-surface-sunken p-0.5">
        <Boton label="Polígono libre" pressed={p.herramienta === 'poligono'} tono={p.herramienta === 'poligono' ? 'activo' : 'normal'}
          onClick={() => p.onHerramienta('poligono')}>
          <Hexagon size={16} /><Texto>Polígono</Texto>
        </Boton>
        <Boton label="Rectángulo" pressed={p.herramienta === 'rectangulo'} tono={p.herramienta === 'rectangulo' ? 'activo' : 'normal'}
          onClick={() => p.onHerramienta('rectangulo')}>
          <Square size={16} /><Texto>Rectángulo</Texto>
        </Boton>
      </div>

      <Boton label={geometry ? 'Dibujar otra parcela' : 'Dibujar parcela'} tono="activo" onClick={p.onIniciar}>
        <PenLine size={16} /> {geometry ? 'Dibujar otra' : 'Dibujar parcela'}
      </Boton>

      {/* Mientras se dibuja */}
      {drawing && p.herramienta === 'poligono' && (
        <Boton label="Terminar parcela" tono="primario" disabled={nPuntos < 3} onClick={p.onTerminar}>
          <Check size={16} /> Terminar
        </Boton>
      )}
      {drawing && (
        <Boton label="Deshacer último punto" disabled={!p.puedeDeshacer} onClick={p.onDeshacer}>
          <Undo2 size={16} /><Texto>Deshacer</Texto>
        </Boton>
      )}

      {/* Con la parcela terminada */}
      {!drawing && geometry && (
        <Boton label={p.editando ? 'Terminar de editar' : 'Editar puntos'} pressed={p.editando}
          tono={p.editando ? 'primario' : 'normal'} onClick={() => p.onEditando(!p.editando)}>
          {p.editando ? <Check size={16} /> : <Move size={16} />}
          <Texto>{p.editando ? 'Listo' : 'Editar puntos'}</Texto>
        </Boton>
      )}
      {!drawing && geometry && p.editando && (
        <>
          <Boton label="Borrar un punto" pressed={p.borrarPunto} tono={p.borrarPunto ? 'activo' : 'normal'}
            onClick={() => p.onBorrarPunto(!p.borrarPunto)}>
            <Eraser size={16} /><Texto>Borrar punto</Texto>
          </Boton>
          <Boton label="Deshacer último cambio" disabled={!p.puedeDeshacer} onClick={p.onDeshacer}>
            <Undo2 size={16} /><Texto>Deshacer</Texto>
          </Boton>
        </>
      )}

      {hayAlgo && (
        <Boton label={confirmar ? 'Confirmar: borrar todo' : 'Borrar todo'} tono="peligro" onClick={borrar}>
          <Trash2 size={16} />
          {confirmar ? <span>¿Borrar todo?</span> : <Texto>Borrar todo</Texto>}
        </Boton>
      )}
    </div>
  );
}
