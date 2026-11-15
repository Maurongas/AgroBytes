// Vite config de la presentación (pitch). Vive fuera de frontend/ pero usa sus node_modules y su código:
//   - '@app/...'  → frontend/src/... (componentes reales, mock.ts, tokens de index.css)
//   - Los imports "desnudos" (react, framer-motion…) que salen de esta carpeta se resuelven como si
//     vinieran de frontend/src, así hay una sola copia de React para la app y el pitch.
// Se carga con --configLoader native (Node la importa tal cual), por eso es .mjs y sin imports desnudos.
import { createRequire } from 'node:module';
import { realpathSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const PITCH = dirname(fileURLToPath(import.meta.url));
const FRONTEND = realpathSync(process.env.FRONTEND_DIR ?? resolve(PITCH, '../../frontend'));
const fromFrontend = createRequire(join(FRONTEND, 'package.json'));
const load = async (pkg) => (await import(pathToFileURL(fromFrontend.resolve(pkg)).href)).default;

const react = await load('@vitejs/plugin-react');
const tailwindcss = await load('@tailwindcss/vite');

const PITCH_POSIX = PITCH.replaceAll('\\', '/');
const ANCHOR = join(FRONTEND, 'src', 'main.tsx');
const isBare = (id) => !/^[./\\\0]/.test(id) && !/^[A-Za-z]:[\\/]/.test(id) && !id.startsWith('@app/') && !id.startsWith('virtual:');

/** Resuelve los paquetes importados desde docs/presentacion como si los importara frontend/src. */
function useFrontendModules() {
  return {
    name: 'pitch:frontend-modules',
    enforce: 'pre',
    async resolveId(source, importer, options) {
      if (!importer || !isBare(source)) return null;
      const from = importer.split('?')[0].replaceAll('\\', '/');
      if (!from.startsWith(PITCH_POSIX + '/')) return null;
      return this.resolve(source, ANCHOR, { ...options, skipSelf: true });
    },
  };
}

export default {
  root: PITCH,
  base: './',
  cacheDir: join(FRONTEND, 'node_modules', '.vite-pitch'),
  plugins: [useFrontendModules(), react(), tailwindcss()],
  resolve: {
    alias: [
      { find: '@app', replacement: join(FRONTEND, 'src') },
      // plugin-react pide pre-empaquetar react/react-dom desde la raíz (esta carpeta, sin node_modules)
      { find: /^(react|react-dom)((?:\/[\w-]+)*)$/, replacement: `${join(FRONTEND, 'node_modules').replaceAll('\\', '/')}/$1$2` },
    ],
  },
  server: {
    host: true,
    port: 3001,
    fs: { allow: [PITCH, FRONTEND] },
    watch: { usePolling: process.env.CHOKIDAR_USEPOLLING === 'true' },
  },
  preview: { port: 3001 },
  build: { outDir: join(PITCH, 'dist'), emptyOutDir: true },
};
