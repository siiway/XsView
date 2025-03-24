<!-- 后台管理系统诊断报告管理页面 -->
<!-- frontend/scorex-admin/src/views/diagnostic/DiagnosticManagement.vue -->

<template>
  <div class="diagnostic-management-container">
    <!-- 搜索和操作栏 -->
    <a-card class="search-card">
      <a-row :gutter="16">
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-input
            v-model="searchForm.keyword"
            placeholder="搜索学生姓名/学号"
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.examId"
            placeholder="选择考试"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="exam in examOptions" :key="exam.value" :value="exam.value">
              {{ exam.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-range-picker
            v-model="searchForm.dateRange"
            style="width: 100%"
            placeholder="生成日期范围"
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
              <icon-file style="color: rgb(var(--primary-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalReports }}</div>
              <div class="stat-label">诊断报告总数</div>
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
              <div class="stat-value">{{ stats.todayReports }}</div>
              <div class="stat-label">今日生成报告</div>
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
              <div class="stat-value">{{ stats.studentsWithReports }}</div>
              <div class="stat-label">已生成报告学生数</div>
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
              <div class="stat-value">{{ stats.viewCount }}</div>
              <div class="stat-label">报告查看次数</div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 诊断报告列表 -->
    <a-card class="table-card">
      <template #title>
        诊断报告列表
      </template>
      <template #extra>
        <a-space>
          <a-button type="primary" @click="handleBatchGenerate">
            <template #icon>
              <icon-plus />
            </template>
            批量生成报告
          </a-button>
          <a-button @click="handleBatchExport">
            <template #icon>
              <icon-download />
            </template>
            批量导出
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
        :data="reportData"
        :pagination="pagination"
        :row-selection="rowSelection"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        row-key="id"
      >
        <template #status="{ record }">
          <a-tag :color="getStatusColor(record.status)">
            {{ getStatusText(record.status) }}
          </a-tag>
        </template>
        
        <template #operations="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleViewReport(record)">
              查看
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleSendReport(record)">
              发送
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleRegenerateReport(record)">
              重新生成
            </a-button>
            <a-divider direction="vertical" />
            <a-popconfirm
              content="确定要删除此诊断报告吗？"
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

    <!-- 批量生成报告弹窗 -->
    <a-modal
      v-model:visible="batchGenerateModalVisible"
      title="批量生成诊断报告"
      @cancel="closeBatchGenerateModal"
      @before-ok="handleConfirmBatchGenerate"
    >
      <a-form :model="batchGenerateForm" ref="batchGenerateFormRef" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="examId" label="选择考试" required>
          <a-select
            v-model="batchGenerateForm.examId"
            placeholder="请选择考试"
            allow-clear
          >
            <a-option v-for="exam in examOptions" :key="exam.value" :value="exam.value">
              {{ exam.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="classIds" label="选择班级" required>
          <a-select
            v-model="batchGenerateForm.classIds"
            placeholder="请选择班级"
            allow-clear
            multiple
          >
            <a-option v-for="cls in classOptions" :key="cls.value" :value="cls.value">
              {{ cls.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="templateId" label="报告模板" required>
          <a-select
            v-model="batchGenerateForm.templateId"
            placeholder="请选择报告模板"
            allow-clear
          >
            <a-option v-for="template in templateOptions" :key="template.value" :value="template.value">
              {{ template.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="includeRecommendations" label="包含学习建议">
          <a-switch v-model="batchGenerateForm.includeRecommendations" />
        </a-form-item>
        <a-form-item field="notifyStudents" label="通知学生">
          <a-switch v-model="batchGenerateForm.notifyStudents" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 发送报告弹窗 -->
    <a-modal
      v-model:visible="sendReportModalVisible"
      title="发送诊断报告"
      @cancel="closeSendReportModal"
      @before-ok="handleConfirmSendReport"
    >
      <a-form :model="sendReportForm" ref="sendReportFormRef" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="recipients" label="接收人" required>
          <a-input v-model="sendReportForm.recipients" placeholder="请输入接收人" disabled />
        </a-form-item>
        <a-form-item field="sendToParents" label="同时发送给家长">
          <a-switch v-model="sendReportForm.sendToParents" />
        </a-form-item>
        <a-form-item field="sendMethod" label="发送方式" required>
          <a-radio-group v-model="sendReportForm.sendMethod">
            <a-radio value="app">应用内通知</a-radio>
            <a-radio value="email">电子邮件</a-radio>
            <a-radio value="sms">短信</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item field="message" label="附加消息">
          <a-textarea v-model="sendReportForm.message" placeholder="请输入附加消息" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 查看报告弹窗 -->
    <a-modal
      v-model:visible="viewReportModalVisible"
      title="诊断报告详情"
      @cancel="closeViewReportModal"
      width="800px"
    >
      <div class="report-preview">
        <div class="report-header">
          <h2>{{ currentReport.title }}</h2>
          <div class="report-meta">
            <span>学生: {{ currentReport.studentName }}</span>
            <span>班级: {{ currentReport.className }}</span>
            <span>生成日期: {{ currentReport.createdAt }}</span>
          </div>
        </div>
        
        <a-divider />
        
        <div class="report-section">
          <h3>考试概况</h3>
          <a-descriptions :data="examInfoData" layout="inline-vertical" bordered />
        </div>
        
        <div class="report-section">
          <h3>成绩分析</h3>
          <div class="score-analysis">
            <div class="score-item">
              <div class="score-label">总分</div>
              <div class="score-value">{{ currentReport.score }}</div>
              <div class="score-max">满分: {{ currentReport.totalScore }}</div>
            </div>
            <div class="score-item">
              <div class="score-label">排名</div>
              <div class="score-value">{{ currentReport.rank }}</div>
              <div class="score-max">总人数: {{ currentReport.totalStudents }}</div>
            </div>
            <div class="score-item">
              <div class="score-label">得分率</div>
              <div class="score-value">{{ ((currentReport.score / currentReport.totalScore) * 100).toFixed(1) }}%</div>
            </div>
          </div>
        </div>
        
        <div class="report-section">
          <h3>知识点掌握情况</h3>
          <div ref="knowledgeRadarChart" class="chart-container"></div>
        </div>
        
        <div class="report-section">
          <h3>题型得分分析</h3>
          <div ref="questionTypeChart" class="chart-container"></div>
        </div>
        
        <div class="report-section">
          <h3>学习建议</h3>
          <div class="recommendations">
            <a-collapse accordion>
              <a-collapse-item v-for="(rec, index) in currentReport.recommendations" :key="index" :header="rec.title">
                <p>{{ rec.content }}</p>
                <div v-if="rec.resources && rec.resources.length > 0" class="resources">
                  <h4>推荐资源:</h4>
                  <ul>
                    <li v-for="(resource, rIndex) in rec.resources" :key="rIndex">
                      <a-link>{{ resource.title }}</a-link>
                    </li>
                  </ul>
                </div>
              </a-collapse-item>
            </a-collapse>
          </div>
        </div>
      </div>
      
      <template #footer>
        <a-space>
          <a-button type="primary" @click="handleExportCurrentReport">
            导出报告
          </a-button>
          <a-button @click="handleSendCurrentReport">
            发送报告
          </a-button>
        </a-space>
      </template>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue';
import { Message } from '@arco-design/web-vue';
import * as echarts from 'echarts/core';
import { BarChart, RadarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// 注册 ECharts 组件
echarts.use([
  BarChart,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CanvasRenderer
]);

export default {
  setup() {
    // 图表引用
    const knowledgeRadarChart = ref(null);
    const questionTypeChart = ref(null);
    
    // 图表实例
    let knowledgeRadarInstance = null;
    let questionTypeInstance = null;
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      examId: undefined,
      dateRange: []
    });

    // 批量生成表单
    const batchGenerateForm = reactive({
      examId: undefined,
      classIds: [],
      templateId: undefined,
      includeRecommendations: true,
      notifyStudents: false
    });

    // 发送报告表单
    const sendReportForm = reactive({
      reportId: '',
      recipients: '',
      sendToParents: false,
      sendMethod: 'app',
      message: ''
    });

    // 表单引用
    const batchGenerateFormRef = ref(null);
    const sendReportFormRef = ref(null);

    // 状态变量
    const loading = ref(false);
    const batchGenerateModalVisible = ref(false);
    const sendReportModalVisible = ref(false);
    const viewReportModalVisible = ref(false);
    const currentReport = reactive({
      id: '',
      title: '',
      studentId: '',
      studentName: '',
      className: '',
      examId: '',
      examName: '',
      score: 0,
      totalScore: 0,
      rank: 0,
      totalStudents: 0,
      createdAt: '',
      status: '',
      recommendations: []
    });
    const examInfoData = ref([]);

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

    // 考试选项
    const examOptions = [
      { label: '高二数学期中考试', value: 'exam-001' },
      { label: '高二英语期中考试', value: 'exam-002' },
      { label: '高二物理期中考试', value: 'exam-003' },
      { label: '高二化学期中考试', value: 'exam-004' }
    ];

    // 班级选项
    const classOptions = [
      { label: '高二(1)班', value: 'class-001' },
      { label: '高二(2)班', value: 'class-002' },
      { label: '高二(3)班', value: 'class-003' },
      { label: '高二(4)班', value: 'class-004' }
    ];

    // 模板选项
    const templateOptions = [
      { label: '标准诊断报告', value: 'template-001' },
      { label: '简洁诊断报告', value: 'template-002' },
      { label: '详细诊断报告', value: 'template-003' }
    ];

    // 统计数据
    const stats = reactive({
      totalReports: 0,
      todayReports: 0,
      studentsWithReports: 0,
      viewCount: 0
    });

    // 表格列定义
    const columns = [
      {
        title: '报告ID',
        dataIndex: 'id',
        width: 100
      },
      {
        title: '报告标题',
        dataIndex: 'title',
        ellipsis: true
      },
      {
        title: '学生姓名',
        dataIndex: 'studentName'
      },
      {
        title: '班级',
        dataIndex: 'className'
      },
      {
        title: '考试名称',
        dataIndex: 'examName',
        ellipsis: true
      },
      {
        title: '分数',
        dataIndex: 'score',
        render: ({ record }) => {
          return `${record.score}/${record.totalScore}`;
        }
      },
      {
        title: '排名',
        dataIndex: 'rank',
        render: ({ record }) => {
          return `${record.rank}/${record.totalStudents}`;
        }
      },
      {
        title: '生成日期',
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

    // 模拟报告数据
    const reportData = ref([]);

    // 生命周期钩子
    onMounted(() => {
      fetchReportData();
    });

    // 获取报告数据
    const fetchReportData = () => {
      loading.value = true;
      
      // 模拟API请求
      setTimeout(() => {
        // 生成模拟数据
        const mockData = generateMockReportData();
        reportData.value = mockData.list;
        pagination.total = mockData.total;
        
        // 更新统计数据
        updateStats(mockData.total);
        
        loading.value = false;
      }, 800);
    };

    // 更新统计数据
    const updateStats = (total) => {
      stats.totalReports = total;
      stats.todayReports = Math.floor(total * 0.1);
      stats.studentsWithReports = Math.floor(total * 0.8);
      stats.viewCount = Math.floor(total * 3.5);
    };

    // 生成模拟报告数据
    const generateMockReportData = () => {
      const names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑十一', '王十二'];
      const classes = ['高二(1)班', '高二(2)班', '高二(3)班', '高二(4)班'];
      const exams = ['高二数学期中考试', '高二英语期中考试', '高二物理期中考试', '高二化学期中考试'];
      const examIds = ['exam-001', 'exam-002', 'exam-003', 'exam-004'];
      const statuses = ['published', 'draft', 'sent'];
      
      const mockList = [];
      const totalItems = 120;
      
      for (let i = 1; i <= totalItems; i++) {
        const studentId = `S${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
        const studentName = names[Math.floor(Math.random() * names.length)] + i;
        const className = classes[Math.floor(Math.random() * classes.length)];
        const examIndex = Math.floor(Math.random() * exams.length);
        const examName = exams[examIndex];
        const examId = examIds[examIndex];
        
        // 生成随机分数
        const totalScore = 150;
        const score = Math.floor(Math.random() * totalScore);
        const totalStudents = 120;
        const rank = Math.floor(Math.random() * totalStudents) + 1;
        
        // 生成随机日期（最近30天内）
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(Math.random() * 30));
        const createdAt = date.toISOString().split('T')[0];
        
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        
        const reportRecord = {
          id: `report-${i.toString().padStart(3, '0')}`,
          title: `${examName}诊断报告`,
          studentId,
          studentName,
          className,
          examId,
          examName,
          score,
          totalScore,
          rank,
          totalStudents,
          createdAt,
          status,
          recommendations: generateMockRecommendations()
        };
        
        // 应用筛选条件
        let match = true;
        
        if (searchForm.keyword) {
          const keyword = searchForm.keyword.toLowerCase();
          const nameMatch = reportRecord.studentName.toLowerCase().includes(keyword);
          const idMatch = reportRecord.studentId.toLowerCase().includes(keyword);
          
          if (!nameMatch && !idMatch) {
            match = false;
          }
        }
        
        if (searchForm.examId && reportRecord.examId !== searchForm.examId) {
          match = false;
        }
        
        if (searchForm.dateRange && searchForm.dateRange.length === 2) {
          const startDate = new Date(searchForm.dateRange[0]);
          const endDate = new Date(searchForm.dateRange[1]);
          const reportDate = new Date(reportRecord.createdAt);
          
          if (reportDate < startDate || reportDate > endDate) {
            match = false;
          }
        }
        
        if (match) {
          mockList.push(reportRecord);
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

    // 生成模拟学习建议
    const generateMockRecommendations = () => {
      const recommendations = [
        {
          title: '函数知识点加强',
          content: '建议加强对函数概念和性质的理解，特别是对函数图像的分析和变换。可以通过多做相关练习题来提高解题能力。',
          resources: [
            { title: '函数图像变换专项练习', url: '#' },
            { title: '高中数学函数知识点总结', url: '#' }
          ]
        },
        {
          title: '三角函数计算提升',
          content: '三角函数的计算和应用是你的薄弱环节，建议重点复习三角函数的基本公式和恒等变换，提高计算准确性。',
          resources: [
            { title: '三角函数公式速记卡片', url: '#' },
            { title: '三角函数计算技巧视频课程', url: '#' }
          ]
        },
        {
          title: '概率统计应用能力培养',
          content: '在概率统计部分，你对基本概念掌握较好，但在实际应用题中存在困难。建议多做一些实际应用题，提高分析和解决问题的能力。',
          resources: [
            { title: '概率统计应用题精选100题', url: '#' },
            { title: '概率统计解题思路分析', url: '#' }
          ]
        }
      ];
      
      // 随机选择1-3个建议
      const count = Math.floor(Math.random() * 3) + 1;
      const shuffled = [...recommendations].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    };

    // 初始化知识点雷达图
    const initKnowledgeRadarChart = () => {
      if (!knowledgeRadarChart.value) return;
      
      knowledgeRadarInstance = echarts.init(knowledgeRadarChart.value);
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        radar: {
          indicator: [
            { name: '函数', max: 100 },
            { name: '导数', max: 100 },
            { name: '三角函数', max: 100 },
            { name: '概率统计', max: 100 },
            { name: '立体几何', max: 100 }
          ],
          radius: 130
        },
        series: [
          {
            type: 'radar',
            data: [
              {
                value: [85, 65, 70, 90, 75],
                name: '知识点掌握度',
                areaStyle: {
                  color: 'rgba(22, 93, 255, 0.3)'
                },
                lineStyle: {
                  color: '#165DFF'
                },
                itemStyle: {
                  color: '#165DFF'
                }
              },
              {
                value: [80, 70, 75, 85, 80],
                name: '班级平均',
                areaStyle: {
                  color: 'rgba(255, 171, 0, 0.3)'
                },
                lineStyle: {
                  color: '#FFAB00',
                  type: 'dashed'
                },
                itemStyle: {
                  color: '#FFAB00'
                }
              }
            ]
          }
        ]
      };
      
      knowledgeRadarInstance.setOption(option);
    };

    // 初始化题型得分图
    const initQuestionTypeChart = () => {
      if (!questionTypeChart.value) return;
      
      questionTypeInstance = echarts.init(questionTypeChart.value);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['得分率', '班级平均']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['选择题', '填空题', '解答题']
        },
        yAxis: {
          type: 'value',
          name: '得分率(%)',
          max: 100
        },
        series: [
          {
            name: '得分率',
            type: 'bar',
            data: [85, 70, 60],
            itemStyle: {
              color: '#165DFF'
            }
          },
          {
            name: '班级平均',
            type: 'bar',
            data: [75, 65, 55],
            itemStyle: {
              color: '#FFAB00'
            }
          }
        ]
      };
      
      questionTypeInstance.setOption(option);
    };

    // 处理搜索
    const handleSearch = () => {
      pagination.current = 1;
      fetchReportData();
    };

    // 重置搜索
    const resetSearch = () => {
      searchForm.keyword = '';
      searchForm.examId = undefined;
      searchForm.dateRange = [];
      pagination.current = 1;
      fetchReportData();
    };

    // 处理分页变化
    const onPageChange = (page) => {
      pagination.current = page;
      fetchReportData();
    };

    // 处理每页条数变化
    const onPageSizeChange = (pageSize) => {
      pagination.pageSize = pageSize;
      pagination.current = 1;
      fetchReportData();
    };

    // 处理批量生成报告
    const handleBatchGenerate = () => {
      batchGenerateForm.examId = undefined;
      batchGenerateForm.classIds = [];
      batchGenerateForm.templateId = 'template-001';
      batchGenerateForm.includeRecommendations = true;
      batchGenerateForm.notifyStudents = false;
      
      batchGenerateModalVisible.value = true;
    };

    // 处理批量导出
    const handleBatchExport = () => {
      if (selectedRowKeys.value.length === 0) {
        Message.warning('请先选择要导出的诊断报告');
        return;
      }
      
      Message.success(`已导出 ${selectedRowKeys.value.length} 份诊断报告`);
    };

    // 处理批量删除
    const handleBatchDelete = () => {
      if (selectedRowKeys.value.length === 0) {
        Message.warning('请先选择要删除的诊断报告');
        return;
      }
      
      Message.success(`已删除 ${selectedRowKeys.value.length} 份诊断报告`);
      selectedRowKeys.value = [];
      fetchReportData();
    };

    // 处理查看报告
    const handleViewReport = (record) => {
      // 填充当前报告数据
      Object.assign(currentReport, record);
      
      // 准备考试信息数据
      examInfoData.value = [
        {
          label: '考试名称',
          value: record.examName
        },
        {
          label: '考试日期',
          value: '2025-03-15'
        },
        {
          label: '总分',
          value: record.totalScore
        },
        {
          label: '参考人数',
          value: record.totalStudents
        }
      ];
      
      viewReportModalVisible.value = true;
      
      nextTick(() => {
        initKnowledgeRadarChart();
        initQuestionTypeChart();
      });
    };

    // 处理发送报告
    const handleSendReport = (record) => {
      sendReportForm.reportId = record.id;
      sendReportForm.recipients = record.studentName;
      sendReportForm.sendToParents = false;
      sendReportForm.sendMethod = 'app';
      sendReportForm.message = `亲爱的${record.studentName}同学，您的${record.examName}诊断报告已生成，请查收。`;
      
      sendReportModalVisible.value = true;
    };

    // 处理重新生成报告
    const handleRegenerateReport = (record) => {
      Message.success(`已重新生成学生 ${record.studentName} 的诊断报告`);
    };

    // 处理删除报告
    const handleDelete = (record) => {
      Message.success(`已删除学生 ${record.studentName} 的诊断报告`);
      
      // 在实际应用中，这里应该调用API来删除报告
      // 然后重新获取报告列表
      
      // 模拟删除
      const index = reportData.value.findIndex(item => item.id === record.id);
      if (index !== -1) {
        reportData.value.splice(index, 1);
      }
    };

    // 确认批量生成报告
    const handleConfirmBatchGenerate = async (done) => {
      try {
        await batchGenerateFormRef.value.validate();
        
        Message.success('诊断报告生成任务已提交，请稍后查看结果');
        
        // 在实际应用中，这里应该调用API来批量生成报告
        // 然后重新获取报告列表
        
        closeBatchGenerateModal();
        fetchReportData();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 确认发送报告
    const handleConfirmSendReport = async (done) => {
      try {
        await sendReportFormRef.value.validate();
        
        Message.success(`诊断报告已成功发送给 ${sendReportForm.recipients}`);
        
        // 在实际应用中，这里应该调用API来发送报告
        // 然后更新报告状态
        
        closeSendReportModal();
        fetchReportData();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 导出当前报告
    const handleExportCurrentReport = () => {
      Message.success(`已导出学生 ${currentReport.studentName} 的诊断报告`);
    };

    // 发送当前报告
    const handleSendCurrentReport = () => {
      handleSendReport(currentReport);
      closeViewReportModal();
    };

    // 关闭批量生成弹窗
    const closeBatchGenerateModal = () => {
      batchGenerateModalVisible.value = false;
    };

    // 关闭发送报告弹窗
    const closeSendReportModal = () => {
      sendReportModalVisible.value = false;
    };

    // 关闭查看报告弹窗
    const closeViewReportModal = () => {
      viewReportModalVisible.value = false;
      
      if (knowledgeRadarInstance) {
        knowledgeRadarInstance.dispose();
        knowledgeRadarInstance = null;
      }
      
      if (questionTypeInstance) {
        questionTypeInstance.dispose();
        questionTypeInstance = null;
      }
    };

    // 获取状态颜色
    const getStatusColor = (status) => {
      switch (status) {
        case 'published':
          return 'green';
        case 'draft':
          return 'orange';
        case 'sent':
          return 'blue';
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
        case 'sent':
          return '已发送';
        default:
          return '未知';
      }
    };

    return {
      searchForm,
      batchGenerateForm,
      sendReportForm,
      batchGenerateFormRef,
      sendReportFormRef,
      loading,
      batchGenerateModalVisible,
      sendReportModalVisible,
      viewReportModalVisible,
      currentReport,
      examInfoData,
      pagination,
      selectedRowKeys,
      rowSelection,
      examOptions,
      classOptions,
      templateOptions,
      stats,
      columns,
      reportData,
      knowledgeRadarChart,
      questionTypeChart,
      handleSearch,
      resetSearch,
      onPageChange,
      onPageSizeChange,
      handleBatchGenerate,
      handleBatchExport,
      handleBatchDelete,
      handleViewReport,
      handleSendReport,
      handleRegenerateReport,
      handleDelete,
      handleConfirmBatchGenerate,
      handleConfirmSendReport,
      handleExportCurrentReport,
      handleSendCurrentReport,
      closeBatchGenerateModal,
      closeSendReportModal,
      closeViewReportModal,
      getStatusColor,
      getStatusText
    };
  }
};
</script>

<style scoped>
.diagnostic-management-container {
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

.chart-container {
  height: 300px;
  width: 100%;
  margin: 16px 0;
}

.report-preview {
  padding: 0 16px;
}

.report-header {
  text-align: center;
  margin-bottom: 24px;
}

.report-meta {
  display: flex;
  justify-content: center;
  gap: 16px;
  color: #86909C;
}

.report-section {
  margin-bottom: 24px;
}

.score-analysis {
  display: flex;
  justify-content: space-around;
  margin: 16px 0;
}

.score-item {
  text-align: center;
}

.score-label {
  font-size: 14px;
  color: #86909C;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
  margin: 8px 0;
}

.score-max {
  font-size: 12px;
  color: #86909C;
}

.recommendations {
  margin-top: 16px;
}

.resources {
  margin-top: 8px;
}

@media (max-width: 768px) {
  .search-card .arco-col {
    margin-bottom: 16px;
  }
  
  .stats-row .arco-col {
    margin-bottom: 16px;
  }
  
  .score-analysis {
    flex-direction: column;
    gap: 16px;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>
