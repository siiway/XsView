<!-- 后台管理系统数据分析大屏页面 -->
<!-- frontend/scorex-admin/src/views/dashboard/DataAnalytics.vue -->

<template>
  <div class="data-analytics-container">
    <!-- 顶部过滤器 -->
    <a-card class="filter-card">
      <a-row :gutter="16">
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="filterForm.timeRange"
            placeholder="时间范围"
            style="width: 100%"
            @change="handleFilterChange"
          >
            <a-option value="today">今日</a-option>
            <a-option value="yesterday">昨日</a-option>
            <a-option value="week">本周</a-option>
            <a-option value="month">本月</a-option>
            <a-option value="quarter">本季度</a-option>
            <a-option value="year">本年度</a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="filterForm.gradeLevel"
            placeholder="年级"
            style="width: 100%"
            allow-clear
            @change="handleFilterChange"
          >
            <a-option value="all">全部年级</a-option>
            <a-option value="grade-10">高一</a-option>
            <a-option value="grade-11">高二</a-option>
            <a-option value="grade-12">高三</a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="filterForm.subject"
            placeholder="学科"
            style="width: 100%"
            allow-clear
            @change="handleFilterChange"
          >
            <a-option value="all">全部学科</a-option>
            <a-option value="math">数学</a-option>
            <a-option value="chinese">语文</a-option>
            <a-option value="english">英语</a-option>
            <a-option value="physics">物理</a-option>
            <a-option value="chemistry">化学</a-option>
            <a-option value="biology">生物</a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-space>
            <a-button type="primary" @click="handleRefreshData">
              <template #icon><icon-refresh /></template>
              刷新数据
            </a-button>
            <a-button @click="handleExportData">
              <template #icon><icon-download /></template>
              导出数据
            </a-button>
          </a-space>
        </a-col>
      </a-row>
    </a-card>

    <!-- 核心指标卡片 -->
    <a-row :gutter="16" class="stats-row">
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--primary-6), 0.1)">
              <icon-user style="color: rgb(var(--primary-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.activeUsers }}</div>
              <div class="stat-label">活跃用户数</div>
              <div class="stat-trend" :class="stats.activeUsersTrend > 0 ? 'up' : 'down'">
                <icon-arrow-rise v-if="stats.activeUsersTrend > 0" />
                <icon-arrow-fall v-else />
                {{ Math.abs(stats.activeUsersTrend) }}%
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--success-6), 0.1)">
              <icon-file style="color: rgb(var(--success-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.examCount }}</div>
              <div class="stat-label">考试数量</div>
              <div class="stat-trend" :class="stats.examCountTrend > 0 ? 'up' : 'down'">
                <icon-arrow-rise v-if="stats.examCountTrend > 0" />
                <icon-arrow-fall v-else />
                {{ Math.abs(stats.examCountTrend) }}%
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--warning-6), 0.1)">
              <icon-book style="color: rgb(var(--warning-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.reportCount }}</div>
              <div class="stat-label">诊断报告数</div>
              <div class="stat-trend" :class="stats.reportCountTrend > 0 ? 'up' : 'down'">
                <icon-arrow-rise v-if="stats.reportCountTrend > 0" />
                <icon-arrow-fall v-else />
                {{ Math.abs(stats.reportCountTrend) }}%
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
      <a-col :span="6" :xs="24" :sm="12" :md="6">
        <a-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-icon" style="background-color: rgba(var(--danger-6), 0.1)">
              <icon-thumb-up style="color: rgb(var(--danger-6))" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.satisfactionRate }}%</div>
              <div class="stat-label">满意度</div>
              <div class="stat-trend" :class="stats.satisfactionRateTrend > 0 ? 'up' : 'down'">
                <icon-arrow-rise v-if="stats.satisfactionRateTrend > 0" />
                <icon-arrow-fall v-else />
                {{ Math.abs(stats.satisfactionRateTrend) }}%
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 用户增长与活跃度 -->
    <a-row :gutter="16" class="chart-row">
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            用户增长趋势
          </template>
          <div class="chart-container" id="userGrowthChart"></div>
        </a-card>
      </a-col>
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            用户活跃度分析
          </template>
          <div class="chart-container" id="userActivityChart"></div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 考试分析 -->
    <a-row :gutter="16" class="chart-row">
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            考试分数分布
          </template>
          <div class="chart-container" id="scoreDistributionChart"></div>
        </a-card>
      </a-col>
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            学科平均分对比
          </template>
          <div class="chart-container" id="subjectComparisonChart"></div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 知识点与错题分析 -->
    <a-row :gutter="16" class="chart-row">
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            知识点掌握情况
          </template>
          <div class="chart-container" id="knowledgePointChart"></div>
        </a-card>
      </a-col>
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            错题分布热力图
          </template>
          <div class="chart-container" id="errorHeatmapChart"></div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 学习资料与诊断报告 -->
    <a-row :gutter="16" class="chart-row">
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            学习资料使用情况
          </template>
          <div class="chart-container" id="learningMaterialsChart"></div>
        </a-card>
      </a-col>
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            诊断报告生成与查看
          </template>
          <div class="chart-container" id="diagnosticReportsChart"></div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 地域分布与设备分析 -->
    <a-row :gutter="16" class="chart-row">
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            用户地域分布
          </template>
          <div class="chart-container" id="geographicDistributionChart"></div>
        </a-card>
      </a-col>
      <a-col :span="12" :xs="24" :md="12">
        <a-card class="chart-card">
          <template #title>
            设备使用分析
          </template>
          <div class="chart-container" id="deviceAnalysisChart"></div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 系统性能监控 -->
    <a-row :gutter="16" class="chart-row">
      <a-col :span="24">
        <a-card class="chart-card">
          <template #title>
            系统性能监控
          </template>
          <div class="chart-container" id="systemPerformanceChart"></div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
import { Message } from '@arco-design/web-vue';
import * as echarts from 'echarts';
import 'echarts/extension/bmap/bmap';

export default {
  setup() {
    // 过滤表单
    const filterForm = reactive({
      timeRange: 'month',
      gradeLevel: 'all',
      subject: 'all'
    });

    // 统计数据
    const stats = reactive({
      activeUsers: 0,
      activeUsersTrend: 0,
      examCount: 0,
      examCountTrend: 0,
      reportCount: 0,
      reportCountTrend: 0,
      satisfactionRate: 0,
      satisfactionRateTrend: 0
    });

    // 图表实例
    const charts = reactive({
      userGrowthChart: null,
      userActivityChart: null,
      scoreDistributionChart: null,
      subjectComparisonChart: null,
      knowledgePointChart: null,
      errorHeatmapChart: null,
      learningMaterialsChart: null,
      diagnosticReportsChart: null,
      geographicDistributionChart: null,
      deviceAnalysisChart: null,
      systemPerformanceChart: null
    });

    // 窗口大小变化处理
    const handleResize = () => {
      Object.values(charts).forEach(chart => {
        if (chart) {
          chart.resize();
        }
      });
    };

    // 生命周期钩子
    onMounted(() => {
      // 初始化图表
      initCharts();
      
      // 加载数据
      loadData();
      
      // 监听窗口大小变化
      window.addEventListener('resize', handleResize);
    });

    onBeforeUnmount(() => {
      // 移除窗口大小变化监听
      window.removeEventListener('resize', handleResize);
      
      // 销毁图表实例
      Object.values(charts).forEach(chart => {
        if (chart) {
          chart.dispose();
        }
      });
    });

    // 初始化图表
    const initCharts = () => {
      // 用户增长趋势图
      charts.userGrowthChart = echarts.init(document.getElementById('userGrowthChart'));
      
      // 用户活跃度分析图
      charts.userActivityChart = echarts.init(document.getElementById('userActivityChart'));
      
      // 考试分数分布图
      charts.scoreDistributionChart = echarts.init(document.getElementById('scoreDistributionChart'));
      
      // 学科平均分对比图
      charts.subjectComparisonChart = echarts.init(document.getElementById('subjectComparisonChart'));
      
      // 知识点掌握情况图
      charts.knowledgePointChart = echarts.init(document.getElementById('knowledgePointChart'));
      
      // 错题分布热力图
      charts.errorHeatmapChart = echarts.init(document.getElementById('errorHeatmapChart'));
      
      // 学习资料使用情况图
      charts.learningMaterialsChart = echarts.init(document.getElementById('learningMaterialsChart'));
      
      // 诊断报告生成与查看图
      charts.diagnosticReportsChart = echarts.init(document.getElementById('diagnosticReportsChart'));
      
      // 用户地域分布图
      charts.geographicDistributionChart = echarts.init(document.getElementById('geographicDistributionChart'));
      
      // 设备使用分析图
      charts.deviceAnalysisChart = echarts.init(document.getElementById('deviceAnalysisChart'));
      
      // 系统性能监控图
      charts.systemPerformanceChart = echarts.init(document.getElementById('systemPerformanceChart'));
    };

    // 加载数据
    const loadData = () => {
      // 模拟加载数据
      setTimeout(() => {
        // 更新统计数据
        updateStats();
        
        // 更新图表数据
        updateCharts();
      }, 1000);
    };

    // 更新统计数据
    const updateStats = () => {
      stats.activeUsers = Math.floor(Math.random() * 5000) + 5000;
      stats.activeUsersTrend = Math.floor(Math.random() * 20) - 5;
      stats.examCount = Math.floor(Math.random() * 500) + 500;
      stats.examCountTrend = Math.floor(Math.random() * 30) - 5;
      stats.reportCount = Math.floor(Math.random() * 2000) + 3000;
      stats.reportCountTrend = Math.floor(Math.random() * 25) - 5;
      stats.satisfactionRate = Math.floor(Math.random() * 10) + 85;
      stats.satisfactionRateTrend = Math.floor(Math.random() * 10) - 2;
    };

    // 更新图表数据
    const updateCharts = () => {
      // 用户增长趋势图
      updateUserGrowthChart();
      
      // 用户活跃度分析图
      updateUserActivityChart();
      
      // 考试分数分布图
      updateScoreDistributionChart();
      
      // 学科平均分对比图
      updateSubjectComparisonChart();
      
      // 知识点掌握情况图
      updateKnowledgePointChart();
      
      // 错题分布热力图
      updateErrorHeatmapChart();
      
      // 学习资料使用情况图
      updateLearningMaterialsChart();
      
      // 诊断报告生成与查看图
      updateDiagnosticReportsChart();
      
      // 用户地域分布图
      updateGeographicDistributionChart();
      
      // 设备使用分析图
      updateDeviceAnalysisChart();
      
      // 系统性能监控图
      updateSystemPerformanceChart();
    };

    // 更新用户增长趋势图
    const updateUserGrowthChart = () => {
      const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
      const newUsers = [];
      const totalUsers = [];
      
      let total = 5000;
      for (let i = 0; i < 12; i++) {
        const newUser = Math.floor(Math.random() * 500) + 200;
        newUsers.push(newUser);
        total += newUser;
        totalUsers.push(total);
      }
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['新增用户', '累计用户']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: months
        },
        yAxis: [
          {
            type: 'value',
            name: '新增用户',
            position: 'left'
          },
          {
            type: 'value',
            name: '累计用户',
            position: 'right'
          }
        ],
        series: [
          {
            name: '新增用户',
            type: 'bar',
            data: newUsers
          },
          {
            name: '累计用户',
            type: 'line',
            yAxisIndex: 1,
            data: totalUsers
          }
        ]
      };
      
      charts.userGrowthChart.setOption(option);
    };

    // 更新用户活跃度分析图
    const updateUserActivityChart = () => {
      const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
      const hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'];
      
      const data = [];
      for (let i = 0; i < 7; i++) {
        for (let j = 0; j < 24; j++) {
          // 生成随机活跃度数据，工作日白天活跃度高，晚上和周末活跃度适中
          let value;
          if (i < 5) { // 工作日
            if (j >= 8 && j <= 17) { // 白天
              value = Math.floor(Math.random() * 50) + 50;
            } else if ((j >= 18 && j <= 22) || (j >= 6 && j <= 7)) { // 早晚
              value = Math.floor(Math.random() * 40) + 30;
            } else { // 深夜
              value = Math.floor(Math.random() * 20) + 5;
            }
          } else { // 周末
            if (j >= 9 && j <= 22) { // 白天到晚上
              value = Math.floor(Math.random() * 60) + 30;
            } else { // 深夜
              value = Math.floor(Math.random() * 30) + 5;
            }
          }
          
          data.push([j, i, value]);
        }
      }
      
      const option = {
        tooltip: {
          position: 'top',
          formatter: function (params) {
            return `${days[params.value[1]]} ${hours[params.value[0]]}<br/>活跃用户: ${params.value[2]}`;
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
          data: hours,
          splitArea: {
            show: true
          },
          axisLabel: {
            interval: 3
          }
        },
        yAxis: {
          type: 'category',
          data: days,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 100,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '0%',
          inRange: {
            color: ['#e9f5e4', '#c6e6c1', '#a3d89e', '#7fca7b', '#5cbc58', '#39ae35']
          }
        },
        series: [{
          name: '用户活跃度',
          type: 'heatmap',
          data: data,
          label: {
            show: false
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      };
      
      charts.userActivityChart.setOption(option);
    };

    // 更新考试分数分布图
    const updateScoreDistributionChart = () => {
      // 生成正态分布的分数数据
      const generateNormalDistribution = (mean, stdDev, count) => {
        const data = [];
        for (let i = 0; i < count; i++) {
          // 使用Box-Muller变换生成正态分布随机数
          const u1 = Math.random();
          const u2 = Math.random();
          const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
          let score = Math.round(z0 * stdDev + mean);
          
          // 限制分数在0-100之间
          score = Math.max(0, Math.min(100, score));
          data.push(score);
        }
        return data;
      };
      
      // 生成三个不同学科的分数分布
      const mathScores = generateNormalDistribution(75, 15, 1000);
      const chineseScores = generateNormalDistribution(80, 10, 1000);
      const englishScores = generateNormalDistribution(70, 12, 1000);
      
      // 计算分数区间的频率
      const calculateFrequency = (scores) => {
        const frequency = new Array(10).fill(0);
        scores.forEach(score => {
          const index = Math.min(9, Math.floor(score / 10));
          frequency[index]++;
        });
        return frequency.map(count => (count / scores.length * 100).toFixed(2));
      };
      
      const mathFrequency = calculateFrequency(mathScores);
      const chineseFrequency = calculateFrequency(chineseScores);
      const englishFrequency = calculateFrequency(englishScores);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['数学', '语文', '英语']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
        },
        yAxis: {
          type: 'value',
          name: '百分比(%)'
        },
        series: [
          {
            name: '数学',
            type: 'bar',
            data: mathFrequency
          },
          {
            name: '语文',
            type: 'bar',
            data: chineseFrequency
          },
          {
            name: '英语',
            type: 'bar',
            data: englishFrequency
          }
        ]
      };
      
      charts.scoreDistributionChart.setOption(option);
    };

    // 更新学科平均分对比图
    const updateSubjectComparisonChart = () => {
      const subjects = ['数学', '语文', '英语', '物理', '化学', '生物', '历史', '地理', '政治'];
      
      // 生成三个不同年级的平均分数据
      const generateAverageScores = (base) => {
        return subjects.map(() => Math.floor(Math.random() * 20) + base);
      };
      
      const grade10Scores = generateAverageScores(65);
      const grade11Scores = generateAverageScores(70);
      const grade12Scores = generateAverageScores(75);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['高一', '高二', '高三']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '平均分'
        },
        yAxis: {
          type: 'category',
          data: subjects
        },
        series: [
          {
            name: '高一',
            type: 'bar',
            data: grade10Scores
          },
          {
            name: '高二',
            type: 'bar',
            data: grade11Scores
          },
          {
            name: '高三',
            type: 'bar',
            data: grade12Scores
          }
        ]
      };
      
      charts.subjectComparisonChart.setOption(option);
    };

    // 更新知识点掌握情况图
    const updateKnowledgePointChart = () => {
      const knowledgePoints = [
        '函数', '导数', '三角函数', '概率统计', 
        '立体几何', '向量', '数列', '复数', '解析几何'
      ];
      
      // 生成知识点掌握度数据
      const generateMasteryData = () => {
        return knowledgePoints.map(() => Math.floor(Math.random() * 40) + 60);
      };
      
      const masteryData = generateMasteryData();
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        radar: {
          indicator: knowledgePoints.map(point => ({ name: point, max: 100 }))
        },
        series: [
          {
            name: '知识点掌握度',
            type: 'radar',
            data: [
              {
                value: masteryData,
                name: '掌握度',
                areaStyle: {
                  color: 'rgba(var(--primary-6), 0.3)'
                },
                lineStyle: {
                  color: 'rgb(var(--primary-6))'
                },
                itemStyle: {
                  color: 'rgb(var(--primary-6))'
                }
              }
            ]
          }
        ]
      };
      
      charts.knowledgePointChart.setOption(option);
    };

    // 更新错题分布热力图
    const updateErrorHeatmapChart = () => {
      const subjects = ['数学', '语文', '英语', '物理', '化学', '生物', '历史', '地理', '政治'];
      const knowledgePoints = [
        '基础概念', '公式应用', '计算能力', '逻辑推理', 
        '图形分析', '文本理解', '实验操作', '综合应用', '创新思维'
      ];
      
      // 生成错题分布数据
      const data = [];
      for (let i = 0; i < subjects.length; i++) {
        for (let j = 0; j < knowledgePoints.length; j++) {
          // 生成随机错题率，范围10%-50%
          const value = Math.floor(Math.random() * 40) + 10;
          data.push([i, j, value]);
        }
      }
      
      const option = {
        tooltip: {
          position: 'top',
          formatter: function (params) {
            return `${subjects[params.value[0]]} - ${knowledgePoints[params.value[1]]}<br/>错题率: ${params.value[2]}%`;
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
          data: subjects,
          splitArea: {
            show: true
          }
        },
        yAxis: {
          type: 'category',
          data: knowledgePoints,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 50,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '0%',
          inRange: {
            color: ['#e9f5e4', '#c6e6c1', '#a3d89e', '#7fca7b', '#5cbc58', '#39ae35']
          }
        },
        series: [{
          name: '错题分布',
          type: 'heatmap',
          data: data,
          label: {
            show: false
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      };
      
      charts.errorHeatmapChart.setOption(option);
    };

    // 更新学习资料使用情况图
    const updateLearningMaterialsChart = () => {
      const resourceTypes = ['课件', '习题', '视频', '文档', '图表', '试卷'];
      
      // 生成学习资料使用数据
      const generateUsageData = () => {
        const viewData = resourceTypes.map(() => Math.floor(Math.random() * 500) + 500);
        const downloadData = resourceTypes.map((_, index) => Math.floor(viewData[index] * (Math.random() * 0.4 + 0.3)));
        return { viewData, downloadData };
      };
      
      const { viewData, downloadData } = generateUsageData();
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['查看次数', '下载次数']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: resourceTypes
        },
        yAxis: {
          type: 'value',
          name: '次数'
        },
        series: [
          {
            name: '查看次数',
            type: 'bar',
            data: viewData
          },
          {
            name: '下载次数',
            type: 'bar',
            data: downloadData
          }
        ]
      };
      
      charts.learningMaterialsChart.setOption(option);
    };

    // 更新诊断报告生成与查看图
    const updateDiagnosticReportsChart = () => {
      const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
      
      // 生成诊断报告数据
      const generateReportData = () => {
        const generatedData = months.map(() => Math.floor(Math.random() * 300) + 200);
        const viewedData = generatedData.map(value => Math.floor(value * (Math.random() * 0.3 + 0.6)));
        return { generatedData, viewedData };
      };
      
      const { generatedData, viewedData } = generateReportData();
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['生成报告数', '查看报告数']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: months
        },
        yAxis: {
          type: 'value',
          name: '报告数'
        },
        series: [
          {
            name: '生成报告数',
            type: 'line',
            smooth: true,
            data: generatedData
          },
          {
            name: '查看报告数',
            type: 'line',
            smooth: true,
            data: viewedData
          }
        ]
      };
      
      charts.diagnosticReportsChart.setOption(option);
    };

    // 更新用户地域分布图
    const updateGeographicDistributionChart = () => {
      // 模拟中国各省份用户分布数据
      const provinces = [
        { name: '北京', value: Math.floor(Math.random() * 1000) + 500 },
        { name: '天津', value: Math.floor(Math.random() * 800) + 300 },
        { name: '河北', value: Math.floor(Math.random() * 1200) + 800 },
        { name: '山西', value: Math.floor(Math.random() * 800) + 400 },
        { name: '内蒙古', value: Math.floor(Math.random() * 600) + 200 },
        { name: '辽宁', value: Math.floor(Math.random() * 900) + 500 },
        { name: '吉林', value: Math.floor(Math.random() * 700) + 300 },
        { name: '黑龙江', value: Math.floor(Math.random() * 800) + 400 },
        { name: '上海', value: Math.floor(Math.random() * 1000) + 600 },
        { name: '江苏', value: Math.floor(Math.random() * 1500) + 1000 },
        { name: '浙江', value: Math.floor(Math.random() * 1400) + 900 },
        { name: '安徽', value: Math.floor(Math.random() * 1100) + 700 },
        { name: '福建', value: Math.floor(Math.random() * 1000) + 600 },
        { name: '江西', value: Math.floor(Math.random() * 900) + 500 },
        { name: '山东', value: Math.floor(Math.random() * 1300) + 900 },
        { name: '河南', value: Math.floor(Math.random() * 1400) + 1000 },
        { name: '湖北', value: Math.floor(Math.random() * 1200) + 800 },
        { name: '湖南', value: Math.floor(Math.random() * 1100) + 700 },
        { name: '广东', value: Math.floor(Math.random() * 1600) + 1200 },
        { name: '广西', value: Math.floor(Math.random() * 900) + 500 },
        { name: '海南', value: Math.floor(Math.random() * 500) + 200 },
        { name: '重庆', value: Math.floor(Math.random() * 900) + 500 },
        { name: '四川', value: Math.floor(Math.random() * 1300) + 900 },
        { name: '贵州', value: Math.floor(Math.random() * 800) + 400 },
        { name: '云南', value: Math.floor(Math.random() * 900) + 500 },
        { name: '西藏', value: Math.floor(Math.random() * 300) + 100 },
        { name: '陕西', value: Math.floor(Math.random() * 1000) + 600 },
        { name: '甘肃', value: Math.floor(Math.random() * 700) + 300 },
        { name: '青海', value: Math.floor(Math.random() * 400) + 200 },
        { name: '宁夏', value: Math.floor(Math.random() * 400) + 200 },
        { name: '新疆', value: Math.floor(Math.random() * 600) + 300 },
        { name: '台湾', value: Math.floor(Math.random() * 800) + 400 },
        { name: '香港', value: Math.floor(Math.random() * 600) + 300 },
        { name: '澳门', value: Math.floor(Math.random() * 400) + 200 }
      ];
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} 用户'
        },
        visualMap: {
          min: 0,
          max: 3000,
          left: 'left',
          top: 'bottom',
          text: ['高', '低'],
          calculable: true,
          inRange: {
            color: ['#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695']
          }
        },
        series: [
          {
            name: '用户分布',
            type: 'map',
            map: 'china',
            roam: true,
            emphasis: {
              label: {
                show: true
              }
            },
            data: provinces
          }
        ]
      };
      
      charts.geographicDistributionChart.setOption(option);
    };

    // 更新设备使用分析图
    const updateDeviceAnalysisChart = () => {
      // 设备类型分布
      const deviceTypeData = [
        { value: Math.floor(Math.random() * 30) + 50, name: '手机' },
        { value: Math.floor(Math.random() * 20) + 30, name: '平板' },
        { value: Math.floor(Math.random() * 15) + 15, name: '电脑' },
        { value: Math.floor(Math.random() * 5) + 5, name: '其他' }
      ];
      
      // 操作系统分布
      const osData = [
        { value: Math.floor(Math.random() * 30) + 40, name: 'Android' },
        { value: Math.floor(Math.random() * 25) + 35, name: 'iOS' },
        { value: Math.floor(Math.random() * 15) + 15, name: 'Windows' },
        { value: Math.floor(Math.random() * 10) + 5, name: 'macOS' },
        { value: Math.floor(Math.random() * 5) + 5, name: '其他' }
      ];
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: ['手机', '平板', '电脑', '其他', 'Android', 'iOS', 'Windows', 'macOS']
        },
        series: [
          {
            name: '设备类型',
            type: 'pie',
            radius: ['0%', '40%'],
            center: ['50%', '50%'],
            label: {
              position: 'inner',
              formatter: '{d}%'
            },
            data: deviceTypeData
          },
          {
            name: '操作系统',
            type: 'pie',
            radius: ['55%', '70%'],
            center: ['50%', '50%'],
            label: {
              formatter: '{b}: {d}%'
            },
            data: osData
          }
        ]
      };
      
      charts.deviceAnalysisChart.setOption(option);
    };

    // 更新系统性能监控图
    const updateSystemPerformanceChart = () => {
      const timePoints = [];
      const cpuData = [];
      const memoryData = [];
      const responseTimeData = [];
      
      // 生成过去24小时的时间点
      const now = new Date();
      for (let i = 23; i >= 0; i--) {
        const time = new Date(now);
        time.setHours(now.getHours() - i);
        timePoints.push(time.getHours() + ':00');
        
        // 生成CPU使用率数据（20%-80%）
        cpuData.push(Math.floor(Math.random() * 60) + 20);
        
        // 生成内存使用率数据（30%-90%）
        memoryData.push(Math.floor(Math.random() * 60) + 30);
        
        // 生成响应时间数据（50ms-500ms）
        responseTimeData.push(Math.floor(Math.random() * 450) + 50);
      }
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: ['CPU使用率', '内存使用率', '响应时间']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: timePoints
        },
        yAxis: [
          {
            type: 'value',
            name: '使用率(%)',
            min: 0,
            max: 100,
            position: 'left'
          },
          {
            type: 'value',
            name: '响应时间(ms)',
            min: 0,
            max: 600,
            position: 'right'
          }
        ],
        series: [
          {
            name: 'CPU使用率',
            type: 'line',
            data: cpuData,
            smooth: true,
            areaStyle: {
              opacity: 0.3
            }
          },
          {
            name: '内存使用率',
            type: 'line',
            data: memoryData,
            smooth: true,
            areaStyle: {
              opacity: 0.3
            }
          },
          {
            name: '响应时间',
            type: 'line',
            yAxisIndex: 1,
            data: responseTimeData,
            smooth: true,
            areaStyle: {
              opacity: 0.3
            }
          }
        ]
      };
      
      charts.systemPerformanceChart.setOption(option);
    };

    // 处理过滤器变化
    const handleFilterChange = () => {
      // 重新加载数据
      loadData();
    };

    // 刷新数据
    const handleRefreshData = () => {
      Message.loading('正在刷新数据...');
      
      // 重新加载数据
      loadData();
      
      setTimeout(() => {
        Message.success('数据刷新成功');
      }, 1000);
    };

    // 导出数据
    const handleExportData = () => {
      Message.loading('正在导出数据...');
      
      setTimeout(() => {
        Message.success('数据导出成功');
      }, 1500);
    };

    return {
      filterForm,
      stats,
      handleFilterChange,
      handleRefreshData,
      handleExportData
    };
  }
};
</script>

<style scoped>
.data-analytics-container {
  padding: 16px;
}

.filter-card {
  margin-bottom: 16px;
}

.stats-row {
  margin-bottom: 16px;
}

.chart-row {
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

.stat-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  margin-top: 4px;
}

.stat-trend.up {
  color: #00B42A;
}

.stat-trend.down {
  color: #F53F3F;
}

.chart-card {
  height: 100%;
}

.chart-container {
  height: 300px;
  width: 100%;
}

@media (max-width: 768px) {
  .filter-card .arco-col {
    margin-bottom: 16px;
  }
  
  .stats-row .arco-col {
    margin-bottom: 16px;
  }
  
  .chart-row .arco-col {
    margin-bottom: 16px;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>
