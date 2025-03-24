<!-- 成绩分析页面 -->
<!-- views/exam/ExamAnalysis.vue -->

<template>
  <div class="exam-analysis-container">
    <n-card v-if="loading" class="loading-card">
      <n-spin size="large" />
    </n-card>
    
    <template v-else>
      <!-- 考试基本信息 -->
      <n-card class="exam-info-card">
        <div class="exam-header">
          <h1 class="exam-title">{{ examAnalysis.title }} - 成绩分析</h1>
          <n-tag v-if="examAnalysis.isImportant" type="error" size="small">重要</n-tag>
        </div>
        <div class="exam-meta">
          <n-space>
            <n-tag :type="getSubjectTagType(examAnalysis.subject)">{{ examAnalysis.subject }}</n-tag>
            <span>考试时间: {{ formatDate(examAnalysis.examTime) }}</span>
            <span>班级: {{ examAnalysis.className }}</span>
          </n-space>
        </div>
      </n-card>

      <!-- 分析内容 -->
      <n-grid :cols="24" :x-gap="16" :y-gap="16" class="analysis-grid">
        <!-- 成绩概览 -->
        <n-grid-item :span="isMobile ? 24 : 8">
          <n-card title="成绩概览" size="small">
            <div class="score-overview">
              <div class="my-score">
                <div class="score-label">我的得分</div>
                <div class="score-value">{{ examAnalysis.score }}</div>
                <div class="score-total">满分 {{ examAnalysis.totalScore }}</div>
              </div>
              <n-divider />
              <div class="score-stats">
                <div class="stat-item">
                  <div class="stat-label">平均分</div>
                  <div class="stat-value">{{ examAnalysis.averageScore }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">最高分</div>
                  <div class="stat-value">{{ examAnalysis.highestScore }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">最低分</div>
                  <div class="stat-value">{{ examAnalysis.lowestScore }}</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">标准差</div>
                  <div class="stat-value">{{ examAnalysis.standardDeviation }}</div>
                </div>
              </div>
              <n-divider />
              <div class="rank-info">
                <div class="rank-label">我的排名</div>
                <div class="rank-value">{{ examAnalysis.rank }}/{{ examAnalysis.totalStudents }}</div>
                <div class="rank-percentile">超过了 {{ calculatePercentile(examAnalysis.rank, examAnalysis.totalStudents) }}% 的同学</div>
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 分数分布 -->
        <n-grid-item :span="isMobile ? 24 : 16">
          <n-card title="分数分布" size="small">
            <div ref="scoreDistributionChart" class="chart-container"></div>
          </n-card>
        </n-grid-item>

        <!-- 历史趋势 -->
        <n-grid-item :span="isMobile ? 24 : 12">
          <n-card title="历史趋势" size="small">
            <div ref="historyTrendChart" class="chart-container"></div>
          </n-card>
        </n-grid-item>

        <!-- 班级排名趋势 -->
        <n-grid-item :span="isMobile ? 24 : 12">
          <n-card title="班级排名趋势" size="small">
            <div ref="rankTrendChart" class="chart-container"></div>
          </n-card>
        </n-grid-item>

        <!-- 知识点掌握度 -->
        <n-grid-item :span="24">
          <n-card title="知识点掌握度" size="small">
            <div ref="knowledgeRadarChart" class="chart-container radar-chart"></div>
          </n-card>
        </n-grid-item>

        <!-- 题型分析 -->
        <n-grid-item :span="isMobile ? 24 : 12">
          <n-card title="题型分析" size="small">
            <div ref="questionTypeChart" class="chart-container"></div>
          </n-card>
        </n-grid-item>

        <!-- 错题分布 -->
        <n-grid-item :span="isMobile ? 24 : 12">
          <n-card title="错题分布" size="small">
            <div ref="wrongQuestionChart" class="chart-container"></div>
          </n-card>
        </n-grid-item>

        <!-- 学习建议 -->
        <n-grid-item :span="24">
          <n-card title="学习建议" size="small">
            <div class="learning-suggestions">
              <div v-if="examAnalysis.suggestions.length === 0" class="empty-container">
                <n-empty description="暂无学习建议" />
              </div>
              <div v-else>
                <n-collapse>
                  <n-collapse-item
                    v-for="(suggestion, index) in examAnalysis.suggestions"
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
                      <div v-if="suggestion.materials.length > 0" class="related-materials">
                        <div class="materials-title">推荐学习资料:</div>
                        <n-list>
                          <n-list-item v-for="material in suggestion.materials" :key="material.id">
                            <n-thing :title="material.title">
                              <template #description>
                                <div class="material-type">{{ material.type }}</div>
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
                  </n-collapse-item>
                </n-collapse>
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <n-space>
          <n-button @click="goToDetail">返回详情</n-button>
          <n-button type="info" @click="generateReport">生成诊断报告</n-button>
          <n-button type="primary" @click="goToLearningMaterials">查看推荐学习资料</n-button>
        </n-space>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getExamAnalysis } from '../../api/exam'
import { generateDiagnosticReport } from '../../api/diagnostic'
import { 
  NCard, 
  NGrid, 
  NGridItem, 
  NSpin, 
  NTag, 
  NSpace, 
  NDivider,
  NEmpty,
  NCollapse,
  NCollapseItem,
  NList,
  NListItem,
  NThing,
  NButton,
  useMessage
} from 'naive-ui'
import * as echarts from 'echarts/core'
import { 
  BarChart, 
  LineChart, 
  PieChart, 
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
  LineChart,
  PieChart,
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
const examAnalysis = ref({
  id: '',
  title: '',
  subject: '',
  examTime: '',
  className: '',
  score: 0,
  totalScore: 100,
  rank: 0,
  totalStudents: 0,
  averageScore: 0,
  highestScore: 0,
  lowestScore: 0,
  standardDeviation: 0,
  distribution: [],
  historyScores: [],
  historyRanks: [],
  knowledgePoints: [],
  questionTypes: [],
  wrongQuestions: [],
  suggestions: []
})
const isMobile = ref(window.innerWidth < 768)

// 图表引用
const scoreDistributionChart = ref(null)
const historyTrendChart = ref(null)
const rankTrendChart = ref(null)
const knowledgeRadarChart = ref(null)
const questionTypeChart = ref(null)
const wrongQuestionChart = ref(null)

// 图表实例
let scoreDistributionInstance = null
let historyTrendInstance = null
let rankTrendInstance = null
let knowledgeRadarInstance = null
let questionTypeInstance = null
let wrongQuestionInstance = null

// 生命周期钩子
onMounted(() => {
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 获取考试分析数据
  fetchExamAnalysis()
})

// 方法
// 获取考试分析数据
const fetchExamAnalysis = async () => {
  loading.value = true
  try {
    const examId = route.params.id
    const res = await getExamAnalysis(examId)
    
    if (res.code === 0) {
      examAnalysis.value = res.data
      
      // 等待DOM更新后初始化图表
      await nextTick()
      initCharts()
    } else {
      message.error('获取考试分析失败')
    }
  } catch (error) {
    console.error('获取考试分析失败:', error)
    message.error('获取考试分析失败')
  } finally {
    loading.value = false
  }
}

// 初始化所有图表
const initCharts = () => {
  initScoreDistributionChart()
  initHistoryTrendChart()
  initRankTrendChart()
  initKnowledgeRadarChart()
  initQuestionTypeChart()
  initWrongQuestionChart()
}

// 初始化分数分布图表
const initScoreDistributionChart = () => {
  if (!scoreDistributionChart.value) return
  
  scoreDistributionInstance = echarts.init(scoreDistributionChart.value)
  
  // 处理分数分布数据
  const scoreRanges = [
    { min: 0, max: 59, label: '不及格 (0-59)' },
    { min: 60, max: 69, label: '及格 (60-69)' },
    { min: 70, max: 79, label: '中等 (70-79)' },
    { min: 80, max: 89, label: '良好 (80-89)' },
    { min: 90, max: 100, label: '优秀 (90-100)' }
  ]
  
  const rangeData = scoreRanges.map(range => {
    const count = examAnalysis.value.distribution.filter(
      score => score >= range.min && score <= range.max
    ).length
    return {
      name: range.label,
      value: count
    }
  })
  
  // 找到我的分数所在的范围
  const myScore = examAnalysis.value.score
  const myScoreRange = scoreRanges.find(
    range => myScore >= range.min && myScore <= range.max
  )
  
  const option = {
    title: {
      text: '分数分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['人数', '我的分数'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: scoreRanges.map(range => range.label)
    },
    yAxis: {
      type: 'value',
      name: '人数'
    },
    series: [
      {
        name: '人数',
        type: 'bar',
        data: rangeData.map(item => item.value),
        itemStyle: {
          color: function(params) {
            const colors = ['#909399', '#d03050', '#f0a020', '#2080f0', '#18a058']
            return colors[params.dataIndex]
          }
        }
      },
      {
        name: '我的分数',
        type: 'scatter',
        symbolSize: 20,
        data: scoreRanges.map((range, index) => {
          if (range === myScoreRange) {
            return [index, rangeData[index].value + 2]
          }
          return [index, -100] // 不显示
        }),
        itemStyle: {
          color: '#ff6b81'
        },
        label: {
          show: true,
          formatter: '{b}',
          position: 'top',
          fontSize: 14,
          color: '#ff6b81'
        }
      }
    ]
  }
  
  scoreDistributionInstance.setOption(option)
}

// 初始化历史趋势图表
const initHistoryTrendChart = () => {
  if (!historyTrendChart.value) return
  
  historyTrendInstance = echarts.init(historyTrendChart.value)
  
  const historyData = examAnalysis.value.historyScores
  
  const option = {
    title: {
      text: '历史成绩趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
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
      data: historyData.map(item => item.examName)
    },
    yAxis: {
      type: 'value',
      name: '分数',
      min: function(value) {
        return Math.max(0, Math.floor(value.min * 0.8))
      }
    },
    series: [
      {
        name: '我的分数',
        type: 'line',
        data: historyData.map(item => item.score),
        itemStyle: {
          color: '#2080f0'
        },
        lineStyle: {
          width: 3
        },
        symbol: 'circle',
        symbolSize: 8,
        markPoint: {
          data: [
            { type: 'max', name: '最高分' },
            { type: 'min', name: '最低分' }
          ]
        },
        markLine: {
          data: [
            { type: 'average', name: '平均分' }
          ]
        }
      },
      {
        name: '班级平均分',
        type: 'line',
        data: historyData.map(item => item.averageScore),
        itemStyle: {
          color: '#f0a020'
        },
        lineStyle: {
          width: 2,
          type: 'dashed'
        },
        symbol: 'circle',
        symbolSize: 6
      }
    ]
  }
  
  historyTrendInstance.setOption(option)
}

// 初始化排名趋势图表
const initRankTrendChart = () => {
  if (!rankTrendChart.value) return
  
  rankTrendInstance = echarts.init(rankTrendChart.value)
  
  const rankData = examAnalysis.value.historyRanks
  
  const option = {
    title: {
      text: '班级排名趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const data = params[0].data
        return `${params[0].name}<br/>${params[0].seriesName}: 第${data}名`
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
      data: rankData.map(item => item.examName)
    },
    yAxis: {
      type: 'value',
      name: '排名',
      inverse: true,
      min: 1,
      max: function(value) {
        return Math.ceil(value.max * 1.1)
      }
    },
    series: [
      {
        name: '排名',
        type: 'line',
        data: rankData.map(item => item.rank),
        itemStyle: {
          color: '#18a058'
        },
        lineStyle: {
          width: 3
        },
        symbol: 'circle',
        symbolSize: 8,
        markPoint: {
          data: [
            { type: 'min', name: '最好排名' },
            { type: 'max', name: '最差排名' }
          ]
        }
      }
    ]
  }
  
  rankTrendInstance.setOption(option)
}

// 初始化知识点雷达图
const initKnowledgeRadarChart = () => {
  if (!knowledgeRadarChart.value) return
  
  knowledgeRadarInstance = echarts.init(knowledgeRadarChart.value)
  
  const knowledgePoints = examAnalysis.value.knowledgePoints
  
  const option = {
    title: {
      text: '知识点掌握度',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      data: ['我的掌握度', '班级平均'],
      bottom: 10
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
            name: '我的掌握度',
            itemStyle: {
              color: '#2080f0'
            },
            areaStyle: {
              color: 'rgba(32, 128, 240, 0.3)'
            }
          },
          {
            value: knowledgePoints.map(point => point.classAverage * 100),
            name: '班级平均',
            itemStyle: {
              color: '#f0a020'
            },
            areaStyle: {
              color: 'rgba(240, 160, 32, 0.3)'
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
  
  const questionTypes = examAnalysis.value.questionTypes
  
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

// 初始化错题分布图表
const initWrongQuestionChart = () => {
  if (!wrongQuestionChart.value) return
  
  wrongQuestionInstance = echarts.init(wrongQuestionChart.value)
  
  // 按知识点统计错题
  const wrongQuestions = examAnalysis.value.wrongQuestions
  const knowledgePointMap = {}
  
  wrongQuestions.forEach(question => {
    question.knowledgePoints.forEach(point => {
      if (!knowledgePointMap[point]) {
        knowledgePointMap[point] = 0
      }
      knowledgePointMap[point]++
    })
  })
  
  const knowledgePointData = Object.entries(knowledgePointMap)
    .map(([name, count]) => ({ name, value: count }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 8) // 最多显示8个
  
  const option = {
    title: {
      text: '错题知识点分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'middle'
    },
    series: [
      {
        name: '错题数量',
        type: 'pie',
        radius: '55%',
        center: ['60%', '50%'],
        data: knowledgePointData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  wrongQuestionInstance.setOption(option)
}

// 处理窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth < 768
  
  // 调整图表大小
  scoreDistributionInstance?.resize()
  historyTrendInstance?.resize()
  rankTrendInstance?.resize()
  knowledgeRadarInstance?.resize()
  questionTypeInstance?.resize()
  wrongQuestionInstance?.resize()
}

// 计算百分位数
const calculatePercentile = (rank, total) => {
  return ((total - rank) / total * 100).toFixed(1)
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

// 生成诊断报告
const generateReport = async () => {
  try {
    const res = await generateDiagnosticReport({ examId: route.params.id })
    if (res.code === 0) {
      message.success('诊断报告生成成功')
      router.push({ name: 'DiagnosticDetail', params: { id: res.data.reportId } })
    }
  } catch (error) {
    console.error('生成诊断报告失败:', error)
    message.error('生成诊断报告失败')
  }
}

// 查看学习资料详情
const goToMaterialDetail = (materialId) => {
  router.push({ name: 'LearningDetail', params: { id: materialId } })
}

// 返回详情
const goToDetail = () => {
  router.push({ name: 'ExamDetail', params: { id: route.params.id } })
}

// 查看推荐学习资料
const goToLearningMaterials = () => {
  router.push({ name: 'LearningMaterials' })
}
</script>

<style scoped>
.exam-analysis-container {
  padding: 16px;
}

.loading-card {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.exam-info-card {
  margin-bottom: 16px;
}

.exam-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.exam-title {
  margin: 0;
  margin-right: 8px;
  font-size: 24px;
}

.exam-meta {
  margin-bottom: 16px;
  color: #666;
}

.analysis-grid {
  margin-bottom: 16px;
}

.score-overview {
  padding: 8px;
}

.my-score {
  text-align: center;
  margin-bottom: 16px;
}

.score-label {
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  color: #18a058;
}

.score-total {
  font-size: 14px;
  color: #999;
}

.score-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
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

.rank-info {
  text-align: center;
}

.rank-label {
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
}

.rank-value {
  font-size: 24px;
  font-weight: bold;
  color: #2080f0;
}

.rank-percentile {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.chart-container {
  height: 300px;
  width: 100%;
}

.radar-chart {
  height: 400px;
}

.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.suggestion-content {
  padding: 8px;
}

.related-points, .related-materials {
  margin-top: 16px;
}

.related-title, .materials-title {
  font-weight: bold;
  margin-bottom: 8px;
}

.related-tags {
  display: flex;
  flex-wrap: wrap;
}

.material-type {
  font-size: 12px;
  color: #666;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

@media (max-width: 767px) {
  .exam-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .exam-title {
    margin-bottom: 8px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .radar-chart {
    height: 300px;
  }
}
</style>
