import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/calls': 'http://localhost:8000',
      '/records': 'http://localhost:8000',
    }
  }
})
