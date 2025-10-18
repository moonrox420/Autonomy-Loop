import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Vite configuration for the Autonomy Loop frontend.
 *
 * The dev server port can be overridden via the FRONTEND_PORT environment
 * variable to align with the loop orchestrator. Tailwind CSS is configured
 * separately in tailwind.config.js.
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: parseInt(process.env.FRONTEND_PORT || '5174'),
  },
});