import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { externalDirective } from './utils/linkHandler'
// 直接导入路由，避免异步加载延迟
import router from './router'

// 记录应用启动时间
performance.mark('app-init-start')

// 创建应用实例
const app = createApp(App)

// 初始化Pinia状态管理
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// 添加自定义指令
app.directive('external', externalDirective)

// 全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('全局错误:', err)
  console.error('错误组件:', instance)
  console.error('错误信息:', info)
}

app.config.warnHandler = (msg, instance, trace) => {
  console.warn('警告:', msg)
  console.warn('警告组件:', instance)
  console.warn('调用栈:', trace)
}

// 使用路由
app.use(router)

// 挂载应用
app.mount('#app')

// 记录应用挂载完成时间
performance.mark('app-mounted')
performance.measure('App Initialization', 'app-init-start', 'app-mounted')
performance.measure('Total App Loading', 'app-loading-start', 'app-mounted')

// 输出性能指标
console.log('Application creating time:', performance.getEntriesByName('App Initialization')[0].duration.toFixed(2) + 'ms')
console.log('Last loading HMR time:', performance.getEntriesByName('Total App Loading')[0].duration.toFixed(2) + 'ms')


