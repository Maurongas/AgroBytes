import { useStore } from '../store/useStore';

export default function SinAnalisis({ titulo }: { titulo: string }) {
  const goTo = useStore((s) => s.goTo);
  return (
    <div className="flex h-full flex-col items-center justify-center gap-3 p-6 text-center">
      <h1 className="font-display text-2xl font-semibold">{titulo}</h1>
      <p className="max-w-sm text-sm text-ink-500">Primero analiza una parcela para ver esta sección.</p>
      <button onClick={() => goTo('select')}
        className="rounded-full bg-leaf-600 px-5 py-2 text-sm font-medium text-paper hover:bg-leaf-700">
        Analizar una parcela
      </button>
    </div>
  );
}