import { useEffect, useState } from 'react';
import { Check, Download } from 'lucide-react';

type EventoInstalar = Event & {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
};

declare global {
  interface Window {
    __eventoInstalar?: EventoInstalar | null;
  }
}

const esIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
const yaInstalada = () =>
  matchMedia('(display-mode: standalone)').matches ||
  (navigator as Navigator & { standalone?: boolean }).standalone === true;

export default function InstallButton() {
  const [evento, setEvento] = useState<EventoInstalar | null>(() => window.__eventoInstalar ?? null);
  const [instalada, setInstalada] = useState(yaInstalada);

  useEffect(() => {
    const alOfrecer = (e: Event) => {
      e.preventDefault(); // guardamos el aviso para mostrarlo con nuestro botón
      setEvento(e as EventoInstalar);
    };
    const alInstalar = () => {
      setInstalada(true);
      setEvento(null);
    };
    window.addEventListener('beforeinstallprompt', alOfrecer);
    window.addEventListener('appinstalled', alInstalar);
    return () => {
      window.removeEventListener('beforeinstallprompt', alOfrecer);
      window.removeEventListener('appinstalled', alInstalar);
    };
  }, []);

  if (instalada) {
    return (
      <p className="inline-flex items-center gap-2 text-sm text-ink-500">
        <Check size={16} aria-hidden /> App instalada
      </p>
    );
  }

  if (evento) {
    return (
      <button
        type="button"
        onClick={async () => {
          await evento.prompt();
                    await evento.userChoice;
          window.__eventoInstalar = null;
          setEvento(null);
        }}
        className="inline-flex items-center gap-2 rounded-full bg-leaf-600 px-5 py-2 text-sm font-medium text-paper hover:bg-leaf-700"
      >
        <Download size={16} aria-hidden /> Instalar app
      </button>
    );
  }

  if (esIOS) {
    return (
      <p className="text-sm text-ink-500">
        Para instalarla en iPhone: toca Compartir y luego "Agregar a pantalla de inicio".
      </p>
    );
  }

  return null; // el navegador no ofrece instalación, o ya se rechazó en esta sesión
}