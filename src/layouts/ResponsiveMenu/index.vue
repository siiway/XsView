<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';
import { h } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { NMenu, NLayoutSider, NDrawer, NDrawerContent, NButton, NIcon, NSpace } from 'naive-ui';
import {
  HomeOutline,
  SettingsOutline,
  InformationOutline,
  MenuOutline,
  CloseOutline
} from '@vicons/ionicons5';

// 获取当前路由
const route = useRoute();

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false
  },
  forceCollapsed: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:collapsed']);

const toggleCollapse = (value: boolean) => {
  if (!props.forceCollapsed) {
    emit('update:collapsed', value);
  }
};

// 计算实际折叠状态
const actualCollapsed = computed(() => props.forceCollapsed || props.collapsed);

// 菜单配置
const menuOptions = computed(() => [
  {
    label: () => h(RouterLink, { to: { name: 'Home' } }, { default: () => '主页' }),
    key: 'Home',
    icon: () => h(HomeOutline)
  },
  {
    label: () => h(RouterLink, { to: { name: 'Settings' } }, { default: () => '系统设置' }),
    key: 'Settings',
    icon: () => h(SettingsOutline)
  },
  {
    label: () => h(RouterLink, { to: { name: 'About' } }, { default: () => '关于面板' }),
    key: 'About',
    icon: () => h(InformationOutline)
  }
]);

// 设置默认选中的菜单项
const selectedKey = ref('Home');

// 监听路由变化，更新选中的菜单项
watch(() => route.name, (newRouteName) => {
  if (newRouteName) {
    // 直接使用路由名称作为key
    const routeKey = newRouteName.toString();
    
    // 检查是否有匹配的菜单项
    const menuItem = menuOptions.value.find(item => item.key === routeKey);
    if (menuItem) {
      selectedKey.value = routeKey;
    }
  }
}, { immediate: true });

// 移动端菜单抽屉控制
const showMobileMenu = ref(false);

// 屏幕宽度检测
const isMobile = ref(false);
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

// 监听窗口大小变化
onMounted(() => {
  checkMobile();
  window.addEventListener('resize', checkMobile);
});

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile);
});

// 处理移动端菜单项点击
const handleMobileMenuClick = (key: string) => {
  selectedKey.value = key;
  showMobileMenu.value = false;
};

</script>

<template>
  <!-- 桌面端侧边栏 -->
  <n-layout-sider 
    v-if="!isMobile"
    bordered 
    collapse-mode="width" 
    :collapsed-width="64" 
    :width="240" 
    :collapsed="actualCollapsed"
    :show-trigger="!forceCollapsed"
    @collapse="toggleCollapse(true)" 
    @expand="toggleCollapse(false)"
  >
    <n-menu 
      :collapsed="actualCollapsed" 
      :collapsed-width="64" 
      :collapsed-icon-size="22" 
      :options="menuOptions"
      v-model:value="selectedKey" 
    />
  </n-layout-sider>
  
  <!-- 移动端菜单按钮 -->
  <div v-if="isMobile" class="mobile-menu-button">
    <n-button quaternary circle @click="showMobileMenu = true" size="large">
      <template #icon>
        <n-icon size="24">
          <MenuOutline />
        </n-icon>
      </template>
    </n-button>
  </div>
  
  <!-- 移动端抽屉菜单 -->
  <n-drawer v-model:show="showMobileMenu" :width="280" placement="left">
    <n-drawer-content :title="null" :closable="false" :header-style="{ padding: '8px', display: 'flex', justifyContent: 'flex-end' }">
      <div class="mobile-menu-header">
        <n-button quaternary circle @click="showMobileMenu = false" size="medium">
          <template #icon>
            <n-icon size="18">
              <CloseOutline />
            </n-icon>
          </template>
        </n-button>
      </div>
      
      <n-space vertical size="medium" class="mobile-menu-list">
        <div 
          v-for="item in menuOptions" 
          :key="item.key" 
          class="mobile-menu-item"
          :class="{ active: selectedKey === item.key }"
          @click="handleMobileMenuClick(item.key)"
        >
          <RouterLink :to="{ name: item.key }">
            <n-space align="center">
              <n-icon size="22">
                <component :is="item.icon().type" />
              </n-icon>
              <span>{{ item.label().children.default() }}</span>
            </n-space>
          </RouterLink>
        </div>
      </n-space>
    </n-drawer-content>
  </n-drawer>
</template>

<style scoped>
.n-menu {
  height: 100%;
}

/* 移动端菜单按钮 */
.mobile-menu-button {
  position: fixed;
  top: 14px;
  left: 16px;
  z-index: 1001;
}

/* 移动端菜单样式 */
.mobile-menu-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 4px;
}

.mobile-menu-list {
  margin-top: 8px;
}

.mobile-menu-item {
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  margin-bottom: 4px;
}

.mobile-menu-item:hover {
  background-color: var(--n-color-hover);
  transform: translateX(4px);
}

.mobile-menu-item:active {
  background-color: rgba(32, 128, 240, 0.1);
  transform: scale(0.98);
}

.mobile-menu-item.active {
  background-color: rgba(32, 128, 240, 0.1);
  border-left: 3px solid var(--n-primary-color);
}

.mobile-menu-item a {
  display: block;
  text-decoration: none;
  color: var(--n-text-color);
  width: 100%;
}

/* 适配底部导航的内容区域 */
:deep(.n-layout-content) {
  padding-bottom: 0 !important;
}
</style>


