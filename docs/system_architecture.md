# ScoreX（查分星）系统架构设计

## 1. 整体架构

ScoreX系统采用前后端分离的架构，包含以下主要组件：

### 1.1 前端应用
- **前台客户端**：面向学生用户的成绩查询与分析平台
  - 基于Vue + Naive UI构建
  - 响应式设计，支持PC/Pad和手机端
  
- **后台管理系统**：面向管理员的系统管理平台
  - 基于Vue + Arco Design Pro构建
  - 提供完整的系统管理功能

### 1.2 后端服务
- **中心服务器**：核心业务逻辑处理中心
  - 基于Python Flask构建
  - 负责数据处理、分析和存储
  - 管理用户认证和授权
  - 协调边缘节点

- **边缘服务节点**：分布式API调用处理节点
  - 基于Node.js Express构建
  - 负责与原平台API交互
  - 提供数据缓存和加速
  - 支持负载均衡和故障转移

### 1.3 数据存储
- **关系型数据库**：存储用户信息、成绩数据等结构化数据
- **缓存系统**：提高数据访问速度，减轻数据库负担
- **文件存储**：存储诊断报告、学习资料等文件

## 2. 数据库设计

### 2.1 用户表(users)
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    role_id INT NOT NULL,
    original_platform_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status TINYINT DEFAULT 1
);
```

### 2.2 角色表(roles)
```sql
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    permissions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 2.3 考试表(exams)
```sql
CREATE TABLE exams (
    id VARCHAR(36) PRIMARY KEY,
    original_exam_id VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    subject VARCHAR(50),
    exam_time TIMESTAMP,
    total_score DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 2.4 成绩表(scores)
```sql
CREATE TABLE scores (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    exam_id VARCHAR(36) NOT NULL,
    score DECIMAL(10,2),
    rank INT,
    original_score_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id)
);
```

### 2.5 知识点表(knowledge_points)
```sql
CREATE TABLE knowledge_points (
    id VARCHAR(36) PRIMARY KEY,
    subject VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES knowledge_points(id)
);
```

### 2.6 错题表(wrong_questions)
```sql
CREATE TABLE wrong_questions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    exam_id VARCHAR(36) NOT NULL,
    question_id VARCHAR(100) NOT NULL,
    knowledge_point_id VARCHAR(36),
    question_content TEXT,
    correct_answer TEXT,
    user_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id)
);
```

### 2.7 诊断报告表(diagnostic_reports)
```sql
CREATE TABLE diagnostic_reports (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    exam_id VARCHAR(36) NOT NULL,
    report_content TEXT,
    suggestions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exam_id) REFERENCES exams(id)
);
```

### 2.8 学习资料表(learning_materials)
```sql
CREATE TABLE learning_materials (
    id VARCHAR(36) PRIMARY KEY,
    knowledge_point_id VARCHAR(36) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    file_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id)
);
```

### 2.9 通知表(notifications)
```sql
CREATE TABLE notifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    title VARCHAR(200) NOT NULL,
    content TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 2.10 API调用日志表(api_logs)
```sql
CREATE TABLE api_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    api_path VARCHAR(255) NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    request_params TEXT,
    response_code INT,
    response_message VARCHAR(255),
    edge_node_id VARCHAR(50),
    execution_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 3. 中心服务器与边缘节点通信方案

### 3.1 通信协议
- 采用HTTPS协议进行安全通信
- 使用RESTful API风格设计接口
- 数据格式采用JSON

### 3.2 通信流程
1. 用户请求发送到中心服务器
2. 中心服务器根据负载均衡策略选择合适的边缘节点
3. 中心服务器向边缘节点发送请求，包含必要的认证信息
4. 边缘节点处理请求，调用原平台API
5. 边缘节点将结果返回给中心服务器
6. 中心服务器处理数据并返回给用户

### 3.3 边缘节点管理
- 中心服务器维护边缘节点列表和状态
- 定期健康检查，自动剔除不可用节点
- 支持动态添加和移除边缘节点
- 实现节点间数据同步机制

### 3.4 数据加密
- 通信过程中使用TLS/SSL加密
- 敏感数据使用对称加密算法加密
- 加密密钥定期轮换

## 4. API安全策略

### 4.1 认证机制
- 基于JWT的用户认证
- 令牌过期机制
- 刷新令牌机制
- 多因素认证支持

### 4.2 授权控制
- 基于角色的访问控制(RBAC)
- 细粒度的权限管理
- API访问频率限制

### 4.3 数据安全
- 敏感数据脱敏处理
- 数据传输加密
- 防SQL注入措施
- XSS防护

### 4.4 防护措施
- 请求签名验证
- 防重放攻击
- CSRF防护
- 风控CC验证

## 5. 用户认证与授权机制

### 5.1 用户认证流程
1. 用户提交登录信息
2. 系统验证用户名和密码
3. 验证通过后生成JWT令牌
4. 返回令牌给客户端
5. 客户端后续请求携带令牌

### 5.2 原平台账号绑定
1. 用户提供原平台账号信息
2. 系统验证原平台账号有效性
3. 验证通过后将原平台账号与系统账号关联
4. 存储必要的认证信息用于后续API调用

### 5.3 权限管理
- 预定义角色：管理员、教师、学生
- 每个角色拥有不同的权限集合
- 支持自定义角色和权限
- 权限可精确到具体API操作

### 5.4 会话管理
- 支持多设备同时登录
- 会话超时自动登出
- 支持强制登出
- 异常登录检测

## 6. 系统扩展性设计

### 6.1 模块化设计
- 核心功能模块化，支持按需加载
- 插件化架构，便于功能扩展
- 标准化接口，支持第三方集成

### 6.2 水平扩展
- 中心服务器支持集群部署
- 边缘节点可动态扩展
- 数据库读写分离，支持分库分表

### 6.3 垂直扩展
- 关键服务可独立部署
- 资源密集型任务异步处理
- 支持微服务架构演进

## 7. 系统容错与高可用设计

### 7.1 故障检测
- 服务健康检查机制
- 边缘节点状态监控
- 数据库连接池管理

### 7.2 故障恢复
- 自动重试机制
- 服务降级策略
- 数据一致性保障

### 7.3 高可用保障
- 关键服务冗余部署
- 负载均衡自动切换
- 数据定期备份
- 灾难恢复方案
