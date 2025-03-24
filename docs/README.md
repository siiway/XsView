# ScoreX（查分星）项目文档

## 1. 项目概述

ScoreX（查分星）是一款面向中学生的成绩查询与考试分析平台，作为第三方服务，通过调用原平台API并结合自有算法，为学生提供优质高效的考试服务。系统采用前后端分离架构，包括前台用户界面、后台管理系统、中心服务器和边缘节点服务。

### 1.1 核心功能

- 用户认证与授权
- 成绩查询与可视化展示
- 学科强弱分析
- 错题知识点分布统计
- 个性化诊断报告生成
- 学习建议推荐
- 班级排名趋势分析
- 知识点掌握进度跟踪
- 成绩更新提醒
- 学习资料推送

### 1.2 技术栈

- 前端：Vue 3、Naive UI、Arco Design Pro、TypeScript
- 后端：Python Flask、Node.js Express、Golang
- 数据库：MySQL/PostgreSQL
- 缓存：Redis
- 部署：Nginx、Supervisor

## 2. 系统架构

### 2.1 整体架构

ScoreX系统采用分布式架构，包括以下主要组件：

1. **前台用户界面**：使用Vue 3和Naive UI构建，提供响应式设计，支持PC端、平板和手机
2. **后台管理系统**：使用Arco Design Pro构建，提供完整的管理功能
3. **中心服务器**：使用Python Flask构建，处理业务逻辑和数据分析
4. **边缘节点服务**：使用Node.js Express构建，负责与原平台API通信
5. **数据库**：存储用户数据、考试信息和分析结果
6. **缓存系统**：提高系统响应速度和减轻服务器负担

### 2.2 数据流

1. 用户通过前台界面发起请求
2. 请求首先到达中心服务器
3. 中心服务器根据需要选择合适的边缘节点
4. 边缘节点调用原平台API获取数据
5. 数据返回到中心服务器进行处理和分析
6. 处理后的结果返回给用户

### 2.3 安全机制

- 所有API请求使用HTTPS加密传输
- 用户认证采用JWT令牌机制
- 边缘节点与中心服务器之间的通信采用加密传输
- 敏感数据脱敏处理
- 支持2FA双因素认证
- API限流和CC防护

## 3. 组件说明

### 3.1 前台用户界面

前台用户界面采用Vue 3和Naive UI构建，提供以下主要页面：

- 登录/注册页面
- 账号绑定页面
- 仪表盘/首页
- 考试列表页面
- 考试详情页面
- 成绩分析页面
- 诊断报告页面
- 学习资料页面
- 通知中心页面
- 个人信息管理页面

### 3.2 后台管理系统

后台管理系统采用Arco Design Pro构建，提供以下主要功能：

- 用户管理
- 考试管理
- 成绩管理
- 诊断报告管理
- 学习资料管理
- 通知管理
- 系统配置
- 数据分析大屏
- 节点管理
- 操作日志审计

### 3.3 中心服务器

中心服务器采用Python Flask构建，提供以下主要API：

- 用户认证API
- 用户信息API
- 考试信息API
- 成绩分析API
- 诊断报告API
- 学习资料API
- 通知API
- 节点管理API
- 代理API

### 3.4 边缘节点服务

边缘节点服务采用Node.js Express构建，负责与原平台API通信，提供以下功能：

- 原平台API代理
- 数据缓存
- 请求限流
- 错误处理
- 健康检查

## 4. 部署指南

### 4.1 系统要求

- Ubuntu 20.04 LTS或更高版本
- Python 3.8或更高版本
- Node.js 14或更高版本
- Nginx
- Supervisor
- Redis

### 4.2 部署步骤

1. 解压部署包
   ```
   tar -xzf scorex-deploy.tar.gz
   cd scorex-deploy
   ```

2. 执行部署脚本
   ```
   sudo ./deploy.sh
   ```

3. 验证部署
   - 访问前台应用：https://your-domain.com
   - 访问后台应用：https://your-domain.com/admin
   - 检查API：`curl -k https://your-domain.com/api/health`

### 4.3 配置说明

#### 环境变量

在 `/opt/scorex/backend/center-server/.env` 文件中配置以下环境变量：

- `DATABASE_URL`：数据库连接URL
- `SECRET_KEY`：应用密钥
- `API_PROXY_URL`：原平台API地址
- `REDIS_URL`：Redis连接URL

#### 边缘节点配置

在 `/opt/scorex/backend/edge-node/.env` 文件中配置：

- `CENTER_SERVER_URL`：中心服务器URL
- `NODE_ID`：节点ID
- `NODE_SECRET`：节点密钥

### 4.4 维护操作

#### 重启服务

```
sudo supervisorctl restart scorex:scorex-center
sudo supervisorctl restart scorex:scorex-edge
```

#### 查看日志

```
sudo tail -f /var/log/supervisor/scorex-center.out.log
sudo tail -f /var/log/supervisor/scorex-edge.out.log
```

#### 备份数据

```
# 备份数据库
mysqldump -u username -p database_name > backup.sql

# 备份配置文件
cp /opt/scorex/backend/center-server/.env /backup/
```

## 5. 用户手册

### 5.1 前台用户界面

#### 5.1.1 注册与登录

1. 访问系统首页，点击"注册"按钮
2. 填写用户名、密码和邮箱，完成注册
3. 使用注册的用户名和密码登录系统
4. 首次登录需要绑定原平台账号

#### 5.1.2 查看考试成绩

1. 登录后，在首页可以看到最近的考试成绩
2. 点击"考试列表"，可以查看所有考试
3. 点击具体考试，可以查看详细成绩

#### 5.1.3 查看成绩分析

1. 在考试详情页面，点击"成绩分析"
2. 系统会显示多种数据可视化图表，包括：
   - 分数分布图
   - 历史成绩趋势图
   - 班级排名趋势图
   - 知识点掌握度雷达图
   - 题型得分率分析图
   - 错题知识点分布图

#### 5.1.4 查看诊断报告

1. 在考试详情页面，点击"生成诊断报告"
2. 系统会自动生成个性化诊断报告
3. 报告包含学科强弱分析、错题分析和学习建议

#### 5.1.5 查看学习资料

1. 点击"学习资料"菜单
2. 系统会根据薄弱知识点推荐相关学习资料
3. 点击资料可以查看详细内容

### 5.2 后台管理系统

#### 5.2.1 用户管理

1. 登录后台管理系统
2. 点击"用户管理"菜单
3. 可以查看、添加、编辑和删除用户

#### 5.2.2 考试管理

1. 点击"考试管理"菜单
2. 可以查看、添加、编辑和删除考试

#### 5.2.3 成绩管理

1. 点击"成绩管理"菜单
2. 可以查看、添加、编辑和删除成绩

#### 5.2.4 系统配置

1. 点击"系统配置"菜单
2. 可以配置系统参数、接口设置和通知设置

## 6. API文档

### 6.1 认证API

#### 登录

- URL: `/api/auth/login`
- 方法: POST
- 请求体:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- 响应:
  ```json
  {
    "token": "string",
    "user": {
      "id": "integer",
      "username": "string",
      "email": "string",
      "role": "string"
    }
  }
  ```

#### 注册

- URL: `/api/auth/register`
- 方法: POST
- 请求体:
  ```json
  {
    "username": "string",
    "password": "string",
    "email": "string"
  }
  ```
- 响应:
  ```json
  {
    "message": "string",
    "user_id": "integer"
  }
  ```

### 6.2 用户API

#### 获取用户信息

- URL: `/api/user/info`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "role": "string",
    "created_at": "string",
    "last_login": "string"
  }
  ```

### 6.3 考试API

#### 获取考试列表

- URL: `/api/exam/list`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  {
    "exams": [
      {
        "id": "integer",
        "name": "string",
        "date": "string",
        "subjects": ["string"],
        "total_score": "number"
      }
    ]
  }
  ```

#### 获取考试详情

- URL: `/api/exam/detail/{exam_id}`
- 方法: GET
- 请求头: `Authorization: Bearer {token}`
- 响应:
  ```json
  {
    "id": "integer",
    "name": "string",
    "date": "string",
    "subjects": ["string"],
    "total_score": "number",
    "scores": [
      {
        "subject": "string",
        "score": "number",
        "max_score": "number"
      }
    ]
  }
  ```

## 7. 常见问题解答

### 7.1 系统使用问题

#### Q: 如何绑定原平台账号？
A: 首次登录系统后，会自动跳转到账号绑定页面，输入原平台的用户名和密码即可完成绑定。

#### Q: 为什么看不到最新的考试成绩？
A: 系统会定期从原平台同步数据，如果需要立即查看最新成绩，可以点击"刷新数据"按钮手动同步。

#### Q: 诊断报告需要多长时间生成？
A: 诊断报告通常会在几秒钟内生成完成，如果数据量较大，可能需要等待10-20秒。

### 7.2 技术问题

#### Q: 系统支持哪些浏览器？
A: 系统支持所有现代浏览器，包括Chrome、Firefox、Safari和Edge的最新版本。

#### Q: 如何处理API调用失败？
A: 系统会自动重试失败的API调用，如果多次失败，会提示用户稍后再试或联系客服。

#### Q: 如何扩展边缘节点？
A: 在后台管理系统的"节点管理"页面，点击"添加节点"，填写节点信息并部署新的边缘节点服务即可。

## 8. 联系与支持

如有任何问题或需要技术支持，请联系：

- 邮箱：support@scorex.example.com
- 电话：123-456-7890
- 在线客服：通过系统内的"客服"按钮联系
