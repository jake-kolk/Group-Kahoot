import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
// IMPORTANT!!! if you want to use http, chnge the target below
// https://vite.dev/config/
export default defineConfig({
  server: {
    port: 5173,
    host: false, // I think false? I use nginx
    proxy: {
      '/ws/': {
        target: 'https://localhost:8080',
        ws: true,
        secure: false, // CHANGE FOR PROD THIS SHIT IS NOT SECURE!!!
      },
    },
    middlewareMode: false,
  },
    build: {
    sourcemap: true,
  },
  
  plugins: [
    /*
    {
      name: "http-logger",
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          const start = Date.now();

          console.log(`Request: ${req.method} ${req.url}`);

          // Log response when finished
          res.on("finish", () => {
            const ms = Date.now() - start;
            console.log(`Response: ${res.statusCode} (${ms}ms)`);
          });

          next();
        });
      }
    },*/
    vue()
  ],
  resolve: {
  alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url))
  }
}
});