import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      'react-router-dom': path.resolve(__dirname, 'src/lib/router.jsx'),
      'lucide-react': path.resolve(__dirname, 'src/lib/icons.jsx'),
      'recharts': path.resolve(__dirname, 'src/lib/charts.jsx')
    }
  },

  server: {
    port: 5173,

    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/uploads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/demo_assets': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      '/reports': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})