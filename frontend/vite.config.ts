import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate', // cuando hay versión nueva, se activa sola al recargar
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
        // Guarda la app completa: incluye las vistas que App.tsx carga con lazy()
        globPatterns: ['**/*.{js,css,html,svg,png,ico,woff2}'],
        maximumFileSizeToCacheInBytes: 4 * 1024 * 1024,
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/api\//],
        cleanupOutdatedCaches: true,
        runtimeCaching: [
          {
            // Lecturas de la API (historial, detalle, suelo): primero la red; si no hay, lo último guardado.
            urlPattern: ({ url }) => url.pathname.startsWith('/api/'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'fieldshift-api',
              networkTimeoutSeconds: 8,
              expiration: { maxEntries: 40, maxAgeSeconds: 60 * 60 * 24 * 7 },
              cacheableResponse: { statuses: [200] },
            },
          },
          {
            // Tipografías de Google Fonts que pide index.html
            urlPattern: ({ url }) =>
              url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com',
            handler: 'StaleWhileRevalidate',
            options: { cacheName: 'fieldshift-fonts', expiration: { maxEntries: 12 } },
          },
          {
            // Mosaicos del mapa: solo los que la persona ya vio, con tope bajo
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