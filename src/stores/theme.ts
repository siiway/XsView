import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { GlobalThemeOverrides } from 'naive-ui'

// 预定义的主题色
export const PRESET_COLORS = {
  blue: {
    name: '蓝色',
    primaryColor: '#72a0c9',
    primaryColorHover: '#529bdb',
    primaryColorPressed: '#0F6FB8',
    primaryColorSuppl: '#529bdb',
  },
  green: {
    name: '绿色',
    primaryColor: '#18a058',
    primaryColorHover: '#36ad6a',
    primaryColorPressed: '#0c7a43',
    primaryColorSuppl: '#36ad6a',
  },
  purple: {
    name: '紫色',
    primaryColor: '#8a2be2',
    primaryColorHover: '#9d3ff3',
    primaryColorPressed: '#6a1cb1',
    primaryColorSuppl: '#9d3ff3',
  },
  orange: {
    name: '橙色',
    primaryColor: '#f0a020',
    primaryColorHover: '#fcb040',
    primaryColorPressed: '#d9910d',
    primaryColorSuppl: '#fcb040',
  },
  red: {
    name: '红色',
    primaryColor: '#d03050',
    primaryColorHover: '#e84c6a',
    primaryColorPressed: '#ab1f3f',
    primaryColorSuppl: '#e84c6a',
  }
}

// 预定义的布局类型
export const LAYOUT_TYPES = {
  default: {
    name: '默认布局',
    value: 'default',
    description: '侧边栏导航 + 顶部标题栏'
  },
  top: {
    name: '顶部导航',
    value: 'top',
    description: '顶部导航栏 + 内容区域'
  },
  compact: {
    name: '紧凑布局',
    value: 'compact',
    description: '折叠侧边栏 + 顶部标题栏'
  }
}

export const useThemeStore = defineStore('theme', () => {
  // 从localStorage获取初始主题，默认为暗色
  const isDark = ref(localStorage.getItem('theme') === 'dark' || 
                     localStorage.getItem('theme') === null)
  
  // 从localStorage获取主题色，默认为蓝色
  const themeColor = ref(localStorage.getItem('themeColor') || 'blue')
  
  // 从localStorage获取布局类型，默认为默认布局
  const layoutType = ref(localStorage.getItem('layoutType') || 'default')
  
  // 自定义主题色
  const customColor = ref(localStorage.getItem('customColor') || '#72a0c9')
  
  // 是否使用自定义颜色
  const useCustomColor = ref(localStorage.getItem('useCustomColor') === 'true')
  
  // 计算当前主题色对象
  const currentThemeColorObject = computed(() => {
    if (useCustomColor.value) {
      // 如果使用自定义颜色，生成一个主题色对象
      const color = customColor.value
      const lightenColor = lightenHexColor(color, 10)
      const darkenColor = darkenHexColor(color, 10)
      
      return {
        primaryColor: color,
        primaryColorHover: lightenColor,
        primaryColorPressed: darkenColor,
        primaryColorSuppl: lightenColor,
      }
    } else {
      // 否则使用预设颜色
      return PRESET_COLORS[themeColor.value as keyof typeof PRESET_COLORS] || PRESET_COLORS.blue
    }
  })
  
  // 计算主题覆盖对象
  const themeOverrides = computed<GlobalThemeOverrides>(() => ({
    common: {
      ...currentThemeColorObject.value
    }
  }))
  
  // 设置主题明暗
  function setTheme(dark: boolean) {
    isDark.value = dark
    // 保存主题设置到localStorage
    localStorage.setItem('theme', dark ? 'dark' : 'light')
    
    // 将主题应用到文档
    if (dark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    
    // 通知Tauri后端主题变化（如果需要）
    try {
      // @ts-ignore
      if (window.__TAURI__) {
        // @ts-ignore
        window.__TAURI__.invoke('set_theme', { dark })
      }
    } catch (e) {
      console.error('无法设置系统主题:', e)
    }
  }
  
  // 设置主题色
  function setThemeColor(color: string) {
    themeColor.value = color
    useCustomColor.value = false
    localStorage.setItem('themeColor', color)
    localStorage.setItem('useCustomColor', 'false')
  }
  
  // 设置自定义主题色
  function setCustomThemeColor(color: string) {
    customColor.value = color
    useCustomColor.value = true
    localStorage.setItem('customColor', color)
    localStorage.setItem('useCustomColor', 'true')
  }
  
  // 设置布局类型
  function setLayoutType(type: string) {
    layoutType.value = type
    localStorage.setItem('layoutType', type)
  }
  
  // 辅助函数：使十六进制颜色变亮
  function lightenHexColor(hex: string, percent: number): string {
    // 移除#号
    hex = hex.replace('#', '')
    
    // 解析RGB值
    const r = parseInt(hex.substring(0, 2), 16)
    const g = parseInt(hex.substring(2, 4), 16)
    const b = parseInt(hex.substring(4, 6), 16)
    
    // 增加亮度
    const factor = 1 + percent / 100
    const newR = Math.min(255, Math.round(r * factor))
    const newG = Math.min(255, Math.round(g * factor))
    const newB = Math.min(255, Math.round(b * factor))
    
    // 转换回十六进制
    return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
  }
  
  // 辅助函数：使十六进制颜色变暗
  function darkenHexColor(hex: string, percent: number): string {
    // 移除#号
    hex = hex.replace('#', '')
    
    // 解析RGB值
    const r = parseInt(hex.substring(0, 2), 16)
    const g = parseInt(hex.substring(2, 4), 16)
    const b = parseInt(hex.substring(4, 6), 16)
    
    // 减少亮度
    const factor = 1 - percent / 100
    const newR = Math.max(0, Math.round(r * factor))
    const newG = Math.max(0, Math.round(g * factor))
    const newB = Math.max(0, Math.round(b * factor))
    
    // 转换回十六进制
    return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
  }
  
  return { 
    isDark, 
    themeColor, 
    layoutType, 
    customColor, 
    useCustomColor,
    themeOverrides,
    currentThemeColorObject,
    setTheme, 
    setThemeColor, 
    setCustomThemeColor, 
    setLayoutType 
  }
}, {
  persist: true
})