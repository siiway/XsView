// API请求模块
// api/auth.js

import request from '../utils/request'

// 登录
export function login(data) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
}

// 注册
export function register(data) {
  return request({
    url: '/api/auth/register',
    method: 'post',
    data
  })
}

// 刷新令牌
export function refreshToken(data) {
  return request({
    url: '/api/auth/refresh-token',
    method: 'post',
    data
  })
}

// 获取用户信息
export function getUserInfo() {
  return request({
    url: '/api/user/info',
    method: 'get'
  })
}

// 更新用户信息
export function updateUserInfo(data) {
  return request({
    url: '/api/user/update',
    method: 'put',
    data
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/api/user/change-password',
    method: 'put',
    data
  })
}

// 绑定原平台账号
export function bindOriginalAccount(data) {
  return request({
    url: '/api/auth/bind-original-account',
    method: 'post',
    data
  })
}

// 找回密码
export function forgotPassword(data) {
  return request({
    url: '/api/auth/forgot-password',
    method: 'post',
    data
  })
}
