<script lang="ts" setup>
import { NButton, NIcon, NText } from 'naive-ui';
import { ref, inject, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { Moon, Sunny } from '@vicons/ionicons5';

// 注入主题控制
const darkMode = inject('darkMode') as any;

// 检测是否为移动设备
const isMobile = ref(false);
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768;
};

onMounted(() => {
  checkMobile();
  window.addEventListener('resize', checkMobile);
});

</script>

<template>
  <div class="header-container">
    <!-- 左侧标题 -->
    <div class="header-left" :class="{ 'mobile-header-left': isMobile }">
      <RouterLink to="/" class="logo-link">
        <span class="xscore-logo">XSVIEW</span>
        <n-text class="header-subtitle" :class="{ 'mobile-subtitle': isMobile }">
          <span v-if="!isMobile">V1.0</span>
        </n-text>
      </RouterLink>
    </div>
    
    <!-- 右侧控制区域 -->
    <div class="header-right">
      <!-- 深色模式切换按钮 -->
      <n-button
        quaternary
        circle
        @click="darkMode.toggleColorScheme"
        class="header-button"
      >
        <template #icon>
          <n-icon>
            <Moon v-if="darkMode.colorScheme.value === 'light'" />
            <Sunny v-else />
          </n-icon>
        </template>
      </n-button>
    </div>
  </div>
</template>

<style scoped>
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
  background: var(--n-color);
  border-bottom: 1px solid var(--n-border-color);
}

.header-left {
  display: flex;
  align-items: center;
}

/* 移动端标题样式，为菜单按钮留出空间 */
.mobile-header-left {
  margin-left: 40px; /* 为移动端菜单按钮留出空间 */
  justify-content: center; /* 居中显示 */
  flex-grow: 1; /* 占据剩余空间 */
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}

.header-subtitle {
  font-size: 16px;
  font-weight: 400;
  color: var(--n-text-color);
  margin-left: 8px;
}

.mobile-subtitle {
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-button {
  width: 36px;
  height: 36px;
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
  }
  
  .header-right {
    gap: 8px;
  }
  
  .header-button {
    width: 32px;
    height: 32px;
  }
}
</style>


