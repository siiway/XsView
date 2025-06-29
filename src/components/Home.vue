<script setup lang="ts">
import { NCard, NSpace, NStatistic, NGrid, NGridItem, NIcon, NButton, NTag, NProgress } from 'naive-ui';
import { h, ref } from 'vue';
import { 
  DocumentTextOutline, 
  AnalyticsOutline, 
  TrophyOutline, 
  TrendingUpOutline,
  CalendarOutline,
  SchoolOutline,
  CheckmarkCircleOutline,
  TimeOutline
} from '@vicons/ionicons5';
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
  <div class="home-container">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner">
      <div class="banner-content">
        <h1>欢迎使用 XsView 面板</h1>
        <p>高度客制化的中前台面板</p>
        <div class="banner-actions">
          <n-button type="primary" size="large" @click="navigateTo('/score-query')">
            ？
          </n-button>
          <n-button size="large" @click="navigateTo('/exam-analysis')">
            试试
          </n-button>
        </div>
      </div>
      <div class="banner-decoration"></div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  padding: 0;
  max-width: 1200px;
  margin: 0 auto;
}

/* 欢迎横幅 */
.welcome-banner {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 40px;
  margin-bottom: 32px;
  color: white;
  overflow: hidden;
}

.banner-content {
  position: relative;
  z-index: 2;
}

.banner-content h1 {
  margin: 0 0 12px 0;
  font-size: 32px;
  font-weight: 600;
}

.banner-content p {
  margin: 0 0 24px 0;
  font-size: 16px;
  opacity: 0.9;
}

.banner-actions {
  display: flex;
  gap: 16px;
}

.banner-decoration {
  position: absolute;
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  z-index: 1;
}


</style>

