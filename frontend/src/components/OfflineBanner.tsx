import { useEffect } from 'react';
import { WifiOff } from 'lucide-react';
import { useStore } from '../store/useStore';
import { guardarAnalisis, guardarUltima, leerUltima, useOnline } from '../lib/offline';

export default function OfflineBanner() {
  const online = useOnline();
  const hayAnalisis = useStore((s) => s.analysis !== null);

  // 1) Cada análisis nuevo se guarda en el dispositivo.
  useEffect(
    () =>
      useStore.subscribe((s, anterior) => {
        if (s.analysis && s.analysis !== anterior.analysis) {
          guardarAnalisis(s.analysis);
          guardarUltima({ analysis: s.analysis, crop: s.crop, priority: s.priority });
        }
      }),
    [],
  );

  // 2) Si la app abre sin red y sin análisis, carga el último guardado.
  useEffect(() => {
    if (navigator.onLine || useStore.getState().analysis) return;
    const u = leerUltima();
    if (u) useStore.setState({ analysis: u.analysis, crop: u.crop, priority: u.priority, view: 'diagnosis' });
  }, []);

  if (online) return null;
  return (
    <div role="status" className="flex items-center gap-2 bg-sun-100 px-4 py-2 text-sm text-ink-900">
      <WifiOff size={16} />
      {hayAnalisis
        ? 'Sin conexión. Mostrando los datos guardados en este dispositivo.'
        : 'Sin conexión. Los análisis nuevos necesitan internet.'}
    </div>
  );
}
