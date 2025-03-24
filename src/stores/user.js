// 用户状态管理
// stores/user.js

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { login, register, getUserInfo, updateUserInfo, changePassword, bindOriginalAccount } from '../api/auth'

export const useUserStore = defineStore('user', () => {
  // 路由实例
  const router = useRouter()
  
  // 消息提示
  const message = useMessage()
  
  // 状态
  const token = ref('')
  const refreshToken = ref('')
  const userId = ref('')
  const username = ref('')
  const email = ref('')
  const phone = ref('')
  const role = ref({})
  const originalPlatformId = ref(null)
  const lastLogin = ref(null)
  const redirectRoute = ref('/')
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isBindOriginalAccount = computed(() => !!originalPlatformId.value)
  
  // 方法
  // 初始化用户状态
  function initUserFromStorage() {
    const storedToken = localStorage.getItem('token')
    const storedRefreshToken = localStorage.getItem('refreshToken')
    const storedUserId = localStorage.getItem('userId')
    const storedUsername = localStorage.getItem('username')
    
    if (storedToken && storedUserId) {
      token.value = storedToken
      refreshToken.value = storedRefreshToken || ''
      userId.value = storedUserId
      username.value = storedUsername || ''
      
      // 获取用户详细信息
      fetchUserInfo()
    }
  }
  
  // 登录
  async function userLogin(loginData) {
    try {
      const res = await login(loginData)
      
      if (res.code === 0) {
        const userData = res.data
        
        // 保存用户信息
        token.value = userData.token
        refreshToken.value = userData.refreshToken || ''
        userId.value = userData.userId
        username.value = userData.username
        
        // 保存到本地存储
        localStorage.setItem('token', userData.token)
        localStorage.setItem('refreshToken', userData.refreshToken || '')
        localStorage.setItem('userId', userData.userId)
        localStorage.setItem('username', userData.username)
        
        // 获取用户详细信息
        await fetchUserInfo()
        
        // 跳转到重定向路由或首页
        router.push(redirectRoute.value)
        
        return { success: true }
      } else {
        message.error(res.msg || '登录失败')
        return { success: false, message: res.msg }
      }
    } catch (error) {
      message.error('登录请求异常')
      return { success: false, message: error.message }
    }
  }
  
  // 注册
  async function userRegister(registerData) {
    try {
      const res = await register(registerData)
      
      if (res.code === 0) {
        const userData = res.data
        
        // 保存用户信息
        token.value = userData.token
        userId.value = userData.userId
        username.value = userData.username
        
        // 保存到本地存储
        localStorage.setItem('token', userData.token)
        localStorage.setItem('userId', userData.userId)
        localStorage.setItem('username', userData.username)
        
        // 获取用户详细信息
        await fetchUserInfo()
        
        // 跳转到绑定原平台账号页面
        router.push({ name: 'BindAccount' })
        
        return { success: true }
      } else {
        message.error(res.msg || '注册失败')
        return { success: false, message: res.msg }
      }
    } catch (error) {
      message.error('注册请求异常')
      return { success: false, message: error.message }
    }
  }
  
  // 获取用户信息
  async function fetchUserInfo() {
    try {
      const res = await getUserInfo()
      
      if (res.code === 0) {
        const userInfo = res.data
        
        // 更新用户信息
        email.value = userInfo.email || ''
        phone.value = userInfo.phone || ''
        role.value = userInfo.role || {}
        originalPlatformId.value = userInfo.originalPlatformId
        lastLogin.value = userInfo.lastLogin
        
        return { success: true }
      } else {
        return { success: false, message: res.msg }
      }
    } catch (error) {
      return { success: false, message: error.message }
    }
  }
  
  // 更新用户信息
  async function updateProfile(profileData) {
    try {
      const res = await updateUserInfo(profileData)
      
      if (res.code === 0) {
        const updatedInfo = res.data
        
        // 更新用户信息
        email.value = updatedInfo.email || email.value
        phone.value = updatedInfo.phone || phone.value
        
        message.success('个人信息更新成功')
        return { success: true }
      } else {
        message.error(res.msg || '更新失败')
        return { success: false, message: res.msg }
      }
    } catch (error) {
      message.error('更新请求异常')
      return { success: false, message: error.message }
    }
  }
  
  // 修改密码
  async function updatePassword(passwordData) {
    try {
      const res = await changePassword(passwordData)
      
      if (res.code === 0) {
        message.success('密码修改成功')
        return { success: true }
      } else {
        message.error(res.msg || '修改失败')
        return { success: false, message: res.msg }
      }
    } catch (error) {
      message.error('修改请求异常')
      return { success: false, message: error.message }
    }
  }
  
  // 绑定原平台账号
  async function bindAccount(accountData) {
    try {
      const res = await bindOriginalAccount(accountData)
      
      if (res.code === 0) {
        const bindData = res.data
        
        // 更新绑定状态
        originalPlatformId.value = bindData.originalPlatformId
        
        message.success('账号绑定成功')
        return { success: true }
      } else {
        message.error(res.msg || '绑定失败')
        return { success: false, message: res.msg }
      }
    } catch (error) {
      message.error('绑定请求异常')
      return { success: false, message: error.message }
    }
  }
  
  // 登出
  function logout() {
    // 清除用户信息
    token.value = ''
    refreshToken.value = ''
    userId.value = ''
    username.value = ''
    email.value = ''
    phone.value = ''
    role.value = {}
    originalPlatformId.value = null
    lastLogin.value = null
    
    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userId')
    localStorage.removeItem('username')
    
    // 跳转到登录页
    router.push({ name: 'Login' })
  }
  
  // 设置重定向路由
  function setRedirectRoute(route) {
    redirectRoute.value = route
  }
  
  return {
    // 状态
    token,
    refreshToken,
    userId,
    username,
    email,
    phone,
    role,
    originalPlatformId,
    lastLogin,
    redirectRoute,
    
    // 计算属性
    isLoggedIn,
    isBindOriginalAccount,
    
    // 方法
    initUserFromStorage,
    userLogin,
    userRegister,
    fetchUserInfo,
    updateProfile,
    updatePassword,
    bindAccount,
    logout,
    setRedirectRoute
  }
})
