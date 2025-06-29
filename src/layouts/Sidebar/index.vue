<script setup lang="ts">
import { ref, watch, inject, computed } from 'vue';
import { h } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { NMenu, NLayoutSider } from 'naive-ui';
import { 
  HomeOutline, 
  SchoolOutline, 
  DocumentTextOutline, 
  CalendarOutline, 
  SettingsOutline, 
  InformationOutline 
} from '@vicons/ionicons5';

// 获取当前路由
const route = useRoute();

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:collapsed']);

const toggleCollapse = (value: boolean) => {
  emit('update:collapsed', value);
};

// 菜单配置
const menuOptions = computed(() => [
  {
    label: () => h(RouterLink, { to: { name: 'Home' } }, { default: () => '主页' }),
    key: 'home',
    icon: () => h(HomeOutline)
  },
  {
    label: () => h(RouterLink, { to: { name: 'ExamQuery' } }, { default: () => '考试查询' }),
    key: 'examquery',
    icon: () => h(SchoolOutline)
  },
  {
    label: () => h(RouterLink, { to: { name: 'ScoreQuery' } }, { default: () => '成绩查询' }),
    key: 'scorequery',
    icon: () => h(DocumentTextOutline)
  },
  {
    label: () => h(RouterLink, { to: { name: 'ExamSchedule' } }, { default: () => '考试安排' }),
    key: 'examschedule',
    icon: () => h(CalendarOutline)
  },
  {
    label: () => h(RouterLink, { to: { name: 'Settings' } }, { default: () => '系统设置' }),
    key: 'settings',
    icon: () => h(SettingsOutline)
  },
  {
    label: () => h(RouterLink, { to: { name: 'About' } }, { default: () => '关于系统' }),
    key: 'about',
    icon: () => h(InformationOutline)
  }
]);

// 设置默认选中的菜单项
const selectedKey = ref('home');

// 监听路由变化，更新选中的菜单项
watch(() => route.name, (newRouteName) => {
  if (newRouteName) {
    // 将路由名称转换为小写，以匹配菜单key
    const routeKey = newRouteName.toString().toLowerCase();
    
    // 检查是否有匹配的菜单项
    const menuItem = menuOptions.value.find(item => item.key === routeKey);
    if (menuItem) {
      selectedKey.value = routeKey;
    }
  }
}, { immediate: true });
</script>

<template>
  <n-layout-sider 
    bordered 
    collapse-mode="width" 
    :collapsed-width="64" 
    :width="240" 
    :collapsed="props.collapsed"
    show-trigger 
    @collapse="toggleCollapse(true)" 
    @expand="toggleCollapse(false)"
  >
    <n-menu 
      :collapsed="props.collapsed" 
      :collapsed-width="64" 
      :collapsed-icon-size="22" 
      :options="menuOptions"
      v-model:value="selectedKey" 
    />
  </n-layout-sider>
</template>

<style scoped>
.n-menu {
  height: 100%;
}
</style>

