# 05 · menaxmn: PWA completa + cliente API

Nov 14, 2026 · @Mia

## Qué te toca y en qué orden

La PWA todavía no existe: no hay manifest, service worker ni íconos propios (el favicon sigue siendo el logo morado de Vite). Tu trabajo es que Field Shift se instale en el celular y abra sin internet, y que el cliente de la API mande el `X-Device-Id` que el backend ya espera.

Hazlo en **dos PRs separados**, en este orden, porque los demás esperan el primero:

1. **PR A · `feature/api-cliente-device`** (30 min): `X-Device-Id`, `deleteAnalysis` y `getSoil` en `src/api/client.ts`. Fernando y Mía dependen de esto: avísales por el grupo en cuanto Mía lo mergee.
2. **PR B · `feature/pwa-instalable`** (2–3 h): vite-plugin-pwa, manifest, íconos reales, service worker, botón "Instalar app".

Solo toca `vite.config.ts`, `index.html`, `package.json`, `public/*`, `pwa-assets.config.ts`, `src/api/client.ts`, `src/lib/deviceId.ts` y el componente nuevo `src/components/InstallButton.tsx`. **No toques** `lib/offline.ts` ni `OfflineBanner.tsx` (son de Fernando): el service worker solo hace que la app *cargue* sin internet; guardar y restaurar el último análisis ya lo hace él.

## PR A · Cliente API: X-Device-Id, borrar y suelo

Antes de empezar pregunta a Mía si su PR #26 (`previewAnalysis`) ya está en `main`: también agrega código al final de `client.ts` y si no esperas habrá conflicto.

**Paso 1 · Rama**

```bash
cd frontend
git switch main && git pull
git switch -c feature/api-cliente-device
```

**Paso 2 · Crea `src/lib/deviceId.ts`.** Es el UUID anónimo que identifica este navegador; el backend lo usa para que cada quien vea solo su historial.

```ts
// Identificador anónimo del dispositivo. El backend lo pide en el header X-Device-Id
// (8–64 caracteres, solo letras, números, _ y -). Ver docs/ARQUITECTURA.md.
const KEY = 'fieldshift:deviceId';
const VALIDO = /^[A-Za-z0-9_-]{8,64}$/;

let enMemoria: string | null = null; // por si localStorage no está disponible

function nuevo(): string {
  return crypto.randomUUID();
}

export function getDeviceId(): string {
  if (enMemoria) return enMemoria;
  try {
    let id = localStorage.getItem(KEY);
    if (!id || !VALIDO.test(id)) {
      id = nuevo();
      localStorage.setItem(KEY, id);
    }
    enMemoria = id;
  } catch {
    enMemoria = nuevo();
  }
  return enMemoria;
}
```

**Paso 3 · Edita `src/api/client.ts`.** Hay cuatro cambios.

(a) Imports de arriba:

```ts
import type { AnalysisRequest, AnalysisResponse, AnalysisSummary, DetectedSoil } from './types';
import { mockAnalysis, mockHistory } from './mock';
import { getDeviceId } from '../lib/deviceId';
```

(b) Dentro de `request()`, el header nuevo y el caso 204 (el DELETE responde sin cuerpo y `res.json()` fallaría):

```ts
    res = await fetch(`${BASE}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'X-Device-Id': getDeviceId(),
        ...init?.headers,
      },
    });
```

```ts
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
```

(c) Al final del archivo, las dos funciones nuevas:

```ts
/** Borra un análisis guardado (DELETE /api/v1/analyses/{id}, responde 204). */
export async function deleteAnalysis(id: string): Promise<void> {
  if (USE_MOCK) return;
  await request<void>(`/api/v1/analyses/${encodeURIComponent(id)}`, { method: 'DELETE' });
}

/** Suelo estimado de un punto (GET /api/v1/soil). Devuelve null si no hay dato o falla: nunca debe bloquear el análisis. */
export async function getSoil(lat: number, lon: number): Promise<DetectedSoil | null> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 800));
    return { texture: 'loam', ph: 6.8, clayPct: 24, sandPct: 41, source: 'Ejemplo (modo demo)' };
  }
  try {
    return await request<DetectedSoil>(`/api/v1/soil?lat=${lat}&lon=${lon}`);
  } catch {
    return null;
  }
}
```

El endpoint se llama con `lon`, no `lng`. Tarda 3–8 s la primera vez, por eso `getSoil` no lanza errores.

**Paso 4 · Prueba y PR**

```bash
npm run build
git add src/lib/deviceId.ts src/api/client.ts
git commit -m "feat: X-Device-Id, deleteAnalysis y getSoil en el cliente API"
git push -u origin feature/api-cliente-device
```

Abre el PR hacia `main` y avisa a Mía. Para verificar el header con el backend real mira la sección *Cómo probar* al final.

## PR B · La PWA: manifest, íconos y service worker

Una PWA son tres piezas: un **manifest** (nombre, colores, íconos), un **service worker** (guarda los archivos de la app para abrirla sin internet) y **íconos** reales. `vite-plugin-pwa` genera el manifest y el service worker en `npm run build`; en `npm run dev` no corre (a propósito).

**Paso 1 · Rama e instalación**

```bash
cd frontend
git switch main && git pull   # con el PR A ya mergeado
git switch -c feature/pwa-instalable
npm install -D vite-plugin-pwa @vite-pwa/assets-generator
```

Si `npm` se queja de peer dependencies de Vite, revisa que `npm ls vite-plugin-pwa` muestre 1.3.0 o más (desde esa versión soporta Vite 8). Si falla, avísale a Mía y no uses `--force`.

**Paso 2 · Un ícono propio.** El `public/favicon.svg` actual es el logo de Vite. Reemplaza todo su contenido por esto (hoja sobre fondo verde del tema; los colores son `orbit` y `canvas`):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="112" fill="#12261F"/>
  <path d="M256 392V240" stroke="#FBF8F1" stroke-width="26" stroke-linecap="round"/>
  <path d="M256 250C256 178 206 138 130 134C130 206 176 254 256 250Z" fill="#FBF8F1"/>
  <path d="M256 288C256 214 312 170 392 166C392 244 340 292 256 288Z" fill="#FBF8F1" fill-opacity=".78"/>
</svg>
```

Si alguien del equipo ya tiene un logo, úsalo en su lugar: solo debe ser cuadrado y de al menos 512 px.

**Paso 3 · Genera los PNG.** Crea `pwa-assets.config.ts` en la raíz de `frontend/`:

```ts
import { defineConfig, minimal2023Preset as preset } from '@vite-pwa/assets-generator/config';

export default defineConfig({
  headLinkOptions: { preset: '2023' },
  preset,
  images: ['public/favicon.svg'],
});
```

Agrega el script en `package.json`, dentro de `"scripts"`:

```json
"pwa:icons": "pwa-assets-generator"
```

Y corre `npm run pwa:icons`. Debe crear en `public/`: `pwa-64x64.png`, `pwa-192x192.png`, `pwa-512x512.png`, `maskable-icon-512x512.png`, `apple-touch-icon-180x180.png` y `favicon.ico`. Esos archivos **sí se suben al repo**.

**Paso 4 · `vite.config.ts` completo.** Reemplaza el archivo por este (conserva tu bloque `server`):

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate', // el SW nuevo se activa solo al recargar
      includeAssets: ['favicon.ico', 'favicon.svg', 'apple-touch-icon-180x180.png'],
      manifest: {
        name: 'Field Shift',
        short_name: 'Field Shift',
        description: 'Rotación de cultivos con datos de NASA para adaptar tu parcela al clima.',
        lang: 'es-MX',
        start_url: '/',
        scope: '/',
        display: 'standalone',
        background_color: '#FBF8F1',
        theme_color: '#12261F',
        icons: [
          { src: 'pwa-64x64.png', sizes: '64x64', type: 'image/png' },
          { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' },
          { src: 'maskable-icon-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
      workbox: {
        // App shell + todos los chunks (incluye las vistas lazy de App.tsx)
        globPatterns: ['**/*.{js,css,html,svg,png,ico,woff2}'],
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/api\//],
        cleanupOutdatedCaches: true,
        runtimeCaching: [
          {
            // GET de la API (historial, detalle, suelo): red primero, caché si no hay internet
            urlPattern: ({ url }) => url.pathname.startsWith('/api/'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'fieldshift-api',
              networkTimeoutSeconds: 6,
              expiration: { maxEntries: 40, maxAgeSeconds: 60 * 60 * 24 * 7 },
              cacheableResponse: { statuses: [200] },
            },
          },
          {
            // Tipografías de Google Fonts (index.html las pide)
            urlPattern: ({ url }) => url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com',
            handler: 'StaleWhileRevalidate',
            options: { cacheName: 'fieldshift-fonts', expiration: { maxEntries: 12 } },
          },
          {
            // Mosaicos del mapa: solo los que ya viste, con tope bajo (no descargamos mapas enteros)
            urlPattern: ({ url }) => /tile\.openstreetmap\.org|arcgisonline\.com/.test(url.hostname),
            handler: 'CacheFirst',
            options: {
              cacheName: 'fieldshift-tiles',
              expiration: { maxEntries: 120, maxAgeSeconds: 60 * 60 * 24 * 3 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
        ],
      },
    }),
  ],
  server: {
    // Escucha en todas las redes (necesario dentro de Docker)
    host: true,
    port: 3000,
    // En Windows + Docker los cambios de archivos solo se detectan con polling
    watch: { usePolling: process.env.CHOKIDAR_USEPOLLING === 'true' },
  },
});
```

Los POST (crear análisis) nunca se cachean: Workbox solo guarda GET. Por eso, sin internet, el análisis nuevo falla con el mensaje de siempre y la app muestra el último análisis guardado por Fernando (`lib/offline.ts`).

**Paso 5 · `index.html`.** Dentro de `<head>`, después del `<link rel="icon" ...>` existente, agrega:

```html
<link rel="icon" href="/favicon.ico" sizes="48x48" />
<link rel="apple-touch-icon" href="/apple-touch-icon-180x180.png" />
<meta name="theme-color" content="#12261F" />
<meta name="description" content="Rotación de cultivos con datos de NASA para adaptar tu parcela al clima." />
```

No hay que agregar `<link rel="manifest">`: el plugin lo inyecta en el build.

**Paso 6 · Botón "Instalar app".** Crea `src/components/InstallButton.tsx`. Chrome y Edge avisan con el evento `beforeinstallprompt`; Safari en iPhone no lo tiene, así que ahí mostramos la instrucción manual.

```tsx
import { useEffect, useState } from 'react';
import { Check, Download } from 'lucide-react';

type EventoInstalar = Event & {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
};

const esIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
const yaInstalada = () =>
  matchMedia('(display-mode: standalone)').matches ||
  (navigator as Navigator & { standalone?: boolean }).standalone === true;

export default function InstallButton() {
  const [evento, setEvento] = useState<EventoInstalar | null>(null);
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

  return null; // el navegador no ofrece instalación (o ya se rechazó en esta sesión)
}
```

Las clases (`bg-leaf-600`, `text-paper`, `text-ink-500`) son las mismas que ya usa `HistoryView.tsx`. Revisa el botón en modo oscuro; si algo no se ve bien, ajusta con los tokens de `src/index.css` (bloque `@theme`).

Mía es la dueña de `AccountView.tsx`: pídele permiso en el grupo y agrega solo estas dos líneas, dentro de la tarjeta que ella prefiera:

```tsx
import InstallButton from '../components/InstallButton';
// ...
<InstallButton />
```

## Cómo probar y mandar el PR

El service worker solo se genera en el build, así que **no pruebes la PWA con `npm run dev` ni con Docker**. Usa:

```bash
npm run build
npm run preview
```

Abre http://localhost:4173 en Chrome y revisa en DevTools → *Application*:

1. **Manifest**: sin errores rojos, con el nombre "Field Shift" y los 4 íconos visibles.
2. **Service workers**: estado *activated and is running*.
3. **Cache Storage**: aparece `workbox-precache-...` y, tras navegar por las vistas, `fieldshift-fonts`.
4. En la barra de direcciones aparece el ícono de instalar (o tu botón "Instalar app" en Cuenta). Instálala: debe abrir en ventana propia, sin barra del navegador.
5. **Sin conexión**: marca *Offline* en DevTools → *Network* y recarga. La app debe abrir, cambiar de vista (las vistas lazy están precacheadas) y, con el modo oscuro, verse igual. Crear un análisis nuevo debe fallar con su mensaje de error normal.
6. **API en caché** (solo con backend real: `VITE_USE_MOCK=false` y `VITE_API_URL` en `frontend/.env` *antes* del build): abre Historial con internet, apaga la red y recarga: la lista sigue ahí.

Para probar en tu celular, el service worker exige HTTPS o `localhost`. En Android con Chrome, conecta el teléfono por USB, abre `chrome://inspect` en la computadora y usa *Port forwarding* (4173 → localhost:4173).

Cuando todo funcione:

```bash
git status   # no debe aparecer dist/ ni .env
git add vite.config.ts index.html package.json package-lock.json pwa-assets.config.ts public src/components/InstallButton.tsx src/views/AccountView.tsx
git commit -m "feat: PWA instalable con service worker y botón de instalar"
git push -u origin feature/pwa-instalable
```

Abre el PR hacia `main`, adjunta una captura de DevTools → Application → Manifest y menciona a Mía y a Fernando. Si hay conflicto en `package-lock.json`: `git checkout origin/main -- package-lock.json && npm install`.
