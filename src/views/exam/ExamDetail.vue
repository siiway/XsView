<!-- 考试详情页面 -->
<!-- views/exam/ExamDetail.vue -->

<template>
  <div class="exam-detail-container">
    <n-card v-if="loading" class="loading-card">
      <n-spin size="large" />
    </n-card>
    
    <template v-else>
      <!-- 考试基本信息 -->
      <n-card class="exam-info-card">
        <n-grid :cols="24" :x-gap="16">
          <n-grid-item :span="isMobile ? 24 : 16">
            <div class="exam-header">
              <h1 class="exam-title">{{ examDetail.title }}</h1>
              <n-tag v-if="examDetail.isImportant" type="error" size="small">重要</n-tag>
            </div>
            <div class="exam-meta">
              <n-space>
                <n-tag :type="getSubjectTagType(examDetail.subject)">{{ examDetail.subject }}</n-tag>
                <span>考试时间: {{ formatDate(examDetail.examTime) }}</span>
                <span>班级: {{ examDetail.className }}</span>
              </n-space>
            </div>
          </n-grid-item>
          <n-grid-item :span="isMobile ? 24 : 8">
            <div class="exam-score-card">
              <div class="score-header">我的成绩</div>
              <div class="score-value">{{ examDetail.score }}</div>
              <div class="score-total">满分 {{ examDetail.totalScore }}</div>
              <n-progress
                type="line"
                :percentage="(examDetail.score / examDetail.totalScore) * 100"
                :color="getScoreColor(examDetail.score, examDetail.totalScore)"
                :height="12"
                :border-radius="6"
              />
              <div class="score-rank">
                <n-icon><trophy-outline /></n-icon>
                排名: {{ examDetail.rank }}/{{ examDetail.totalStudents }}
              </div>
            </div>
          </n-grid-item>
        </n-grid>
      </n-card>

      <!-- 成绩详情 -->
      <n-card title="成绩详情" class="score-detail-card">
        <n-tabs type="line" animated>
          <!-- 分数详情 -->
          <n-tab-pane name="scores" tab="分数详情">
            <n-grid :cols="24" :x-gap="16" :y-gap="16">
              <n-grid-item :span="isMobile ? 24 : 12">
                <n-card title="各题得分" size="small">
                  <n-data-table
                    :columns="questionColumns"
                    :data="examDetail.questions"
                    :pagination="false"
                    :bordered="false"
                  />
                </n-card>
              </n-grid-item>
              <n-grid-item :span="isMobile ? 24 : 12">
                <n-card title="得分统计" size="small">
                  <div class="score-stats">
                    <div class="stat-item">
                      <div class="stat-label">平均分</div>
                      <div class="stat-value">{{ examDetail.averageScore }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">最高分</div>
                      <div class="stat-value">{{ examDetail.highestScore }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">最低分</div>
                      <div class="stat-value">{{ examDetail.lowestScore }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">标准差</div>
                      <div class="stat-value">{{ examDetail.standardDeviation }}</div>
                    </div>
                  </div>
                  <div class="score-distribution">
                    <div class="distribution-title">分数分布</div>
                    <n-progress
                      v-for="(range, index) in scoreRanges"
                      :key="index"
                      type="line"
                      :percentage="getDistributionPercentage(range.min, range.max)"
                      :color="range.color"
                      :height="12"
                      :border-radius="6"
                      :show-indicator="false"
                      style="margin-bottom: 8px"
                    />
                    <div class="distribution-legend">
                      <div v-for="(range, index) in scoreRanges" :key="index" class="legend-item">
                        <div class="legend-color" :style="{ backgroundColor: range.color }"></div>
                        <div class="legend-label">{{ range.label }}</div>
                      </div>
                    </div>
                  </div>
                </n-card>
              </n-grid-item>
            </n-grid>
          </n-tab-pane>

          <!-- 错题分析 -->
          <n-tab-pane name="wrong" tab="错题分析">
            <div v-if="examDetail.wrongQuestions.length === 0" class="empty-container">
              <n-empty description="恭喜你，没有错题！" />
            </div>
            <div v-else>
              <n-collapse>
                <n-collapse-item
                  v-for="question in examDetail.wrongQuestions"
                  :key="question.id"
                  :title="`第${question.number}题 (${question.type}) - 得分: ${question.score}/${question.totalScore}`"
                >
                  <div class="wrong-question-content">
                    <div class="question-content">
                      <div class="content-title">题目内容:</div>
                      <div class="content-text">{{ question.content }}</div>
                    </div>
                    <div class="question-answer">
                      <div class="answer-title">我的答案:</div>
                      <div class="answer-text">{{ question.myAnswer }}</div>
                    </div>
                    <div class="question-correct">
                      <div class="correct-title">正确答案:</div>
                      <div class="correct-text">{{ question.correctAnswer }}</div>
                    </div>
                    <div class="question-analysis">
                      <div class="analysis-title">解析:</div>
                      <div class="analysis-text">{{ question.analysis }}</div>
                    </div>
                    <div class="question-knowledge">
                      <div class="knowledge-title">知识点:</div>
                      <div class="knowledge-tags">
                        <n-tag
                          v-for="point in question.knowledgePoints"
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
          </n-tab-pane>

          <!-- 知识点分析 -->
          <n-tab-pane name="knowledge" tab="知识点分析">
            <n-grid :cols="24" :x-gap="16" :y-gap="16">
              <n-grid-item :span="isMobile ? 24 : 12">
                <n-card title="知识点掌握情况" size="small">
                  <div class="knowledge-mastery">
                    <div
                      v-for="point in examDetail.knowledgePoints"
                      :key="point.name"
                      class="mastery-item"
                    >
                      <div class="mastery-name">{{ point.name }}</div>
                      <n-progress
                        type="line"
                        :percentage="point.mastery * 100"
                        :color="getMasteryColor(point.mastery)"
                        :height="12"
                        :border-radius="6"
                        :format="percentageFormat"
                      />
                    </div>
                  </div>
                </n-card>
              </n-grid-item>
              <n-grid-item :span="isMobile ? 24 : 12">
                <n-card title="薄弱知识点" size="small">
                  <div v-if="weakPoints.length === 0" class="empty-container">
                    <n-empty description="没有明显的薄弱知识点" />
                  </div>
                  <div v-else class="weak-points">
                    <n-list>
                      <n-list-item v-for="point in weakPoints" :key="point.name">
                        <n-thing :title="point.name">
                          <template #description>
                            <div class="weak-point-desc">
                              <div class="mastery-bar">
                                <n-progress
                                  type="line"
                                  :percentage="point.mastery * 100"
                                  :color="getMasteryColor(point.mastery)"
                                  :height="8"
                                  :border-radius="4"
                                  :show-indicator="false"
                                />
                              </div>
                              <div class="recommendation">
                                <div class="recommendation-title">学习建议:</div>
                                <div class="recommendation-text">{{ point.recommendation }}</div>
                              </div>
                            </div>
                          </template>
                          <template #footer>
                            <n-button text size="small" @click="findLearningMaterials(point.name)">
                              查看相关学习资料
                            </n-button>
                          </template>
                        </n-thing>
                      </n-list-item>
                    </n-list>
                  </div>
                </n-card>
              </n-grid-item>
            </n-grid>
          </n-tab-pane>
        </n-tabs>
      </n-card>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <n-space>
          <n-button @click="goBack">返回列表</n-button>
          <n-button type="primary" @click="goToAnalysis">查看详细分析</n-button>
          <n-button type="info" @click="generateReport">生成诊断报告</n-button>
        </n-space>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getExamDetail, getWrongQuestions } from '../../api/exam'
import { generateDiagnosticReport } from '../../api/diagnostic'
import { 
  NCard, 
  NGrid, 
  NGridItem, 
  NSpin, 
  NTag, 
  NSpace, 
  NProgress,
  NTabs,
  NTabPane,
  NDataTable,
  NEmpty,
  NCollapse,
  NCollapseItem,
  NList,
  NListItem,
  NThing,
  NButton,
  NIcon,
  useMessage
} from 'naive-ui'
import { TrophyOutline } from '@vicons/ionicons5'

// 路由实例
const route = useRoute()
const router = useRouter()

// 消息提示
const message = useMessage()

// 响应式状态
const loading = ref(true)
const examDetail = ref({
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
  questions: [],
  wrongQuestions: [],
  knowledgePoints: []
})
const isMobile = ref(window.innerWidth < 768)

// 计算属性
const weakPoints = computed(() => {
  return examDetail.value.knowledgePoints
    .filter(point => point.mastery < 0.6)
    .sort((a, b) => a.mastery - b.mastery)
})

// 分数分布范围
const scoreRanges = [
  { min: 90, max: 100, color: '#18a058', label: '优秀 (90-100)' },
  { min: 80, max: 89, color: '#2080f0', label: '良好 (80-89)' },
  { min: 70, max: 79, color: '#f0a020', label: '中等 (70-79)' },
  { min: 60, max: 69, color: '#d03050', label: '及格 (60-69)' },
  { min: 0, max: 59, color: '#909399', label: '不及格 (0-59)' }
]

// 表格列定义
const questionColumns = [
  {
    title: '题号',
    key: 'number',
    width: 80
  },
  {
    title: '类型',
    key: 'type',
    width: 100
  },
  {
    title: '得分',
    key: 'score',
    width: 100,
    render(row) {
      return `${row.score}/${row.totalScore}`
    }
  },
  {
    title: '知识点',
    key: 'knowledgePoints',
    render(row) {
      return row.knowledgePoints.join(', ')
    }
  }
]

// 生命周期钩子
onMounted(() => {
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth < 768
  })
  
  // 获取考试详情
  fetchExamDetail()
})

// 方法
// 获取考试详情
const fetchExamDetail = async () => {
  loading.value = true
  try {
    const examId = route.params.id
    const res = await getExamDetail(examId)
    
    if (res.code === 0) {
      examDetail.value = res.data
      
      // 获取错题列表
      const wrongRes = await getWrongQuestions(examId)
      if (wrongRes.code === 0) {
        examDetail.value.wrongQuestions = wrongRes.data.list
      }
    } else {
      message.error('获取考试详情失败')
    }
  } catch (error) {
    console.error('获取考试详情失败:', error)
    message.error('获取考试详情失败')
  } finally {
    loading.value = false
  }
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

// 获取分布百分比
const getDistributionPercentage = (min, max) => {
  const count = examDetail.value.distribution.filter(
    score => score >= min && score <= max
  ).length
  return (count / examDetail.value.totalStudents) * 100
}

// 获取掌握度颜色
const getMasteryColor = (mastery) => {
  if (mastery >= 0.8) return '#18a058'
  if (mastery >= 0.6) return '#2080f0'
  if (mastery >= 0.4) return '#f0a020'
  return '#d03050'
}

// 百分比格式化
const percentageFormat = (percentage) => {
  return `${percentage.toFixed(0)}%`
}

// 查找学习资料
const findLearningMaterials = (knowledgePoint) => {
  router.push({
    name: 'LearningMaterials',
    query: { keyword: knowledgePoint }
  })
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

// 返回列表
const goBack = () => {
  router.push({ name: 'ExamList' })
}

// 查看详细分析
const goToAnalysis = () => {
  router.push({ name: 'ExamAnalysis', params: { id: route.params.id } })
}
</script>

<style scoped>
.exam-detail-container {
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

.exam-score-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.score-header {
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
  margin-bottom: 8px;
}

.score-rank {
  margin-top: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.score-rank .n-icon {
  margin-right: 4px;
  color: #f0a020;
}

.score-detail-card {
  margin-bottom: 16px;
}

.score-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
}

.score-distribution {
  margin-top: 16px;
}

.distribution-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 12px;
}

.distribution-legend {
  display: flex;
  flex-wrap: wrap;
  margin-top: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: 16px;
  margin-bottom: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 4px;
}

.legend-label {
  font-size: 12px;
  color: #666;
}

.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.wrong-question-content {
  padding: 8px;
}

.content-title, .answer-title, .correct-title, .analysis-title, .knowledge-title {
  font-weight: bold;
  margin-bottom: 8px;
}

.content-text, .answer-text, .correct-text, .analysis-text {
  margin-bottom: 16px;
  white-space: pre-wrap;
}

.knowledge-tags {
  display: flex;
  flex-wrap: wrap;
}

.knowledge-mastery {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.mastery-item {
  margin-bottom: 8px;
}

.mastery-name {
  font-size: 14px;
  margin-bottom: 4px;
}

.weak-point-desc {
  margin-top: 8px;
}

.mastery-bar {
  margin-bottom: 8px;
}

.recommendation-title {
  font-size: 13px;
  font-weight: bold;
  margin-bottom: 4px;
}

.recommendation-text {
  font-size: 13px;
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
  
  .exam-score-card {
    margin-top: 16px;
  }
  
  .score-stats {
    grid-template-columns: 1fr;
  }
}
</style>
