import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 5173,
    host: false, // I think false? I use nginx
    proxy: {
      '/ws/': {
        target: 'http://localhost:8080',
        ws: true,
      },
    },
  },
  plugins: [react()],
})
