import { createRouter, createWebHashHistory } from 'vue-router'
import { useRouteLoadingStore } from '../stores/routeLoading'

// 预加载首页和常用组件
import Home from '../components/Home.vue'

// 使用动态导入实现路由懒加载
const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {
      title: '主页'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../components/Settings.vue'),
    meta: {
      title: '系统设置'
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../components/About.vue'),
    meta: {
      title: '关于面板'
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const routeLoadingStore = useRouteLoadingStore()
  routeLoadingStore.setLoading(true)
  
  // 设置页面标题
  if (to.meta?.title) {
    document.title = `${to.meta.title} - XsView`
  }
  
  next()
})

router.afterEach(() => {
  const routeLoadingStore = useRouteLoadingStore()
  routeLoadingStore.setLoading(false)
})

export default router


