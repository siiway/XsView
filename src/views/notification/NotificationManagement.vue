<!-- 后台管理系统通知管理页面 -->
<!-- frontend/scorex-admin/src/views/notification/NotificationManagement.vue -->

<template>
  <div class="notification-management-container">
    <!-- 搜索和操作栏 -->
    <a-card class="search-card">
      <a-row :gutter="16">
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-input
            v-model="searchForm.keyword"
            placeholder="搜索通知标题/内容"
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.type"
            placeholder="通知类型"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="type in notificationTypeOptions" :key="type.value" :value="type.value">
              {{ type.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-range-picker
            v-model="searchForm.dateRange"
            style="width: 100%"
            placeholder="发送日期范围"
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

    <!-- 统计卡片 -->
    <a-row :gutter="16" class="stats-row">
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--primary-6), 0.1)">
              <icon-notification style="color: rgb(var(--primary-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalNotifications }}</div>
              <div class="stat-label">通知总数</div>
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
              <div class="stat-value">{{ stats.todayNotifications }}</div>
              <div class="stat-label">今日发送通知</div>
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
              <div class="stat-value">{{ stats.readCount }}</div>
              <div class="stat-label">已读通知数</div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--danger-6), 0.1)">
              <icon-eye style="color: rgb(var(--danger-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.readRate }}%</div>
              <div class="stat-label">通知阅读率</div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 通知列表 -->
    <a-card class="table-card">
      <template #title>
        通知列表
      </template>
      <template #extra>
        <a-space>
          <a-button type="primary" @click="openAddNotificationModal">
            <template #icon>
              <icon-plus />
            </template>
            发送通知
          </a-button>
          <a-button @click="handleBatchDelete" status="danger">
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
        :data="notificationData"
        :pagination="pagination"
        :row-selection="rowSelection"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        row-key="id"
      >
        <template #type="{ record }">
          <a-tag :color="getTypeColor(record.type)">
            {{ getTypeText(record.type) }}
          </a-tag>
        </template>
        
        <template #priority="{ record }">
          <a-tag :color="getPriorityColor(record.priority)">
            {{ getPriorityText(record.priority) }}
          </a-tag>
        </template>
        
        <template #status="{ record }">
          <a-tag :color="getStatusColor(record.status)">
            {{ getStatusText(record.status) }}
          </a-tag>
        </template>
        
        <template #readRate="{ record }">
          <a-progress
            :percent="record.readRate"
            :stroke-color="getProgressColor(record.readRate)"
            :show-text="true"
          />
        </template>
        
        <template #operations="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleViewDetail(record)">
              详情
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleResend(record)">
              重新发送
            </a-button>
            <a-divider direction="vertical" />
            <a-popconfirm
              content="确定要删除此通知吗？"
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

    <!-- 发送通知弹窗 -->
    <a-modal
      v-model:visible="notificationModalVisible"
      :title="isEdit ? '编辑通知' : '发送通知'"
      @cancel="closeNotificationModal"
      @before-ok="handleSubmitNotification"
      width="700px"
    >
      <a-form :model="notificationForm" ref="notificationFormRef" :rules="notificationFormRules" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="title" label="通知标题" required>
          <a-input v-model="notificationForm.title" placeholder="请输入通知标题" />
        </a-form-item>
        <a-form-item field="content" label="通知内容" required>
          <a-textarea v-model="notificationForm.content" placeholder="请输入通知内容" :auto-size="{ minRows: 4, maxRows: 8 }" />
        </a-form-item>
        <a-form-item field="type" label="通知类型" required>
          <a-select v-model="notificationForm.type" placeholder="请选择通知类型">
            <a-option v-for="type in notificationTypeOptions" :key="type.value" :value="type.value">
              {{ type.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="priority" label="优先级" required>
          <a-radio-group v-model="notificationForm.priority">
            <a-radio value="low">低</a-radio>
            <a-radio value="medium">中</a-radio>
            <a-radio value="high">高</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item field="targetType" label="接收对象" required>
          <a-radio-group v-model="notificationForm.targetType">
            <a-radio value="all">所有用户</a-radio>
            <a-radio value="student">指定学生</a-radio>
            <a-radio value="class">指定班级</a-radio>
            <a-radio value="grade">指定年级</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item field="targetIds" label="选择对象" v-if="notificationForm.targetType !== 'all'" required>
          <a-select v-model="notificationForm.targetIds" placeholder="请选择接收对象" multiple>
            <a-option v-for="target in getTargetOptions()" :key="target.value" :value="target.value">
              {{ target.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="sendMethod" label="发送方式" required>
          <a-checkbox-group v-model="notificationForm.sendMethod">
            <a-checkbox value="app">应用内通知</a-checkbox>
            <a-checkbox value="email">电子邮件</a-checkbox>
            <a-checkbox value="sms">短信</a-checkbox>
          </a-checkbox-group>
        </a-form-item>
        <a-form-item field="scheduledTime" label="定时发送">
          <a-date-picker
            v-model="notificationForm.scheduledTime"
            show-time
            format="YYYY-MM-DD HH:mm:ss"
            placeholder="选择发送时间"
            style="width: 100%"
          />
        </a-form-item>
        <a-form-item field="attachments" label="附件">
          <a-upload
            :file-list="fileList"
            :custom-request="customUploadRequest"
            :limit="5"
          >
            <template #upload-button>
              <a-button>
                <template #icon>
                  <icon-upload />
                </template>
                上传附件
              </a-button>
            </template>
          </a-upload>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 通知详情弹窗 -->
    <a-modal
      v-model:visible="detailModalVisible"
      title="通知详情"
      @cancel="closeDetailModal"
      width="700px"
    >
      <div class="notification-detail">
        <div class="notification-header">
          <h2>{{ currentNotification.title }}</h2>
          <div class="notification-meta">
            <a-tag :color="getTypeColor(currentNotification.type)">
              {{ getTypeText(currentNotification.type) }}
            </a-tag>
            <a-tag :color="getPriorityColor(currentNotification.priority)">
              {{ getPriorityText(currentNotification.priority) }}
            </a-tag>
            <span>发送时间: {{ currentNotification.sendTime }}</span>
          </div>
        </div>
        
        <a-divider />
        
        <div class="notification-section">
          <h3>通知内容</h3>
          <div class="notification-content">
            {{ currentNotification.content }}
          </div>
        </div>
        
        <div class="notification-section" v-if="currentNotification.attachments && currentNotification.attachments.length > 0">
          <h3>附件</h3>
          <div class="notification-attachments">
            <a-space direction="vertical">
              <a-link v-for="(attachment, index) in currentNotification.attachments" :key="index">
                {{ attachment.name }}
              </a-link>
            </a-space>
          </div>
        </div>
        
        <div class="notification-section">
          <h3>接收对象</h3>
          <div class="notification-targets">
            <a-descriptions :data="targetInfoData" layout="inline-horizontal" bordered />
          </div>
        </div>
        
        <div class="notification-section">
          <h3>发送方式</h3>
          <div class="notification-methods">
            <a-space>
              <a-tag v-for="method in currentNotification.sendMethod" :key="method" color="blue">
                {{ getSendMethodText(method) }}
              </a-tag>
            </a-space>
          </div>
        </div>
        
        <div class="notification-section">
          <h3>阅读统计</h3>
          <a-descriptions :data="readStatsData" layout="inline-horizontal" bordered />
        </div>
      </div>
      
      <template #footer>
        <a-space>
          <a-button type="primary" @click="handleResendCurrent">
            重新发送
          </a-button>
          <a-popconfirm
            content="确定要删除此通知吗？"
            @ok="handleDeleteCurrent"
          >
            <a-button status="danger">
              删除
            </a-button>
          </a-popconfirm>
        </a-space>
      </template>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { Message } from '@arco-design/web-vue';

export default {
  setup() {
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      type: undefined,
      dateRange: []
    });

    // 通知表单
    const notificationForm = reactive({
      id: '',
      title: '',
      content: '',
      type: 'system',
      priority: 'medium',
      targetType: 'all',
      targetIds: [],
      sendMethod: ['app'],
      scheduledTime: null,
      attachments: []
    });

    // 文件列表
    const fileList = ref([]);

    // 表单引用
    const notificationFormRef = ref(null);

    // 状态变量
    const loading = ref(false);
    const notificationModalVisible = ref(false);
    const detailModalVisible = ref(false);
    const isEdit = ref(false);
    const currentNotification = reactive({
      id: '',
      title: '',
      content: '',
      type: '',
      priority: '',
      targetType: '',
      targetIds: [],
      sendMethod: [],
      sendTime: '',
      status: '',
      readCount: 0,
      totalCount: 0,
      readRate: 0,
      attachments: []
    });
    const targetInfoData = ref([]);
    const readStatsData = ref([]);

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

    // 通知类型选项
    const notificationTypeOptions = [
      { label: '系统通知', value: 'system' },
      { label: '考试通知', value: 'exam' },
      { label: '成绩通知', value: 'score' },
      { label: '活动通知', value: 'activity' },
      { label: '学习资料', value: 'learning' }
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

    // 年级选项
    const gradeOptions = [
      { label: '高一', value: 'grade-10' },
      { label: '高二', value: 'grade-11' },
      { label: '高三', value: 'grade-12' }
    ];

    // 统计数据
    const stats = reactive({
      totalNotifications: 0,
      todayNotifications: 0,
      readCount: 0,
      readRate: 0
    });

    // 表格列定义
    const columns = [
      {
        title: 'ID',
        dataIndex: 'id',
        width: 80
      },
      {
        title: '通知标题',
        dataIndex: 'title',
        ellipsis: true
      },
      {
        title: '通知类型',
        slotName: 'type'
      },
      {
        title: '优先级',
        slotName: 'priority'
      },
      {
        title: '接收对象',
        dataIndex: 'targetType',
        render: ({ record }) => {
          return getTargetTypeText(record.targetType);
        }
      },
      {
        title: '发送时间',
        dataIndex: 'sendTime'
      },
      {
        title: '状态',
        slotName: 'status'
      },
      {
        title: '阅读率',
        slotName: 'readRate'
      },
      {
        title: '操作',
        slotName: 'operations',
        fixed: 'right',
        width: 200
      }
    ];

    // 通知表单校验规则
    const notificationFormRules = {
      title: [
        { required: true, message: '请输入通知标题' }
      ],
      content: [
        { required: true, message: '请输入通知内容' }
      ],
      type: [
        { required: true, message: '请选择通知类型' }
      ],
      priority: [
        { required: true, message: '请选择优先级' }
      ],
      targetType: [
        { required: true, message: '请选择接收对象' }
      ],
      targetIds: [
        { 
          required: true, 
          message: '请选择接收对象',
          validator: (value, cb) => {
            if (notificationForm.targetType !== 'all' && (!value || value.length === 0)) {
              return cb('请选择接收对象');
            }
            return cb();
          }
        }
      ],
      sendMethod: [
        { required: true, message: '请选择发送方式' }
      ]
    };

    // 模拟通知数据
    const notificationData = ref([]);

    // 生命周期钩子
    onMounted(() => {
      fetchNotificationData();
    });

    // 获取通知数据
    const fetchNotificationData = () => {
      loading.value = true;
      
      // 模拟API请求
      setTimeout(() => {
        // 生成模拟数据
        const mockData = generateMockNotificationData();
        notificationData.value = mockData.list;
        pagination.total = mockData.total;
        
        // 更新统计数据
        updateStats(mockData);
        
        loading.value = false;
      }, 800);
    };

    // 更新统计数据
    const updateStats = (data) => {
      stats.totalNotifications = data.total;
      stats.todayNotifications = data.todayCount;
      stats.readCount = data.readCount;
      stats.readRate = data.readRate;
    };

    // 生成模拟通知数据
    const generateMockNotificationData = () => {
      const titles = [
        '关于期中考试安排的通知',
        '最新学习资料已上传',
        '系统维护公告',
        '成绩单已生成，请查看',
        '关于举办学科竞赛的通知',
        '寒假作业安排',
        '家长会通知',
        '关于调整作息时间的通知',
        '新功能上线公告'
      ];
      
      const contents = [
        '本学期期中考试将于下周一开始，请各位同学做好准备。考试科目包括语文、数学、英语、物理、化学。请携带必要的文具，不要迟到。',
        '最新的学习资料已上传到系统，包括各科复习资料和模拟试题，请同学们及时查看和下载。',
        '系统将于本周六晚上22:00-24:00进行维护升级，期间系统将无法访问，请提前做好准备。',
        '本次月考成绩已公布，请登录系统查看详细成绩单和分析报告。如有疑问，请联系班主任。',
        '学校将于下月举办学科竞赛，有意参加的同学请向班主任报名。竞赛科目包括数学、物理、化学、生物。',
        '寒假作业已安排，请同学们在假期认真完成。开学后将进行检查和评比。',
        '本学期家长会将于本周五晚上7点在学校礼堂举行，请通知家长准时参加。',
        '根据上级通知，从下周开始，学校作息时间将做如下调整：早自习提前至7:30，晚自习延长至21:00。',
        '系统新增了错题本和学习计划功能，欢迎使用并提供反馈。'
      ];
      
      const types = ['system', 'exam', 'score', 'activity', 'learning'];
      const priorities = ['low', 'medium', 'high'];
      const targetTypes = ['all', 'student', 'class', 'grade'];
      const statuses = ['sent', 'scheduled', 'failed'];
      const sendMethods = [['app'], ['app', 'email'], ['app', 'sms'], ['app', 'email', 'sms']];
      
      const mockList = [];
      const totalItems = 120;
      let totalReadCount = 0;
      let todayCount = 0;
      
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      for (let i = 1; i <= totalItems; i++) {
        const titleIndex = Math.floor(Math.random() * titles.length);
        const title = titles[titleIndex];
        const content = contents[titleIndex];
        const type = types[Math.floor(Math.random() * types.length)];
        const priority = priorities[Math.floor(Math.random() * priorities.length)];
        const targetType = targetTypes[Math.floor(Math.random() * targetTypes.length)];
        
        // 生成目标ID
        let targetIds = [];
        if (targetType === 'student') {
          const count = Math.floor(Math.random() * 3) + 1;
          for (let j = 0; j < count; j++) {
            const id = studentOptions[Math.floor(Math.random() * studentOptions.length)].value;
            if (!targetIds.includes(id)) {
              targetIds.push(id);
            }
          }
        } else if (targetType === 'class') {
          const count = Math.floor(Math.random() * 2) + 1;
          for (let j = 0; j < count; j++) {
            const id = classOptions[Math.floor(Math.random() * classOptions.length)].value;
            if (!targetIds.includes(id)) {
              targetIds.push(id);
            }
          }
        } else if (targetType === 'grade') {
          const count = Math.floor(Math.random() * 2) + 1;
          for (let j = 0; j < count; j++) {
            const id = gradeOptions[Math.floor(Math.random() * gradeOptions.length)].value;
            if (!targetIds.includes(id)) {
              targetIds.push(id);
            }
          }
        }
        
        // 生成发送时间（最近30天内）
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(Math.random() * 30));
        const sendTime = date.toISOString().split('T')[0] + ' ' + 
                        String(Math.floor(Math.random() * 24)).padStart(2, '0') + ':' +
                        String(Math.floor(Math.random() * 60)).padStart(2, '0') + ':' +
                        String(Math.floor(Math.random() * 60)).padStart(2, '0');
        
        // 检查是否是今天发送的
        if (date.getTime() >= today.getTime()) {
          todayCount++;
        }
        
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        const method = sendMethods[Math.floor(Math.random() * sendMethods.length)];
        
        // 生成阅读统计
        const totalCount = targetType === 'all' ? 120 : (targetIds.length * (targetType === 'grade' ? 30 : (targetType === 'class' ? 40 : 1)));
        const readCount = Math.floor(totalCount * (Math.random() * 0.5 + 0.5));
        const readRate = Math.floor((readCount / totalCount) * 100);
        
        totalReadCount += readCount;
        
        // 生成附件
        const attachments = [];
        if (Math.random() > 0.7) {
          const attachmentCount = Math.floor(Math.random() * 3) + 1;
          for (let j = 0; j < attachmentCount; j++) {
            attachments.push({
              name: `附件${j + 1}.${['pdf', 'docx', 'xlsx'][Math.floor(Math.random() * 3)]}`,
              url: '#'
            });
          }
        }
        
        const notificationRecord = {
          id: `notification-${i.toString().padStart(3, '0')}`,
          title,
          content,
          type,
          priority,
          targetType,
          targetIds,
          sendMethod: method,
          sendTime,
          status,
          readCount,
          totalCount,
          readRate,
          attachments
        };
        
        // 应用筛选条件
        let match = true;
        
        if (searchForm.keyword) {
          const keyword = searchForm.keyword.toLowerCase();
          const titleMatch = notificationRecord.title.toLowerCase().includes(keyword);
          const contentMatch = notificationRecord.content.toLowerCase().includes(keyword);
          
          if (!titleMatch && !contentMatch) {
            match = false;
          }
        }
        
        if (searchForm.type && notificationRecord.type !== searchForm.type) {
          match = false;
        }
        
        if (searchForm.dateRange && searchForm.dateRange.length === 2) {
          const startDate = new Date(searchForm.dateRange[0]);
          const endDate = new Date(searchForm.dateRange[1]);
          const notificationDate = new Date(notificationRecord.sendTime);
          
          if (notificationDate < startDate || notificationDate > endDate) {
            match = false;
          }
        }
        
        if (match) {
          mockList.push(notificationRecord);
        }
      }
      
      // 分页
      const startIndex = (pagination.current - 1) * pagination.pageSize;
      const endIndex = startIndex + pagination.pageSize;
      const paginatedList = mockList.slice(startIndex, endIndex);
      
      return {
        list: paginatedList,
        total: mockList.length,
        todayCount,
        readCount: totalReadCount,
        readRate: Math.floor((totalReadCount / (totalItems * 50)) * 100)
      };
    };

    // 获取通知类型文本
    const getTypeText = (type) => {
      switch (type) {
        case 'system':
          return '系统通知';
        case 'exam':
          return '考试通知';
        case 'score':
          return '成绩通知';
        case 'activity':
          return '活动通知';
        case 'learning':
          return '学习资料';
        default:
          return '未知';
      }
    };

    // 获取通知类型颜色
    const getTypeColor = (type) => {
      switch (type) {
        case 'system':
          return 'blue';
        case 'exam':
          return 'orange';
        case 'score':
          return 'green';
        case 'activity':
          return 'purple';
        case 'learning':
          return 'cyan';
        default:
          return 'gray';
      }
    };

    // 获取优先级文本
    const getPriorityText = (priority) => {
      switch (priority) {
        case 'low':
          return '低';
        case 'medium':
          return '中';
        case 'high':
          return '高';
        default:
          return '未知';
      }
    };

    // 获取优先级颜色
    const getPriorityColor = (priority) => {
      switch (priority) {
        case 'low':
          return 'blue';
        case 'medium':
          return 'orange';
        case 'high':
          return 'red';
        default:
          return 'gray';
      }
    };

    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'sent':
          return '已发送';
        case 'scheduled':
          return '定时发送';
        case 'failed':
          return '发送失败';
        default:
          return '未知';
      }
    };

    // 获取状态颜色
    const getStatusColor = (status) => {
      switch (status) {
        case 'sent':
          return 'green';
        case 'scheduled':
          return 'blue';
        case 'failed':
          return 'red';
        default:
          return 'gray';
      }
    };

    // 获取目标类型文本
    const getTargetTypeText = (targetType) => {
      switch (targetType) {
        case 'all':
          return '所有用户';
        case 'student':
          return '指定学生';
        case 'class':
          return '指定班级';
        case 'grade':
          return '指定年级';
        default:
          return '未知';
      }
    };

    // 获取发送方式文本
    const getSendMethodText = (method) => {
      switch (method) {
        case 'app':
          return '应用内通知';
        case 'email':
          return '电子邮件';
        case 'sms':
          return '短信';
        default:
          return '未知';
      }
    };

    // 获取进度条颜色
    const getProgressColor = (percent) => {
      if (percent >= 80) return '#00B42A';
      if (percent >= 60) return '#0FC6C2';
      if (percent >= 40) return '#165DFF';
      if (percent >= 20) return '#FF7D00';
      return '#F53F3F';
    };

    // 获取推荐对象选项
    const getTargetOptions = () => {
      switch (notificationForm.targetType) {
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
      fetchNotificationData();
    };

    // 重置搜索
    const resetSearch = () => {
      searchForm.keyword = '';
      searchForm.type = undefined;
      searchForm.dateRange = [];
      pagination.current = 1;
      fetchNotificationData();
    };

    // 处理分页变化
    const onPageChange = (page) => {
      pagination.current = page;
      fetchNotificationData();
    };

    // 处理每页条数变化
    const onPageSizeChange = (pageSize) => {
      pagination.pageSize = pageSize;
      pagination.current = 1;
      fetchNotificationData();
    };

    // 打开添加通知弹窗
    const openAddNotificationModal = () => {
      isEdit.value = false;
      resetNotificationForm();
      notificationModalVisible.value = true;
    };

    // 处理查看详情
    const handleViewDetail = (record) => {
      // 填充当前通知数据
      Object.assign(currentNotification, record);
      
      // 准备目标信息数据
      let targetInfo = '';
      if (record.targetType === 'all') {
        targetInfo = '所有用户';
      } else {
        const targetOptions = record.targetType === 'student' ? studentOptions : 
                             (record.targetType === 'class' ? classOptions : gradeOptions);
        
        const targetNames = record.targetIds.map(id => {
          const target = targetOptions.find(item => item.value === id);
          return target ? target.label : id;
        }).join(', ');
        
        targetInfo = `${getTargetTypeText(record.targetType)}: ${targetNames}`;
      }
      
      targetInfoData.value = [
        {
          label: '接收对象',
          value: targetInfo
        },
        {
          label: '接收人数',
          value: record.totalCount
        }
      ];
      
      // 准备阅读统计数据
      readStatsData.value = [
        {
          label: '已读人数',
          value: record.readCount
        },
        {
          label: '总接收人数',
          value: record.totalCount
        },
        {
          label: '阅读率',
          value: `${record.readRate}%`
        }
      ];
      
      detailModalVisible.value = true;
    };

    // 处理重新发送
    const handleResend = (record) => {
      Message.success(`通知"${record.title}"已重新发送`);
    };

    // 处理删除
    const handleDelete = (record) => {
      Message.success(`已删除通知：${record.title}`);
      
      // 在实际应用中，这里应该调用API来删除通知
      // 然后重新获取通知列表
      
      // 模拟删除
      const index = notificationData.value.findIndex(item => item.id === record.id);
      if (index !== -1) {
        notificationData.value.splice(index, 1);
      }
    };

    // 处理批量删除
    const handleBatchDelete = () => {
      if (selectedRowKeys.value.length === 0) {
        Message.warning('请先选择要删除的通知');
        return;
      }
      
      Message.success(`已删除 ${selectedRowKeys.value.length} 条通知`);
      selectedRowKeys.value = [];
      fetchNotificationData();
    };

    // 处理重新发送当前通知
    const handleResendCurrent = () => {
      handleResend(currentNotification);
      closeDetailModal();
    };

    // 处理删除当前通知
    const handleDeleteCurrent = () => {
      handleDelete(currentNotification);
      closeDetailModal();
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
        
        fileList.value.push({ name: file.name, url });
        notificationForm.attachments.push({ name: file.name, url });
        
        onSuccess();
      }, 500);
    };

    // 提交通知表单
    const handleSubmitNotification = async (done) => {
      try {
        await notificationFormRef.value.validate();
        
        if (notificationForm.scheduledTime) {
          Message.success(`通知"${notificationForm.title}"已设置为定时发送`);
        } else {
          Message.success(`通知"${notificationForm.title}"发送成功`);
        }
        
        // 在实际应用中，这里应该调用API来发送通知
        // 然后重新获取通知列表
        
        closeNotificationModal();
        fetchNotificationData();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 关闭通知弹窗
    const closeNotificationModal = () => {
      notificationModalVisible.value = false;
      resetNotificationForm();
      fileList.value = [];
    };

    // 关闭详情弹窗
    const closeDetailModal = () => {
      detailModalVisible.value = false;
    };

    // 重置通知表单
    const resetNotificationForm = () => {
      notificationForm.id = '';
      notificationForm.title = '';
      notificationForm.content = '';
      notificationForm.type = 'system';
      notificationForm.priority = 'medium';
      notificationForm.targetType = 'all';
      notificationForm.targetIds = [];
      notificationForm.sendMethod = ['app'];
      notificationForm.scheduledTime = null;
      notificationForm.attachments = [];
    };

    return {
      searchForm,
      notificationForm,
      fileList,
      notificationFormRef,
      loading,
      notificationModalVisible,
      detailModalVisible,
      isEdit,
      currentNotification,
      targetInfoData,
      readStatsData,
      pagination,
      selectedRowKeys,
      rowSelection,
      notificationTypeOptions,
      stats,
      columns,
      notificationFormRules,
      notificationData,
      getTypeText,
      getTypeColor,
      getPriorityText,
      getPriorityColor,
      getStatusText,
      getStatusColor,
      getTargetTypeText,
      getSendMethodText,
      getProgressColor,
      getTargetOptions,
      handleSearch,
      resetSearch,
      onPageChange,
      onPageSizeChange,
      openAddNotificationModal,
      handleViewDetail,
      handleResend,
      handleDelete,
      handleBatchDelete,
      handleResendCurrent,
      handleDeleteCurrent,
      customUploadRequest,
      handleSubmitNotification,
      closeNotificationModal,
      closeDetailModal
    };
  }
};
</script>

<style scoped>
.notification-management-container {
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

.notification-detail {
  padding: 0 16px;
}

.notification-header {
  text-align: center;
  margin-bottom: 24px;
}

.notification-meta {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 8px;
}

.notification-section {
  margin-bottom: 24px;
}

.notification-content {
  white-space: pre-line;
  line-height: 1.6;
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
}

.notification-attachments,
.notification-methods {
  margin-top: 8px;
}

@media (max-width: 768px) {
  .search-card .arco-col {
    margin-bottom: 16px;
  }
  
  .stats-row .arco-col {
    margin-bottom: 16px;
  }
  
  .notification-meta {
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
}
</style>
