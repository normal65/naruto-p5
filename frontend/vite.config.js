import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 配置本地代理，使前端请求 /api 时自动转发至 Flask 服务的 5000 端口
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})