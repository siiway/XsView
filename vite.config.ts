import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
// 确保已安装 unplugin-auto-import 包
// 如果未安装，请运行: npm install unplugin-auto-import --save-dev
import AutoImport from 'unplugin-auto-import/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'

// @ts-expect-error process is a nodejs global
const host = process.env.TAURI_DEV_HOST;


// https://vitejs.dev/config/
export default defineConfig(async () => ({
  plugins: [vue(),
    AutoImport({
      imports: [
        'vue',
        {
          'naive-ui': [
            'useDialog',
            'useMessage',
            'useNotification',
            'useLoadingBar'
          ]
        }
      ]
    }),
    Components({
      resolvers: [NaiveUiResolver()]
    })
  ],

  // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
  //
  // 1. prevent vite from obscuring rust errors
  clearScreen: false,
  // 2. tauri expects a fixed port, fail if that port is not available
  server: {
    port: 3003,
    strictPort: true,
    host: host || '0.0.0.0',
    hmr: host
      ? {
          protocol: "ws",
          host,
          port: 3001,
        }
      : undefined,
    watch: {
      // 3. tell vite to ignore watching `src-tauri`
      ignored: ["**/src-tauri/**"],
    },
    allowedHosts: ['xs2test.siiway.top', 'localhost', '127.0.0.1'],
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  
  // 优化构建配置
  build: {
    // 启用源码映射，但使用更轻量级的选项
    sourcemap: 'hidden',
    
    // 分块策略
    rollupOptions: {
      output: {
        // 将依赖项拆分为更小的块
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'naive-ui': ['naive-ui'],
          'icons': ['@vicons/ionicons5'],
        },
        // 为静态资源添加内容哈希，优化缓存
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
      },
    },
    
    // 启用CSS代码分割
    cssCodeSplit: true,
    
    // 压缩选项
    minify: 'terser',
    terserOptions: {
      compress: {
        // 移除console.log，但保留警告和错误
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log'],
      },
    },
    
    // 启用gzip压缩
    // 注意：需要服务器支持
    // brotliSize: true,
    
    // 设置较大的警告限制，避免不必要的警告
    chunkSizeWarningLimit: 1000,
  },
}));

