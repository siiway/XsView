<script setup lang="ts">
import { NSpace, NIcon } from 'naive-ui';
import { Mail, Globe, LogoGithub } from '@vicons/ionicons5';

// 系统功能列表
const features = [
  '请在features模块添加'
];

// 联系信息
const contactInfo = {
  email: '请添加',
  website: '请添加',
  github: '请添加'
};

// 更新日志
const changelog = {
  version: 'v1.0',
  date: '2025-06-29',
  updates: [
    '重构路由系统，优化用户体验',
    '开源',
    '新增服务模块',
    '升级依赖包到最新版本',
    '优化界面设计和交互'
  ]
};
</script>

<template>
<div class="section">
      <h3>关于<n-gradient-text type="info">
    XsView
  </n-gradient-text></h3>
      <div class="team-info">
        <p>SiiWay团队的XsView项目致力于肝一款麻雀虽小而五脏俱全的中前台管理面板。</p>
        <p>团队成员来自不同专业背景，但共同为打造更好的项目而努力。</p>
      </div>
    </div>
  <div class="about-container">
    <!-- 功能列表 -->
    <div class="section">
      <h3>系统功能</h3>
      <n-space vertical>
        <div v-for="feature in features" :key="feature" class="feature-item">
          <span class="bullet">•</span>
          <span>{{ feature }}</span>
        </div>
      </n-space>
    </div>

    <!-- 联系我们 -->
    <div class="section">
      <h3>联系我们</h3>
      <n-space vertical>
        <div class="contact-item">
          <n-icon size="18"><Mail /></n-icon>
          <span>邮箱: {{ contactInfo.email }}</span>
        </div>
        <div class="contact-item">
          <n-icon size="18"><Globe /></n-icon>
          <span>官网: {{ contactInfo.website }}</span>
        </div>
        <div class="contact-item">
          <n-icon size="18"><LogoGithub /></n-icon>
          <span>GitHub: {{ contactInfo.github }}</span>
        </div>
      </n-space>
    </div>

    <!-- 更新日志 -->
    <div class="section">
      <h3>更新日志</h3>
      <div class="changelog">
        <div class="version">{{ changelog.version }} ({{ changelog.date }})</div>
        <ul class="updates">
          <li v-for="update in changelog.updates" :key="update" class="update-item">
            <span class="bullet">•</span>
            <span>{{ update }}</span>
          </li>
        </ul>
      </div>
    </div>

  </div>
</template>

<style scoped>
.about-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
  color: var(--n-text-color);
}

.section {
  margin-bottom: 24px;
}

h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 500;
}

.feature-item, .update-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 4px 0;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
}

.bullet {
  color: var(--n-primary-color);
  font-weight: bold;
}

.changelog {
  margin-top: 8px;
}

.version {
  font-weight: 500;
  margin-bottom: 8px;
}

.updates {
  list-style: none;
  padding: 0;
  margin: 0;
}

.team-info {
  line-height: 1.6;
}

.team-info p {
  margin: 0 0 12px 0;
}
</style>

