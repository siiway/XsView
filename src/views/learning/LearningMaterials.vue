<!-- 学习资料列表页面 -->
<!-- views/learning/LearningMaterials.vue -->

<template>
  <div class="learning-materials-container">
    <n-card title="学习资料">
      <template #header-extra>
        <n-space>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索资料名称或知识点"
            clearable
            @keydown.enter="handleSearch"
          >
            <template #suffix>
              <n-icon :component="SearchOutline" />
            </template>
          </n-input>
          <n-select
            v-model:value="filterType"
            placeholder="资料类型"
            clearable
            :options="typeOptions"
            style="width: 120px"
          />
        </n-space>
      </template>
      
      <div v-if="loading" class="loading-container">
        <n-spin size="large" />
      </div>
      
      <div v-else-if="materials.length === 0" class="empty-container">
        <n-empty description="暂无学习资料" />
      </div>
      
      <div v-else class="materials-grid">
        <n-grid :cols="isMobile ? 1 : (isTablet ? 2 : 3)" :x-gap="16" :y-gap="16">
          <n-grid-item v-for="material in materials" :key="material.id">
            <n-card hoverable class="material-card">
              <template #cover>
                <div class="material-cover" :class="material.type.toLowerCase()">
                  <div class="material-icon">
                    <n-icon size="36" :color="getMaterialIconColor(material.type)">
                      <component :is="getMaterialIcon(material.type)" />
                    </n-icon>
                  </div>
                  <div class="material-type">{{ material.type }}</div>
                </div>
              </template>
              <div class="material-title">{{ material.title }}</div>
              <div class="material-description">{{ material.description }}</div>
              <div class="material-knowledge">
                <div class="knowledge-label">知识点:</div>
                <div class="knowledge-tags">
                  <n-tag
                    v-for="point in material.knowledgePoints"
                    :key="point"
                    size="small"
                    style="margin-right: 4px; margin-bottom: 4px"
                  >
                    {{ point }}
                  </n-tag>
                </div>
              </div>
              <div class="material-meta">
                <div class="material-date">{{ formatDate(material.createdAt) }}</div>
                <div class="material-views">
                  <n-icon size="small"><eye-outline /></n-icon>
                  {{ material.views }}
                </div>
              </div>
              <div class="material-actions">
                <n-button type="primary" @click="goToMaterialDetail(material.id)">
                  查看详情
                </n-button>
              </div>
            </n-card>
          </n-grid-item>
        </n-grid>
      </div>
      
      <div class="pagination-container">
        <n-pagination
          v-model:page="page"
          v-model:page-size="pageSize"
          :item-count="total"
          :page-sizes="[12, 24, 36]"
          show-size-picker
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </div>
    </n-card>
    
    <!-- 推荐资料 -->
    <n-card title="推荐学习资料" class="recommended-card">
      <div v-if="loadingRecommended" class="loading-container">
        <n-spin size="medium" />
      </div>
      
      <div v-else-if="recommendedMaterials.length === 0" class="empty-container">
        <n-empty description="暂无推荐资料" />
      </div>
      
      <div v-else>
        <n-list>
          <n-list-item v-for="material in recommendedMaterials" :key="material.id">
            <n-thing :title="material.title">
              <template #avatar>
                <n-avatar round :style="{ backgroundColor: getMaterialColor(material.type) }">
                  {{ getMaterialTypeIcon(material.type) }}
                </n-avatar>
              </template>
              <template #description>
                <div class="material-info">
                  <div class="material-type-tag">{{ material.type }}</div>
                  <div class="material-knowledge-point">{{ material.knowledgePoints.join(', ') }}</div>
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
    </n-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getRecommendedMaterials, getMaterialDetail } from '../../api/learning'
import { 
  NCard, 
  NGrid, 
  NGridItem, 
  NSpin, 
  NSpace, 
  NInput,
  NSelect,
  NEmpty,
  NTag,
  NButton,
  NPagination,
  NList,
  NListItem,
  NThing,
  NAvatar,
  NIcon,
  useMessage
} from 'naive-ui'
import { 
  SearchOutline, 
  DocumentTextOutline, 
  VideocamOutline, 
  BookOutline,
  EyeOutline
} from '@vicons/ionicons5'

// 路由实例
const route = useRoute()
const router = useRouter()

// 消息提示
const message = useMessage()

// 响应式状态
const loading = ref(false)
const loadingRecommended = ref(false)
const materials = ref([])
const recommendedMaterials = ref([])
const searchKeyword = ref('')
const filterType = ref(null)
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)
const isMobile = ref(window.innerWidth < 768)
const isTablet = ref(window.innerWidth >= 768 && window.innerWidth < 1024)

// 资料类型选项
const typeOptions = [
  { label: '文档', value: '文档' },
  { label: '视频', value: '视频' },
  { label: '习题', value: '习题' }
]

// 生命周期钩子
onMounted(() => {
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 检查URL参数
  const { keyword } = route.query
  if (keyword) {
    searchKeyword.value = keyword
  }
  
  // 获取学习资料
  fetchMaterials()
  
  // 获取推荐学习资料
  fetchRecommendedMaterials()
})

// 监听搜索关键词和筛选条件变化
watch([searchKeyword, filterType], () => {
  page.value = 1
  fetchMaterials()
})

// 方法
// 获取学习资料
const fetchMaterials = async () => {
  loading.value = true
  try {
    // 模拟API请求
    // 实际项目中应该调用真实的API
    setTimeout(() => {
      // 生成模拟数据
      const mockData = generateMockMaterials()
      materials.value = mockData.list
      total.value = mockData.total
      loading.value = false
    }, 800)
  } catch (error) {
    console.error('获取学习资料失败:', error)
    message.error('获取学习资料失败')
    loading.value = false
  }
}

// 获取推荐学习资料
const fetchRecommendedMaterials = async () => {
  loadingRecommended.value = true
  try {
    const res = await getRecommendedMaterials()
    if (res.code === 0) {
      recommendedMaterials.value = res.data.materials.slice(0, 5)
    }
  } catch (error) {
    console.error('获取推荐学习资料失败:', error)
  } finally {
    loadingRecommended.value = false
  }
}

// 生成模拟数据
const generateMockMaterials = () => {
  const types = ['文档', '视频', '习题']
  const knowledgePointsMap = {
    '语文': ['文言文阅读', '现代文阅读', '诗歌鉴赏', '作文写作', '语法修辞'],
    '数学': ['函数', '导数', '三角函数', '概率统计', '立体几何', '解析几何'],
    '英语': ['阅读理解', '完形填空', '语法', '写作', '听力'],
    '物理': ['力学', '电学', '热学', '光学', '原子物理'],
    '化学': ['元素化合物', '化学反应', '有机化学', '物质结构']
  }
  
  const subjects = Object.keys(knowledgePointsMap)
  
  // 生成模拟数据
  const mockList = []
  const totalItems = 50
  
  for (let i = 1; i <= totalItems; i++) {
    const type = types[Math.floor(Math.random() * types.length)]
    const subject = subjects[Math.floor(Math.random() * subjects.length)]
    const knowledgePointsForSubject = knowledgePointsMap[subject]
    const knowledgePoints = []
    
    // 随机选择1-3个知识点
    const numPoints = Math.floor(Math.random() * 3) + 1
    for (let j = 0; j < numPoints; j++) {
      const point = knowledgePointsForSubject[Math.floor(Math.random() * knowledgePointsForSubject.length)]
      if (!knowledgePoints.includes(point)) {
        knowledgePoints.push(point)
      }
    }
    
    const material = {
      id: `material-${i}`,
      title: `${subject}${type === '习题' ? '练习题' : type} - ${knowledgePoints[0]}专项`,
      description: `这是一份关于${subject}中${knowledgePoints.join('、')}的${type}资料，适合中学生学习和复习使用。`,
      type,
      subject,
      knowledgePoints,
      createdAt: new Date(Date.now() - Math.floor(Math.random() * 30) * 24 * 60 * 60 * 1000),
      views: Math.floor(Math.random() * 1000) + 100
    }
    
    // 应用筛选条件
    let match = true
    
    if (searchKeyword.value) {
      const keyword = searchKeyword.value.toLowerCase()
      const titleMatch = material.title.toLowerCase().includes(keyword)
      const knowledgeMatch = material.knowledgePoints.some(point => point.toLowerCase().includes(keyword))
      
      if (!titleMatch && !knowledgeMatch) {
        match = false
      }
    }
    
    if (filterType.value && material.type !== filterType.value) {
      match = false
    }
    
    if (match) {
      mockList.push(material)
    }
  }
  
  // 排序：最新的在前面
  mockList.sort((a, b) => b.createdAt - a.createdAt)
  
  // 分页
  const startIndex = (page.value - 1) * pageSize.value
  const endIndex = startIndex + pageSize.value
  const paginatedList = mockList.slice(startIndex, endIndex)
  
  return {
    list: paginatedList,
    total: mockList.length
  }
}

// 处理搜索
const handleSearch = () => {
  page.value = 1
  fetchMaterials()
}

// 处理页码变化
const handlePageChange = (newPage) => {
  page.value = newPage
  fetchMaterials()
}

// 处理每页条数变化
const handlePageSizeChange = (newPageSize) => {
  pageSize.value = newPageSize
  page.value = 1
  fetchMaterials()
}

// 处理窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth < 768
  isTablet.value = window.innerWidth >= 768 && window.innerWidth < 1024
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 获取资料图标
const getMaterialIcon = (type) => {
  const iconMap = {
    '文档': DocumentTextOutline,
    '视频': VideocamOutline,
    '习题': BookOutline
  }
  return iconMap[type] || DocumentTextOutline
}

// 获取资料图标颜色
const getMaterialIconColor = (type) => {
  const colorMap = {
    '文档': '#2080f0',
    '视频': '#f0a020',
    '习题': '#18a058'
  }
  return colorMap[type] || '#2080f0'
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
const getMaterialTypeIcon = (type) => {
  const iconMap = {
    '文档': '文',
    '视频': '视',
    '习题': '习'
  }
  return iconMap[type] || '资'
}

// 查看资料详情
const goToMaterialDetail = (materialId) => {
  router.push({ name: 'LearningDetail', params: { id: materialId } })
}
</script>

<style scoped>
.learning-materials-container {
  padding: 16px;
}

.loading-container, .empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.materials-grid {
  margin-bottom: 24px;
}

.material-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.material-cover {
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
}

.material-cover.文档 {
  background: linear-gradient(135deg, #2080f0, #1a6fc9);
}

.material-cover.视频 {
  background: linear-gradient(135deg, #f0a020, #d08c1c);
}

.material-cover.习题 {
  background: linear-gradient(135deg, #18a058, #14864a);
}

.material-icon {
  margin-bottom: 8px;
}

.material-type {
  font-size: 14px;
}

.material-title {
  font-size: 16px;
  font-weight: bold;
  margin: 12px 0 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.material-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  flex-grow: 1;
}

.material-knowledge {
  margin-bottom: 12px;
}

.knowledge-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.knowledge-tags {
  display: flex;
  flex-wrap: wrap;
}

.material-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}

.material-views {
  display: flex;
  align-items: center;
}

.material-views .n-icon {
  margin-right: 4px;
}

.material-actions {
  text-align: center;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.recommended-card {
  margin-top: 16px;
}

.material-info {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}

.material-type-tag {
  padding: 2px 6px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
}

.material-knowledge-point {
  font-size: 12px;
  color: #666;
}

@media (max-width: 767px) {
  .material-cover {
    height: 100px;
  }
}
</style>
