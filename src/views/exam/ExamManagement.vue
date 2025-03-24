<!-- 后台管理系统考试管理页面 -->
<!-- frontend/scorex-admin/src/views/exam/ExamManagement.vue -->

<template>
  <div class="exam-management-container">
    <!-- 搜索和操作栏 -->
    <a-card class="search-card">
      <a-row :gutter="16">
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-input
            v-model="searchForm.keyword"
            placeholder="搜索考试名称"
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.subject"
            placeholder="学科"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="subject in subjectOptions" :key="subject.value" :value="subject.value">
              {{ subject.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-range-picker
            v-model="searchForm.dateRange"
            style="width: 100%"
            format="YYYY-MM-DD"
          />
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

    <!-- 考试列表 -->
    <a-card class="table-card">
      <template #title>
        考试列表
      </template>
      <template #extra>
        <a-space>
          <a-button type="primary" @click="openAddExamModal">
            <template #icon>
              <icon-plus />
            </template>
            新增考试
          </a-button>
          <a-button @click="handleBatchImport">
            <template #icon>
              <icon-upload />
            </template>
            批量导入
          </a-button>
          <a-button @click="handleBatchExport">
            <template #icon>
              <icon-download />
            </template>
            导出
          </a-button>
        </a-space>
      </template>

      <a-table
        :loading="loading"
        :columns="columns"
        :data="examData"
        :pagination="pagination"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        row-key="id"
      >
        <template #subject="{ record }">
          <a-tag :color="getSubjectColor(record.subject)">{{ record.subject }}</a-tag>
        </template>
        
        <template #status="{ record }">
          <a-badge
            :status="record.status === '已发布' ? 'success' : (record.status === '草稿' ? 'warning' : 'default')"
            :text="record.status"
          />
        </template>
        
        <template #operations="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleViewExam(record)">
              查看
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleEdit(record)">
              编辑
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleScoreManagement(record)">
              成绩管理
            </a-button>
            <a-divider direction="vertical" />
            <a-button
              type="text"
              size="small"
              :status="record.status === '已发布' ? 'warning' : 'success'"
              @click="handleToggleStatus(record)"
            >
              {{ record.status === '已发布' ? '撤回' : '发布' }}
            </a-button>
            <a-divider direction="vertical" />
            <a-popconfirm
              content="确定要删除此考试吗？"
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

    <!-- 新增/编辑考试弹窗 -->
    <a-modal
      v-model:visible="examModalVisible"
      :title="isEdit ? '编辑考试' : '新增考试'"
      @cancel="closeExamModal"
      @before-ok="handleSubmitExam"
      width="700px"
    >
      <a-form :model="examForm" ref="examFormRef" :rules="examFormRules" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="name" label="考试名称" required>
          <a-input v-model="examForm.name" placeholder="请输入考试名称" />
        </a-form-item>
        <a-form-item field="subject" label="学科" required>
          <a-select v-model="examForm.subject" placeholder="请选择学科">
            <a-option v-for="subject in subjectOptions" :key="subject.value" :value="subject.value">
              {{ subject.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="examDate" label="考试日期" required>
          <a-date-picker v-model="examForm.examDate" style="width: 100%" />
        </a-form-item>
        <a-form-item field="totalScore" label="总分" required>
          <a-input-number v-model="examForm.totalScore" placeholder="请输入总分" :min="0" :max="1000" style="width: 100%" />
        </a-form-item>
        <a-form-item field="duration" label="考试时长(分钟)" required>
          <a-input-number v-model="examForm.duration" placeholder="请输入考试时长" :min="0" :max="300" style="width: 100%" />
        </a-form-item>
        <a-form-item field="gradeLevel" label="年级" required>
          <a-select v-model="examForm.gradeLevel" placeholder="请选择年级">
            <a-option v-for="grade in gradeOptions" :key="grade.value" :value="grade.value">
              {{ grade.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="classes" label="班级" required>
          <a-select v-model="examForm.classes" placeholder="请选择班级" multiple>
            <a-option v-for="cls in classOptions" :key="cls.value" :value="cls.value">
              {{ cls.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="knowledgePoints" label="知识点">
          <a-select v-model="examForm.knowledgePoints" placeholder="请选择知识点" multiple>
            <a-option v-for="point in knowledgePointOptions" :key="point.value" :value="point.value">
              {{ point.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="description" label="考试说明">
          <a-textarea v-model="examForm.description" placeholder="请输入考试说明" />
        </a-form-item>
        <a-form-item field="status" label="状态" required>
          <a-radio-group v-model="examForm.status">
            <a-radio value="草稿">草稿</a-radio>
            <a-radio value="已发布">发布</a-radio>
          </a-radio-group>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 批量导入弹窗 -->
    <a-modal
      v-model:visible="importModalVisible"
      title="批量导入考试"
      @cancel="closeImportModal"
      @before-ok="handleConfirmImport"
    >
      <a-form :model="importForm" ref="importFormRef" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="file" label="导入文件">
          <a-upload
            action="/"
            :file-list="fileList"
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
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue';
import { Message } from '@arco-design/web-vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      subject: undefined,
      dateRange: []
    });

    // 考试表单
    const examForm = reactive({
      id: '',
      name: '',
      subject: '',
      examDate: null,
      totalScore: 100,
      duration: 120,
      gradeLevel: '',
      classes: [],
      knowledgePoints: [],
      description: '',
      status: '草稿'
    });

    // 导入表单
    const importForm = reactive({});
    const fileList = ref([]);

    // 表单引用
    const examFormRef = ref(null);
    const importFormRef = ref(null);

    // 状态变量
    const loading = ref(false);
    const examModalVisible = ref(false);
    const importModalVisible = ref(false);
    const isEdit = ref(false);
    const currentExamId = ref('');

    // 分页配置
    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0,
      showTotal: true,
      showPageSize: true,
      pageSizeOptions: [10, 20, 50, 100]
    });

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
    ];

    // 年级选项
    const gradeOptions = [
      { label: '初一', value: '初一' },
      { label: '初二', value: '初二' },
      { label: '初三', value: '初三' },
      { label: '高一', value: '高一' },
      { label: '高二', value: '高二' },
      { label: '高三', value: '高三' }
    ];

    // 班级选项
    const classOptions = [
      { label: '1班', value: '1班' },
      { label: '2班', value: '2班' },
      { label: '3班', value: '3班' },
      { label: '4班', value: '4班' },
      { label: '5班', value: '5班' },
      { label: '6班', value: '6班' },
      { label: '7班', value: '7班' },
      { label: '8班', value: '8班' }
    ];

    // 知识点选项 - 根据学科动态变化
    const knowledgePointOptions = ref([]);

    // 监听学科变化，更新知识点选项
    watch(() => examForm.subject, (newSubject) => {
      if (newSubject) {
        updateKnowledgePoints(newSubject);
      } else {
        knowledgePointOptions.value = [];
      }
    });

    // 更新知识点选项
    const updateKnowledgePoints = (subject) => {
      const knowledgePointsMap = {
        '语文': [
          { label: '文言文阅读', value: '文言文阅读' },
          { label: '现代文阅读', value: '现代文阅读' },
          { label: '诗歌鉴赏', value: '诗歌鉴赏' },
          { label: '作文写作', value: '作文写作' },
          { label: '语法修辞', value: '语法修辞' }
        ],
        '数学': [
          { label: '函数', value: '函数' },
          { label: '导数', value: '导数' },
          { label: '三角函数', value: '三角函数' },
          { label: '概率统计', value: '概率统计' },
          { label: '立体几何', value: '立体几何' },
          { label: '解析几何', value: '解析几何' }
        ],
        '英语': [
          { label: '阅读理解', value: '阅读理解' },
          { label: '完形填空', value: '完形填空' },
          { label: '语法', value: '语法' },
          { label: '写作', value: '写作' },
          { label: '听力', value: '听力' }
        ],
        '物理': [
          { label: '力学', value: '力学' },
          { label: '电学', value: '电学' },
          { label: '热学', value: '热学' },
          { label: '光学', value: '光学' },
          { label: '原子物理', value: '原子物理' }
        ],
        '化学': [
          { label: '元素化合物', value: '元素化合物' },
          { label: '化学反应', value: '化学反应' },
          { label: '有机化学', value: '有机化学' },
          { label: '物质结构', value: '物质结构' }
        ]
      };
      
      knowledgePointOptions.value = knowledgePointsMap[subject] || [];
    };

    // 表格列定义
    const columns = [
      {
        title: '考试名称',
        dataIndex: 'name'
      },
      {
        title: '学科',
        slotName: 'subject'
      },
      {
        title: '年级',
        dataIndex: 'gradeLevel'
      },
      {
        title: '考试日期',
        dataIndex: 'examDate'
      },
      {
        title: '总分',
        dataIndex: 'totalScore'
      },
      {
        title: '时长(分钟)',
        dataIndex: 'duration'
      },
      {
        title: '参与班级',
        dataIndex: 'classesText'
      },
      {
        title: '状态',
        slotName: 'status'
      },
      {
        title: '创建时间',
        dataIndex: 'createTime'
      },
      {
        title: '操作',
        slotName: 'operations',
        fixed: 'right',
        width: 320
      }
    ];

    // 考试表单校验规则
    const examFormRules = {
      name: [
        { required: true, message: '请输入考试名称' }
      ],
      subject: [
        { required: true, message: '请选择学科' }
      ],
      examDate: [
        { required: true, message: '请选择考试日期' }
      ],
      totalScore: [
        { required: true, message: '请输入总分' },
        { type: 'number', min: 0, max: 1000, message: '总分应在0-1000之间' }
      ],
      duration: [
        { required: true, message: '请输入考试时长' },
        { type: 'number', min: 0, max: 300, message: '考试时长应在0-300分钟之间' }
      ],
      gradeLevel: [
        { required: true, message: '请选择年级' }
      ],
      classes: [
        { required: true, message: '请选择班级' }
      ],
      status: [
        { required: true, message: '请选择状态' }
      ]
    };

    // 模拟考试数据
    const examData = ref([]);

    // 生命周期钩子
    onMounted(() => {
      fetchExamData();
    });

    // 获取考试数据
    const fetchExamData = () => {
      loading.value = true;
      
      // 模拟API请求
      setTimeout(() => {
        // 生成模拟数据
        const mockData = generateMockExamData();
        examData.value = mockData.list;
        pagination.total = mockData.total;
        loading.value = false;
      }, 800);
    };

    // 生成模拟考试数据
    const generateMockExamData = () => {
      const subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'];
      const gradeLevels = ['初一', '初二', '初三', '高一', '高二', '高三'];
      const statuses = ['草稿', '已发布'];
      
      const mockList = [];
      const totalItems = 45;
      
      for (let i = 1; i <= totalItems; i++) {
        const subject = subjects[Math.floor(Math.random() * subjects.length)];
        const gradeLevel = gradeLevels[Math.floor(Math.random() * gradeLevels.length)];
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        
        // 随机选择1-4个班级
        const classCount = Math.floor(Math.random() * 4) + 1;
        const classes = [];
        for (let j = 0; j < classCount; j++) {
          const classNum = Math.floor(Math.random() * 8) + 1;
          const className = `${classNum}班`;
          if (!classes.includes(className)) {
            classes.push(className);
          }
        }
        
        const exam = {
          id: `exam-${i}`,
          name: `${gradeLevel}${subject}${Math.random() > 0.5 ? '期中' : '期末'}考试`,
          subject,
          gradeLevel,
          examDate: `2025-0${Math.floor(Math.random() * 3) + 1}-${Math.floor(Math.random() * 28) + 1}`,
          totalScore: Math.floor(Math.random() * 50) * 2 + 100,
          duration: Math.floor(Math.random() * 6) * 15 + 60,
          classes,
          classesText: classes.join(', '),
          status,
          createTime: `2025-0${Math.floor(Math.random() * 3) + 1}-${Math.floor(Math.random() * 28) + 1} ${Math.floor(Math.random() * 24).toString().padStart(2, '0')}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`
        };
        
        // 应用筛选条件
        let match = true;
        
        if (searchForm.keyword) {
          const keyword = searchForm.keyword.toLowerCase();
          if (!exam.name.toLowerCase().includes(keyword)) {
            match = false;
          }
        }
        
        if (searchForm.subject && exam.subject !== searchForm.subject) {
          match = false;
        }
        
        if (searchForm.dateRange && searchForm.dateRange.length === 2) {
          const examDate = new Date(exam.examDate);
          const startDate = new Date(searchForm.dateRange[0]);
          const endDate = new Date(searchForm.dateRange[1]);
          
          if (examDate < startDate || examDate > endDate) {
            match = false;
          }
        }
        
        if (match) {
          mockList.push(exam);
        }
      }
      
      // 排序：最新的在前面
      mockList.sort((a, b) => new Date(b.createTime) - new Date(a.createTime));
      
      // 分页
      const startIndex = (pagination.current - 1) * pagination.pageSize;
      const endIndex = startIndex + pagination.pageSize;
      const paginatedList = mockList.slice(startIndex, endIndex);
      
      return {
        list: paginatedList,
        total: mockList.length
      };
    };

    // 处理搜索
    const handleSearch = () => {
      pagination.current = 1;
      fetchExamData();
    };

    // 重置搜索
    const resetSearch = () => {
      searchForm.keyword = '';
      searchForm.subject = undefined;
      searchForm.dateRange = [];
      pagination.current = 1;
      fetchExamData();
    };

    // 处理分页变化
    const onPageChange = (page) => {
      pagination.current = page;
      fetchExamData();
    };

    // 处理每页条数变化
    const onPageSizeChange = (pageSize) => {
      pagination.pageSize = pageSize;
      pagination.current = 1;
      fetchExamData();
    };

    // 打开新增考试弹窗
    const openAddExamModal = () => {
      isEdit.value = false;
      resetExamForm();
      examModalVisible.value = true;
    };

    // 处理查看考试
    const handleViewExam = (record) => {
      router.push({ name: 'ExamDetail', params: { id: record.id } });
    };

    // 处理编辑考试
    const handleEdit = (record) => {
      isEdit.value = true;
      currentExamId.value = record.id;
      
      // 填充表单数据
      examForm.id = record.id;
      examForm.name = record.name;
      examForm.subject = record.subject;
      examForm.examDate = record.examDate;
      examForm.totalScore = record.totalScore;
      examForm.duration = record.duration;
      examForm.gradeLevel = record.gradeLevel;
      examForm.classes = record.classes;
      examForm.status = record.status;
      
      // 更新知识点选项
      updateKnowledgePoints(record.subject);
      
      examModalVisible.value = true;
    };

    // 处理成绩管理
    const handleScoreManagement = (record) => {
      router.push({ name: 'ScoreManagement', params: { examId: record.id } });
    };

    // 处理切换考试状态
    const handleToggleStatus = (record) => {
      const newStatus = record.status === '已发布' ? '草稿' : '已发布';
      const action = newStatus === '已发布' ? '发布' : '撤回';
      
      Message.success(`已${action}考试 ${record.name}`);
      
      // 在实际应用中，这里应该调用API来更新考试状态
      // 然后重新获取考试列表
      
      // 模拟更新
      const index = examData.value.findIndex(exam => exam.id === record.id);
      if (index !== -1) {
        examData.value[index].status = newStatus;
      }
    };

    // 处理删除考试
    const handleDelete = (record) => {
      Message.success(`已删除考试 ${record.name}`);
      
      // 在实际应用中，这里应该调用API来删除考试
      // 然后重新获取考试列表
      
      // 模拟删除
      const index = examData.value.findIndex(exam => exam.id === record.id);
      if (index !== -1) {
        examData.value.splice(index, 1);
      }
    };

    // 处理批量导入
    const handleBatchImport = () => {
      fileList.value = [];
      importModalVisible.value = true;
    };

    // 处理批量导出
    const handleBatchExport = () => {
      Message.success('考试数据导出成功');
    };

    // 自定义上传请求
    const customUploadRequest = (options) => {
      const { file, onSuccess } = options;
      fileList.value = [{ name: file.name, status: 'done' }];
      onSuccess();
    };

    // 提交考试表单
    const handleSubmitExam = async (done) => {
      try {
        await examFormRef.value.validate();
        
        if (isEdit.value) {
          Message.success(`考试 ${examForm.name} 更新成功`);
        } else {
          Message.success(`考试 ${examForm.name} 创建成功`);
        }
        
        // 在实际应用中，这里应该调用API来创建或更新考试
        // 然后重新获取考试列表
        
        closeExamModal();
        fetchExamData();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 确认导入
    const handleConfirmImport = (done) => {
      if (fileList.value.length === 0) {
        Message.error('请选择要导入的文件');
        done(false);
        return;
      }
      
      Message.success('考试数据导入成功');
      
      // 在实际应用中，这里应该调用API来导入考试数据
      // 然后重新获取考试列表
      
      closeImportModal();
      fetchExamData();
      done();
    };

    // 关闭考试弹窗
    const closeExamModal = () => {
      examModalVisible.value = false;
      resetExamForm();
    };

    // 关闭导入弹窗
    const closeImportModal = () => {
      importModalVisible.value = false;
      fileList.value = [];
    };

    // 重置考试表单
    const resetExamForm = () => {
      examForm.id = '';
      examForm.name = '';
      examForm.subject = '';
      examForm.examDate = null;
      examForm.totalScore = 100;
      examForm.duration = 120;
      examForm.gradeLevel = '';
      examForm.classes = [];
      examForm.knowledgePoints = [];
      examForm.description = '';
      examForm.status = '草稿';
    };

    // 获取学科颜色
    const getSubjectColor = (subject) => {
      const colorMap = {
        '语文': 'blue',
        '数学': 'green',
        '英语': 'orange',
        '物理': 'purple',
        '化学': 'red',
        '生物': 'cyan',
        '历史': 'gold',
        '地理': 'lime',
        '政治': 'magenta'
      };
      return colorMap[subject] || 'gray';
    };

    return {
      searchForm,
      examForm,
      importForm,
      fileList,
      examFormRef,
      importFormRef,
      loading,
      examModalVisible,
      importModalVisible,
      isEdit,
      pagination,
      subjectOptions,
      gradeOptions,
      classOptions,
      knowledgePointOptions,
      columns,
      examFormRules,
      examData,
      handleSearch,
      resetSearch,
      onPageChange,
      onPageSizeChange,
      openAddExamModal,
      handleViewExam,
      handleEdit,
      handleScoreManagement,
      handleToggleStatus,
      handleDelete,
      handleBatchImport,
      handleBatchExport,
      customUploadRequest,
      handleSubmitExam,
      handleConfirmImport,
      closeExamModal,
      closeImportModal,
      getSubjectColor
    };
  }
};
</script>

<style scoped>
.exam-management-container {
  padding: 16px;
}

.search-card {
  margin-bottom: 16px;
}

.table-card {
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .search-card .arco-col {
    margin-bottom: 16px;
  }
}
</style>
