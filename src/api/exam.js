// API请求模块 - 考试相关
// api/exam.js

import request from '../utils/request'

// 获取考试列表
export function getExamList(params) {
  return request({
    url: '/api/exam/list',
    method: 'get',
    params
  })
}

// 获取考试详情
export function getExamDetail(examId) {
  return request({
    url: '/api/exam/detail',
    method: 'get',
    params: { examId }
  })
}

// 获取考试分析
export function getExamAnalysis(examId) {
  return request({
    url: '/api/exam/analysis',
    method: 'get',
    params: { examId }
  })
}

// 获取错题列表
export function getWrongQuestions(examId) {
  return request({
    url: '/api/exam/wrong-questions',
    method: 'get',
    params: { examId }
  })
}
