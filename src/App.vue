<script setup lang="ts">
import { computed, provide, ref, watch, onMounted } from 'vue';
import { darkTheme, dateZhCN, useOsTheme, zhCN } from 'naive-ui';
import { NConfigProvider, NLoadingBarProvider, NDialogProvider, NNotificationProvider, NMessageProvider, NGlobalStyle, NLayout, NLayoutHeader, NLayoutContent, NText, NScrollbar } from 'naive-ui';
import { useRouter, useRoute } from 'vue-router';
// 导入布局组件
import Header from './layouts/Header/index.vue';
import ResponsiveMenu from './layouts/ResponsiveMenu/index.vue';
// 导入主题存储
import { useThemeStore, LAYOUT_TYPES } from './stores/theme';
// 导入路由加载状态存储
import { useRouteLoadingStore } from './stores/routeLoading';

const router = useRouter();
const route = useRoute();

// 获取路由加载状态
const routeLoadingStore = useRouteLoadingStore();

// 主题相关
const osThemeRef = useOsTheme();
const colorScheme = ref<'dark' | 'light'>(
  localStorage.getItem('colorScheme') as 'dark' | 'light' || 
  (osThemeRef.value === 'dark' ? 'dark' : 'light')
);

const collapsed = ref(false);
provide('collapsed', collapsed);

const currentVersion = ref('v1.0');

// 检测是否为移动设备
const isMobile = ref(false);
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

// 使用主题存储
const themeStore = useThemeStore();

onMounted(() => {
  checkMobile();
  window.addEventListener('resize', checkMobile);
  
  // 记录应用挂载时间
  performance.mark('app-vue-mounted');
  
  // 隐藏加载动画
  const loading = document.getElementById('app-loading');
  if (loading) {
    loading.style.opacity = '0';
    setTimeout(() => {
      loading.style.display = 'none';
    }, 500);
  }
});

// 主题相关
watch(osThemeRef, () => beAttachToggleColorScheme(osThemeRef.value === 'dark' ? 'dark' : 'light'));
const theme = computed(() => (colorScheme.value === 'dark' ? darkTheme : null));

const updateBodyColorSchemeForCssColorScheme = () => {
  if (theme.value !== darkTheme) {
    document.documentElement.classList.remove('actual-dark');
  } else {
    document.documentElement.classList.add('actual-dark');
  }
};

const toggleColorScheme = () => {
  if (colorScheme.value === 'dark') {
    colorScheme.value = 'light';
  } else {
    colorScheme.value = 'dark';
  }
  window.localStorage.setItem('colorScheme', colorScheme.value);
};

const beAttachToggleColorScheme = (x: string) => {
  if (x === 'dark' && colorScheme.value === 'light') {
    colorScheme.value = 'dark';
  } else if (x === 'light' && colorScheme.value === 'dark') {
    colorScheme.value = 'light';
  }
  window.localStorage.setItem('colorScheme', colorScheme.value);
};

provide('darkMode', { colorScheme, toggleColorScheme });
watch(theme, () => updateBodyColorSchemeForCssColorScheme());
updateBodyColorSchemeForCssColorScheme();

// 计算是否使用紧凑布局
const isCompactLayout = computed(() => {
  // 移动端不应用紧凑布局
  if (isMobile.value) {
    return false;
  }
  return themeStore.layoutType === 'compact';
});

// 监听布局类型变化，更新折叠状态
watch(() => themeStore.layoutType, (newLayout) => {
  // 移动端不应用紧凑布局
  if (isMobile.value) {
    return;
  }
  
  if (newLayout === 'compact') {
    collapsed.value = true;
  } else if (newLayout === 'default') {
    collapsed.value = false;
  }
});
</script>
<template>
  <n-config-provider :theme-overrides="themeStore.themeOverrides" :locale="zhCN" :date-locale="dateZhCN" :theme="theme">
    <n-dialog-provider>
      <n-loading-bar-provider>
        <n-notification-provider>
          <n-message-provider>
            <n-layout style="height: 100vh">
              <!-- 头部 -->
              <n-layout-header bordered style="height: 64px; padding: 0">
                <Header />
              </n-layout-header>
              
              <!-- 主体布局 -->
              <n-layout has-sider position="absolute" style="top: 64px; bottom: 0">
                <!-- 自适应菜单组件 -->
                <ResponsiveMenu v-model:collapsed="collapsed" :force-collapsed="isCompactLayout" />
                
                <!-- 内容区域 -->
                <n-layout>
                  <n-layout-content :content-style="isMobile ? 'padding: 24px 16px 72px;' : 'padding: 24px;'">
                    <n-text
                      style="position:fixed;display:flex; right:40px;bottom: 40px;z-index:99;pointer-events: none; user-select: none;opacity: 0.5;">
                      XsView<br />{{ currentVersion }}
                    </n-text>
                    <n-scrollbar :style="isMobile ? 'max-height: calc(100vh - 64px - 72px);' : 'max-height: calc(100vh - 64px - 48px);'">
                      <transition name="fade-slide" mode="out-in">
                        <keep-alive>
                          <component :is="route.meta.keepAlive ? route.matched[0].components.default : null" v-if="route.meta.keepAlive" />
                        </keep-alive>
                      </transition>
                      <transition name="fade-slide" mode="out-in">
                        <component :is="!route.meta.keepAlive ? route.matched[0].components.default : null" v-if="!route.meta.keepAlive" />
                      </transition>
                    </n-scrollbar>
                  </n-layout-content>
                </n-layout>
              </n-layout>
            </n-layout>
          </n-message-provider>
        </n-notification-provider>
      </n-loading-bar-provider>
    </n-dialog-provider>
    <n-global-style />
  </n-config-provider>
</template>
<style>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}
#app {
  height: 100%;
  width: 100%;
}
.n-layout-content {
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  flex: auto;
}
a {
  text-decoration: none;
  color: #72a0c9;
}
a:hover {
  color: #529bdb;
}
.animate__animated {
  --animate-duration: 0.55s;
}
/* 暗色模式样式 */
.actual-dark {
  color-scheme: dark light;
}
/* 亮色模式样式 */
:not(.actual-dark) {
  color-scheme: light;
}
/* 根样式 */
:root {
  font-family: 'Segoe UI', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol' !important;
  height: 100%;
}
body {
  margin: 0;
  padding: 0;
  border: 0;
}
#root,
.actual-dark,
.actual-light {
  height: 100%;
}
@media screen and (min-width: 700px) {
  .n-config-provider,
  body {
    height: 100%;
  }
  #root {
    height: 100%;
  }
}
/* 处理亮/暗模式样式 */
.actual-dark {
  color-scheme: dark light;
}
.actual-light {
  color-scheme: light;
}

/* 路由过渡动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>


