import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 80,
    host: true,
    proxy: {
      '/ws/': {
        target: 'http://localhost:8080',
        ws: true,
      },
    },
  },
  plugins: [react()],
})
