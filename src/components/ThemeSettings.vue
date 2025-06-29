<script setup lang="ts">
import { ref, computed } from 'vue';
import { 
  NCard, 
  NSpace, 
  NTabs, 
  NTabPane, 
  NRadioGroup, 
  NRadio, 
  NColorPicker, 
  NSwitch, 
  NDivider,
  NText,
  NButton,
  NIcon,
  NTooltip
} from 'naive-ui';
import { useThemeStore, PRESET_COLORS, LAYOUT_TYPES } from '../stores/theme';
import { ColorPaletteOutline, DesktopOutline, RefreshOutline } from '@vicons/ionicons5';

// 使用主题存储
const themeStore = useThemeStore();

// 预设颜色列表
const presetColorList = Object.entries(PRESET_COLORS).map(([key, value]) => ({
  key,
  name: value.name,
  color: value.primaryColor
}));

// 布局类型列表
const layoutTypeList = Object.entries(LAYOUT_TYPES).map(([key, value]) => ({
  key,
  name: value.name,
  description: value.description
}));

// 当前选中的主题色
const selectedThemeColor = ref(themeStore.themeColor);

// 当前选中的布局类型
const selectedLayoutType = ref(themeStore.layoutType);

// 自定义颜色
const customColor = ref(themeStore.customColor);

// 是否使用自定义颜色
const useCustomColor = ref(themeStore.useCustomColor);

// 应用主题色设置
const applyThemeColor = () => {
  if (useCustomColor.value) {
    themeStore.setCustomThemeColor(customColor.value);
  } else {
    themeStore.setThemeColor(selectedThemeColor.value);
  }
};

// 应用布局设置
const applyLayoutType = () => {
  themeStore.setLayoutType(selectedLayoutType.value);
};

// 重置为默认设置
const resetToDefault = () => {
  selectedThemeColor.value = 'blue';
  selectedLayoutType.value = 'default';
  useCustomColor.value = false;
  customColor.value = '#72a0c9';
  
  themeStore.setThemeColor('blue');
  themeStore.setLayoutType('default');
};
</script>

<template>
  <n-card title="主题设置" class="theme-settings-card">
    <n-tabs type="line" animated>
      <!-- 主题色设置 -->
      <n-tab-pane name="color" tab="主题色">
        <n-space vertical>
          <n-text>预设主题色</n-text>
          <div class="color-preset-container">
            <div 
              v-for="item in presetColorList" 
              :key="item.key"
              class="color-preset-item"
              :class="{ active: selectedThemeColor === item.key && !useCustomColor }"
              @click="() => { selectedThemeColor = item.key; useCustomColor = false; }"
            >
              <div class="color-circle" :style="{ backgroundColor: item.color }"></div>
              <div class="color-name">{{ item.name }}</div>
            </div>
          </div>
          
          <n-divider />
          
          <n-space vertical size="small">
            <n-space align="center" justify="space-between">
              <n-text>自定义颜色</n-text>
              <n-switch v-model:value="useCustomColor" />
            </n-space>
            
            <n-color-picker 
              v-model:value="customColor" 
              :disabled="!useCustomColor"
              :show-alpha="false"
            />
          </n-space>
          
          <n-button 
            type="primary" 
            block 
            @click="applyThemeColor"
            :disabled="!useCustomColor && selectedThemeColor === themeStore.themeColor"
          >
            应用主题色
          </n-button>
        </n-space>
      </n-tab-pane>
      
      <!-- 布局设置 -->
      <n-tab-pane name="layout" tab="布局设置">
        <n-space vertical>
          <n-radio-group v-model:value="selectedLayoutType">
            <n-space vertical>
              <n-radio 
                v-for="item in layoutTypeList" 
                :key="item.key" 
                :value="item.key"
              >
                <n-space align="center">
                  <n-text>{{ item.name }}</n-text>
                  <n-tooltip trigger="hover">
                    <template #trigger>
                      <n-icon size="16">
                        <DesktopOutline />
                      </n-icon>
                    </template>
                    {{ item.description }}
                  </n-tooltip>
                </n-space>
              </n-radio>
            </n-space>
          </n-radio-group>
          
          <n-button 
            type="primary" 
            block 
            @click="applyLayoutType"
            :disabled="selectedLayoutType === themeStore.layoutType"
          >
            应用布局设置
          </n-button>
        </n-space>
      </n-tab-pane>
    </n-tabs>
    
    <template #footer>
      <n-space justify="end">
        <n-button @click="resetToDefault">
          <template #icon>
            <n-icon>
              <RefreshOutline />
            </n-icon>
          </template>
          重置为默认设置
        </n-button>
      </n-space>
    </template>
  </n-card>
</template>

<style scoped>
.theme-settings-card {
  max-width: 600px;
  margin: 0 auto;
}

.color-preset-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin: 16px 0;
}

.color-preset-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.color-preset-item:hover {
  background-color: var(--n-color-hover);
}

.color-preset-item.active {
  background-color: rgba(114, 160, 201, 0.1);
}

.color-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-bottom: 8px;
  border: 2px solid var(--n-border-color);
}

.color-name {
  font-size: 12px;
  color: var(--n-text-color);
}
</style>

