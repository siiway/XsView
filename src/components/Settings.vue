<script setup lang="ts">
import { NCard, NSpace, NSwitch, NSelect, NForm, NFormItem, NButton, NDivider, NTabs, NTabPane } from 'naive-ui';
import { ref, inject } from 'vue';
import ThemeSettings from './ThemeSettings.vue';
import { useThemeStore } from '../stores/theme';

// 注入主题控制
const darkMode = inject('darkMode') as any;

// 使用主题存储
const themeStore = useThemeStore();

// 设置选项
const settings = ref({
  theme: darkMode.colorScheme.value,
});

// 处理主题切换
const handleThemeChange = (value: boolean) => {
  darkMode.toggleColorScheme();
  settings.value.theme = darkMode.colorScheme.value;
};

// 保存设置
const saveSettings = () => {
  console.log('保存设置:', settings.value);
  // 这里可以添加实际的保存逻辑
};

// 重置设置
const resetSettings = () => {
  settings.value = {
    theme: darkMode.colorScheme.value,
  };
};

// 当前活动的标签页
const activeTab = ref('general');
</script>

<template>
  <div class="settings-container">
    <n-tabs v-model:value="activeTab" type="card" animated>
      <!-- 常规设置 -->
      <n-tab-pane name="general" tab="常规设置">
        <n-card title="系统设置" class="settings-card">
          <n-form :model="settings" label-placement="left" label-width="120px">
            <n-form-item label="界面主题">
              <n-switch
                :value="darkMode.colorScheme.value === 'dark'"
                @update:value="handleThemeChange"
              >
                <template #checked>深色</template>
                <template #unchecked>浅色</template>
              </n-switch>
            </n-form-item>
            
            <n-divider />
            
            <n-form-item>
              <n-space>
                <n-button type="primary" @click="saveSettings">保存设置</n-button>
                <n-button @click="resetSettings">重置设置</n-button>
              </n-space>
            </n-form-item>
          </n-form>
        </n-card>
      </n-tab-pane>
      
      <!-- 主题设置 -->
      <n-tab-pane name="theme" tab="主题与外观">
        <ThemeSettings />
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<style scoped>
.settings-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-card {
  margin-bottom: 16px;
}
</style>


