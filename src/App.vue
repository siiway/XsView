<!-- 根组件 -->
<!-- App.vue -->

<template>
  <n-config-provider :theme="theme" :locale="locale" :date-locale="dateLocale">
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-message-provider>
            <router-view />
          </n-message-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  NConfigProvider, 
  NLoadingBarProvider, 
  NDialogProvider, 
  NNotificationProvider, 
  NMessageProvider,
  darkTheme, 
  zhCN, 
  dateZhCN 
} from 'naive-ui'
import { useUserStore } from './stores/user'

// 路由实例
const router = useRouter()

// 用户状态
const userStore = useUserStore()

// 主题设置
const theme = ref(null) // 默认浅色主题
const locale = ref(zhCN)
const dateLocale = ref(dateZhCN)

// 监听路由变化，检查登录状态
router.beforeEach((to, from, next) => {
  // 需要登录的路由
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    // 保存目标路由，登录后跳转
    userStore.setRedirectRoute(to.fullPath)
    next({ name: 'Login' })
  } else {
    next()
  }
})

// 初始化用户状态
userStore.initUserFromStorage()
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

#app {
  width: 100%;
  height: 100%;
}
</style>
