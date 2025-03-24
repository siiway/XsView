<!-- 考试列表页面 -->
<!-- views/exam/ExamList.vue -->

<template>
  <div class="exam-list-container">
    <n-card title="考试列表">
      <template #header-extra>
        <n-space>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索考试名称"
            clearable
            @keydown.enter="handleSearch"
          >
            <template #suffix>
              <n-icon :component="SearchOutline" />
            </template>
          </n-input>
          <n-select
            v-model:value="filterSubject"
            placeholder="学科筛选"
            clearable
            :options="subjectOptions"
            style="width: 120px"
          />
        </n-space>
      </template>
      
      <div v-if="loading" class="loading-container">
        <n-spin size="large" />
      </div>
      
      <div v-else-if="examList.length === 0" class="empty-container">
        <n-empty description="暂无考试数据" />
      </div>
      
      <div v-else>
        <n-data-table
          :columns="columns"
          :data="examList"
          :pagination="pagination"
          :bordered="false"
          :single-line="false"
          @update:page="handlePageChange"
        />
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { h, ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getExamList } from '../../api/exam'
import { 
  NCard, 
  NDataTable, 
  NButton, 
  NSpace, 
  NInput, 
  NSelect,
  NSpin,
  NEmpty,
  NIcon,
  NTag,
  useMessage
} from 'naive-ui'
import { SearchOutline } from '@vicons/ionicons5'

// 路由实例
const router = useRouter()

// 消息提示
const message = useMessage()

// 响应式状态
const loading = ref(false)
const examList = ref([])
const searchKeyword = ref('')
const filterSubject = ref(null)
const pagination = reactive({
  page: 1,
  pageSize: 10,
  itemCount: 0,
  pageSizes: [10, 20, 30, 50],
  showSizePicker: true,
  onChange: (page) => {
    pagination.page = page
    fetchExamList()
  },
  onUpdatePageSize: (pageSize) => {
    pagination.pageSize = pageSize
    pagination.page = 1
    fetchExamList()
  }
})

// 学科选项
const subjectOptions = [
  { label: '语文', value: '语文' },
  { label: '数学', value: '数学' },
  { label: '英语', value: '英语' },
  { label: '物理', value: '物理' },
  { label: '化学', value: '化学' },
  { label: '生物', value: '生物' },
  { label: '历史', value: '历史' },
  { label: '地理', value: '地理' },
  { label: '政治', value: '政治' }
]

// 表格列定义
const columns = [
  {
    title: '考试名称',
    key: 'title',
    render(row) {
      return h(
        'div',
        {
          class: 'exam-title'
        },
        [
          h('span', null, row.title),
          row.isImportant ? h(
            NTag,
            {
              type: 'error',
              size: 'small',
              style: {
                marginLeft: '8px'
              }
            },
            { default: () => '重要' }
          ) : null
        ]
      )
    }
  },
  {
    title: '学科',
    key: 'subject',
    width: 100,
    render(row) {
      return h(
        NTag,
        {
          type: getSubjectTagType(row.subject),
          size: 'small'
        },
        { default: () => row.subject }
      )
    }
  },
  {
    title: '考试时间',
    key: 'examTime',
    width: 120,
    render(row) {
      return formatDate(row.examTime)
    }
  },
  {
    title: '得分',
    key: 'score',
    width: 100,
    render(row) {
      return h(
        'div',
        {
          class: 'exam-score'
        },
        [
          h(
            'span',
            {
              class: 'score-value'
            },
            row.score
          ),
          h(
            'span',
            {
              class: 'score-total'
            },
            `/${row.totalScore}`
          )
        ]
      )
    }
  },
  {
    title: '排名',
    key: 'rank',
    width: 100,
    render(row) {
      return `${row.rank}/${row.totalStudents}`
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    render(row) {
      return h(
        NSpace,
        {
          justify: 'center',
          align: 'center'
        },
        [
          h(
            NButton,
            {
              size: 'small',
              onClick: () => goToExamDetail(row.id)
            },
            { default: () => '详情' }
          ),
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              onClick: () => goToExamAnalysis(row.id)
            },
            { default: () => '分析' }
          ),
          h(
            NButton,
            {
              size: 'small',
              type: 'info',
              onClick: () => generateDiagnosticReport(row.id)
            },
            { default: () => '诊断' }
          )
        ]
      )
    }
  }
]

// 生命周期钩子
onMounted(() => {
  fetchExamList()
})

// 方法
// 获取考试列表
const fetchExamList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      pageSize: pagination.pageSize
    }
    
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    
    if (filterSubject.value) {
      params.subject = filterSubject.value
    }
    
    const res = await getExamList(params)
    if (res.code === 0) {
      examList.value = res.data.list
      pagination.itemCount = res.data.total
    }
  } catch (error) {
    console.error('获取考试列表失败:', error)
    message.error('获取考试列表失败')
  } finally {
    loading.value = false
  }
}

// 处理搜索
const handleSearch = () => {
  pagination.page = 1
  fetchExamList()
}

// 处理页码变化
const handlePageChange = (page) => {
  pagination.page = page
  fetchExamList()
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
const generateDiagnosticReport = async (examId) => {
  try {
    const res = await generateReport({ examId })
    if (res.code === 0) {
      message.success('诊断报告生成成功')
      // 跳转到诊断报告详情页
      router.push({ name: 'DiagnosticDetail', params: { id: res.data.reportId } })
    }
  } catch (error) {
    console.error('生成诊断报告失败:', error)
    message.error('生成诊断报告失败')
  }
}

// 导航方法
const goToExamDetail = (examId) => {
  router.push({ name: 'ExamDetail', params: { id: examId } })
}

const goToExamAnalysis = (examId) => {
  router.push({ name: 'ExamAnalysis', params: { id: examId } })
}
</script>

<style scoped>
.exam-list-container {
  padding: 16px;
}

.loading-container, .empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.exam-title {
  font-weight: 500;
}

.exam-score .score-value {
  font-weight: bold;
  color: #18a058;
}

.exam-score .score-total {
  color: #999;
}
</style>
