// API请求模块 - 通知相关
// api/notification.js

import request from '../utils/request'

// 获取通知列表
export function getNotificationList(params) {
  return request({
    url: '/api/notification/list',
    method: 'get',
    params
  })
}

// 标记通知为已读
export function markNotificationRead(data) {
  return request({
    url: '/api/notification/read',
    method: 'put',
    data
  })
}
