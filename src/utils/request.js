// HTTP请求工具
// utils/request.js

import axios from 'axios'
import { useUserStore } from '../stores/user'
import { createDiscreteApi } from 'naive-ui'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    
    // 如果有token，添加到请求头
    if (userStore.token) {
      config.headers['Authorization'] = `Bearer ${userStore.token}`
    }
    
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果返回的不是JSON格式，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }
    
    // 如果状态码不为0，说明有错误
    if (res.code !== 0) {
      const { message } = createDiscreteApi(['message'])
      
      // 处理登录状态失效
      if (res.code === 2004) {
        message.error('登录状态已失效，请重新登录')
        
        // 清除用户状态并跳转到登录页
        const userStore = useUserStore()
        userStore.logout()
      } else {
        // 显示错误消息
        message.error(res.msg || '请求失败')
      }
      
      return Promise.reject(new Error(res.msg || '请求失败'))
    } else {
      return res
    }
  },
  error => {
    const { message } = createDiscreteApi(['message'])
    
    // 处理网络错误
    if (error.message.includes('Network Error')) {
      message.error('网络错误，请检查您的网络连接')
    } else if (error.message.includes('timeout')) {
      message.error('请求超时，请稍后重试')
    } else {
      message.error(error.message)
    }
    
    return Promise.reject(error)
  }
)

export default service
