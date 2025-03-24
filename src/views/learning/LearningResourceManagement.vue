<!-- 后台管理系统学习资料管理页面 -->
<!-- frontend/scorex-admin/src/views/learning/LearningResourceManagement.vue -->

<template>
  <div class="learning-resource-management-container">
    <!-- 搜索和操作栏 -->
    <a-card class="search-card">
      <a-row :gutter="16">
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-input
            v-model="searchForm.keyword"
            placeholder="搜索资料标题/关键词"
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.subjectId"
            placeholder="选择学科"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="subject in subjectOptions" :key="subject.value" :value="subject.value">
              {{ subject.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.resourceType"
            placeholder="资料类型"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="type in resourceTypeOptions" :key="type.value" :value="type.value">
              {{ type.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-space>
            <a-button type="primary" @click="handleSearch">
              <template #icon>
                <icon-search />
              </template>
              搜索
            </a-button>
            <a-button @click="resetSearch">
              <template #icon>
                <icon-refresh />
              </template>
              重置
            </a-button>
          </a-space>
        </a-col>
      </a-row>
    </a-card>

    <!-- 统计卡片 -->
    <a-row :gutter="16" class="stats-row">
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--primary-6), 0.1)">
              <icon-file style="color: rgb(var(--primary-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalResources }}</div>
              <div class="stat-label">学习资料总数</div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--success-6), 0.1)">
              <icon-calendar style="color: rgb(var(--success-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.todayResources }}</div>
              <div class="stat-label">今日新增资料</div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--warning-6), 0.1)">
              <icon-user style="color: rgb(var(--warning-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.viewCount }}</div>
              <div class="stat-label">资料查看次数</div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--danger-6), 0.1)">
              <icon-download style="color: rgb(var(--danger-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.downloadCount }}</div>
              <div class="stat-label">资料下载次数</div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 学习资料列表 -->
    <a-card class="table-card">
      <template #title>
        学习资料列表
      </template>
      <template #extra>
        <a-space>
          <a-button type="primary" @click="openAddResourceModal">
            <template #icon>
              <icon-plus />
            </template>
            添加资料
          </a-button>
          <a-button @click="handleBatchImport">
            <template #icon>
              <icon-upload />
            </template>
            批量导入
          </a-button>
          <a-button status="danger" @click="handleBatchDelete">
            <template #icon>
              <icon-delete />
            </template>
            批量删除
          </a-button>
        </a-space>
      </template>

      <a-table
        :loading="loading"
        :columns="columns"
        :data="resourceData"
        :pagination="pagination"
        :row-selection="rowSelection"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        row-key="id"
      >
        <template #resourceType="{ record }">
          <a-tag :color="getResourceTypeColor(record.resourceType)">
            {{ getResourceTypeText(record.resourceType) }}
          </a-tag>
        </template>
        
        <template #status="{ record }">
          <a-tag :color="getStatusColor(record.status)">
            {{ getStatusText(record.status) }}
          </a-tag>
        </template>
        
        <template #operations="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handlePreview(record)">
              预览
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleEdit(record)">
              编辑
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleRecommend(record)">
              推荐
            </a-button>
            <a-divider direction="vertical" />
            <a-popconfirm
              content="确定要删除此学习资料吗？"
              @ok="handleDelete(record)"
            >
              <a-button type="text" status="danger" size="small">
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 添加/编辑资料弹窗 -->
    <a-modal
      v-model:visible="resourceModalVisible"
      :title="isEdit ? '编辑学习资料' : '添加学习资料'"
      @cancel="closeResourceModal"
      @before-ok="handleSubmitResource"
      width="700px"
    >
      <a-form :model="resourceForm" ref="resourceFormRef" :rules="resourceFormRules" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="title" label="资料标题" required>
          <a-input v-model="resourceForm.title" placeholder="请输入资料标题" />
        </a-form-item>
        <a-form-item field="subjectId" label="所属学科" required>
          <a-select v-model="resourceForm.subjectId" placeholder="请选择学科">
            <a-option v-for="subject in subjectOptions" :key="subject.value" :value="subject.value">
              {{ subject.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="resourceType" label="资料类型" required>
          <a-select v-model="resourceForm.resourceType" placeholder="请选择资料类型">
            <a-option v-for="type in resourceTypeOptions" :key="type.value" :value="type.value">
              {{ type.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="knowledgePoints" label="知识点" required>
          <a-select v-model="resourceForm.knowledgePoints" placeholder="请选择知识点" multiple>
            <a-option v-for="point in knowledgePointOptions" :key="point.value" :value="point.value">
              {{ point.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="gradeLevel" label="适用年级" required>
          <a-select v-model="resourceForm.gradeLevel" placeholder="请选择适用年级" multiple>
            <a-option v-for="grade in gradeLevelOptions" :key="grade.value" :value="grade.value">
              {{ grade.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="difficulty" label="难度等级" required>
          <a-rate v-model="resourceForm.difficulty" :count="5" allow-half />
        </a-form-item>
        <a-form-item field="description" label="资料描述">
          <a-textarea v-model="resourceForm.description" placeholder="请输入资料描述" />
        </a-form-item>
        <a-form-item field="resourceUrl" label="资料链接" required>
          <a-input-group>
            <a-input v-model="resourceForm.resourceUrl" placeholder="请输入资料链接" />
            <a-button>上传</a-button>
          </a-input-group>
        </a-form-item>
        <a-form-item field="coverImage" label="封面图片">
          <a-upload
            list-type="picture-card"
            :file-list="fileList"
            :custom-request="customUploadRequest"
            :limit="1"
          >
            <template #upload-button>
              <div>
                <icon-plus />
                <div style="margin-top: 10px">上传</div>
              </div>
            </template>
          </a-upload>
        </a-form-item>
        <a-form-item field="status" label="状态">
          <a-radio-group v-model="resourceForm.status">
            <a-radio value="published">发布</a-radio>
            <a-radio value="draft">草稿</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 批量导入弹窗 -->
    <a-modal
      v-model:visible="importModalVisible"
      title="批量导入学习资料"
      @cancel="closeImportModal"
      @before-ok="handleConfirmImport"
    >
      <a-form :model="importForm" ref="importFormRef" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="file" label="导入文件">
          <a-upload
            action="/"
            :file-list="importFileList"
            :custom-request="customUploadRequest"
            :limit="1"
            accept=".xlsx,.xls,.csv"
          >
            <template #upload-button>
              <a-button>
                <template #icon>
                  <icon-upload />
                </template>
                选择文件
              </a-button>
            </template>
          </a-upload>
        </a-form-item>
        <a-form-item>
          <a-alert type="info">
            <template #message>
              <div>
                <p>请按照模板格式上传Excel文件，支持.xlsx、.xls、.csv格式</p>
                <a-link>下载导入模板</a-link>
              </div>
            </template>
          </a-alert>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 推荐资料弹窗 -->
    <a-modal
      v-model:visible="recommendModalVisible"
      title="推荐学习资料"
      @cancel="closeRecommendModal"
      @before-ok="handleConfirmRecommend"
    >
      <a-form :model="recommendForm" ref="recommendFormRef" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="resourceTitle" label="资料标题">
          <a-input v-model="recommendForm.resourceTitle" disabled />
        </a-form-item>
        <a-form-item field="targetType" label="推荐对象" required>
          <a-radio-group v-model="recommendForm.targetType">
            <a-radio value="student">指定学生</a-radio>
            <a-radio value="class">指定班级</a-radio>
            <a-radio value="grade">指定年级</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item field="targetIds" label="选择对象" required>
          <a-select v-model="recommendForm.targetIds" placeholder="请选择推荐对象" multiple>
            <a-option v-for="target in getTargetOptions()" :key="target.value" :value="target.value">
              {{ target.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="recommendReason" label="推荐理由">
          <a-textarea v-model="recommendForm.recommendReason" placeholder="请输入推荐理由" />
        </a-form-item>
        <a-form-item field="notifyNow" label="立即通知">
          <a-switch v-model="recommendForm.notifyNow" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 预览资料弹窗 -->
    <a-modal
      v-model:visible="previewModalVisible"
      title="资料预览"
      @cancel="closePreviewModal"
      width="800px"
    >
      <div class="resource-preview">
        <div class="resource-header">
          <h2>{{ currentResource.title }}</h2>
          <div class="resource-meta">
            <span>学科: {{ getSubjectName(currentResource.subjectId) }}</span>
            <span>类型: {{ getResourceTypeText(currentResource.resourceType) }}</span>
            <span>难度: <a-rate :model-value="currentResource.difficulty" :count="5" readonly allow-half /></span>
          </div>
        </div>
        
        <a-divider />
        
        <div class="resource-section">
          <h3>资料描述</h3>
          <p>{{ currentResource.description }}</p>
        </div>
        
        <div class="resource-section">
          <h3>知识点</h3>
          <div class="knowledge-points">
            <a-tag v-for="point in currentResource.knowledgePoints" :key="point" color="blue">
              {{ getKnowledgePointName(point) }}
            </a-tag>
          </div>
        </div>
        
        <div class="resource-section">
          <h3>适用年级</h3>
          <div class="grade-levels">
            <a-tag v-for="grade in currentResource.gradeLevel" :key="grade" color="green">
              {{ getGradeLevelName(grade) }}
            </a-tag>
          </div>
        </div>
        
        <div class="resource-section">
          <h3>资料内容</h3>
          <div class="resource-content">
            <a-empty v-if="!currentResource.resourceUrl" description="暂无预览内容" />
            <div v-else class="resource-iframe-container">
              <iframe :src="currentResource.resourceUrl" frameborder="0" class="resource-iframe"></iframe>
            </div>
          </div>
        </div>
        
        <div class="resource-section">
          <h3>使用统计</h3>
          <a-descriptions :data="resourceStatsData" layout="inline-horizontal" bordered />
        </div>
      </div>
      
      <template #footer>
        <a-space>
          <a-button type="primary" @click="handleDownloadResource">
            下载资料
          </a-button>
          <a-button @click="handleRecommendCurrent">
            推荐资料
          </a-button>
        </a-space>
      </template>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue';
import { Message } from '@arco-design/web-vue';

export default {
  setup() {
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subjectId: undefined,
      resourceType: undefined
    });

    // 资料表单
    const resourceForm = reactive({
      id: '',
      title: '',
      subjectId: undefined,
      resourceType: undefined,
      knowledgePoints: [],
      gradeLevel: [],
      difficulty: 3,
      description: '',
      resourceUrl: '',
      coverImage: '',
      status: 'published'
    });

    // 导入表单
    const importForm = reactive({});

    // 推荐表单
    const recommendForm = reactive({
      resourceId: '',
      resourceTitle: '',
      targetType: 'student',
      targetIds: [],
      recommendReason: '',
      notifyNow: true
    });

    // 文件列表
    const fileList = ref([]);
    const importFileList = ref([]);

    // 表单引用
    const resourceFormRef = ref(null);
    const importFormRef = ref(null);
    const recommendFormRef = ref(null);

    // 状态变量
    const loading = ref(false);
    const resourceModalVisible = ref(false);
    const importModalVisible = ref(false);
    const recommendModalVisible = ref(false);
    const previewModalVisible = ref(false);
    const isEdit = ref(false);
    const currentResource = reactive({
      id: '',
      title: '',
      subjectId: '',
      resourceType: '',
      knowledgePoints: [],
      gradeLevel: [],
      difficulty: 3,
      description: '',
      resourceUrl: '',
      coverImage: '',
      status: '',
      viewCount: 0,
      downloadCount: 0,
      recommendCount: 0,
      createdAt: ''
    });
    const resourceStatsData = ref([]);

    // 分页配置
    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0,
      showTotal: true,
      showPageSize: true,
      pageSizeOptions: [10, 20, 50, 100]
    });

    // 表格选择配置
    const selectedRowKeys = ref([]);
    const rowSelection = {
      type: 'checkbox',
      showCheckedAll: true,
      onlyCurrent: false,
      modelValue: selectedRowKeys.value,
      'onUpdate:modelValue': (val) => {
        selectedRowKeys.value = val;
      }
    };

    // 学科选项
    const subjectOptions = [
      { label: '数学', value: 'subject-001' },
      { label: '语文', value: 'subject-002' },
      { label: '英语', value: 'subject-003' },
      { label: '物理', value: 'subject-004' },
      { label: '化学', value: 'subject-005' },
      { label: '生物', value: 'subject-006' },
      { label: '历史', value: 'subject-007' },
      { label: '地理', value: 'subject-008' },
      { label: '政治', value: 'subject-009' }
    ];

    // 资料类型选项
    const resourceTypeOptions = [
      { label: '课件', value: 'slides' },
      { label: '习题', value: 'exercises' },
      { label: '视频', value: 'video' },
      { label: '文档', value: 'document' },
      { label: '图表', value: 'chart' },
      { label: '试卷', value: 'exam' }
    ];

    // 知识点选项
    const knowledgePointOptions = [
      { label: '函数', value: 'kp-001' },
      { label: '导数', value: 'kp-002' },
      { label: '三角函数', value: 'kp-003' },
      { label: '概率统计', value: 'kp-004' },
      { label: '立体几何', value: 'kp-005' },
      { label: '向量', value: 'kp-006' },
      { label: '数列', value: 'kp-007' },
      { label: '复数', value: 'kp-008' },
      { label: '解析几何', value: 'kp-009' }
    ];

    // 年级选项
    const gradeLevelOptions = [
      { label: '高一', value: 'grade-10' },
      { label: '高二', value: 'grade-11' },
      { label: '高三', value: 'grade-12' }
    ];

    // 学生选项
    const studentOptions = [
      { label: '张三', value: 'student-001' },
      { label: '李四', value: 'student-002' },
      { label: '王五', value: 'student-003' },
      { label: '赵六', value: 'student-004' },
      { label: '钱七', value: 'student-005' }
    ];

    // 班级选项
    const classOptions = [
      { label: '高二(1)班', value: 'class-001' },
      { label: '高二(2)班', value: 'class-002' },
      { label: '高二(3)班', value: 'class-003' },
      { label: '高二(4)班', value: 'class-004' }
    ];

    // 年级选项（用于推荐）
    const gradeOptions = [
      { label: '高一', value: 'grade-10' },
      { label: '高二', value: 'grade-11' },
      { label: '高三', value: 'grade-12' }
    ];

    // 统计数据
    const stats = reactive({
      totalResources: 0,
      todayResources: 0,
      viewCount: 0,
      downloadCount: 0
    });

    // 表格列定义
    const columns = [
      {
        title: 'ID',
        dataIndex: 'id',
        width: 80
      },
      {
        title: '资料标题',
        dataIndex: 'title',
        ellipsis: true
      },
      {
        title: '学科',
        dataIndex: 'subjectId',
        render: ({ record }) => {
          return getSubjectName(record.subjectId);
        }
      },
      {
        title: '资料类型',
        slotName: 'resourceType'
      },
      {
        title: '难度',
        dataIndex: 'difficulty',
        render: ({ record }) => {
          return `${record.difficulty}星`;
        }
      },
      {
        title: '查看次数',
        dataIndex: 'viewCount'
      },
      {
        title: '下载次数',
        dataIndex: 'downloadCount'
      },
      {
        title: '创建时间',
        dataIndex: 'createdAt'
      },
      {
        title: '状态',
        slotName: 'status'
      },
      {
        title: '操作',
        slotName: 'operations',
        fixed: 'right',
        width: 250
      }
    ];

    // 资料表单校验规则
    const resourceFormRules = {
      title: [
        { required: true, message: '请输入资料标题' }
      ],
      subjectId: [
        { required: true, message: '请选择所属学科' }
      ],
      resourceType: [
        { required: true, message: '请选择资料类型' }
      ],
      knowledgePoints: [
        { required: true, message: '请选择知识点' }
      ],
      gradeLevel: [
        { required: true, message: '请选择适用年级' }
      ],
      resourceUrl: [
        { required: true, message: '请输入资料链接' }
      ]
    };

    // 模拟资料数据
    const resourceData = ref([]);

    // 生命周期钩子
    onMounted(() => {
      fetchResourceData();
    });

    // 获取资料数据
    const fetchResourceData = () => {
      loading.value = true;
      
      // 模拟API请求
      setTimeout(() => {
        // 生成模拟数据
        const mockData = generateMockResourceData();
        resourceData.value = mockData.list;
        pagination.total = mockData.total;
        
        // 更新统计数据
        updateStats(mockData.total);
        
        loading.value = false;
      }, 800);
    };

    // 更新统计数据
    const updateStats = (total) => {
      stats.totalResources = total;
      stats.todayResources = Math.floor(total * 0.05);
      stats.viewCount = Math.floor(total * 15);
      stats.downloadCount = Math.floor(total * 5);
    };

    // 生成模拟资料数据
    const generateMockResourceData = () => {
      const titles = [
        '高中数学函数知识点总结',
        '高中物理力学综合练习',
        '高中英语阅读理解技巧',
        '高中化学元素周期表详解',
        '高中生物细胞结构与功能',
        '高中语文古诗文鉴赏方法',
        '高中历史重要事件年表',
        '高中地理自然地理基础',
        '高中政治经济学基本概念'
      ];
      
      const mockList = [];
      const totalItems = 120;
      
      for (let i = 1; i <= totalItems; i++) {
        const subjectId = subjectOptions[Math.floor(Math.random() * subjectOptions.length)].value;
        const resourceType = resourceTypeOptions[Math.floor(Math.random() * resourceTypeOptions.length)].value;
        
        // 随机选择1-3个知识点
        const knowledgePointCount = Math.floor(Math.random() * 3) + 1;
        const knowledgePoints = [];
        for (let j = 0; j < knowledgePointCount; j++) {
          const point = knowledgePointOptions[Math.floor(Math.random() * knowledgePointOptions.length)].value;
          if (!knowledgePoints.includes(point)) {
            knowledgePoints.push(point);
          }
        }
        
        // 随机选择1-2个年级
        const gradeLevelCount = Math.floor(Math.random() * 2) + 1;
        const gradeLevel = [];
        for (let j = 0; j < gradeLevelCount; j++) {
          const grade = gradeLevelOptions[Math.floor(Math.random() * gradeLevelOptions.length)].value;
          if (!gradeLevel.includes(grade)) {
            gradeLevel.push(grade);
          }
        }
        
        // 随机难度
        const difficulty = Math.floor(Math.random() * 5) + 1;
        
        // 随机查看和下载次数
        const viewCount = Math.floor(Math.random() * 1000);
        const downloadCount = Math.floor(viewCount * 0.3);
        
        // 随机创建时间（最近30天内）
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(Math.random() * 30));
        const createdAt = date.toISOString().split('T')[0];
        
        // 随机状态
        const status = Math.random() > 0.2 ? 'published' : 'draft';
        
        const title = titles[Math.floor(Math.random() * titles.length)] + ` ${i}`;
        
        const resourceRecord = {
          id: `resource-${i.toString().padStart(3, '0')}`,
          title,
          subjectId,
          resourceType,
          knowledgePoints,
          gradeLevel,
          difficulty,
          description: `这是一份关于${title}的学习资料，适合${getGradeLevelNames(gradeLevel)}学生学习使用。包含了${getKnowledgePointNames(knowledgePoints)}等知识点的详细讲解和练习题。`,
          resourceUrl: 'https://example.com/resource.pdf',
          coverImage: '',
          status,
          viewCount,
          downloadCount,
          recommendCount: Math.floor(downloadCount * 0.5),
          createdAt
        };
        
        // 应用筛选条件
        let match = true;
        
        if (searchForm.keyword) {
          const keyword = searchForm.keyword.toLowerCase();
          const titleMatch = resourceRecord.title.toLowerCase().includes(keyword);
          const descMatch = resourceRecord.description.toLowerCase().includes(keyword);
          
          if (!titleMatch && !descMatch) {
            match = false;
          }
        }
        
        if (searchForm.subjectId && resourceRecord.subjectId !== searchForm.subjectId) {
          match = false;
        }
        
        if (searchForm.resourceType && resourceRecord.resourceType !== searchForm.resourceType) {
          match = false;
        }
        
        if (match) {
          mockList.push(resourceRecord);
        }
      }
      
      // 分页
      const startIndex = (pagination.current - 1) * pagination.pageSize;
      const endIndex = startIndex + pagination.pageSize;
      const paginatedList = mockList.slice(startIndex, endIndex);
      
      return {
        list: paginatedList,
        total: mockList.length
      };
    };

    // 获取学科名称
    const getSubjectName = (subjectId) => {
      const subject = subjectOptions.find(item => item.value === subjectId);
      return subject ? subject.label : '';
    };

    // 获取知识点名称
    const getKnowledgePointName = (pointId) => {
      const point = knowledgePointOptions.find(item => item.value === pointId);
      return point ? point.label : '';
    };

    // 获取知识点名称列表
    const getKnowledgePointNames = (pointIds) => {
      return pointIds.map(id => getKnowledgePointName(id)).join('、');
    };

    // 获取年级名称
    const getGradeLevelName = (gradeId) => {
      const grade = gradeLevelOptions.find(item => item.value === gradeId);
      return grade ? grade.label : '';
    };

    // 获取年级名称列表
    const getGradeLevelNames = (gradeIds) => {
      return gradeIds.map(id => getGradeLevelName(id)).join('、');
    };

    // 获取资料类型文本
    const getResourceTypeText = (type) => {
      switch (type) {
        case 'slides':
          return '课件';
        case 'exercises':
          return '习题';
        case 'video':
          return '视频';
        case 'document':
          return '文档';
        case 'chart':
          return '图表';
        case 'exam':
          return '试卷';
        default:
          return '未知';
      }
    };

    // 获取资料类型颜色
    const getResourceTypeColor = (type) => {
      switch (type) {
        case 'slides':
          return 'blue';
        case 'exercises':
          return 'green';
        case 'video':
          return 'purple';
        case 'document':
          return 'cyan';
        case 'chart':
          return 'orange';
        case 'exam':
          return 'red';
        default:
          return 'gray';
      }
    };

    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'published':
          return '已发布';
        case 'draft':
          return '草稿';
        default:
          return '未知';
      }
    };

    // 获取状态颜色
    const getStatusColor = (status) => {
      switch (status) {
        case 'published':
          return 'green';
        case 'draft':
          return 'orange';
        default:
          return 'gray';
      }
    };

    // 获取推荐对象选项
    const getTargetOptions = () => {
      switch (recommendForm.targetType) {
        case 'student':
          return studentOptions;
        case 'class':
          return classOptions;
        case 'grade':
          return gradeOptions;
        default:
          return [];
      }
    };

    // 处理搜索
    const handleSearch = () => {
      pagination.current = 1;
      fetchResourceData();
    };

    // 重置搜索
    const resetSearch = () => {
      searchForm.keyword = '';
      searchForm.subjectId = undefined;
      searchForm.resourceType = undefined;
      pagination.current = 1;
      fetchResourceData();
    };

    // 处理分页变化
    const onPageChange = (page) => {
      pagination.current = page;
      fetchResourceData();
    };

    // 处理每页条数变化
    const onPageSizeChange = (pageSize) => {
      pagination.pageSize = pageSize;
      pagination.current = 1;
      fetchResourceData();
    };

    // 打开添加资料弹窗
    const openAddResourceModal = () => {
      isEdit.value = false;
      resetResourceForm();
      resourceModalVisible.value = true;
    };

    // 处理预览
    const handlePreview = (record) => {
      // 填充当前资料数据
      Object.assign(currentResource, record);
      
      // 准备资料统计数据
      resourceStatsData.value = [
        {
          label: '查看次数',
          value: record.viewCount
        },
        {
          label: '下载次数',
          value: record.downloadCount
        },
        {
          label: '推荐次数',
          value: record.recommendCount
        },
        {
          label: '创建时间',
          value: record.createdAt
        }
      ];
      
      previewModalVisible.value = true;
    };

    // 处理编辑
    const handleEdit = (record) => {
      isEdit.value = true;
      
      // 填充表单数据
      resourceForm.id = record.id;
      resourceForm.title = record.title;
      resourceForm.subjectId = record.subjectId;
      resourceForm.resourceType = record.resourceType;
      resourceForm.knowledgePoints = record.knowledgePoints;
      resourceForm.gradeLevel = record.gradeLevel;
      resourceForm.difficulty = record.difficulty;
      resourceForm.description = record.description;
      resourceForm.resourceUrl = record.resourceUrl;
      resourceForm.coverImage = record.coverImage;
      resourceForm.status = record.status;
      
      // 设置文件列表
      if (record.coverImage) {
        fileList.value = [
          {
            uid: '1',
            name: 'cover.jpg',
            url: record.coverImage
          }
        ];
      } else {
        fileList.value = [];
      }
      
      resourceModalVisible.value = true;
    };

    // 处理推荐
    const handleRecommend = (record) => {
      recommendForm.resourceId = record.id;
      recommendForm.resourceTitle = record.title;
      recommendForm.targetType = 'student';
      recommendForm.targetIds = [];
      recommendForm.recommendReason = `推荐学习《${record.title}》，这是一份很好的学习资料，适合${getGradeLevelNames(record.gradeLevel)}学生学习使用。`;
      recommendForm.notifyNow = true;
      
      recommendModalVisible.value = true;
    };

    // 处理删除
    const handleDelete = (record) => {
      Message.success(`已删除学习资料：${record.title}`);
      
      // 在实际应用中，这里应该调用API来删除资料
      // 然后重新获取资料列表
      
      // 模拟删除
      const index = resourceData.value.findIndex(item => item.id === record.id);
      if (index !== -1) {
        resourceData.value.splice(index, 1);
      }
    };

    // 处理批量导入
    const handleBatchImport = () => {
      importFileList.value = [];
      importModalVisible.value = true;
    };

    // 处理批量删除
    const handleBatchDelete = () => {
      if (selectedRowKeys.value.length === 0) {
        Message.warning('请先选择要删除的学习资料');
        return;
      }
      
      Message.success(`已删除 ${selectedRowKeys.value.length} 份学习资料`);
      selectedRowKeys.value = [];
      fetchResourceData();
    };

    // 处理下载资源
    const handleDownloadResource = () => {
      Message.success(`已下载学习资料：${currentResource.title}`);
    };

    // 处理推荐当前资源
    const handleRecommendCurrent = () => {
      handleRecommend(currentResource);
      closePreviewModal();
    };

    // 自定义上传请求
    const customUploadRequest = (options) => {
      const { file, onSuccess } = options;
      
      // 模拟上传
      setTimeout(() => {
        const url = URL.createObjectURL(file);
        
        if (options.fileItem) {
          options.fileItem.url = url;
        }
        
        if (importFileList.value.length > 0) {
          importFileList.value = [{ name: file.name, url }];
        } else {
          fileList.value = [{ name: file.name, url }];
          resourceForm.coverImage = url;
        }
        
        onSuccess();
      }, 500);
    };

    // 提交资料表单
    const handleSubmitResource = async (done) => {
      try {
        await resourceFormRef.value.validate();
        
        if (isEdit.value) {
          Message.success(`学习资料 ${resourceForm.title} 更新成功`);
        } else {
          Message.success(`学习资料 ${resourceForm.title} 添加成功`);
        }
        
        // 在实际应用中，这里应该调用API来创建或更新资料
        // 然后重新获取资料列表
        
        closeResourceModal();
        fetchResourceData();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 确认导入
    const handleConfirmImport = (done) => {
      if (importFileList.value.length === 0) {
        Message.error('请选择要导入的文件');
        done(false);
        return;
      }
      
      Message.success('学习资料导入成功');
      
      // 在实际应用中，这里应该调用API来导入资料
      // 然后重新获取资料列表
      
      closeImportModal();
      fetchResourceData();
      done();
    };

    // 确认推荐
    const handleConfirmRecommend = async (done) => {
      try {
        await recommendFormRef.value.validate();
        
        Message.success(`学习资料推荐成功`);
        
        // 在实际应用中，这里应该调用API来推荐资料
        
        closeRecommendModal();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 关闭资料弹窗
    const closeResourceModal = () => {
      resourceModalVisible.value = false;
      resetResourceForm();
      fileList.value = [];
    };

    // 关闭导入弹窗
    const closeImportModal = () => {
      importModalVisible.value = false;
      importFileList.value = [];
    };

    // 关闭推荐弹窗
    const closeRecommendModal = () => {
      recommendModalVisible.value = false;
    };

    // 关闭预览弹窗
    const closePreviewModal = () => {
      previewModalVisible.value = false;
    };

    // 重置资料表单
    const resetResourceForm = () => {
      resourceForm.id = '';
      resourceForm.title = '';
      resourceForm.subjectId = undefined;
      resourceForm.resourceType = undefined;
      resourceForm.knowledgePoints = [];
      resourceForm.gradeLevel = [];
      resourceForm.difficulty = 3;
      resourceForm.description = '';
      resourceForm.resourceUrl = '';
      resourceForm.coverImage = '';
      resourceForm.status = 'published';
    };

    return {
      searchForm,
      resourceForm,
      importForm,
      recommendForm,
      fileList,
      importFileList,
      resourceFormRef,
      importFormRef,
      recommendFormRef,
      loading,
      resourceModalVisible,
      importModalVisible,
      recommendModalVisible,
      previewModalVisible,
      isEdit,
      currentResource,
      resourceStatsData,
      pagination,
      selectedRowKeys,
      rowSelection,
      subjectOptions,
      resourceTypeOptions,
      knowledgePointOptions,
      gradeLevelOptions,
      stats,
      columns,
      resourceFormRules,
      resourceData,
      getSubjectName,
      getKnowledgePointName,
      getGradeLevelName,
      getResourceTypeText,
      getResourceTypeColor,
      getStatusText,
      getStatusColor,
      getTargetOptions,
      handleSearch,
      resetSearch,
      onPageChange,
      onPageSizeChange,
      openAddResourceModal,
      handlePreview,
      handleEdit,
      handleRecommend,
      handleDelete,
      handleBatchImport,
      handleBatchDelete,
      handleDownloadResource,
      handleRecommendCurrent,
      customUploadRequest,
      handleSubmitResource,
      handleConfirmImport,
      handleConfirmRecommend,
      closeResourceModal,
      closeImportModal,
      closeRecommendModal,
      closePreviewModal
    };
  }
};
</script>

<style scoped>
.learning-resource-management-container {
  padding: 16px;
}

.search-card,
.table-card {
  margin-bottom: 16px;
}

.stats-row {
  margin-bottom: 16px;
}

.stat-card {
  height: 100%;
}

.stat-card-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #86909C;
}

.resource-preview {
  padding: 0 16px;
}

.resource-header {
  text-align: center;
  margin-bottom: 24px;
}

.resource-meta {
  display: flex;
  justify-content: center;
  gap: 16px;
  color: #86909C;
}

.resource-section {
  margin-bottom: 24px;
}

.knowledge-points,
.grade-levels {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.resource-content {
  margin-top: 16px;
}

.resource-iframe-container {
  width: 100%;
  height: 400px;
  border: 1px solid #e5e6eb;
  border-radius: 4px;
  overflow: hidden;
}

.resource-iframe {
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .search-card .arco-col {
    margin-bottom: 16px;
  }
  
  .stats-row .arco-col {
    margin-bottom: 16px;
  }
  
  .resource-meta {
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  
  .resource-iframe-container {
    height: 300px;
  }
}
</style>
