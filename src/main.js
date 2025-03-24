// 前台应用入口文件
// main.js

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { setupNaive } from './plugins/naive'
import './styles/main.css'

// 创建应用实例
const app = createApp(App)

// 设置状态管理
app.use(createPinia())

// 设置路由
app.use(router)

// 设置UI组件库
setupNaive(app)

// 挂载应用
app.mount('#app')
