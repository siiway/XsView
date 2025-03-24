// API请求模块 - 诊断报告相关
// api/diagnostic.js

import request from '../utils/request'

// 生成诊断报告
export function generateDiagnosticReport(data) {
  return request({
    url: '/api/diagnostic/generate',
    method: 'post',
    data
  })
}

// 获取诊断报告详情
export function getDiagnosticReport(reportId) {
  return request({
    url: '/api/diagnostic/report',
    method: 'get',
    params: { reportId }
  })
}

// 获取历史诊断报告列表
export function getHistoryReports(params) {
  return request({
    url: '/api/diagnostic/history',
    method: 'get',
    params
  })
}
