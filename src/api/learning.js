// API请求模块 - 学习资料相关
// api/learning.js

import request from '../utils/request'

// 获取推荐学习资料
export function getRecommendedMaterials() {
  return request({
    url: '/api/learning/recommended',
    method: 'get'
  })
}

// 获取学习资料详情
export function getMaterialDetail(materialId) {
  return request({
    url: '/api/learning/material',
    method: 'get',
    params: { materialId }
  })
}
