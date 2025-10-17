import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [vue()],
    server: {
      host: env.VITE_FRONTEND_HOST || 'localhost',
      port: parseInt(env.VITE_FRONTEND_PORT) || 3000
    }
  }
})

