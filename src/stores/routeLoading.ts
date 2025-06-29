import { defineStore } from 'pinia';
import { ref } from 'vue';

// 定义路由加载状态存储
export const useRouteLoadingStore = defineStore('routeLoading', () => {
  // 是否正在加载路由
  const isLoading = ref(false);
  
  // 当前加载的路由名称
  const loadingRouteName = ref('');
  
  // 设置加载状态
  const setLoading = (loading: boolean, routeName: string = '') => {
    isLoading.value = loading;
    loadingRouteName.value = routeName;
  };
  
  // 开始加载
  const startLoading = (routeName: string) => {
    setLoading(true, routeName);
  };
  
  // 结束加载
  const endLoading = () => {
    setLoading(false, '');
  };
  
  return {
    isLoading,
    loadingRouteName,
    setLoading,
    startLoading,
    endLoading
  };
}, {
  persist: false // 不需要持久化
});

