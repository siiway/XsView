<!-- 后台管理系统配置页面 -->
<!-- frontend/scorex-admin/src/views/system/SystemConfig.vue -->

<template>
  <div class="system-config-container">
    <a-row :gutter="16">
      <a-col :span="6" :xs="24" :sm="24" :md="6">
        <!-- 配置导航菜单 -->
        <a-card class="menu-card">
          <a-menu
            :selected-keys="[activeConfigType]"
            @menu-item-click="handleMenuClick"
          >
            <a-menu-item key="basic">
              <template #icon><icon-settings /></template>
              基础配置
            </a-menu-item>
            <a-menu-item key="security">
              <template #icon><icon-safe /></template>
              安全配置
            </a-menu-item>
            <a-menu-item key="api">
              <template #icon><icon-code-square /></template>
              API配置
            </a-menu-item>
            <a-menu-item key="node">
              <template #icon><icon-cloud /></template>
              节点管理
            </a-menu-item>
            <a-menu-item key="notification">
              <template #icon><icon-notification /></template>
              通知配置
            </a-menu-item>
            <a-menu-item key="backup">
              <template #icon><icon-save /></template>
              备份与恢复
            </a-menu-item>
            <a-menu-item key="log">
              <template #icon><icon-file /></template>
              日志配置
            </a-menu-item>
            <a-menu-item key="cache">
              <template #icon><icon-database /></template>
              缓存配置
            </a-menu-item>
          </a-menu>
        </a-card>
      </a-col>
      
      <a-col :span="18" :xs="24" :sm="24" :md="18">
        <!-- 配置内容区域 -->
        <a-card class="config-card">
          <template #title>
            <div class="config-header">
              <span class="config-title">{{ getConfigTitle() }}</span>
              <a-space>
                <a-button type="primary" @click="handleSaveConfig">
                  <template #icon><icon-save /></template>
                  保存配置
                </a-button>
                <a-button @click="handleResetConfig">
                  <template #icon><icon-refresh /></template>
                  重置
                </a-button>
              </a-space>
            </div>
          </template>
          
          <!-- 基础配置 -->
          <div v-if="activeConfigType === 'basic'" class="config-section">
            <a-form :model="basicConfig" ref="basicConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="siteName" label="系统名称">
                <a-input v-model="basicConfig.siteName" placeholder="请输入系统名称" />
              </a-form-item>
              <a-form-item field="siteDescription" label="系统描述">
                <a-textarea v-model="basicConfig.siteDescription" placeholder="请输入系统描述" />
              </a-form-item>
              <a-form-item field="logo" label="系统Logo">
                <a-upload
                  list-type="picture-card"
                  :file-list="logoFileList"
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
              <a-form-item field="contactEmail" label="联系邮箱">
                <a-input v-model="basicConfig.contactEmail" placeholder="请输入联系邮箱" />
              </a-form-item>
              <a-form-item field="contactPhone" label="联系电话">
                <a-input v-model="basicConfig.contactPhone" placeholder="请输入联系电话" />
              </a-form-item>
              <a-form-item field="recordNumber" label="备案号">
                <a-input v-model="basicConfig.recordNumber" placeholder="请输入备案号" />
              </a-form-item>
              <a-form-item field="copyright" label="版权信息">
                <a-input v-model="basicConfig.copyright" placeholder="请输入版权信息" />
              </a-form-item>
              <a-form-item field="defaultLanguage" label="默认语言">
                <a-select v-model="basicConfig.defaultLanguage" placeholder="请选择默认语言">
                  <a-option value="zh-CN">简体中文</a-option>
                  <a-option value="en-US">English</a-option>
                </a-select>
              </a-form-item>
              <a-form-item field="defaultTheme" label="默认主题">
                <a-select v-model="basicConfig.defaultTheme" placeholder="请选择默认主题">
                  <a-option value="light">浅色</a-option>
                  <a-option value="dark">深色</a-option>
                  <a-option value="auto">跟随系统</a-option>
                </a-select>
              </a-form-item>
            </a-form>
          </div>
          
          <!-- 安全配置 -->
          <div v-if="activeConfigType === 'security'" class="config-section">
            <a-form :model="securityConfig" ref="securityConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="passwordPolicy.minLength" label="密码最小长度">
                <a-input-number v-model="securityConfig.passwordPolicy.minLength" :min="6" :max="20" />
              </a-form-item>
              <a-form-item field="passwordPolicy.requireUppercase" label="要求大写字母">
                <a-switch v-model="securityConfig.passwordPolicy.requireUppercase" />
              </a-form-item>
              <a-form-item field="passwordPolicy.requireLowercase" label="要求小写字母">
                <a-switch v-model="securityConfig.passwordPolicy.requireLowercase" />
              </a-form-item>
              <a-form-item field="passwordPolicy.requireNumbers" label="要求数字">
                <a-switch v-model="securityConfig.passwordPolicy.requireNumbers" />
              </a-form-item>
              <a-form-item field="passwordPolicy.requireSpecialChars" label="要求特殊字符">
                <a-switch v-model="securityConfig.passwordPolicy.requireSpecialChars" />
              </a-form-item>
              <a-form-item field="passwordPolicy.expiryDays" label="密码过期天数">
                <a-input-number v-model="securityConfig.passwordPolicy.expiryDays" :min="0" :max="365" />
                <template #extra>0表示永不过期</template>
              </a-form-item>
              <a-divider />
              <a-form-item field="loginPolicy.maxFailedAttempts" label="最大失败尝试次数">
                <a-input-number v-model="securityConfig.loginPolicy.maxFailedAttempts" :min="3" :max="10" />
              </a-form-item>
              <a-form-item field="loginPolicy.lockoutDuration" label="锁定时长(分钟)">
                <a-input-number v-model="securityConfig.loginPolicy.lockoutDuration" :min="5" :max="1440" />
              </a-form-item>
              <a-form-item field="loginPolicy.enableCaptcha" label="启用验证码">
                <a-switch v-model="securityConfig.loginPolicy.enableCaptcha" />
              </a-form-item>
              <a-form-item field="loginPolicy.enable2FA" label="启用双因素认证">
                <a-switch v-model="securityConfig.loginPolicy.enable2FA" />
              </a-form-item>
              <a-divider />
              <a-form-item field="sessionPolicy.tokenExpiry" label="令牌过期时间(分钟)">
                <a-input-number v-model="securityConfig.sessionPolicy.tokenExpiry" :min="15" :max="1440" />
              </a-form-item>
              <a-form-item field="sessionPolicy.idleTimeout" label="空闲超时时间(分钟)">
                <a-input-number v-model="securityConfig.sessionPolicy.idleTimeout" :min="5" :max="120" />
              </a-form-item>
              <a-form-item field="sessionPolicy.maxConcurrentSessions" label="最大并发会话数">
                <a-input-number v-model="securityConfig.sessionPolicy.maxConcurrentSessions" :min="1" :max="10" />
              </a-form-item>
              <a-divider />
              <a-form-item field="dataPolicy.sensitiveDataMask" label="敏感数据脱敏">
                <a-switch v-model="securityConfig.dataPolicy.sensitiveDataMask" />
              </a-form-item>
              <a-form-item field="dataPolicy.dataRetentionDays" label="数据保留天数">
                <a-input-number v-model="securityConfig.dataPolicy.dataRetentionDays" :min="30" :max="3650" />
              </a-form-item>
            </a-form>
          </div>
          
          <!-- API配置 -->
          <div v-if="activeConfigType === 'api'" class="config-section">
            <a-form :model="apiConfig" ref="apiConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="baseUrl" label="API基础URL">
                <a-input v-model="apiConfig.baseUrl" placeholder="请输入API基础URL" />
              </a-form-item>
              <a-form-item field="timeout" label="请求超时时间(秒)">
                <a-input-number v-model="apiConfig.timeout" :min="5" :max="60" />
              </a-form-item>
              <a-form-item field="retryCount" label="重试次数">
                <a-input-number v-model="apiConfig.retryCount" :min="0" :max="5" />
              </a-form-item>
              <a-form-item field="rateLimitPerMinute" label="每分钟请求限制">
                <a-input-number v-model="apiConfig.rateLimitPerMinute" :min="60" :max="1000" />
              </a-form-item>
              <a-form-item field="enableCache" label="启用API缓存">
                <a-switch v-model="apiConfig.enableCache" />
              </a-form-item>
              <a-form-item field="cacheExpiry" label="缓存过期时间(秒)" v-if="apiConfig.enableCache">
                <a-input-number v-model="apiConfig.cacheExpiry" :min="60" :max="3600" />
              </a-form-item>
              <a-divider />
              <a-form-item field="apiKeys" label="API密钥管理">
                <div class="api-keys-section">
                  <a-table :columns="apiKeyColumns" :data="apiConfig.apiKeys" :pagination="false" row-key="id">
                    <template #operations="{ record }">
                      <a-space>
                        <a-button type="text" size="small" @click="handleViewApiKey(record)">
                          查看
                        </a-button>
                        <a-divider direction="vertical" />
                        <a-popconfirm
                          content="确定要删除此API密钥吗？"
                          @ok="handleDeleteApiKey(record)"
                        >
                          <a-button type="text" status="danger" size="small">
                            删除
                          </a-button>
                        </a-popconfirm>
                      </a-space>
                    </template>
                  </a-table>
                  <div class="api-key-actions">
                    <a-button type="primary" @click="handleAddApiKey">
                      <template #icon><icon-plus /></template>
                      添加API密钥
                    </a-button>
                  </div>
                </div>
              </a-form-item>
            </a-form>
          </div>
          
          <!-- 节点管理 -->
          <div v-if="activeConfigType === 'node'" class="config-section">
            <a-form :model="nodeConfig" ref="nodeConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="centerNodeUrl" label="中心节点URL">
                <a-input v-model="nodeConfig.centerNodeUrl" placeholder="请输入中心节点URL" />
              </a-form-item>
              <a-form-item field="loadBalanceStrategy" label="负载均衡策略">
                <a-select v-model="nodeConfig.loadBalanceStrategy" placeholder="请选择负载均衡策略">
                  <a-option value="round-robin">轮询</a-option>
                  <a-option value="weighted">加权</a-option>
                  <a-option value="least-connection">最少连接</a-option>
                  <a-option value="ip-hash">IP哈希</a-option>
                </a-select>
              </a-form-item>
              <a-form-item field="healthCheckInterval" label="健康检查间隔(秒)">
                <a-input-number v-model="nodeConfig.healthCheckInterval" :min="5" :max="300" />
              </a-form-item>
              <a-form-item field="failoverEnabled" label="启用故障转移">
                <a-switch v-model="nodeConfig.failoverEnabled" />
              </a-form-item>
              <a-form-item field="autoScalingEnabled" label="启用自动扩缩容">
                <a-switch v-model="nodeConfig.autoScalingEnabled" />
              </a-form-item>
              <a-divider />
              <a-form-item field="edgeNodes" label="边缘节点管理">
                <div class="edge-nodes-section">
                  <a-table :columns="edgeNodeColumns" :data="nodeConfig.edgeNodes" :pagination="false" row-key="id">
                    <template #status="{ record }">
                      <a-tag :color="getNodeStatusColor(record.status)">
                        {{ getNodeStatusText(record.status) }}
                      </a-tag>
                    </template>
                    <template #operations="{ record }">
                      <a-space>
                        <a-button type="text" size="small" @click="handleEditNode(record)">
                          编辑
                        </a-button>
                        <a-divider direction="vertical" />
                        <a-button type="text" size="small" @click="handleTestNode(record)">
                          测试
                        </a-button>
                        <a-divider direction="vertical" />
                        <a-popconfirm
                          content="确定要删除此节点吗？"
                          @ok="handleDeleteNode(record)"
                        >
                          <a-button type="text" status="danger" size="small">
                            删除
                          </a-button>
                        </a-popconfirm>
                      </a-space>
                    </template>
                  </a-table>
                  <div class="edge-node-actions">
                    <a-button type="primary" @click="handleAddNode">
                      <template #icon><icon-plus /></template>
                      添加节点
                    </a-button>
                  </div>
                </div>
              </a-form-item>
            </a-form>
          </div>
          
          <!-- 通知配置 -->
          <div v-if="activeConfigType === 'notification'" class="config-section">
            <a-form :model="notificationConfig" ref="notificationConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="email.enabled" label="启用邮件通知">
                <a-switch v-model="notificationConfig.email.enabled" />
              </a-form-item>
              <template v-if="notificationConfig.email.enabled">
                <a-form-item field="email.smtpServer" label="SMTP服务器">
                  <a-input v-model="notificationConfig.email.smtpServer" placeholder="请输入SMTP服务器地址" />
                </a-form-item>
                <a-form-item field="email.smtpPort" label="SMTP端口">
                  <a-input-number v-model="notificationConfig.email.smtpPort" :min="1" :max="65535" />
                </a-form-item>
                <a-form-item field="email.username" label="邮箱账号">
                  <a-input v-model="notificationConfig.email.username" placeholder="请输入邮箱账号" />
                </a-form-item>
                <a-form-item field="email.password" label="邮箱密码">
                  <a-input-password v-model="notificationConfig.email.password" placeholder="请输入邮箱密码" />
                </a-form-item>
                <a-form-item field="email.senderName" label="发件人名称">
                  <a-input v-model="notificationConfig.email.senderName" placeholder="请输入发件人名称" />
                </a-form-item>
                <a-form-item field="email.senderEmail" label="发件人邮箱">
                  <a-input v-model="notificationConfig.email.senderEmail" placeholder="请输入发件人邮箱" />
                </a-form-item>
                <a-form-item field="email.enableSSL" label="启用SSL">
                  <a-switch v-model="notificationConfig.email.enableSSL" />
                </a-form-item>
                <a-form-item>
                  <a-button @click="handleTestEmail">
                    <template #icon><icon-send /></template>
                    测试邮件发送
                  </a-button>
                </a-form-item>
              </template>
              <a-divider />
              <a-form-item field="sms.enabled" label="启用短信通知">
                <a-switch v-model="notificationConfig.sms.enabled" />
              </a-form-item>
              <template v-if="notificationConfig.sms.enabled">
                <a-form-item field="sms.provider" label="短信服务商">
                  <a-select v-model="notificationConfig.sms.provider" placeholder="请选择短信服务商">
                    <a-option value="aliyun">阿里云</a-option>
                    <a-option value="tencent">腾讯云</a-option>
                    <a-option value="netease">网易云</a-option>
                  </a-select>
                </a-form-item>
                <a-form-item field="sms.accessKey" label="AccessKey">
                  <a-input v-model="notificationConfig.sms.accessKey" placeholder="请输入AccessKey" />
                </a-form-item>
                <a-form-item field="sms.secretKey" label="SecretKey">
                  <a-input-password v-model="notificationConfig.sms.secretKey" placeholder="请输入SecretKey" />
                </a-form-item>
                <a-form-item field="sms.signName" label="短信签名">
                  <a-input v-model="notificationConfig.sms.signName" placeholder="请输入短信签名" />
                </a-form-item>
                <a-form-item field="sms.templateCode" label="模板代码">
                  <a-input v-model="notificationConfig.sms.templateCode" placeholder="请输入模板代码" />
                </a-form-item>
                <a-form-item>
                  <a-button @click="handleTestSMS">
                    <template #icon><icon-mobile /></template>
                    测试短信发送
                  </a-button>
                </a-form-item>
              </template>
              <a-divider />
              <a-form-item field="dingtalk.enabled" label="启用钉钉通知">
                <a-switch v-model="notificationConfig.dingtalk.enabled" />
              </a-form-item>
              <template v-if="notificationConfig.dingtalk.enabled">
                <a-form-item field="dingtalk.webhookUrl" label="Webhook URL">
                  <a-input v-model="notificationConfig.dingtalk.webhookUrl" placeholder="请输入钉钉Webhook URL" />
                </a-form-item>
                <a-form-item field="dingtalk.secret" label="加签密钥">
                  <a-input-password v-model="notificationConfig.dingtalk.secret" placeholder="请输入加签密钥" />
                </a-form-item>
                <a-form-item>
                  <a-button @click="handleTestDingTalk">
                    <template #icon><icon-message /></template>
                    测试钉钉通知
                  </a-button>
                </a-form-item>
              </template>
              <a-divider />
              <a-form-item field="pushInterval" label="推送间隔(分钟)">
                <a-input-number v-model="notificationConfig.pushInterval" :min="1" :max="1440" />
              </a-form-item>
              <a-form-item field="maxPushPerDay" label="每日最大推送数">
                <a-input-number v-model="notificationConfig.maxPushPerDay" :min="1" :max="100" />
              </a-form-item>
            </a-form>
          </div>
          
          <!-- 备份与恢复 -->
          <div v-if="activeConfigType === 'backup'" class="config-section">
            <a-form :model="backupConfig" ref="backupConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="autoBackup" label="启用自动备份">
                <a-switch v-model="backupConfig.autoBackup" />
              </a-form-item>
              <template v-if="backupConfig.autoBackup">
                <a-form-item field="backupFrequency" label="备份频率">
                  <a-select v-model="backupConfig.backupFrequency" placeholder="请选择备份频率">
                    <a-option value="daily">每日</a-option>
                    <a-option value="weekly">每周</a-option>
                    <a-option value="monthly">每月</a-option>
                  </a-select>
                </a-form-item>
                <a-form-item field="backupTime" label="备份时间">
                  <a-time-picker v-model="backupConfig.backupTime" format="HH:mm" />
                </a-form-item>
                <a-form-item field="backupDay" label="备份日" v-if="backupConfig.backupFrequency === 'weekly'">
                  <a-select v-model="backupConfig.backupDay" placeholder="请选择备份日">
                    <a-option value="1">周一</a-option>
                    <a-option value="2">周二</a-option>
                    <a-option value="3">周三</a-option>
                    <a-option value="4">周四</a-option>
                    <a-option value="5">周五</a-option>
                    <a-option value="6">周六</a-option>
                    <a-option value="0">周日</a-option>
                  </a-select>
                </a-form-item>
                <a-form-item field="backupDate" label="备份日期" v-if="backupConfig.backupFrequency === 'monthly'">
                  <a-input-number v-model="backupConfig.backupDate" :min="1" :max="28" />
                </a-form-item>
              </template>
              <a-form-item field="backupRetention" label="备份保留天数">
                <a-input-number v-model="backupConfig.backupRetention" :min="1" :max="365" />
              </a-form-item>
              <a-form-item field="backupLocation" label="备份存储位置">
                <a-select v-model="backupConfig.backupLocation" placeholder="请选择备份存储位置">
                  <a-option value="local">本地存储</a-option>
                  <a-option value="s3">Amazon S3</a-option>
                  <a-option value="oss">阿里云OSS</a-option>
                  <a-option value="cos">腾讯云COS</a-option>
                </a-select>
              </a-form-item>
              <template v-if="backupConfig.backupLocation !== 'local'">
                <a-form-item field="cloudStorage.accessKey" label="AccessKey">
                  <a-input v-model="backupConfig.cloudStorage.accessKey" placeholder="请输入AccessKey" />
                </a-form-item>
                <a-form-item field="cloudStorage.secretKey" label="SecretKey">
                  <a-input-password v-model="backupConfig.cloudStorage.secretKey" placeholder="请输入SecretKey" />
                </a-form-item>
                <a-form-item field="cloudStorage.bucket" label="Bucket">
                  <a-input v-model="backupConfig.cloudStorage.bucket" placeholder="请输入Bucket名称" />
                </a-form-item>
                <a-form-item field="cloudStorage.region" label="区域">
                  <a-input v-model="backupConfig.cloudStorage.region" placeholder="请输入区域" />
                </a-form-item>
              </template>
              <a-divider />
              <a-form-item>
                <a-space>
                  <a-button type="primary" @click="handleManualBackup">
                    <template #icon><icon-download /></template>
                    立即备份
                  </a-button>
                  <a-button @click="handleViewBackups">
                    <template #icon><icon-list /></template>
                    查看备份
                  </a-button>
                </a-space>
              </a-form-item>
            </a-form>
          </div>
          
          <!-- 日志配置 -->
          <div v-if="activeConfigType === 'log'" class="config-section">
            <a-form :model="logConfig" ref="logConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="logLevel" label="日志级别">
                <a-select v-model="logConfig.logLevel" placeholder="请选择日志级别">
                  <a-option value="debug">Debug</a-option>
                  <a-option value="info">Info</a-option>
                  <a-option value="warn">Warn</a-option>
                  <a-option value="error">Error</a-option>
                </a-select>
              </a-form-item>
              <a-form-item field="logRetention" label="日志保留天数">
                <a-input-number v-model="logConfig.logRetention" :min="7" :max="365" />
              </a-form-item>
              <a-form-item field="enableAccessLog" label="启用访问日志">
                <a-switch v-model="logConfig.enableAccessLog" />
              </a-form-item>
              <a-form-item field="enableErrorLog" label="启用错误日志">
                <a-switch v-model="logConfig.enableErrorLog" />
              </a-form-item>
              <a-form-item field="enableOperationLog" label="启用操作日志">
                <a-switch v-model="logConfig.enableOperationLog" />
              </a-form-item>
              <a-form-item field="enableLoginLog" label="启用登录日志">
                <a-switch v-model="logConfig.enableLoginLog" />
              </a-form-item>
              <a-form-item field="logFormat" label="日志格式">
                <a-select v-model="logConfig.logFormat" placeholder="请选择日志格式">
                  <a-option value="text">文本</a-option>
                  <a-option value="json">JSON</a-option>
                </a-select>
              </a-form-item>
              <a-form-item field="logOutput" label="日志输出">
                <a-select v-model="logConfig.logOutput" placeholder="请选择日志输出">
                  <a-option value="file">文件</a-option>
                  <a-option value="console">控制台</a-option>
                  <a-option value="both">文件和控制台</a-option>
                </a-select>
              </a-form-item>
              <a-divider />
              <a-form-item>
                <a-space>
                  <a-button @click="handleViewLogs">
                    <template #icon><icon-file /></template>
                    查看日志
                  </a-button>
                  <a-button status="danger" @click="handleClearLogs">
                    <template #icon><icon-delete /></template>
                    清除日志
                  </a-button>
                </a-space>
              </a-form-item>
            </a-form>
          </div>
          
          <!-- 缓存配置 -->
          <div v-if="activeConfigType === 'cache'" class="config-section">
            <a-form :model="cacheConfig" ref="cacheConfigForm" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
              <a-form-item field="enableCache" label="启用缓存">
                <a-switch v-model="cacheConfig.enableCache" />
              </a-form-item>
              <template v-if="cacheConfig.enableCache">
                <a-form-item field="cacheType" label="缓存类型">
                  <a-select v-model="cacheConfig.cacheType" placeholder="请选择缓存类型">
                    <a-option value="memory">内存缓存</a-option>
                    <a-option value="redis">Redis</a-option>
                    <a-option value="memcached">Memcached</a-option>
                  </a-select>
                </a-form-item>
                <template v-if="cacheConfig.cacheType !== 'memory'">
                  <a-form-item field="cacheServer" label="缓存服务器">
                    <a-input v-model="cacheConfig.cacheServer" placeholder="请输入缓存服务器地址" />
                  </a-form-item>
                  <a-form-item field="cachePort" label="缓存端口">
                    <a-input-number v-model="cacheConfig.cachePort" :min="1" :max="65535" />
                  </a-form-item>
                  <a-form-item field="cachePassword" label="缓存密码">
                    <a-input-password v-model="cacheConfig.cachePassword" placeholder="请输入缓存密码" />
                  </a-form-item>
                  <a-form-item field="cacheDatabase" label="缓存数据库" v-if="cacheConfig.cacheType === 'redis'">
                    <a-input-number v-model="cacheConfig.cacheDatabase" :min="0" :max="15" />
                  </a-form-item>
                </template>
                <a-form-item field="defaultExpiry" label="默认过期时间(秒)">
                  <a-input-number v-model="cacheConfig.defaultExpiry" :min="60" :max="86400" />
                </a-form-item>
                <a-form-item field="maxCacheSize" label="最大缓存大小(MB)">
                  <a-input-number v-model="cacheConfig.maxCacheSize" :min="10" :max="1024" />
                </a-form-item>
              </template>
              <a-divider />
              <a-form-item>
                <a-space>
                  <a-button @click="handleTestCache">
                    <template #icon><icon-check-circle /></template>
                    测试缓存连接
                  </a-button>
                  <a-button status="danger" @click="handleClearCache">
                    <template #icon><icon-delete /></template>
                    清除缓存
                  </a-button>
                </a-space>
              </a-form-item>
            </a-form>
          </div>
        </a-card>
      </a-col>
    </a-row>
    
    <!-- API密钥弹窗 -->
    <a-modal
      v-model:visible="apiKeyModalVisible"
      :title="isEditApiKey ? '编辑API密钥' : '添加API密钥'"
      @cancel="closeApiKeyModal"
      @before-ok="handleSubmitApiKey"
    >
      <a-form :model="apiKeyForm" ref="apiKeyFormRef" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="name" label="名称" required>
          <a-input v-model="apiKeyForm.name" placeholder="请输入API密钥名称" />
        </a-form-item>
        <a-form-item field="description" label="描述">
          <a-textarea v-model="apiKeyForm.description" placeholder="请输入API密钥描述" />
        </a-form-item>
        <a-form-item field="expiryDate" label="过期日期">
          <a-date-picker v-model="apiKeyForm.expiryDate" placeholder="请选择过期日期" style="width: 100%" />
        </a-form-item>
        <a-form-item field="permissions" label="权限" required>
          <a-checkbox-group v-model="apiKeyForm.permissions">
            <a-checkbox value="read">读取</a-checkbox>
            <a-checkbox value="write">写入</a-checkbox>
            <a-checkbox value="delete">删除</a-checkbox>
          </a-checkbox-group>
        </a-form-item>
      </a-form>
    </a-modal>
    
    <!-- 节点弹窗 -->
    <a-modal
      v-model:visible="nodeModalVisible"
      :title="isEditNode ? '编辑节点' : '添加节点'"
      @cancel="closeNodeModal"
      @before-ok="handleSubmitNode"
    >
      <a-form :model="nodeForm" ref="nodeFormRef" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="name" label="节点名称" required>
          <a-input v-model="nodeForm.name" placeholder="请输入节点名称" />
        </a-form-item>
        <a-form-item field="url" label="节点URL" required>
          <a-input v-model="nodeForm.url" placeholder="请输入节点URL" />
        </a-form-item>
        <a-form-item field="type" label="节点类型" required>
          <a-select v-model="nodeForm.type" placeholder="请选择节点类型">
            <a-option value="cloudflare">Cloudflare Worker</a-option>
            <a-option value="server">服务器</a-option>
            <a-option value="serverless">Serverless</a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="region" label="区域">
          <a-select v-model="nodeForm.region" placeholder="请选择区域">
            <a-option value="cn-north">华北</a-option>
            <a-option value="cn-east">华东</a-option>
            <a-option value="cn-south">华南</a-option>
            <a-option value="us-west">美国西部</a-option>
            <a-option value="us-east">美国东部</a-option>
            <a-option value="eu-central">欧洲中部</a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="weight" label="权重">
          <a-input-number v-model="nodeForm.weight" :min="1" :max="100" />
        </a-form-item>
        <a-form-item field="maxConnections" label="最大连接数">
          <a-input-number v-model="nodeForm.maxConnections" :min="10" :max="1000" />
        </a-form-item>
        <a-form-item field="timeout" label="超时时间(秒)">
          <a-input-number v-model="nodeForm.timeout" :min="5" :max="60" />
        </a-form-item>
        <a-form-item field="enabled" label="启用">
          <a-switch v-model="nodeForm.enabled" />
        </a-form-item>
      </a-form>
    </a-modal>
    
    <!-- 备份列表弹窗 -->
    <a-modal
      v-model:visible="backupListModalVisible"
      title="备份列表"
      @cancel="closeBackupListModal"
      width="800px"
    >
      <a-table :columns="backupColumns" :data="backupList" :pagination="backupPagination" row-key="id">
        <template #operations="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleRestoreBackup(record)">
              恢复
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleDownloadBackup(record)">
              下载
            </a-button>
            <a-divider direction="vertical" />
            <a-popconfirm
              content="确定要删除此备份吗？"
              @ok="handleDeleteBackup(record)"
            >
              <a-button type="text" status="danger" size="small">
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </a-table>
    </a-modal>
    
    <!-- 日志查看弹窗 -->
    <a-modal
      v-model:visible="logViewModalVisible"
      title="日志查看"
      @cancel="closeLogViewModal"
      width="800px"
    >
      <a-tabs>
        <a-tab-pane key="access" title="访问日志">
          <a-textarea v-model="accessLogContent" readonly :auto-size="{ minRows: 10, maxRows: 20 }" />
        </a-tab-pane>
        <a-tab-pane key="error" title="错误日志">
          <a-textarea v-model="errorLogContent" readonly :auto-size="{ minRows: 10, maxRows: 20 }" />
        </a-tab-pane>
        <a-tab-pane key="operation" title="操作日志">
          <a-textarea v-model="operationLogContent" readonly :auto-size="{ minRows: 10, maxRows: 20 }" />
        </a-tab-pane>
        <a-tab-pane key="login" title="登录日志">
          <a-textarea v-model="loginLogContent" readonly :auto-size="{ minRows: 10, maxRows: 20 }" />
        </a-tab-pane>
      </a-tabs>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { Message } from '@arco-design/web-vue';

export default {
  setup() {
    // 当前配置类型
    const activeConfigType = ref('basic');
    
    // 基础配置
    const basicConfig = reactive({
      siteName: 'ScoreX查分星',
      siteDescription: '面向中学生的成绩查询与考试分析平台',
      logo: '',
      contactEmail: 'support@scorex.com',
      contactPhone: '400-123-4567',
      recordNumber: '京ICP备12345678号',
      copyright: '© 2025 ScoreX查分星 版权所有',
      defaultLanguage: 'zh-CN',
      defaultTheme: 'light'
    });
    
    // 安全配置
    const securityConfig = reactive({
      passwordPolicy: {
        minLength: 8,
        requireUppercase: true,
        requireLowercase: true,
        requireNumbers: true,
        requireSpecialChars: true,
        expiryDays: 90
      },
      loginPolicy: {
        maxFailedAttempts: 5,
        lockoutDuration: 30,
        enableCaptcha: true,
        enable2FA: false
      },
      sessionPolicy: {
        tokenExpiry: 120,
        idleTimeout: 30,
        maxConcurrentSessions: 3
      },
      dataPolicy: {
        sensitiveDataMask: true,
        dataRetentionDays: 365
      }
    });
    
    // API配置
    const apiConfig = reactive({
      baseUrl: 'https://api.scorex.com',
      timeout: 30,
      retryCount: 3,
      rateLimitPerMinute: 300,
      enableCache: true,
      cacheExpiry: 300,
      apiKeys: [
        {
          id: 'api-key-001',
          name: '开发环境',
          key: 'sk_dev_123456789abcdef',
          description: '开发环境使用的API密钥',
          createdAt: '2025-01-15',
          expiryDate: '2026-01-15',
          permissions: ['read', 'write']
        },
        {
          id: 'api-key-002',
          name: '生产环境',
          key: 'sk_prod_abcdef123456789',
          description: '生产环境使用的API密钥',
          createdAt: '2025-01-15',
          expiryDate: '2026-01-15',
          permissions: ['read', 'write', 'delete']
        }
      ]
    });
    
    // 节点配置
    const nodeConfig = reactive({
      centerNodeUrl: 'https://center.scorex.com',
      loadBalanceStrategy: 'round-robin',
      healthCheckInterval: 30,
      failoverEnabled: true,
      autoScalingEnabled: false,
      edgeNodes: [
        {
          id: 'node-001',
          name: '华北节点1',
          url: 'https://edge1.scorex.com',
          type: 'server',
          region: 'cn-north',
          weight: 100,
          maxConnections: 500,
          timeout: 30,
          status: 'online',
          enabled: true
        },
        {
          id: 'node-002',
          name: '华东节点1',
          url: 'https://edge2.scorex.com',
          type: 'server',
          region: 'cn-east',
          weight: 100,
          maxConnections: 500,
          timeout: 30,
          status: 'online',
          enabled: true
        },
        {
          id: 'node-003',
          name: 'Cloudflare节点',
          url: 'https://worker.scorex.workers.dev',
          type: 'cloudflare',
          region: 'global',
          weight: 50,
          maxConnections: 200,
          timeout: 15,
          status: 'online',
          enabled: true
        },
        {
          id: 'node-004',
          name: '华南节点1',
          url: 'https://edge3.scorex.com',
          type: 'server',
          region: 'cn-south',
          weight: 80,
          maxConnections: 400,
          timeout: 30,
          status: 'offline',
          enabled: false
        }
      ]
    });
    
    // 通知配置
    const notificationConfig = reactive({
      email: {
        enabled: true,
        smtpServer: 'smtp.exmail.qq.com',
        smtpPort: 465,
        username: 'notification@scorex.com',
        password: '********',
        senderName: 'ScoreX查分星',
        senderEmail: 'notification@scorex.com',
        enableSSL: true
      },
      sms: {
        enabled: true,
        provider: 'aliyun',
        accessKey: 'LTAI4G*************',
        secretKey: '********',
        signName: 'ScoreX查分星',
        templateCode: 'SMS_123456789'
      },
      dingtalk: {
        enabled: true,
        webhookUrl: 'https://oapi.dingtalk.com/robot/send?access_token=******',
        secret: '********'
      },
      pushInterval: 15,
      maxPushPerDay: 5
    });
    
    // 备份配置
    const backupConfig = reactive({
      autoBackup: true,
      backupFrequency: 'daily',
      backupTime: '03:00',
      backupDay: '1',
      backupDate: 1,
      backupRetention: 30,
      backupLocation: 'local',
      cloudStorage: {
        accessKey: '',
        secretKey: '',
        bucket: '',
        region: ''
      }
    });
    
    // 日志配置
    const logConfig = reactive({
      logLevel: 'info',
      logRetention: 30,
      enableAccessLog: true,
      enableErrorLog: true,
      enableOperationLog: true,
      enableLoginLog: true,
      logFormat: 'json',
      logOutput: 'file'
    });
    
    // 缓存配置
    const cacheConfig = reactive({
      enableCache: true,
      cacheType: 'redis',
      cacheServer: 'localhost',
      cachePort: 6379,
      cachePassword: '',
      cacheDatabase: 0,
      defaultExpiry: 3600,
      maxCacheSize: 100
    });
    
    // API密钥表单
    const apiKeyForm = reactive({
      id: '',
      name: '',
      description: '',
      expiryDate: null,
      permissions: ['read']
    });
    
    // 节点表单
    const nodeForm = reactive({
      id: '',
      name: '',
      url: '',
      type: 'server',
      region: 'cn-north',
      weight: 100,
      maxConnections: 500,
      timeout: 30,
      enabled: true
    });
    
    // 文件列表
    const logoFileList = ref([]);
    
    // 表单引用
    const basicConfigForm = ref(null);
    const securityConfigForm = ref(null);
    const apiConfigForm = ref(null);
    const nodeConfigForm = ref(null);
    const notificationConfigForm = ref(null);
    const backupConfigForm = ref(null);
    const logConfigForm = ref(null);
    const cacheConfigForm = ref(null);
    const apiKeyFormRef = ref(null);
    const nodeFormRef = ref(null);
    
    // 状态变量
    const apiKeyModalVisible = ref(false);
    const nodeModalVisible = ref(false);
    const backupListModalVisible = ref(false);
    const logViewModalVisible = ref(false);
    const isEditApiKey = ref(false);
    const isEditNode = ref(false);
    
    // 备份列表
    const backupList = ref([]);
    const backupPagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0
    });
    
    // 日志内容
    const accessLogContent = ref('');
    const errorLogContent = ref('');
    const operationLogContent = ref('');
    const loginLogContent = ref('');
    
    // API密钥列
    const apiKeyColumns = [
      {
        title: '名称',
        dataIndex: 'name'
      },
      {
        title: '创建时间',
        dataIndex: 'createdAt'
      },
      {
        title: '过期时间',
        dataIndex: 'expiryDate'
      },
      {
        title: '权限',
        dataIndex: 'permissions',
        render: ({ record }) => {
          return record.permissions.join(', ');
        }
      },
      {
        title: '操作',
        slotName: 'operations',
        width: 150
      }
    ];
    
    // 边缘节点列
    const edgeNodeColumns = [
      {
        title: '节点名称',
        dataIndex: 'name'
      },
      {
        title: '节点URL',
        dataIndex: 'url',
        ellipsis: true
      },
      {
        title: '类型',
        dataIndex: 'type',
        render: ({ record }) => {
          return getNodeTypeText(record.type);
        }
      },
      {
        title: '区域',
        dataIndex: 'region',
        render: ({ record }) => {
          return getRegionText(record.region);
        }
      },
      {
        title: '权重',
        dataIndex: 'weight'
      },
      {
        title: '状态',
        slotName: 'status'
      },
      {
        title: '操作',
        slotName: 'operations',
        width: 200
      }
    ];
    
    // 备份列
    const backupColumns = [
      {
        title: '备份名称',
        dataIndex: 'name'
      },
      {
        title: '备份时间',
        dataIndex: 'createdAt'
      },
      {
        title: '备份大小',
        dataIndex: 'size'
      },
      {
        title: '备份类型',
        dataIndex: 'type'
      },
      {
        title: '存储位置',
        dataIndex: 'location'
      },
      {
        title: '操作',
        slotName: 'operations',
        width: 200
      }
    ];
    
    // 生命周期钩子
    onMounted(() => {
      // 初始化Logo文件列表
      if (basicConfig.logo) {
        logoFileList.value = [
          {
            uid: '1',
            name: 'logo.png',
            url: basicConfig.logo
          }
        ];
      }
      
      // 初始化备份列表
      generateMockBackups();
      
      // 初始化日志内容
      generateMockLogs();
    });
    
    // 获取配置标题
    const getConfigTitle = () => {
      switch (activeConfigType.value) {
        case 'basic':
          return '基础配置';
        case 'security':
          return '安全配置';
        case 'api':
          return 'API配置';
        case 'node':
          return '节点管理';
        case 'notification':
          return '通知配置';
        case 'backup':
          return '备份与恢复';
        case 'log':
          return '日志配置';
        case 'cache':
          return '缓存配置';
        default:
          return '系统配置';
      }
    };
    
    // 获取节点类型文本
    const getNodeTypeText = (type) => {
      switch (type) {
        case 'cloudflare':
          return 'Cloudflare Worker';
        case 'server':
          return '服务器';
        case 'serverless':
          return 'Serverless';
        default:
          return '未知';
      }
    };
    
    // 获取区域文本
    const getRegionText = (region) => {
      switch (region) {
        case 'cn-north':
          return '华北';
        case 'cn-east':
          return '华东';
        case 'cn-south':
          return '华南';
        case 'us-west':
          return '美国西部';
        case 'us-east':
          return '美国东部';
        case 'eu-central':
          return '欧洲中部';
        case 'global':
          return '全球';
        default:
          return '未知';
      }
    };
    
    // 获取节点状态文本
    const getNodeStatusText = (status) => {
      switch (status) {
        case 'online':
          return '在线';
        case 'offline':
          return '离线';
        case 'error':
          return '错误';
        case 'maintenance':
          return '维护中';
        default:
          return '未知';
      }
    };
    
    // 获取节点状态颜色
    const getNodeStatusColor = (status) => {
      switch (status) {
        case 'online':
          return 'green';
        case 'offline':
          return 'red';
        case 'error':
          return 'orange';
        case 'maintenance':
          return 'blue';
        default:
          return 'gray';
      }
    };
    
    // 生成模拟备份
    const generateMockBackups = () => {
      const backups = [];
      const types = ['完整备份', '增量备份', '数据库备份'];
      const locations = ['本地存储', 'Amazon S3', '阿里云OSS'];
      
      for (let i = 1; i <= 20; i++) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const createdAt = date.toISOString().split('T')[0] + ' ' + 
                        String(Math.floor(Math.random() * 24)).padStart(2, '0') + ':' +
                        String(Math.floor(Math.random() * 60)).padStart(2, '0') + ':' +
                        String(Math.floor(Math.random() * 60)).padStart(2, '0');
        
        backups.push({
          id: `backup-${i.toString().padStart(3, '0')}`,
          name: `备份_${date.toISOString().split('T')[0]}`,
          createdAt,
          size: `${Math.floor(Math.random() * 900) + 100} MB`,
          type: types[Math.floor(Math.random() * types.length)],
          location: locations[Math.floor(Math.random() * locations.length)]
        });
      }
      
      backupList.value = backups;
      backupPagination.total = backups.length;
    };
    
    // 生成模拟日志
    const generateMockLogs = () => {
      accessLogContent.value = `[2025-03-24 10:15:23] 192.168.1.100 - GET /api/exams HTTP/1.1 200 0.123s
[2025-03-24 10:15:25] 192.168.1.101 - GET /api/scores HTTP/1.1 200 0.098s
[2025-03-24 10:15:30] 192.168.1.102 - POST /api/auth/login HTTP/1.1 200 0.187s
[2025-03-24 10:15:35] 192.168.1.103 - GET /api/users/profile HTTP/1.1 200 0.076s
[2025-03-24 10:15:40] 192.168.1.104 - GET /api/diagnostic/reports HTTP/1.1 200 0.156s
[2025-03-24 10:15:45] 192.168.1.105 - GET /api/learning/materials HTTP/1.1 200 0.112s
[2025-03-24 10:15:50] 192.168.1.106 - POST /api/notifications/read HTTP/1.1 200 0.065s
[2025-03-24 10:15:55] 192.168.1.107 - GET /api/exams/details/123 HTTP/1.1 200 0.143s
[2025-03-24 10:16:00] 192.168.1.108 - GET /api/scores/analysis/456 HTTP/1.1 200 0.178s
[2025-03-24 10:16:05] 192.168.1.109 - POST /api/auth/logout HTTP/1.1 200 0.054s`;
      
      errorLogContent.value = `[2025-03-24 09:12:34] [ERROR] Failed to connect to database: Connection timed out
[2025-03-24 09:15:45] [ERROR] API request failed: https://api.example.com/data - 500 Internal Server Error
[2025-03-24 10:23:12] [ERROR] Invalid user input: Missing required field 'email'
[2025-03-24 11:34:56] [ERROR] File upload failed: Permission denied
[2025-03-24 12:45:23] [ERROR] Memory limit exceeded in process: score-analysis
[2025-03-24 13:56:34] [ERROR] Cache write failed: Redis connection error
[2025-03-24 14:23:45] [ERROR] Authentication failed for user: user123
[2025-03-24 15:34:12] [ERROR] API rate limit exceeded for IP: 192.168.1.100
[2025-03-24 16:45:23] [ERROR] Failed to send notification: SMTP connection refused
[2025-03-24 17:56:34] [ERROR] Edge node connection failed: https://edge1.scorex.com - Timeout`;
      
      operationLogContent.value = `[2025-03-24 08:12:34] [ADMIN] admin1 - Created new user: student123
[2025-03-24 08:23:45] [ADMIN] admin1 - Updated system configuration: security settings
[2025-03-24 09:34:56] [ADMIN] admin2 - Deleted exam record: exam-123
[2025-03-24 10:45:12] [ADMIN] admin1 - Added new learning material: Math-Functions-Guide
[2025-03-24 11:56:23] [ADMIN] admin2 - Updated user permissions for: teacher456
[2025-03-24 12:12:34] [ADMIN] admin1 - Performed system backup: backup-20250324-1
[2025-03-24 13:23:45] [ADMIN] admin3 - Sent notification to all users: System maintenance
[2025-03-24 14:34:56] [ADMIN] admin2 - Added new edge node: edge5.scorex.com
[2025-03-24 15:45:12] [ADMIN] admin1 - Generated diagnostic reports for class: class-10A
[2025-03-24 16:56:23] [ADMIN] admin3 - Cleared system cache`;
      
      loginLogContent.value = `[2025-03-24 07:12:34] [LOGIN] admin1 - Login successful from 192.168.1.100
[2025-03-24 07:23:45] [LOGIN] student123 - Login successful from 192.168.1.101
[2025-03-24 07:34:56] [LOGIN] teacher456 - Login successful from 192.168.1.102
[2025-03-24 07:45:12] [LOGIN] unknown - Login failed from 192.168.1.103 (Invalid credentials)
[2025-03-24 08:56:23] [LOGIN] student456 - Login successful from 192.168.1.104
[2025-03-24 09:12:34] [LOGIN] admin2 - Login successful from 192.168.1.105
[2025-03-24 10:23:45] [LOGIN] unknown - Login failed from 192.168.1.106 (Account locked)
[2025-03-24 11:34:56] [LOGIN] student789 - Login successful from 192.168.1.107
[2025-03-24 12:45:12] [LOGIN] teacher789 - Login successful from 192.168.1.108
[2025-03-24 13:56:23] [LOGIN] admin3 - Login successful from 192.168.1.109`;
    };
    
    // 处理菜单点击
    const handleMenuClick = (key) => {
      activeConfigType.value = key;
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
        
        logoFileList.value = [{ name: file.name, url }];
        basicConfig.logo = url;
        
        onSuccess();
      }, 500);
    };
    
    // 保存配置
    const handleSaveConfig = () => {
      // 根据当前配置类型保存对应的配置
      switch (activeConfigType.value) {
        case 'basic':
          Message.success('基础配置保存成功');
          break;
        case 'security':
          Message.success('安全配置保存成功');
          break;
        case 'api':
          Message.success('API配置保存成功');
          break;
        case 'node':
          Message.success('节点配置保存成功');
          break;
        case 'notification':
          Message.success('通知配置保存成功');
          break;
        case 'backup':
          Message.success('备份配置保存成功');
          break;
        case 'log':
          Message.success('日志配置保存成功');
          break;
        case 'cache':
          Message.success('缓存配置保存成功');
          break;
        default:
          Message.success('配置保存成功');
      }
    };
    
    // 重置配置
    const handleResetConfig = () => {
      // 根据当前配置类型重置对应的配置
      switch (activeConfigType.value) {
        case 'basic':
          // 重置基础配置
          basicConfig.siteName = 'ScoreX查分星';
          basicConfig.siteDescription = '面向中学生的成绩查询与考试分析平台';
          basicConfig.logo = '';
          basicConfig.contactEmail = 'support@scorex.com';
          basicConfig.contactPhone = '400-123-4567';
          basicConfig.recordNumber = '京ICP备12345678号';
          basicConfig.copyright = '© 2025 ScoreX查分星 版权所有';
          basicConfig.defaultLanguage = 'zh-CN';
          basicConfig.defaultTheme = 'light';
          logoFileList.value = [];
          Message.success('基础配置已重置');
          break;
        case 'security':
          // 重置安全配置
          securityConfig.passwordPolicy.minLength = 8;
          securityConfig.passwordPolicy.requireUppercase = true;
          securityConfig.passwordPolicy.requireLowercase = true;
          securityConfig.passwordPolicy.requireNumbers = true;
          securityConfig.passwordPolicy.requireSpecialChars = true;
          securityConfig.passwordPolicy.expiryDays = 90;
          securityConfig.loginPolicy.maxFailedAttempts = 5;
          securityConfig.loginPolicy.lockoutDuration = 30;
          securityConfig.loginPolicy.enableCaptcha = true;
          securityConfig.loginPolicy.enable2FA = false;
          securityConfig.sessionPolicy.tokenExpiry = 120;
          securityConfig.sessionPolicy.idleTimeout = 30;
          securityConfig.sessionPolicy.maxConcurrentSessions = 3;
          securityConfig.dataPolicy.sensitiveDataMask = true;
          securityConfig.dataPolicy.dataRetentionDays = 365;
          Message.success('安全配置已重置');
          break;
        // 其他配置类型的重置逻辑...
        default:
          Message.success('配置已重置');
      }
    };
    
    // 查看API密钥
    const handleViewApiKey = (record) => {
      Message.info(`API密钥: ${record.key}`);
    };
    
    // 添加API密钥
    const handleAddApiKey = () => {
      isEditApiKey.value = false;
      apiKeyForm.id = '';
      apiKeyForm.name = '';
      apiKeyForm.description = '';
      apiKeyForm.expiryDate = null;
      apiKeyForm.permissions = ['read'];
      apiKeyModalVisible.value = true;
    };
    
    // 删除API密钥
    const handleDeleteApiKey = (record) => {
      const index = apiConfig.apiKeys.findIndex(item => item.id === record.id);
      if (index !== -1) {
        apiConfig.apiKeys.splice(index, 1);
        Message.success('API密钥删除成功');
      }
    };
    
    // 提交API密钥
    const handleSubmitApiKey = (done) => {
      if (!apiKeyForm.name) {
        Message.error('请输入API密钥名称');
        done(false);
        return;
      }
      
      if (apiKeyForm.permissions.length === 0) {
        Message.error('请选择至少一个权限');
        done(false);
        return;
      }
      
      const now = new Date();
      const formattedDate = now.toISOString().split('T')[0];
      
      if (isEditApiKey.value) {
        // 编辑现有API密钥
        const index = apiConfig.apiKeys.findIndex(item => item.id === apiKeyForm.id);
        if (index !== -1) {
          apiConfig.apiKeys[index].name = apiKeyForm.name;
          apiConfig.apiKeys[index].description = apiKeyForm.description;
          apiConfig.apiKeys[index].expiryDate = apiKeyForm.expiryDate ? apiKeyForm.expiryDate : null;
          apiConfig.apiKeys[index].permissions = apiKeyForm.permissions;
          Message.success('API密钥更新成功');
        }
      } else {
        // 添加新API密钥
        const newKey = {
          id: `api-key-${Date.now().toString(36)}`,
          name: apiKeyForm.name,
          key: `sk_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`,
          description: apiKeyForm.description,
          createdAt: formattedDate,
          expiryDate: apiKeyForm.expiryDate ? apiKeyForm.expiryDate : null,
          permissions: apiKeyForm.permissions
        };
        
        apiConfig.apiKeys.push(newKey);
        Message.success('API密钥创建成功');
      }
      
      closeApiKeyModal();
      done();
    };
    
    // 关闭API密钥弹窗
    const closeApiKeyModal = () => {
      apiKeyModalVisible.value = false;
    };
    
    // 编辑节点
    const handleEditNode = (record) => {
      isEditNode.value = true;
      nodeForm.id = record.id;
      nodeForm.name = record.name;
      nodeForm.url = record.url;
      nodeForm.type = record.type;
      nodeForm.region = record.region;
      nodeForm.weight = record.weight;
      nodeForm.maxConnections = record.maxConnections;
      nodeForm.timeout = record.timeout;
      nodeForm.enabled = record.enabled;
      nodeModalVisible.value = true;
    };
    
    // 添加节点
    const handleAddNode = () => {
      isEditNode.value = false;
      nodeForm.id = '';
      nodeForm.name = '';
      nodeForm.url = '';
      nodeForm.type = 'server';
      nodeForm.region = 'cn-north';
      nodeForm.weight = 100;
      nodeForm.maxConnections = 500;
      nodeForm.timeout = 30;
      nodeForm.enabled = true;
      nodeModalVisible.value = true;
    };
    
    // 测试节点
    const handleTestNode = (record) => {
      Message.loading('正在测试节点连接...');
      
      // 模拟测试过程
      setTimeout(() => {
        if (record.status === 'online') {
          Message.success(`节点 ${record.name} 连接正常，延迟: 45ms`);
        } else {
          Message.error(`节点 ${record.name} 连接失败`);
        }
      }, 1500);
    };
    
    // 删除节点
    const handleDeleteNode = (record) => {
      const index = nodeConfig.edgeNodes.findIndex(item => item.id === record.id);
      if (index !== -1) {
        nodeConfig.edgeNodes.splice(index, 1);
        Message.success('节点删除成功');
      }
    };
    
    // 提交节点
    const handleSubmitNode = (done) => {
      if (!nodeForm.name) {
        Message.error('请输入节点名称');
        done(false);
        return;
      }
      
      if (!nodeForm.url) {
        Message.error('请输入节点URL');
        done(false);
        return;
      }
      
      if (isEditNode.value) {
        // 编辑现有节点
        const index = nodeConfig.edgeNodes.findIndex(item => item.id === nodeForm.id);
        if (index !== -1) {
          nodeConfig.edgeNodes[index].name = nodeForm.name;
          nodeConfig.edgeNodes[index].url = nodeForm.url;
          nodeConfig.edgeNodes[index].type = nodeForm.type;
          nodeConfig.edgeNodes[index].region = nodeForm.region;
          nodeConfig.edgeNodes[index].weight = nodeForm.weight;
          nodeConfig.edgeNodes[index].maxConnections = nodeForm.maxConnections;
          nodeConfig.edgeNodes[index].timeout = nodeForm.timeout;
          nodeConfig.edgeNodes[index].enabled = nodeForm.enabled;
          Message.success('节点更新成功');
        }
      } else {
        // 添加新节点
        const newNode = {
          id: `node-${Date.now().toString(36)}`,
          name: nodeForm.name,
          url: nodeForm.url,
          type: nodeForm.type,
          region: nodeForm.region,
          weight: nodeForm.weight,
          maxConnections: nodeForm.maxConnections,
          timeout: nodeForm.timeout,
          status: 'online',
          enabled: nodeForm.enabled
        };
        
        nodeConfig.edgeNodes.push(newNode);
        Message.success('节点添加成功');
      }
      
      closeNodeModal();
      done();
    };
    
    // 关闭节点弹窗
    const closeNodeModal = () => {
      nodeModalVisible.value = false;
    };
    
    // 测试邮件发送
    const handleTestEmail = () => {
      if (!notificationConfig.email.enabled) {
        Message.warning('请先启用邮件通知');
        return;
      }
      
      if (!notificationConfig.email.smtpServer || !notificationConfig.email.username || !notificationConfig.email.password) {
        Message.error('请完善邮件配置信息');
        return;
      }
      
      Message.loading('正在发送测试邮件...');
      
      // 模拟发送过程
      setTimeout(() => {
        Message.success('测试邮件发送成功');
      }, 1500);
    };
    
    // 测试短信发送
    const handleTestSMS = () => {
      if (!notificationConfig.sms.enabled) {
        Message.warning('请先启用短信通知');
        return;
      }
      
      if (!notificationConfig.sms.accessKey || !notificationConfig.sms.secretKey || !notificationConfig.sms.templateCode) {
        Message.error('请完善短信配置信息');
        return;
      }
      
      Message.loading('正在发送测试短信...');
      
      // 模拟发送过程
      setTimeout(() => {
        Message.success('测试短信发送成功');
      }, 1500);
    };
    
    // 测试钉钉通知
    const handleTestDingTalk = () => {
      if (!notificationConfig.dingtalk.enabled) {
        Message.warning('请先启用钉钉通知');
        return;
      }
      
      if (!notificationConfig.dingtalk.webhookUrl) {
        Message.error('请输入钉钉Webhook URL');
        return;
      }
      
      Message.loading('正在发送测试钉钉通知...');
      
      // 模拟发送过程
      setTimeout(() => {
        Message.success('测试钉钉通知发送成功');
      }, 1500);
    };
    
    // 手动备份
    const handleManualBackup = () => {
      Message.loading('正在执行备份...');
      
      // 模拟备份过程
      setTimeout(() => {
        const now = new Date();
        const formattedDate = now.toISOString().split('T')[0];
        const formattedTime = now.toTimeString().split(' ')[0].replace(/:/g, '-');
        
        const newBackup = {
          id: `backup-${Date.now().toString(36)}`,
          name: `手动备份_${formattedDate}_${formattedTime}`,
          createdAt: `${formattedDate} ${now.toTimeString().split(' ')[0]}`,
          size: `${Math.floor(Math.random() * 900) + 100} MB`,
          type: '完整备份',
          location: backupConfig.backupLocation === 'local' ? '本地存储' : 
                   (backupConfig.backupLocation === 's3' ? 'Amazon S3' : 
                   (backupConfig.backupLocation === 'oss' ? '阿里云OSS' : '腾讯云COS'))
        };
        
        backupList.value.unshift(newBackup);
        backupPagination.total = backupList.value.length;
        
        Message.success('备份执行成功');
      }, 3000);
    };
    
    // 查看备份
    const handleViewBackups = () => {
      backupListModalVisible.value = true;
    };
    
    // 关闭备份列表弹窗
    const closeBackupListModal = () => {
      backupListModalVisible.value = false;
    };
    
    // 恢复备份
    const handleRestoreBackup = (record) => {
      Message.loading(`正在恢复备份: ${record.name}...`);
      
      // 模拟恢复过程
      setTimeout(() => {
        Message.success('备份恢复成功');
      }, 3000);
    };
    
    // 下载备份
    const handleDownloadBackup = (record) => {
      Message.loading(`正在准备下载: ${record.name}...`);
      
      // 模拟下载过程
      setTimeout(() => {
        Message.success('备份下载已开始');
      }, 1500);
    };
    
    // 删除备份
    const handleDeleteBackup = (record) => {
      const index = backupList.value.findIndex(item => item.id === record.id);
      if (index !== -1) {
        backupList.value.splice(index, 1);
        backupPagination.total = backupList.value.length;
        Message.success('备份删除成功');
      }
    };
    
    // 查看日志
    const handleViewLogs = () => {
      logViewModalVisible.value = true;
    };
    
    // 关闭日志查看弹窗
    const closeLogViewModal = () => {
      logViewModalVisible.value = false;
    };
    
    // 清除日志
    const handleClearLogs = () => {
      Message.loading('正在清除日志...');
      
      // 模拟清除过程
      setTimeout(() => {
        accessLogContent.value = '';
        errorLogContent.value = '';
        operationLogContent.value = '';
        loginLogContent.value = '';
        Message.success('日志清除成功');
      }, 1500);
    };
    
    // 测试缓存连接
    const handleTestCache = () => {
      if (!cacheConfig.enableCache) {
        Message.warning('请先启用缓存');
        return;
      }
      
      if (cacheConfig.cacheType !== 'memory' && (!cacheConfig.cacheServer || !cacheConfig.cachePort)) {
        Message.error('请完善缓存配置信息');
        return;
      }
      
      Message.loading('正在测试缓存连接...');
      
      // 模拟测试过程
      setTimeout(() => {
        Message.success('缓存连接测试成功');
      }, 1500);
    };
    
    // 清除缓存
    const handleClearCache = () => {
      Message.loading('正在清除缓存...');
      
      // 模拟清除过程
      setTimeout(() => {
        Message.success('缓存清除成功');
      }, 1500);
    };
    
    return {
      activeConfigType,
      basicConfig,
      securityConfig,
      apiConfig,
      nodeConfig,
      notificationConfig,
      backupConfig,
      logConfig,
      cacheConfig,
      apiKeyForm,
      nodeForm,
      logoFileList,
      basicConfigForm,
      securityConfigForm,
      apiConfigForm,
      nodeConfigForm,
      notificationConfigForm,
      backupConfigForm,
      logConfigForm,
      cacheConfigForm,
      apiKeyFormRef,
      nodeFormRef,
      apiKeyModalVisible,
      nodeModalVisible,
      backupListModalVisible,
      logViewModalVisible,
      isEditApiKey,
      isEditNode,
      backupList,
      backupPagination,
      accessLogContent,
      errorLogContent,
      operationLogContent,
      loginLogContent,
      apiKeyColumns,
      edgeNodeColumns,
      backupColumns,
      getConfigTitle,
      getNodeTypeText,
      getRegionText,
      getNodeStatusText,
      getNodeStatusColor,
      handleMenuClick,
      customUploadRequest,
      handleSaveConfig,
      handleResetConfig,
      handleViewApiKey,
      handleAddApiKey,
      handleDeleteApiKey,
      handleSubmitApiKey,
      closeApiKeyModal,
      handleEditNode,
      handleAddNode,
      handleTestNode,
      handleDeleteNode,
      handleSubmitNode,
      closeNodeModal,
      handleTestEmail,
      handleTestSMS,
      handleTestDingTalk,
      handleManualBackup,
      handleViewBackups,
      closeBackupListModal,
      handleRestoreBackup,
      handleDownloadBackup,
      handleDeleteBackup,
      handleViewLogs,
      closeLogViewModal,
      handleClearLogs,
      handleTestCache,
      handleClearCache
    };
  }
};
</script>

<style scoped>
.system-config-container {
  padding: 16px;
}

.menu-card,
.config-card {
  margin-bottom: 16px;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.config-title {
  font-size: 16px;
  font-weight: bold;
}

.config-section {
  padding: 16px 0;
}

.api-keys-section,
.edge-nodes-section {
  margin-bottom: 16px;
}

.api-key-actions,
.edge-node-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .config-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .config-title {
    margin-bottom: 16px;
  }
}
</style>
