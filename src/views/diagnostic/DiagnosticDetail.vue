<!-- 诊断报告详情页面 -->
<!-- views/diagnostic/DiagnosticDetail.vue -->

<template>
  <div class="diagnostic-detail-container">
    <n-card v-if="loading" class="loading-card">
      <n-spin size="large" />
    </n-card>
    
    <template v-else>
      <!-- 报告头部 -->
      <n-card class="report-header-card">
        <div class="report-title">
          <h1>{{ report.examTitle }} - 诊断报告</h1>
          <n-tag type="info" size="small">{{ formatDate(report.createdAt) }}</n-tag>
        </div>
        <div class="report-meta">
          <n-space>
            <n-tag :type="getSubjectTagType(report.subject)">{{ report.subject }}</n-tag>
            <span>考试时间: {{ formatDate(report.examTime) }}</span>
            <span>得分: {{ report.score }}/{{ report.totalScore }}</span>
            <span>排名: {{ report.rank }}/{{ report.totalStudents }}</span>
          </n-space>
        </div>
      </n-card>

      <!-- 报告内容 -->
      <n-card title="诊断结果" class="report-content-card">
        <n-tabs type="line" animated>
          <!-- 总体评价 -->
          <n-tab-pane name="overview" tab="总体评价">
            <div class="overview-section">
              <div class="overview-score">
                <div class="score-circle" :style="{ borderColor: getScoreColor(report.score, report.totalScore) }">
                  <div class="score-value">{{ report.score }}</div>
                  <div class="score-total">/ {{ report.totalScore }}</div>
                </div>
                <div class="score-level" :style="{ color: getScoreColor(report.score, report.totalScore) }">
                  {{ getScoreLevel(report.score, report.totalScore) }}
                </div>
              </div>
              <div class="overview-content">
                <div class="overview-title">总体表现</div>
                <div class="overview-text">{{ report.overallEvaluation }}</div>
                <div class="overview-stats">
                  <div class="stat-item">
                    <div class="stat-label">正确率</div>
                    <div class="stat-value">{{ (report.correctRate * 100).toFixed(1) }}%</div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-label">完成率</div>
                    <div class="stat-value">{{ (report.completionRate * 100).toFixed(1) }}%</div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-label">超过同学</div>
                    <div class="stat-value">{{ ((report.totalStudents - report.rank) / report.totalStudents * 100).toFixed(1) }}%</div>
                  </div>
                </div>
              </div>
            </div>
            <n-divider />
            <div class="strengths-weaknesses">
              <div class="strengths">
                <div class="section-title">
                  <n-icon color="#18a058"><checkmark-circle-outline /></n-icon>
                  <span>优势</span>
                </div>
                <div class="section-content">
                  <n-list>
                    <n-list-item v-for="(strength, index) in report.strengths" :key="index">
                      <n-thing>
                        <template #description>
                          <div class="strength-item">{{ strength }}</div>
                        </template>
                      </n-thing>
                    </n-list-item>
                  </n-list>
                </div>
              </div>
              <div class="weaknesses">
                <div class="section-title">
                  <n-icon color="#d03050"><alert-circle-outline /></n-icon>
                  <span>不足</span>
                </div>
                <div class="section-content">
                  <n-list>
                    <n-list-item v-for="(weakness, index) in report.weaknesses" :key="index">
                      <n-thing>
                        <template #description>
                          <div class="weakness-item">{{ weakness }}</div>
                        </template>
                      </n-thing>
                    </n-list-item>
                  </n-list>
                </div>
              </div>
            </div>
          </n-tab-pane>

          <!-- 知识点分析 -->
          <n-tab-pane name="knowledge" tab="知识点分析">
            <div class="knowledge-section">
              <div class="knowledge-chart">
                <div ref="knowledgeRadarChart" class="radar-chart"></div>
              </div>
              <div class="knowledge-list">
                <n-list>
                  <n-list-item v-for="point in report.knowledgePoints" :key="point.name">
                    <n-thing :title="point.name">
                      <template #description>
                        <div class="knowledge-mastery">
                          <div class="mastery-label">掌握度:</div>
                          <n-progress
                            type="line"
                            :percentage="point.mastery * 100"
                            :color="getMasteryColor(point.mastery)"
                            :height="12"
                            :border-radius="6"
                            :format="percentageFormat"
                          />
                        </div>
                        <div class="knowledge-evaluation">{{ point.evaluation }}</div>
                      </template>
                    </n-thing>
                  </n-list-item>
                </n-list>
              </div>
            </div>
          </n-tab-pane>

          <!-- 题型分析 -->
          <n-tab-pane name="question-types" tab="题型分析">
            <div class="question-types-section">
              <div class="question-types-chart">
                <div ref="questionTypeChart" class="bar-chart"></div>
              </div>
              <div class="question-types-list">
                <n-list>
                  <n-list-item v-for="type in report.questionTypes" :key="type.name">
                    <n-thing :title="type.name">
                      <template #description>
                        <div class="type-score">
                          <div class="score-label">得分率:</div>
                          <n-progress
                            type="line"
                            :percentage="(type.score / type.totalScore) * 100"
                            :color="getScoreRateColor(type.score / type.totalScore)"
                            :height="12"
                            :border-radius="6"
                            :format="percentageFormat"
                          />
                        </div>
                        <div class="type-evaluation">{{ type.evaluation }}</div>
                      </template>
                    </n-thing>
                  </n-list-item>
                </n-list>
              </div>
            </div>
          </n-tab-pane>

          <!-- 学习建议 -->
          <n-tab-pane name="suggestions" tab="学习建议">
            <div class="suggestions-section">
              <div class="general-suggestions">
                <div class="section-title">总体建议</div>
                <div class="section-content">{{ report.generalSuggestion }}</div>
              </div>
              <n-divider />
              <div class="specific-suggestions">
                <div class="section-title">具体建议</div>
                <n-collapse>
                  <n-collapse-item
                    v-for="(suggestion, index) in report.specificSuggestions"
                    :key="index"
                    :title="suggestion.title"
                  >
                    <div class="suggestion-content">
                      <p>{{ suggestion.content }}</p>
                      <div v-if="suggestion.relatedKnowledgePoints.length > 0" class="related-points">
                        <div class="related-title">相关知识点:</div>
                        <div class="related-tags">
                          <n-tag
                            v-for="point in suggestion.relatedKnowledgePoints"
                            :key="point"
                            size="small"
                            style="margin-right: 8px; margin-bottom: 8px"
                          >
                            {{ point }}
                          </n-tag>
                        </div>
                      </div>
                    </div>
                  </n-collapse-item>
                </n-collapse>
              </div>
              <n-divider />
              <div class="learning-materials">
                <div class="section-title">推荐学习资料</div>
                <n-list>
                  <n-list-item v-for="material in report.recommendedMaterials" :key="material.id">
                    <n-thing :title="material.title">
                      <template #avatar>
                        <n-avatar round :style="{ backgroundColor: getMaterialColor(material.type) }">
                          {{ getMaterialIcon(material.type) }}
                        </n-avatar>
                      </template>
                      <template #description>
                        <div class="material-info">
                          <div class="material-type">{{ material.type }}</div>
                          <div class="material-knowledge-point">{{ material.knowledgePoint }}</div>
                        </div>
                      </template>
                      <template #footer>
                        <n-button text size="small" @click="goToMaterialDetail(material.id)">
                          查看详情
                        </n-button>
                      </template>
                    </n-thing>
                  </n-list-item>
                </n-list>
              </div>
            </div>
          </n-tab-pane>
        </n-tabs>
      </n-card>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <n-space>
          <n-button @click="goBack">返回列表</n-button>
          <n-button type="primary" @click="downloadReport">下载报告</n-button>
          <n-button type="info" @click="goToLearningMaterials">查看推荐学习资料</n-button>
        </n-space>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDiagnosticReport } from '../../api/diagnostic'
import { 
  NCard, 
  NSpin, 
  NTag, 
  NSpace, 
  NTabs,
  NTabPane,
  NDivider,
  NList,
  NListItem,
  NThing,
  NButton,
  NProgress,
  NCollapse,
  NCollapseItem,
  NAvatar,
  NIcon,
  useMessage
} from 'naive-ui'
import { 
  CheckmarkCircleOutline, 
  AlertCircleOutline 
} from '@vicons/ionicons5'
import * as echarts from 'echarts/core'
import { 
  BarChart, 
  RadarChart 
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

// 注册 ECharts 组件
echarts.use([
  BarChart,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CanvasRenderer
])

// 路由实例
const route = useRoute()
const router = useRouter()

// 消息提示
const message = useMessage()

// 响应式状态
const loading = ref(true)
const report = ref({
  id: '',
  examId: '',
  examTitle: '',
  subject: '',
  examTime: '',
  score: 0,
  totalScore: 100,
  rank: 0,
  totalStudents: 0,
  correctRate: 0,
  completionRate: 0,
  overallEvaluation: '',
  strengths: [],
  weaknesses: [],
  knowledgePoints: [],
  questionTypes: [],
  generalSuggestion: '',
  specificSuggestions: [],
  recommendedMaterials: [],
  createdAt: ''
})

// 图表引用
const knowledgeRadarChart = ref(null)
const questionTypeChart = ref(null)

// 图表实例
let knowledgeRadarInstance = null
let questionTypeInstance = null

// 生命周期钩子
onMounted(() => {
  // 获取诊断报告数据
  fetchDiagnosticReport()
})

// 方法
// 获取诊断报告数据
const fetchDiagnosticReport = async () => {
  loading.value = true
  try {
    const reportId = route.params.id
    const res = await getDiagnosticReport(reportId)
    
    if (res.code === 0) {
      report.value = res.data
      
      // 等待DOM更新后初始化图表
      await nextTick()
      initCharts()
    } else {
      message.error('获取诊断报告失败')
    }
  } catch (error) {
    console.error('获取诊断报告失败:', error)
    message.error('获取诊断报告失败')
  } finally {
    loading.value = false
  }
}

// 初始化所有图表
const initCharts = () => {
  initKnowledgeRadarChart()
  initQuestionTypeChart()
}

// 初始化知识点雷达图
const initKnowledgeRadarChart = () => {
  if (!knowledgeRadarChart.value) return
  
  knowledgeRadarInstance = echarts.init(knowledgeRadarChart.value)
  
  const knowledgePoints = report.value.knowledgePoints
  
  const option = {
    title: {
      text: '知识点掌握度',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: knowledgePoints.map(point => ({
        name: point.name,
        max: 100
      })),
      radius: '65%',
      center: ['50%', '50%']
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: knowledgePoints.map(point => point.mastery * 100),
            name: '掌握度',
            itemStyle: {
              color: '#2080f0'
            },
            areaStyle: {
              color: 'rgba(32, 128, 240, 0.3)'
            }
          }
        ]
      }
    ]
  }
  
  knowledgeRadarInstance.setOption(option)
}

// 初始化题型分析图表
const initQuestionTypeChart = () => {
  if (!questionTypeChart.value) return
  
  questionTypeInstance = echarts.init(questionTypeChart.value)
  
  const questionTypes = report.value.questionTypes
  
  const option = {
    title: {
      text: '题型得分率',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        const data = params[0].data
        return `${params[0].name}<br/>${params[0].seriesName}: ${data}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: questionTypes.map(type => type.name)
    },
    yAxis: {
      type: 'value',
      name: '得分率(%)',
      min: 0,
      max: 100
    },
    series: [
      {
        name: '得分率',
        type: 'bar',
        data: questionTypes.map(type => (type.score / type.totalScore * 100).toFixed(1)),
        itemStyle: {
          color: function(params) {
            const value = params.value
            if (value >= 80) return '#18a058'
            if (value >= 60) return '#2080f0'
            if (value >= 40) return '#f0a020'
            return '#d03050'
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}%'
        }
      }
    ]
  }
  
  questionTypeInstance.setOption(option)
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 获取学科标签类型
const getSubjectTagType = (subject) => {
  const typeMap = {
    '语文': 'success',
    '数学': 'info',
    '英语': 'warning',
    '物理': 'error',
    '化学': 'default',
    '生物': 'success',
    '历史': 'info',
    '地理': 'warning',
    '政治': 'error'
  }
  return typeMap[subject] || 'default'
}

// 获取分数颜色
const getScoreColor = (score, totalScore) => {
  const percentage = (score / totalScore) * 100
  if (percentage >= 90) return '#18a058'
  if (percentage >= 80) return '#2080f0'
  if (percentage >= 70) return '#f0a020'
  if (percentage >= 60) return '#d03050'
  return '#909399'
}

// 获取分数等级
const getScoreLevel = (score, totalScore) => {
  const percentage = (score / totalScore) * 100
  if (percentage >= 90) return '优秀'
  if (percentage >= 80) return '良好'
  if (percentage >= 70) return '中等'
  if (percentage >= 60) return '及格'
  return '不及格'
}

// 获取掌握度颜色
const getMasteryColor = (mastery) => {
  if (mastery >= 0.8) return '#18a058'
  if (mastery >= 0.6) return '#2080f0'
  if (mastery >= 0.4) return '#f0a020'
  return '#d03050'
}

// 获取得分率颜色
const getScoreRateColor = (rate) => {
  if (rate >= 0.8) return '#18a058'
  if (rate >= 0.6) return '#2080f0'
  if (rate >= 0.4) return '#f0a020'
  return '#d03050'
}

// 百分比格式化
const percentageFormat = (percentage) => {
  return `${percentage.toFixed(0)}%`
}

// 获取资料类型颜色
const getMaterialColor = (type) => {
  const colorMap = {
    '文档': '#2080f0',
    '视频': '#f0a020',
    '习题': '#18a058'
  }
  return colorMap[type] || '#2080f0'
}

// 获取资料类型图标
const getMaterialIcon = (type) => {
  const iconMap = {
    '文档': '文',
    '视频': '视',
    '习题': '习'
  }
  return iconMap[type] || '资'
}

// 查看学习资料详情
const goToMaterialDetail = (materialId) => {
  router.push({ name: 'LearningDetail', params: { id: materialId } })
}

// 返回列表
const goBack = () => {
  router.push({ name: 'DiagnosticList' })
}

// 下载报告
const downloadReport = () => {
  message.success('报告下载中...')
  // 实际项目中这里应该调用下载API
  setTimeout(() => {
    message.success('报告下载完成')
  }, 1500)
}

// 查看推荐学习资料
const goToLearningMaterials = () => {
  router.push({ name: 'LearningMaterials' })
}
</script>

<style scoped>
.diagnostic-detail-container {
  padding: 16px;
}

.loading-card {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.report-header-card {
  margin-bottom: 16px;
}

.report-title {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.report-title h1 {
  margin: 0;
  margin-right: 8px;
  font-size: 24px;
}

.report-meta {
  margin-bottom: 16px;
  color: #666;
}

.report-content-card {
  margin-bottom: 16px;
}

.overview-section {
  display: flex;
  margin-bottom: 24px;
}

.overview-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 32px;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 6px solid #18a058;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 8px;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
}

.score-total {
  font-size: 14px;
  color: #666;
}

.score-level {
  font-size: 18px;
  font-weight: bold;
  color: #18a058;
}

.overview-content {
  flex: 1;
}

.overview-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
}

.overview-text {
  margin-bottom: 16px;
  line-height: 1.6;
}

.overview-stats {
  display: flex;
  justify-content: space-between;
}

.stat-item {
  text-align: center;
  padding: 8px 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
}

.strengths-weaknesses {
  display: flex;
  gap: 24px;
}

.strengths, .weaknesses {
  flex: 1;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}

.section-title .n-icon {
  margin-right: 8px;
}

.strength-item, .weakness-item {
  margin-bottom: 8px;
  line-height: 1.6;
}

.knowledge-section {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.knowledge-chart {
  flex: 1;
  min-width: 300px;
}

.knowledge-list {
  flex: 1;
  min-width: 300px;
}

.radar-chart, .bar-chart {
  height: 400px;
  width: 100%;
}

.knowledge-mastery {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.mastery-label {
  width: 60px;
  margin-right: 8px;
}

.knowledge-evaluation {
  margin-top: 8px;
  color: #666;
  line-height: 1.6;
}

.question-types-section {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}

.question-types-chart {
  flex: 1;
  min-width: 300px;
}

.question-types-list {
  flex: 1;
  min-width: 300px;
}

.type-score {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.score-label {
  width: 60px;
  margin-right: 8px;
}

.type-evaluation {
  margin-top: 8px;
  color: #666;
  line-height: 1.6;
}

.suggestions-section {
  padding: 8px;
}

.general-suggestions {
  margin-bottom: 24px;
}

.section-content {
  line-height: 1.6;
}

.suggestion-content {
  padding: 8px;
  line-height: 1.6;
}

.related-points {
  margin-top: 16px;
}

.related-title {
  font-weight: bold;
  margin-bottom: 8px;
}

.related-tags {
  display: flex;
  flex-wrap: wrap;
}

.learning-materials {
  margin-top: 24px;
}

.material-info {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}

.material-type {
  padding: 2px 6px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
}

.material-knowledge-point {
  font-size: 12px;
  color: #666;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

@media (max-width: 767px) {
  .report-title {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .report-title h1 {
    margin-bottom: 8px;
  }
  
  .overview-section {
    flex-direction: column;
  }
  
  .overview-score {
    margin-right: 0;
    margin-bottom: 24px;
  }
  
  .strengths-weaknesses {
    flex-direction: column;
  }
  
  .radar-chart, .bar-chart {
    height: 300px;
  }
}
</style>
