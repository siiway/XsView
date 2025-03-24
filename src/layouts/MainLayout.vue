<!-- 主布局组件 -->
<!-- layouts/MainLayout.vue -->

<template>
  <div class="main-layout">
    <!-- 移动端顶部导航 -->
    <div class="mobile-header" v-if="isMobile">
      <div class="logo">
        <img src="../assets/logo.png" alt="ScoreX Logo" />
        <span>查分星</span>
      </div>
      <n-button quaternary circle @click="showDrawer = true">
        <template #icon>
          <n-icon><menu-outline /></n-icon>
        </template>
      </n-button>
    </div>

    <!-- PC端侧边栏 -->
    <div class="sidebar" v-if="!isMobile">
      <div class="logo">
        <img src="../assets/logo.png" alt="ScoreX Logo" />
        <span>查分星</span>
      </div>
      <n-menu
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleMenuUpdate"
      />
      <div class="sidebar-footer">
        <n-dropdown :options="userOptions" @select="handleUserAction">
          <div class="user-info">
            <n-avatar round>{{ userStore.username.charAt(0) }}</n-avatar>
            <span>{{ userStore.username }}</span>
          </div>
        </n-dropdown>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content" :class="{ 'with-sidebar': !isMobile }">
      <!-- 页面内容 -->
      <div class="page-container">
        <router-view />
      </div>
    </div>

    <!-- 移动端底部导航 -->
    <div class="mobile-footer" v-if="isMobile">
      <n-grid :cols="5" :x-gap="4">
        <n-grid-item v-for="item in mobileMenuItems" :key="item.key">
          <div
            class="mobile-nav-item"
            :class="{ active: activeKey === item.key }"
            @click="handleMobileNavClick(item.key)"
          >
            <n-icon size="20">
              <component :is="item.icon" />
            </n-icon>
            <span>{{ item.label }}</span>
          </div>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 移动端侧边抽屉 -->
    <n-drawer v-model:show="showDrawer" :width="280" placement="left">
      <n-drawer-content title="菜单">
        <div class="drawer-user-info">
          <n-avatar round size="large">{{ userStore.username.charAt(0) }}</n-avatar>
          <div class="user-details">
            <div class="username">{{ userStore.username }}</div>
            <div class="role">{{ userStore.role.name || '学生' }}</div>
          </div>
        </div>
        <n-divider />
        <n-menu
          :options="menuOptions"
          :value="activeKey"
          @update:value="handleDrawerMenuUpdate"
        />
        <n-divider />
        <n-button
          block
          type="error"
          @click="handleLogout"
        >
          退出登录
        </n-button>
      </n-drawer-content>
    </n-drawer>

    <!-- 通知抽屉 -->
    <n-drawer v-model:show="showNotificationDrawer" :width="300" placement="right">
      <n-drawer-content title="通知中心">
        <notification-list @close="showNotificationDrawer = false" />
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  NMenu, 
  NDrawer, 
  NDrawerContent, 
  NButton, 
  NIcon, 
  NAvatar, 
  NDropdown,
  NDivider,
  NGrid,
  NGridItem
} from 'naive-ui'
import { 
  HomeOutline, 
  DocumentTextOutline, 
  AnalyticsOutline, 
  BookOutline, 
  NotificationsOutline,
  PersonOutline,
  MenuOutline,
  LogOutOutline,
  SettingsOutline
} from '@vicons/ionicons5'
import { useUserStore } from '../stores/user'
import NotificationList from '../components/notification/NotificationList.vue'

// 路由实例
const router = useRouter()
const route = useRoute()

// 用户状态
const userStore = useUserStore()

// 响应式状态
const showDrawer = ref(false)
const showNotificationDrawer = ref(false)
const activeKey = ref('dashboard')
const isMobile = ref(false)

// 监听窗口大小变化
const checkIsMobile = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', checkIsMobile)
  
  // 根据当前路由设置活动菜单项
  setActiveKeyFromRoute(route)
})

// 监听路由变化
watch(
  () => route.name,
  () => {
    setActiveKeyFromRoute(route)
  }
)

// 根据路由设置活动菜单项
const setActiveKeyFromRoute = (route) => {
  const routeMap = {
    'Dashboard': 'dashboard',
    'ExamList': 'exams',
    'ExamDetail': 'exams',
    'ExamAnalysis': 'exams',
    'DiagnosticList': 'diagnostic',
    'DiagnosticDetail': 'diagnostic',
    'LearningMaterials': 'learning',
    'LearningDetail': 'learning',
    'Notifications': 'notifications',
    'Profile': 'profile'
  }
  
  activeKey.value = routeMap[route.name] || 'dashboard'
}

// 菜单选项
const menuOptions = computed(() => [
  {
    label: '首页',
    key: 'dashboard',
    icon: () => h(NIcon, null, { default: () => h(HomeOutline) })
  },
  {
    label: '考试成绩',
    key: 'exams',
    icon: () => h(NIcon, null, { default: () => h(DocumentTextOutline) })
  },
  {
    label: '诊断报告',
    key: 'diagnostic',
    icon: () => h(NIcon, null, { default: () => h(AnalyticsOutline) })
  },
  {
    label: '学习资料',
    key: 'learning',
    icon: () => h(NIcon, null, { default: () => h(BookOutline) })
  },
  {
    label: '通知中心',
    key: 'notifications',
    icon: () => h(NIcon, null, { default: () => h(NotificationsOutline) })
  },
  {
    label: '个人设置',
    key: 'profile',
    icon: () => h(NIcon, null, { default: () => h(PersonOutline) })
  }
])

// 移动端底部导航项
const mobileMenuItems = [
  {
    label: '首页',
    key: 'dashboard',
    icon: HomeOutline
  },
  {
    label: '考试',
    key: 'exams',
    icon: DocumentTextOutline
  },
  {
    label: '诊断',
    key: 'diagnostic',
    icon: AnalyticsOutline
  },
  {
    label: '资料',
    key: 'learning',
    icon: BookOutline
  },
  {
    label: '我的',
    key: 'profile',
    icon: PersonOutline
  }
]

// 用户下拉菜单选项
const userOptions = [
  {
    label: '个人设置',
    key: 'profile',
    icon: () => h(NIcon, null, { default: () => h(SettingsOutline) })
  },
  {
    label: '通知中心',
    key: 'notifications',
    icon: () => h(NIcon, null, { default: () => h(NotificationsOutline) })
  },
  {
    type: 'divider',
    key: 'd1'
  },
  {
    label: '退出登录',
    key: 'logout',
    icon: () => h(NIcon, null, { default: () => h(LogOutOutline) })
  }
]

// 处理菜单点击
const handleMenuUpdate = (key) => {
  activeKey.value = key
  navigateToRoute(key)
}

// 处理抽屉菜单点击
const handleDrawerMenuUpdate = (key) => {
  activeKey.value = key
  showDrawer.value = false
  navigateToRoute(key)
}

// 处理移动端底部导航点击
const handleMobileNavClick = (key) => {
  activeKey.value = key
  navigateToRoute(key)
}

// 根据菜单键导航到对应路由
const navigateToRoute = (key) => {
  const routeMap = {
    'dashboard': { name: 'Dashboard' },
    'exams': { name: 'ExamList' },
    'diagnostic': { name: 'DiagnosticList' },
    'learning': { name: 'LearningMaterials' },
    'notifications': { name: 'Notifications' },
    'profile': { name: 'Profile' }
  }
  
  if (routeMap[key]) {
    router.push(routeMap[key])
  }
}

// 处理用户操作
const handleUserAction = (key) => {
  if (key === 'logout') {
    handleLogout()
  } else if (key === 'notifications') {
    showNotificationDrawer.value = true
  } else if (key === 'profile') {
    router.push({ name: 'Profile' })
  }
}

// 处理退出登录
const handleLogout = () => {
  userStore.logout()
}
</script>

<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.sidebar {
  width: 240px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f8f8f8;
  border-right: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
  padding: 16px;
  height: 64px;
}

.logo img {
  height: 32px;
  margin-right: 8px;
}

.logo span {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.sidebar-footer {
  margin-top: auto;
  padding: 16px;
  border-top: 1px solid #eee;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #eee;
}

.user-info span {
  margin-left: 8px;
  font-size: 14px;
}

.main-content {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  background-color: #f5f7fa;
}

.main-content.with-sidebar {
  margin-left: 0;
}

.page-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.mobile-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 100;
}

.mobile-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  background-color: #fff;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.08);
  z-index: 100;
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 56px;
  cursor: pointer;
}

.mobile-nav-item span {
  font-size: 12px;
  margin-top: 4px;
}

.mobile-nav-item.active {
  color: #18a058;
}

.drawer-user-info {
  display: flex;
  align-items: center;
  padding: 16px;
}

.user-details {
  margin-left: 12px;
}

.username {
  font-weight: bold;
  font-size: 16px;
}

.role {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}

@media (max-width: 767px) {
  .main-content {
    padding-top: 56px;
    padding-bottom: 56px;
  }
}
</style>
