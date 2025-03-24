<!-- 后台管理系统首页 -->
<!-- frontend/scorex-admin/src/views/Dashboard.vue -->

<template>
  <div class="dashboard-container">
    <a-row :gutter="16">
      <!-- 数据概览卡片 -->
      <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6">
        <a-card class="stat-card">
          <div class="stat-icon user-icon">
            <icon-user />
          </div>
          <div class="stat-content">
            <div class="stat-title">用户总数</div>
            <div class="stat-value">{{ stats.userCount }}</div>
            <div class="stat-trend">
              <span class="trend-value up">
                <icon-arrow-rise />
                {{ stats.userGrowth }}%
              </span>
              <span class="trend-label">较上月</span>
            </div>
          </div>
        </a-card>
      </a-col>
      
      <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6">
        <a-card class="stat-card">
          <div class="stat-icon exam-icon">
            <icon-file />
          </div>
          <div class="stat-content">
            <div class="stat-title">考试总数</div>
            <div class="stat-value">{{ stats.examCount }}</div>
            <div class="stat-trend">
              <span class="trend-value up">
                <icon-arrow-rise />
                {{ stats.examGrowth }}%
              </span>
              <span class="trend-label">较上月</span>
            </div>
          </div>
        </a-card>
      </a-col>
      
      <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6">
        <a-card class="stat-card">
          <div class="stat-icon report-icon">
            <icon-book />
          </div>
          <div class="stat-content">
            <div class="stat-title">诊断报告</div>
            <div class="stat-value">{{ stats.reportCount }}</div>
            <div class="stat-trend">
              <span class="trend-value up">
                <icon-arrow-rise />
                {{ stats.reportGrowth }}%
              </span>
              <span class="trend-label">较上月</span>
            </div>
          </div>
        </a-card>
      </a-col>
      
      <a-col :span="6" :xs="24" :sm="12" :md="12" :lg="6">
        <a-card class="stat-card">
          <div class="stat-icon active-icon">
            <icon-fire />
          </div>
          <div class="stat-content">
            <div class="stat-title">活跃用户</div>
            <div class="stat-value">{{ stats.activeUsers }}</div>
            <div class="stat-trend">
              <span class="trend-value up">
                <icon-arrow-rise />
                {{ stats.activeGrowth }}%
              </span>
              <span class="trend-label">较上月</span>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>
    
    <a-row :gutter="16" style="margin-top: 16px;">
      <!-- 用户增长趋势图 -->
      <a-col :span="12" :xs="24" :md="12">
        <a-card title="用户增长趋势">
          <div ref="userGrowthChart" class="chart-container"></div>
        </a-card>
      </a-col>
      
      <!-- 考试分布图 -->
      <a-col :span="12" :xs="24" :md="12">
        <a-card title="考试学科分布">
          <div ref="examDistributionChart" class="chart-container"></div>
        </a-card>
      </a-col>
    </a-row>
    
    <a-row :gutter="16" style="margin-top: 16px;">
      <!-- 最近考试列表 -->
      <a-col :span="12" :xs="24" :md="12">
        <a-card title="最近考试" extra="查看全部">
          <a-table
            :columns="examColumns"
            :data="recentExams"
            :pagination="false"
            :bordered="false"
          />
        </a-card>
      </a-col>
      
      <!-- 系统日志 -->
      <a-col :span="12" :xs="24" :md="12">
        <a-card title="系统日志" extra="查看全部">
          <a-list>
            <a-list-item v-for="(log, index) in systemLogs" :key="index">
              <a-list-item-meta>
                <template #avatar>
                  <a-avatar :style="{ backgroundColor: getLogTypeColor(log.type) }">
                    {{ getLogTypeIcon(log.type) }}
                  </a-avatar>
                </template>
                <template #title>{{ log.title }}</template>
                <template #description>
                  <div class="log-description">
                    <span>{{ log.description }}</span>
                    <span class="log-time">{{ log.time }}</span>
                  </div>
                </template>
              </a-list-item-meta>
            </a-list-item>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
    
    <a-row :gutter="16" style="margin-top: 16px;">
      <!-- 服务器状态 -->
      <a-col :span="24">
        <a-card title="服务器状态">
          <a-row :gutter="16">
            <a-col :span="8" :xs="24" :md="8">
              <div class="server-stat">
                <div class="server-stat-title">
                  <icon-cpu /> CPU使用率
                </div>
                <a-progress
                  :percent="serverStats.cpu"
                  :stroke-color="getProgressColor(serverStats.cpu)"
                  :show-text="true"
                />
              </div>
            </a-col>
            
            <a-col :span="8" :xs="24" :md="8">
              <div class="server-stat">
                <div class="server-stat-title">
                  <icon-computer /> 内存使用率
                </div>
                <a-progress
                  :percent="serverStats.memory"
                  :stroke-color="getProgressColor(serverStats.memory)"
                  :show-text="true"
                />
              </div>
            </a-col>
            
            <a-col :span="8" :xs="24" :md="8">
              <div class="server-stat">
                <div class="server-stat-title">
                  <icon-storage /> 磁盘使用率
                </div>
                <a-progress
                  :percent="serverStats.disk"
                  :stroke-color="getProgressColor(serverStats.disk)"
                  :show-text="true"
                />
              </div>
            </a-col>
          </a-row>
          
          <a-divider style="margin: 16px 0" />
          
          <a-row :gutter="16">
            <a-col :span="12" :xs="24" :md="12">
              <div class="node-status">
                <div class="node-status-title">边缘节点状态</div>
                <a-table
                  :columns="nodeColumns"
                  :data="edgeNodes"
                  :pagination="false"
                  :bordered="false"
                />
              </div>
            </a-col>
            
            <a-col :span="12" :xs="24" :md="12">
              <div class="api-status">
                <div class="api-status-title">API调用统计（今日）</div>
                <div ref="apiCallsChart" class="chart-container-small"></div>
              </div>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts/core';
import { LineChart, PieChart, BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// 注册 ECharts 组件
echarts.use([
  LineChart,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  CanvasRenderer
]);

export default {
  setup() {
    // 图表引用
    const userGrowthChart = ref(null);
    const examDistributionChart = ref(null);
    const apiCallsChart = ref(null);
    
    // 图表实例
    let userGrowthInstance = null;
    let examDistributionInstance = null;
    let apiCallsInstance = null;
    
    // 数据统计
    const stats = ref({
      userCount: 5284,
      userGrowth: 12.5,
      examCount: 1872,
      examGrowth: 8.3,
      reportCount: 3641,
      reportGrowth: 15.2,
      activeUsers: 2156,
      activeGrowth: 9.7
    });
    
    // 服务器状态
    const serverStats = ref({
      cpu: 42,
      memory: 58,
      disk: 35
    });
    
    // 最近考试列表
    const examColumns = [
      {
        title: '考试名称',
        dataIndex: 'name'
      },
      {
        title: '学科',
        dataIndex: 'subject',
        width: 100
      },
      {
        title: '参与人数',
        dataIndex: 'participants',
        width: 100
      },
      {
        title: '平均分',
        dataIndex: 'averageScore',
        width: 100
      },
      {
        title: '时间',
        dataIndex: 'time',
        width: 150
      }
    ];
    
    const recentExams = ref([
      {
        name: '高二年级期中考试',
        subject: '数学',
        participants: 320,
        averageScore: 78.5,
        time: '2025-03-20'
      },
      {
        name: '高一年级月考',
        subject: '英语',
        participants: 285,
        averageScore: 82.3,
        time: '2025-03-18'
      },
      {
        name: '高三模拟考试',
        subject: '物理',
        participants: 156,
        averageScore: 75.8,
        time: '2025-03-15'
      },
      {
        name: '高二年级单元测试',
        subject: '化学',
        participants: 210,
        averageScore: 80.1,
        time: '2025-03-12'
      }
    ]);
    
    // 系统日志
    const systemLogs = ref([
      {
        type: 'user',
        title: '新用户注册',
        description: '新增用户 zhang_san 完成注册',
        time: '10分钟前'
      },
      {
        type: 'exam',
        title: '考试数据导入',
        description: '管理员导入了"高二年级期中考试"数据',
        time: '30分钟前'
      },
      {
        type: 'system',
        title: '系统更新',
        description: '系统完成自动更新至v2.3.1版本',
        time: '2小时前'
      },
      {
        type: 'warning',
        title: '服务器负载警告',
        description: '边缘节点2负载超过80%',
        time: '3小时前'
      },
      {
        type: 'user',
        title: '用户登录异常',
        description: '用户li_si尝试多次登录失败',
        time: '5小时前'
      }
    ]);
    
    // 边缘节点状态
    const nodeColumns = [
      {
        title: '节点名称',
        dataIndex: 'name'
      },
      {
        title: '状态',
        dataIndex: 'status',
        width: 100,
        render: ({ record }) => {
          return (
            <a-tag color={record.status === '正常' ? 'green' : (record.status === '警告' ? 'orange' : 'red')}>
              {record.status}
            </a-tag>
          );
        }
      },
      {
        title: '负载',
        dataIndex: 'load',
        width: 100
      },
      {
        title: '响应时间',
        dataIndex: 'responseTime',
        width: 120
      }
    ];
    
    const edgeNodes = ref([
      {
        name: '边缘节点1 (华东)',
        status: '正常',
        load: '42%',
        responseTime: '68ms'
      },
      {
        name: '边缘节点2 (华南)',
        status: '警告',
        load: '82%',
        responseTime: '125ms'
      },
      {
        name: '边缘节点3 (华北)',
        status: '正常',
        load: '35%',
        responseTime: '72ms'
      },
      {
        name: '边缘节点4 (西南)',
        status: '正常',
        load: '28%',
        responseTime: '85ms'
      }
    ]);
    
    // 初始化图表
    const initCharts = () => {
      initUserGrowthChart();
      initExamDistributionChart();
      initApiCallsChart();
    };
    
    // 初始化用户增长趋势图
    const initUserGrowthChart = () => {
      if (!userGrowthChart.value) return;
      
      userGrowthInstance = echarts.init(userGrowthChart.value);
      
      const months = ['1月', '2月', '3月', '4月', '5月', '6月'];
      const userData = [120, 180, 240, 320, 450, 520];
      const activeData = [80, 120, 160, 220, 280, 350];
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['总用户数', '活跃用户数'],
          right: 10,
          top: 10
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
          data: months
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '总用户数',
            type: 'line',
            data: userData,
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#165DFF'
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(22, 93, 255, 0.3)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(22, 93, 255, 0.1)'
                  }
                ]
              }
            }
          },
          {
            name: '活跃用户数',
            type: 'line',
            data: activeData,
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#37C2FF'
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(55, 194, 255, 0.3)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(55, 194, 255, 0.1)'
                  }
                ]
              }
            }
          }
        ]
      };
      
      userGrowthInstance.setOption(option);
    };
    
    // 初始化考试分布图
    const initExamDistributionChart = () => {
      if (!examDistributionChart.value) return;
      
      examDistributionInstance = echarts.init(examDistributionChart.value);
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center',
          data: ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治']
        },
        series: [
          {
            name: '考试分布',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 235, name: '语文' },
              { value: 274, name: '数学' },
              { value: 310, name: '英语' },
              { value: 185, name: '物理' },
              { value: 148, name: '化学' },
              { value: 120, name: '生物' },
              { value: 98, name: '历史' },
              { value: 82, name: '地理' },
              { value: 72, name: '政治' }
            ]
          }
        ]
      };
      
      examDistributionInstance.setOption(option);
    };
    
    // 初始化API调用统计图
    const initApiCallsChart = () => {
      if (!apiCallsChart.value) return;
      
      apiCallsInstance = echarts.init(apiCallsChart.value);
      
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
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: ['登录认证', '用户信息', '考试列表', '考试详情', '成绩分析', '诊断报告']
        },
        series: [
          {
            name: '调用次数',
            type: 'bar',
            data: [8542, 5263, 4875, 3982, 2854, 1932],
            itemStyle: {
              color: function(params) {
                const colorList = [
                  '#165DFF', '#37C2FF', '#00B42A', 
                  '#FFAB00', '#FF7D00', '#EB0AA4'
                ];
                return colorList[params.dataIndex];
              }
            }
          }
        ]
      };
      
      apiCallsInstance.setOption(option);
    };
    
    // 获取日志类型颜色
    const getLogTypeColor = (type) => {
      const colorMap = {
        'user': '#165DFF',
        'exam': '#00B42A',
        'system': '#86909C',
        'warning': '#FF7D00',
        'error': '#F53F3F'
      };
      return colorMap[type] || '#86909C';
    };
    
    // 获取日志类型图标
    const getLogTypeIcon = (type) => {
      const iconMap = {
        'user': '用',
        'exam': '考',
        'system': '系',
        'warning': '警',
        'error': '错'
      };
      return iconMap[type] || '日';
    };
    
    // 获取进度条颜色
    const getProgressColor = (value) => {
      if (value < 50) return '#00B42A';
      if (value < 80) return '#FFAB00';
      return '#F53F3F';
    };
    
    onMounted(() => {
      nextTick(() => {
        initCharts();
        
        // 监听窗口大小变化
        window.addEventListener('resize', () => {
          userGrowthInstance?.resize();
          examDistributionInstance?.resize();
          apiCallsInstance?.resize();
        });
      });
    });
    
    return {
      stats,
      serverStats,
      examColumns,
      recentExams,
      systemLogs,
      nodeColumns,
      edgeNodes,
      userGrowthChart,
      examDistributionChart,
      apiCallsChart,
      getLogTypeColor,
      getLogTypeIcon,
      getProgressColor
    };
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 16px;
  font-size: 24px;
}

.user-icon {
  background-color: rgba(22, 93, 255, 0.1);
  color: #165DFF;
}

.exam-icon {
  background-color: rgba(0, 180, 42, 0.1);
  color: #00B42A;
}

.report-icon {
  background-color: rgba(255, 171, 0, 0.1);
  color: #FFAB00;
}

.active-icon {
  background-color: rgba(255, 125, 0, 0.1);
  color: #FF7D00;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #86909C;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-trend {
  font-size: 12px;
}

.trend-value {
  display: inline-flex;
  align-items: center;
  margin-right: 4px;
}

.trend-value.up {
  color: #00B42A;
}

.trend-value.down {
  color: #F53F3F;
}

.trend-label {
  color: #86909C;
}

.chart-container {
  height: 300px;
  width: 100%;
}

.chart-container-small {
  height: 200px;
  width: 100%;
}

.log-description {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-time {
  color: #86909C;
}

.server-stat {
  margin-bottom: 16px;
}

.server-stat-title {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
}

.server-stat-title .arco-icon {
  margin-right: 8px;
}

.node-status-title, .api-status-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .stat-card {
    margin-bottom: 16px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .chart-container-small {
    height: 180px;
  }
}
</style>
