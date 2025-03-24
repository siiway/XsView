<!-- 后台管理系统成绩管理页面 -->
<!-- frontend/scorex-admin/src/views/score/ScoreManagement.vue -->

<template>
  <div class="score-management-container">
    <!-- 考试信息卡片 -->
    <a-card class="exam-info-card">
      <template #title>考试信息</template>
      <a-descriptions :data="examInfoData" layout="inline-vertical" bordered />
    </a-card>

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
            v-model="searchForm.class"
            placeholder="班级"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="cls in classOptions" :key="cls.value" :value="cls.value">
              {{ cls.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.scoreRange"
            placeholder="分数段"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="range in scoreRangeOptions" :key="range.value" :value="range.value">
              {{ range.label }}
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

    <!-- 成绩统计卡片 -->
    <a-card class="stats-card">
      <a-row :gutter="16">
        <a-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-item">
            <div class="stat-title">参考人数</div>
            <div class="stat-value">{{ stats.totalStudents }}</div>
          </div>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-item">
            <div class="stat-title">平均分</div>
            <div class="stat-value">{{ stats.averageScore }}</div>
          </div>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-item">
            <div class="stat-title">最高分</div>
            <div class="stat-value">{{ stats.highestScore }}</div>
          </div>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="6">
          <div class="stat-item">
            <div class="stat-title">最低分</div>
            <div class="stat-value">{{ stats.lowestScore }}</div>
          </div>
        </a-col>
      </a-row>
    </a-card>

    <!-- 成绩分布图 -->
    <a-card class="chart-card">
      <template #title>成绩分布</template>
      <div ref="scoreDistributionChart" class="chart-container"></div>
    </a-card>

    <!-- 成绩列表 -->
    <a-card class="table-card">
      <template #title>
        成绩列表
      </template>
      <template #extra>
        <a-space>
          <a-button type="primary" @click="openAddScoreModal">
            <template #icon>
              <icon-plus />
            </template>
            录入成绩
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
          <a-button type="primary" status="success" @click="handleGenerateReports">
            <template #icon>
              <icon-file />
            </template>
            生成诊断报告
          </a-button>
        </a-space>
      </template>

      <a-table
        :loading="loading"
        :columns="columns"
        :data="scoreData"
        :pagination="pagination"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        row-key="id"
      >
        <template #score="{ record }">
          <span :style="{ color: getScoreColor(record.score, examInfo.totalScore) }">
            {{ record.score }}
          </span>
        </template>
        
        <template #rank="{ record }">
          <a-tag :color="getRankColor(record.rank)">
            {{ record.rank }}
          </a-tag>
        </template>
        
        <template #operations="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleViewDetail(record)">
              详情
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleEdit(record)">
              编辑
            </a-button>
            <a-divider direction="vertical" />
            <a-popconfirm
              content="确定要删除此成绩记录吗？"
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

    <!-- 录入/编辑成绩弹窗 -->
    <a-modal
      v-model:visible="scoreModalVisible"
      :title="isEdit ? '编辑成绩' : '录入成绩'"
      @cancel="closeScoreModal"
      @before-ok="handleSubmitScore"
    >
      <a-form :model="scoreForm" ref="scoreFormRef" :rules="scoreFormRules" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="studentId" label="学号" required>
          <a-input v-model="scoreForm.studentId" placeholder="请输入学号" :disabled="isEdit" />
        </a-form-item>
        <a-form-item field="studentName" label="学生姓名" required>
          <a-input v-model="scoreForm.studentName" placeholder="请输入学生姓名" :disabled="isEdit" />
        </a-form-item>
        <a-form-item field="class" label="班级" required>
          <a-select v-model="scoreForm.class" placeholder="请选择班级" :disabled="isEdit">
            <a-option v-for="cls in classOptions" :key="cls.value" :value="cls.value">
              {{ cls.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="score" label="总分" required>
          <a-input-number v-model="scoreForm.score" placeholder="请输入总分" :min="0" :max="examInfo.totalScore" style="width: 100%" />
        </a-form-item>
        
        <a-divider>题目得分</a-divider>
        
        <div v-for="(question, index) in scoreForm.questions" :key="index" class="question-score-item">
          <a-form-item :field="`questions[${index}].score`" :label="`第${index + 1}题 (${question.points}分)`">
            <a-input-number v-model="question.score" :min="0" :max="question.points" style="width: 100%" />
          </a-form-item>
        </div>
        
        <a-form-item field="comment" label="评语">
          <a-textarea v-model="scoreForm.comment" placeholder="请输入评语" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 批量导入弹窗 -->
    <a-modal
      v-model:visible="importModalVisible"
      title="批量导入成绩"
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

    <!-- 成绩详情弹窗 -->
    <a-modal
      v-model:visible="detailModalVisible"
      title="成绩详情"
      @cancel="closeDetailModal"
      width="800px"
    >
      <a-descriptions :data="studentInfoData" layout="inline-vertical" bordered />
      
      <a-divider>题目得分</a-divider>
      
      <a-table
        :columns="questionColumns"
        :data="currentQuestionScores"
        :pagination="false"
      >
        <template #scoreRate="{ record }">
          <a-progress
            :percent="(record.score / record.points) * 100"
            :stroke-color="getProgressColor((record.score / record.points) * 100)"
            :show-text="true"
          />
        </template>
      </a-table>
      
      <a-divider>知识点掌握情况</a-divider>
      
      <div ref="knowledgeRadarChart" class="chart-container-small"></div>
      
      <template #footer>
        <a-button type="primary" @click="handleGenerateSingleReport">
          生成诊断报告
        </a-button>
      </template>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
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
    const route = useRoute();
    const examId = route.params.examId;
    
    // 图表引用
    const scoreDistributionChart = ref(null);
    const knowledgeRadarChart = ref(null);
    
    // 图表实例
    let scoreDistributionInstance = null;
    let knowledgeRadarInstance = null;
    
    // 考试信息
    const examInfo = reactive({
      id: examId,
      name: '高二数学期中考试',
      subject: '数学',
      examDate: '2025-03-15',
      totalScore: 150,
      duration: 120,
      gradeLevel: '高二',
      classes: ['1班', '2班', '3班', '4班'],
      knowledgePoints: ['函数', '导数', '三角函数', '概率统计', '立体几何']
    });
    
    // 考试信息描述数据
    const examInfoData = [
      {
        label: '考试名称',
        value: examInfo.name
      },
      {
        label: '学科',
        value: examInfo.subject
      },
      {
        label: '考试日期',
        value: examInfo.examDate
      },
      {
        label: '总分',
        value: examInfo.totalScore
      },
      {
        label: '时长',
        value: `${examInfo.duration}分钟`
      },
      {
        label: '年级',
        value: examInfo.gradeLevel
      },
      {
        label: '参与班级',
        value: examInfo.classes.join(', ')
      }
    ];
    
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      class: undefined,
      scoreRange: undefined
    });

    // 成绩表单
    const scoreForm = reactive({
      id: '',
      studentId: '',
      studentName: '',
      class: '',
      score: 0,
      questions: [],
      comment: ''
    });

    // 导入表单
    const importForm = reactive({});
    const fileList = ref([]);

    // 表单引用
    const scoreFormRef = ref(null);
    const importFormRef = ref(null);

    // 状态变量
    const loading = ref(false);
    const scoreModalVisible = ref(false);
    const importModalVisible = ref(false);
    const detailModalVisible = ref(false);
    const isEdit = ref(false);
    const currentStudentId = ref('');
    const currentQuestionScores = ref([]);
    const studentInfoData = ref([]);

    // 分页配置
    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0,
      showTotal: true,
      showPageSize: true,
      pageSizeOptions: [10, 20, 50, 100]
    });

    // 班级选项
    const classOptions = [
      { label: '1班', value: '1班' },
      { label: '2班', value: '2班' },
      { label: '3班', value: '3班' },
      { label: '4班', value: '4班' }
    ];

    // 分数段选项
    const scoreRangeOptions = [
      { label: '优秀 (90-100%)', value: 'excellent' },
      { label: '良好 (80-89%)', value: 'good' },
      { label: '中等 (70-79%)', value: 'average' },
      { label: '及格 (60-69%)', value: 'pass' },
      { label: '不及格 (<60%)', value: 'fail' }
    ];

    // 统计数据
    const stats = reactive({
      totalStudents: 0,
      averageScore: 0,
      highestScore: 0,
      lowestScore: 0
    });

    // 表格列定义
    const columns = [
      {
        title: '学号',
        dataIndex: 'studentId'
      },
      {
        title: '姓名',
        dataIndex: 'studentName'
      },
      {
        title: '班级',
        dataIndex: 'class'
      },
      {
        title: '分数',
        slotName: 'score'
      },
      {
        title: '得分率',
        dataIndex: 'scoreRate',
        render: ({ record }) => {
          return `${((record.score / examInfo.totalScore) * 100).toFixed(1)}%`;
        }
      },
      {
        title: '排名',
        slotName: 'rank'
      },
      {
        title: '评语',
        dataIndex: 'comment',
        ellipsis: true
      },
      {
        title: '操作',
        slotName: 'operations',
        fixed: 'right',
        width: 180
      }
    ];

    // 题目列定义
    const questionColumns = [
      {
        title: '题号',
        dataIndex: 'questionNumber',
        width: 80
      },
      {
        title: '题型',
        dataIndex: 'type'
      },
      {
        title: '分值',
        dataIndex: 'points',
        width: 80
      },
      {
        title: '得分',
        dataIndex: 'score',
        width: 80
      },
      {
        title: '得分率',
        slotName: 'scoreRate',
        width: 200
      },
      {
        title: '知识点',
        dataIndex: 'knowledgePoints'
      }
    ];

    // 成绩表单校验规则
    const scoreFormRules = {
      studentId: [
        { required: true, message: '请输入学号' }
      ],
      studentName: [
        { required: true, message: '请输入学生姓名' }
      ],
      class: [
        { required: true, message: '请选择班级' }
      ],
      score: [
        { required: true, message: '请输入总分' },
        { type: 'number', min: 0, max: examInfo.totalScore, message: `总分应在0-${examInfo.totalScore}之间` }
      ]
    };

    // 模拟成绩数据
    const scoreData = ref([]);

    // 生命周期钩子
    onMounted(() => {
      fetchScoreData();
      
      nextTick(() => {
        initScoreDistributionChart();
      });
    });

    // 获取成绩数据
    const fetchScoreData = () => {
      loading.value = true;
      
      // 模拟API请求
      setTimeout(() => {
        // 生成模拟数据
        const mockData = generateMockScoreData();
        scoreData.value = mockData.list;
        pagination.total = mockData.total;
        
        // 更新统计数据
        updateStats(mockData.allScores);
        
        loading.value = false;
      }, 800);
    };

    // 更新统计数据
    const updateStats = (allScores) => {
      if (allScores.length === 0) return;
      
      stats.totalStudents = allScores.length;
      stats.averageScore = (allScores.reduce((sum, score) => sum + score, 0) / allScores.length).toFixed(1);
      stats.highestScore = Math.max(...allScores);
      stats.lowestScore = Math.min(...allScores);
      
      // 更新成绩分布图
      updateScoreDistributionChart(allScores);
    };

    // 生成模拟成绩数据
    const generateMockScoreData = () => {
      const names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十', '郑十一', '王十二'];
      const classes = examInfo.classes;
      
      const mockList = [];
      const allScores = [];
      const totalItems = 120;
      
      for (let i = 1; i <= totalItems; i++) {
        const studentId = `S${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
        const studentName = names[Math.floor(Math.random() * names.length)] + i;
        const studentClass = classes[Math.floor(Math.random() * classes.length)];
        
        // 生成随机分数，正态分布
        let score = Math.floor(Math.random() * examInfo.totalScore);
        // 调整分数使其更接近正态分布
        score = Math.min(examInfo.totalScore, Math.max(0, Math.floor(score * 0.7 + (examInfo.totalScore * 0.6) * 0.3)));
        
        allScores.push(score);
        
        // 生成题目得分
        const questions = [];
        const questionCount = 10;
        let totalPoints = 0;
        
        for (let j = 1; j <= questionCount; j++) {
          const points = j <= 5 ? 10 : 20;
          totalPoints += points;
          
          // 根据总分比例计算每题得分
          const questionScore = Math.min(points, Math.max(0, Math.floor((score / examInfo.totalScore) * points * (0.8 + Math.random() * 0.4))));
          
          questions.push({
            questionNumber: j,
            type: j <= 5 ? '选择题' : (j <= 8 ? '填空题' : '解答题'),
            points,
            score: questionScore,
            knowledgePoints: getRandomKnowledgePoints()
          });
        }
        
        const scoreRecord = {
          id: `score-${i}`,
          studentId,
          studentName,
          class: studentClass,
          score,
          scoreRate: ((score / examInfo.totalScore) * 100).toFixed(1),
          questions,
          comment: getRandomComment(score, examInfo.totalScore)
        };
        
        // 应用筛选条件
        let match = true;
        
        if (searchForm.keyword) {
          const keyword = searchForm.keyword.toLowerCase();
          const nameMatch = scoreRecord.studentName.toLowerCase().includes(keyword);
          const idMatch = scoreRecord.studentId.toLowerCase().includes(keyword);
          
          if (!nameMatch && !idMatch) {
            match = false;
          }
        }
        
        if (searchForm.class && scoreRecord.class !== searchForm.class) {
          match = false;
        }
        
        if (searchForm.scoreRange) {
          const scorePercent = (score / examInfo.totalScore) * 100;
          
          switch (searchForm.scoreRange) {
            case 'excellent':
              if (scorePercent < 90) match = false;
              break;
            case 'good':
              if (scorePercent < 80 || scorePercent >= 90) match = false;
              break;
            case 'average':
              if (scorePercent < 70 || scorePercent >= 80) match = false;
              break;
            case 'pass':
              if (scorePercent < 60 || scorePercent >= 70) match = false;
              break;
            case 'fail':
              if (scorePercent >= 60) match = false;
              break;
          }
        }
        
        if (match) {
          mockList.push(scoreRecord);
        }
      }
      
      // 计算排名
      mockList.sort((a, b) => b.score - a.score);
      mockList.forEach((item, index) => {
        item.rank = index + 1;
      });
      
      // 分页
      const startIndex = (pagination.current - 1) * pagination.pageSize;
      const endIndex = startIndex + pagination.pageSize;
      const paginatedList = mockList.slice(startIndex, endIndex);
      
      return {
        list: paginatedList,
        total: mockList.length,
        allScores
      };
    };

    // 获取随机知识点
    const getRandomKnowledgePoints = () => {
      const knowledgePoints = examInfo.knowledgePoints;
      const count = Math.floor(Math.random() * 2) + 1;
      const result = [];
      
      for (let i = 0; i < count; i++) {
        const point = knowledgePoints[Math.floor(Math.random() * knowledgePoints.length)];
        if (!result.includes(point)) {
          result.push(point);
        }
      }
      
      return result.join(', ');
    };

    // 获取随机评语
    const getRandomComment = (score, totalScore) => {
      const scorePercent = (score / totalScore) * 100;
      
      if (scorePercent >= 90) {
        return '优秀！掌握了所有知识点，继续保持。';
      } else if (scorePercent >= 80) {
        return '良好，大部分知识点掌握得很好，个别题目需要加强。';
      } else if (scorePercent >= 70) {
        return '中等水平，基础知识掌握较好，复杂题目需要加强。';
      } else if (scorePercent >= 60) {
        return '及格，基础知识有所欠缺，需要加强练习。';
      } else {
        return '需要加强基础知识的学习，建议重新复习相关章节。';
      }
    };

    // 初始化成绩分布图
    const initScoreDistributionChart = () => {
      if (!scoreDistributionChart.value) return;
      
      scoreDistributionInstance = echarts.init(scoreDistributionChart.value);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['0-60', '60-70', '70-80', '80-90', '90-100'],
          axisTick: {
            alignWithLabel: true
          }
        },
        yAxis: {
          type: 'value',
          name: '人数'
        },
        series: [
          {
            name: '人数',
            type: 'bar',
            barWidth: '60%',
            data: [0, 0, 0, 0, 0],
            itemStyle: {
              color: function(params) {
                const colors = ['#F53F3F', '#FF7D00', '#FFAB00', '#00B42A', '#165DFF'];
                return colors[params.dataIndex];
              }
            }
          }
        ]
      };
      
      scoreDistributionInstance.setOption(option);
    };

    // 更新成绩分布图
    const updateScoreDistributionChart = (scores) => {
      if (!scoreDistributionInstance) return;
      
      const distribution = [0, 0, 0, 0, 0];
      
      scores.forEach(score => {
        const percent = (score / examInfo.totalScore) * 100;
        
        if (percent < 60) {
          distribution[0]++;
        } else if (percent < 70) {
          distribution[1]++;
        } else if (percent < 80) {
          distribution[2]++;
        } else if (percent < 90) {
          distribution[3]++;
        } else {
          distribution[4]++;
        }
      });
      
      scoreDistributionInstance.setOption({
        series: [
          {
            data: distribution
          }
        ]
      });
    };

    // 初始化知识点雷达图
    const initKnowledgeRadarChart = (data) => {
      if (!knowledgeRadarChart.value) return;
      
      knowledgeRadarInstance = echarts.init(knowledgeRadarChart.value);
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        radar: {
          indicator: data.indicators,
          radius: 80
        },
        series: [
          {
            type: 'radar',
            data: [
              {
                value: data.values,
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
              }
            ]
          }
        ]
      };
      
      knowledgeRadarInstance.setOption(option);
    };

    // 处理搜索
    const handleSearch = () => {
      pagination.current = 1;
      fetchScoreData();
    };

    // 重置搜索
    const resetSearch = () => {
      searchForm.keyword = '';
      searchForm.class = undefined;
      searchForm.scoreRange = undefined;
      pagination.current = 1;
      fetchScoreData();
    };

    // 处理分页变化
    const onPageChange = (page) => {
      pagination.current = page;
      fetchScoreData();
    };

    // 处理每页条数变化
    const onPageSizeChange = (pageSize) => {
      pagination.pageSize = pageSize;
      pagination.current = 1;
      fetchScoreData();
    };

    // 打开新增成绩弹窗
    const openAddScoreModal = () => {
      isEdit.value = false;
      resetScoreForm();
      
      // 初始化题目得分
      const questions = [];
      for (let i = 1; i <= 10; i++) {
        const points = i <= 5 ? 10 : 20;
        questions.push({
          questionNumber: i,
          type: i <= 5 ? '选择题' : (i <= 8 ? '填空题' : '解答题'),
          points,
          score: 0,
          knowledgePoints: getRandomKnowledgePoints()
        });
      }
      scoreForm.questions = questions;
      
      scoreModalVisible.value = true;
    };

    // 处理查看详情
    const handleViewDetail = (record) => {
      currentStudentId.value = record.studentId;
      currentQuestionScores.value = record.questions;
      
      // 准备学生信息数据
      studentInfoData.value = [
        {
          label: '学号',
          value: record.studentId
        },
        {
          label: '姓名',
          value: record.studentName
        },
        {
          label: '班级',
          value: record.class
        },
        {
          label: '分数',
          value: record.score
        },
        {
          label: '得分率',
          value: `${record.scoreRate}%`
        },
        {
          label: '排名',
          value: record.rank
        },
        {
          label: '评语',
          value: record.comment
        }
      ];
      
      detailModalVisible.value = true;
      
      // 准备知识点雷达图数据
      const knowledgeData = prepareKnowledgeRadarData(record.questions);
      
      nextTick(() => {
        initKnowledgeRadarChart(knowledgeData);
      });
    };

    // 准备知识点雷达图数据
    const prepareKnowledgeRadarData = (questions) => {
      const knowledgeMap = {};
      const knowledgeScoreMap = {};
      const knowledgeMaxMap = {};
      
      // 统计每个知识点的得分和总分
      questions.forEach(question => {
        const points = question.points;
        const score = question.score;
        const knowledgePointsList = question.knowledgePoints.split(', ');
        
        knowledgePointsList.forEach(point => {
          if (!knowledgeMap[point]) {
            knowledgeMap[point] = 0;
            knowledgeScoreMap[point] = 0;
            knowledgeMaxMap[point] = 0;
          }
          
          knowledgeMap[point]++;
          knowledgeScoreMap[point] += score;
          knowledgeMaxMap[point] += points;
        });
      });
      
      // 计算每个知识点的掌握度
      const indicators = [];
      const values = [];
      
      Object.keys(knowledgeMap).forEach(point => {
        indicators.push({
          name: point,
          max: 100
        });
        
        const masteryRate = (knowledgeScoreMap[point] / knowledgeMaxMap[point]) * 100;
        values.push(masteryRate.toFixed(1));
      });
      
      return {
        indicators,
        values
      };
    };

    // 处理编辑成绩
    const handleEdit = (record) => {
      isEdit.value = true;
      currentStudentId.value = record.studentId;
      
      // 填充表单数据
      scoreForm.id = record.id;
      scoreForm.studentId = record.studentId;
      scoreForm.studentName = record.studentName;
      scoreForm.class = record.class;
      scoreForm.score = record.score;
      scoreForm.questions = record.questions;
      scoreForm.comment = record.comment;
      
      scoreModalVisible.value = true;
    };

    // 处理删除成绩
    const handleDelete = (record) => {
      Message.success(`已删除学生 ${record.studentName} 的成绩记录`);
      
      // 在实际应用中，这里应该调用API来删除成绩记录
      // 然后重新获取成绩列表
      
      // 模拟删除
      const index = scoreData.value.findIndex(item => item.id === record.id);
      if (index !== -1) {
        scoreData.value.splice(index, 1);
      }
    };

    // 处理批量导入
    const handleBatchImport = () => {
      fileList.value = [];
      importModalVisible.value = true;
    };

    // 处理批量导出
    const handleBatchExport = () => {
      Message.success('成绩数据导出成功');
    };

    // 处理生成诊断报告
    const handleGenerateReports = () => {
      Message.success('已为所有学生生成诊断报告');
    };

    // 处理生成单个诊断报告
    const handleGenerateSingleReport = () => {
      Message.success(`已为学生 ${currentStudentId.value} 生成诊断报告`);
      closeDetailModal();
    };

    // 自定义上传请求
    const customUploadRequest = (options) => {
      const { file, onSuccess } = options;
      fileList.value = [{ name: file.name, status: 'done' }];
      onSuccess();
    };

    // 提交成绩表单
    const handleSubmitScore = async (done) => {
      try {
        await scoreFormRef.value.validate();
        
        if (isEdit.value) {
          Message.success(`学生 ${scoreForm.studentName} 的成绩更新成功`);
        } else {
          Message.success(`学生 ${scoreForm.studentName} 的成绩录入成功`);
        }
        
        // 在实际应用中，这里应该调用API来创建或更新成绩记录
        // 然后重新获取成绩列表
        
        closeScoreModal();
        fetchScoreData();
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
      
      Message.success('成绩数据导入成功');
      
      // 在实际应用中，这里应该调用API来导入成绩数据
      // 然后重新获取成绩列表
      
      closeImportModal();
      fetchScoreData();
      done();
    };

    // 关闭成绩弹窗
    const closeScoreModal = () => {
      scoreModalVisible.value = false;
      resetScoreForm();
    };

    // 关闭导入弹窗
    const closeImportModal = () => {
      importModalVisible.value = false;
      fileList.value = [];
    };

    // 关闭详情弹窗
    const closeDetailModal = () => {
      detailModalVisible.value = false;
      currentStudentId.value = '';
      currentQuestionScores.value = [];
      studentInfoData.value = [];
      
      if (knowledgeRadarInstance) {
        knowledgeRadarInstance.dispose();
        knowledgeRadarInstance = null;
      }
    };

    // 重置成绩表单
    const resetScoreForm = () => {
      scoreForm.id = '';
      scoreForm.studentId = '';
      scoreForm.studentName = '';
      scoreForm.class = '';
      scoreForm.score = 0;
      scoreForm.questions = [];
      scoreForm.comment = '';
    };

    // 获取分数颜色
    const getScoreColor = (score, totalScore) => {
      const percent = (score / totalScore) * 100;
      
      if (percent >= 90) return '#00B42A';
      if (percent >= 80) return '#0FC6C2';
      if (percent >= 70) return '#165DFF';
      if (percent >= 60) return '#FF7D00';
      return '#F53F3F';
    };

    // 获取排名颜色
    const getRankColor = (rank) => {
      if (rank <= 3) return 'red';
      if (rank <= 10) return 'orange';
      if (rank <= 20) return 'green';
      if (rank <= 50) return 'blue';
      return 'gray';
    };

    // 获取进度条颜色
    const getProgressColor = (percent) => {
      if (percent >= 90) return '#00B42A';
      if (percent >= 80) return '#0FC6C2';
      if (percent >= 70) return '#165DFF';
      if (percent >= 60) return '#FF7D00';
      return '#F53F3F';
    };

    return {
      examInfo,
      examInfoData,
      searchForm,
      scoreForm,
      importForm,
      fileList,
      scoreFormRef,
      importFormRef,
      loading,
      scoreModalVisible,
      importModalVisible,
      detailModalVisible,
      isEdit,
      pagination,
      classOptions,
      scoreRangeOptions,
      stats,
      columns,
      questionColumns,
      scoreFormRules,
      scoreData,
      currentQuestionScores,
      studentInfoData,
      scoreDistributionChart,
      knowledgeRadarChart,
      handleSearch,
      resetSearch,
      onPageChange,
      onPageSizeChange,
      openAddScoreModal,
      handleViewDetail,
      handleEdit,
      handleDelete,
      handleBatchImport,
      handleBatchExport,
      handleGenerateReports,
      handleGenerateSingleReport,
      customUploadRequest,
      handleSubmitScore,
      handleConfirmImport,
      closeScoreModal,
      closeImportModal,
      closeDetailModal,
      getScoreColor,
      getRankColor,
      getProgressColor
    };
  }
};
</script>

<style scoped>
.score-management-container {
  padding: 16px;
}

.exam-info-card,
.search-card,
.stats-card,
.chart-card,
.table-card {
  margin-bottom: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
}

.stat-title {
  font-size: 14px;
  color: #86909C;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
}

.chart-container {
  height: 300px;
  width: 100%;
}

.chart-container-small {
  height: 250px;
  width: 100%;
}

.question-score-item {
  margin-bottom: 8px;
}

@media (max-width: 768px) {
  .search-card .arco-col,
  .stats-card .arco-col {
    margin-bottom: 16px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .chart-container-small {
    height: 200px;
  }
}
</style>
