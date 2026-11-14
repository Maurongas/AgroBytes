import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // Escucha en todas las redes (necesario dentro de Docker)
    host: true,
    port: 5173,
    // En Windows + Docker los cambios de archivos solo se detectan con polling
    watch: { usePolling: process.env.CHOKIDAR_USEPOLLING === 'true' },
  },
});
