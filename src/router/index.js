// 路由配置
// router/index.js

import { createRouter, createWebHistory } from 'vue-router'

// 布局组件
import MainLayout from '../layouts/MainLayout.vue'
import AuthLayout from '../layouts/AuthLayout.vue'

// 路由配置
const routes = [
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'exams',
        name: 'ExamList',
        component: () => import('../views/exam/ExamList.vue'),
        meta: { title: '考试列表' }
      },
      {
        path: 'exams/:id',
        name: 'ExamDetail',
        component: () => import('../views/exam/ExamDetail.vue'),
        meta: { title: '考试详情' }
      },
      {
        path: 'analysis/:id',
        name: 'ExamAnalysis',
        component: () => import('../views/exam/ExamAnalysis.vue'),
        meta: { title: '成绩分析' }
      },
      {
        path: 'diagnostic',
        name: 'DiagnosticList',
        component: () => import('../views/diagnostic/DiagnosticList.vue'),
        meta: { title: '诊断报告列表' }
      },
      {
        path: 'diagnostic/:id',
        name: 'DiagnosticDetail',
        component: () => import('../views/diagnostic/DiagnosticDetail.vue'),
        meta: { title: '诊断报告详情' }
      },
      {
        path: 'learning',
        name: 'LearningMaterials',
        component: () => import('../views/learning/LearningMaterials.vue'),
        meta: { title: '学习资料' }
      },
      {
        path: 'learning/:id',
        name: 'LearningDetail',
        component: () => import('../views/learning/LearningDetail.vue'),
        meta: { title: '资料详情' }
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: () => import('../views/notification/NotificationList.vue'),
        meta: { title: '通知中心' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/user/Profile.vue'),
        meta: { title: '个人设置' }
      }
    ]
  },
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('../views/auth/Login.vue'),
        meta: { title: '登录' }
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('../views/auth/Register.vue'),
        meta: { title: '注册' }
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: () => import('../views/auth/ForgotPassword.vue'),
        meta: { title: '找回密码' }
      },
      {
        path: 'bind-account',
        name: 'BindAccount',
        component: () => import('../views/auth/BindAccount.vue'),
        meta: { title: '绑定原平台账号', requiresAuth: true }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '页面不存在' }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由标题设置
router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - ScoreX查分星` : 'ScoreX查分星'
})

export default router
