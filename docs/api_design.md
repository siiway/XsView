# ScoreX（查分星）API设计文档

## 1. 中心服务器API

### 1.1 用户认证API

#### 1.1.1 用户注册
- **路径**: `/api/auth/register`
- **方法**: POST
- **描述**: 注册新用户
- **请求参数**:
  ```json
  {
    "username": "string",
    "password": "string",
    "email": "string",
    "phone": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "注册成功",
    "data": {
      "userId": "string",
      "username": "string",
      "token": "string"
    }
  }
  ```

#### 1.1.2 用户登录
- **路径**: `/api/auth/login`
- **方法**: POST
- **描述**: 用户登录
- **请求参数**:
  ```json
  {
    "username": "string",
    "password": "string",
    "rememberMe": boolean
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "登录成功",
    "data": {
      "userId": "string",
      "username": "string",
      "token": "string",
      "refreshToken": "string",
      "expiresIn": number
    }
  }
  ```

#### 1.1.3 刷新令牌
- **路径**: `/api/auth/refresh-token`
- **方法**: POST
- **描述**: 刷新访问令牌
- **请求参数**:
  ```json
  {
    "refreshToken": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "刷新成功",
    "data": {
      "token": "string",
      "refreshToken": "string",
      "expiresIn": number
    }
  }
  ```

#### 1.1.4 绑定原平台账号
- **路径**: `/api/auth/bind-original-account`
- **方法**: POST
- **描述**: 绑定原平台账号
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```json
  {
    "loginName": "string",
    "password": "string",
    "deviceType": number,
    "roleType": number
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "绑定成功",
    "data": {
      "originalPlatformId": "string",
      "bindStatus": true
    }
  }
  ```

### 1.2 用户信息API

#### 1.2.1 获取用户信息
- **路径**: `/api/user/info`
- **方法**: GET
- **描述**: 获取当前用户信息
- **请求头**: Authorization: Bearer {token}
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "userId": "string",
      "username": "string",
      "email": "string",
      "phone": "string",
      "role": {
        "id": number,
        "name": "string"
      },
      "originalPlatformId": "string",
      "lastLogin": "string"
    }
  }
  ```

#### 1.2.2 更新用户信息
- **路径**: `/api/user/update`
- **方法**: PUT
- **描述**: 更新用户信息
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```json
  {
    "email": "string",
    "phone": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "更新成功",
    "data": {
      "userId": "string",
      "email": "string",
      "phone": "string"
    }
  }
  ```

#### 1.2.3 修改密码
- **路径**: `/api/user/change-password`
- **方法**: PUT
- **描述**: 修改用户密码
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```json
  {
    "oldPassword": "string",
    "newPassword": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "密码修改成功",
    "data": null
  }
  ```

### 1.3 考试成绩API

#### 1.3.1 获取考试列表
- **路径**: `/api/exam/list`
- **方法**: GET
- **描述**: 获取用户考试列表
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  page: number (页码，默认1)
  pageSize: number (每页数量，默认10)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "total": number,
      "list": [
        {
          "id": "string",
          "title": "string",
          "subject": "string",
          "examTime": "string",
          "totalScore": number,
          "score": number,
          "rank": number
        }
      ]
    }
  }
  ```

#### 1.3.2 获取考试详情
- **路径**: `/api/exam/detail`
- **方法**: GET
- **描述**: 获取考试详细信息
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  examId: string (考试ID)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "id": "string",
      "title": "string",
      "subject": "string",
      "examTime": "string",
      "totalScore": number,
      "score": number,
      "rank": number,
      "classRank": number,
      "gradeRank": number,
      "subjectScores": [
        {
          "subject": "string",
          "score": number,
          "totalScore": number,
          "rank": number
        }
      ],
      "questionStats": {
        "correct": number,
        "wrong": number,
        "partial": number,
        "unanswered": number
      }
    }
  }
  ```

#### 1.3.3 获取成绩分析
- **路径**: `/api/exam/analysis`
- **方法**: GET
- **描述**: 获取考试成绩分析
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  examId: string (考试ID)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "examId": "string",
      "scoreDistribution": {
        "ranges": ["0-60", "60-70", "70-80", "80-90", "90-100"],
        "counts": [10, 20, 30, 25, 15]
      },
      "subjectAnalysis": [
        {
          "subject": "string",
          "score": number,
          "averageScore": number,
          "maxScore": number,
          "minScore": number,
          "standardDeviation": number
        }
      ],
      "knowledgePointAnalysis": [
        {
          "knowledgePoint": "string",
          "masteryLevel": number,
          "averageMasteryLevel": number
        }
      ],
      "rankTrend": [
        {
          "examId": "string",
          "examTitle": "string",
          "rank": number,
          "totalStudents": number
        }
      ]
    }
  }
  ```

#### 1.3.4 获取错题列表
- **路径**: `/api/exam/wrong-questions`
- **方法**: GET
- **描述**: 获取考试错题列表
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  examId: string (考试ID)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "examId": "string",
      "wrongQuestions": [
        {
          "id": "string",
          "questionId": "string",
          "content": "string",
          "correctAnswer": "string",
          "userAnswer": "string",
          "knowledgePoint": "string"
        }
      ]
    }
  }
  ```

### 1.4 诊断报告API

#### 1.4.1 生成诊断报告
- **路径**: `/api/diagnostic/generate`
- **方法**: POST
- **描述**: 生成考试诊断报告
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```json
  {
    "examId": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "生成成功",
    "data": {
      "reportId": "string"
    }
  }
  ```

#### 1.4.2 获取诊断报告
- **路径**: `/api/diagnostic/report`
- **方法**: GET
- **描述**: 获取考试诊断报告
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  reportId: string (报告ID)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "id": "string",
      "examId": "string",
      "examTitle": "string",
      "createdAt": "string",
      "overallAnalysis": "string",
      "subjectAnalysis": [
        {
          "subject": "string",
          "analysis": "string",
          "suggestions": "string"
        }
      ],
      "weaknessAnalysis": [
        {
          "knowledgePoint": "string",
          "masteryLevel": number,
          "suggestions": "string",
          "learningMaterials": [
            {
              "id": "string",
              "title": "string"
            }
          ]
        }
      ],
      "improvementSuggestions": "string"
    }
  }
  ```

#### 1.4.3 获取历史报告列表
- **路径**: `/api/diagnostic/history`
- **方法**: GET
- **描述**: 获取历史诊断报告列表
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  page: number (页码，默认1)
  pageSize: number (每页数量，默认10)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "total": number,
      "list": [
        {
          "id": "string",
          "examId": "string",
          "examTitle": "string",
          "createdAt": "string"
        }
      ]
    }
  }
  ```

### 1.5 学习资料API

#### 1.5.1 获取推荐学习资料
- **路径**: `/api/learning/recommended`
- **方法**: GET
- **描述**: 获取推荐学习资料
- **请求头**: Authorization: Bearer {token}
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "materials": [
        {
          "id": "string",
          "title": "string",
          "knowledgePoint": "string",
          "type": "string",
          "description": "string"
        }
      ]
    }
  }
  ```

#### 1.5.2 获取学习资料详情
- **路径**: `/api/learning/material`
- **方法**: GET
- **描述**: 获取学习资料详情
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  materialId: string (资料ID)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "id": "string",
      "title": "string",
      "knowledgePoint": "string",
      "content": "string",
      "filePath": "string"
    }
  }
  ```

### 1.6 通知API

#### 1.6.1 获取通知列表
- **路径**: `/api/notification/list`
- **方法**: GET
- **描述**: 获取通知列表
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```
  page: number (页码，默认1)
  pageSize: number (每页数量，默认10)
  isRead: boolean (是否已读，可选)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "total": number,
      "unreadCount": number,
      "list": [
        {
          "id": "string",
          "title": "string",
          "content": "string",
          "isRead": boolean,
          "type": "string",
          "createdAt": "string"
        }
      ]
    }
  }
  ```

#### 1.6.2 标记通知为已读
- **路径**: `/api/notification/read`
- **方法**: PUT
- **描述**: 标记通知为已读
- **请求头**: Authorization: Bearer {token}
- **请求参数**:
  ```json
  {
    "notificationId": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "标记成功",
    "data": null
  }
  ```

## 2. 边缘节点API

### 2.1 节点管理API

#### 2.1.1 节点注册
- **路径**: `/api/node/register`
- **方法**: POST
- **描述**: 边缘节点向中心服务器注册
- **请求参数**:
  ```json
  {
    "nodeId": "string",
    "nodeSecret": "string",
    "nodeIp": "string",
    "nodeCapacity": number,
    "nodeStatus": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "注册成功",
    "data": {
      "nodeToken": "string",
      "expiresIn": number
    }
  }
  ```

#### 2.1.2 节点心跳
- **路径**: `/api/node/heartbeat`
- **方法**: POST
- **描述**: 边缘节点向中心服务器发送心跳
- **请求头**: Node-Authorization: {nodeToken}
- **请求参数**:
  ```json
  {
    "nodeId": "string",
    "currentLoad": number,
    "activeConnections": number,
    "nodeStatus": "string"
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "心跳成功",
    "data": {
      "serverTime": "string",
      "configUpdated": boolean,
      "newConfig": object
    }
  }
  ```

### 2.2 原平台API代理

#### 2.2.1 登录接口代理
- **路径**: `/api/proxy/login`
- **方法**: POST
- **描述**: 代理原平台登录接口
- **请求头**: Node-Authorization: {nodeToken}
- **请求参数**:
  ```json
  {
    "userId": "string",
    "loginName": "string",
    "password": "string",
    "deviceType": number,
    "rememberMe": number,
    "roleType": number
  }
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "登录成功",
    "data": {
      "token": "string",
      "fdToken": "string",
      "userId": "string",
      "studentId": "string"
    }
  }
  ```

#### 2.2.2 用户信息代理
- **路径**: `/api/proxy/user-info`
- **方法**: GET
- **描述**: 代理原平台用户信息接口
- **请求头**: Node-Authorization: {nodeToken}
- **请求参数**:
  ```
  userId: string (用户ID)
  token: string (原平台token)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "userInfo": object
    }
  }
  ```

#### 2.2.3 考试列表代理
- **路径**: `/api/proxy/exam-list`
- **方法**: GET
- **描述**: 代理原平台考试列表接口
- **请求头**: Node-Authorization: {nodeToken}
- **请求参数**:
  ```
  userId: string (用户ID)
  token: string (原平台token)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "examList": array
    }
  }
  ```

#### 2.2.4 考试详情代理
- **路径**: `/api/proxy/exam-detail`
- **方法**: GET
- **描述**: 代理原平台考试详情接口
- **请求头**: Node-Authorization: {nodeToken}
- **请求参数**:
  ```
  userId: string (用户ID)
  token: string (原平台token)
  examId: string (考试ID)
  ```
- **响应**:
  ```json
  {
    "code": 0,
    "msg": "获取成功",
    "data": {
      "examDetail": object
    }
  }
  ```

## 3. 错误码定义

- **0**: 成功
- **1001**: 参数错误
- **1002**: 数据验证失败
- **2001**: 用户不存在
- **2002**: 密码错误
- **2003**: 账号已被禁用
- **2004**: 令牌无效或已过期
- **2005**: 权限不足
- **3001**: 原平台API调用失败
- **3002**: 边缘节点不可用
- **4001**: 数据库操作失败
- **4002**: 缓存操作失败
- **5001**: 系统内部错误

## 4. 通用响应格式

所有API响应均遵循以下格式：

```json
{
  "code": number,  // 状态码，0表示成功，非0表示失败
  "msg": "string", // 状态消息
  "data": object   // 响应数据，可能为null
}
```

## 5. 安全要求

1. 所有API请求必须通过HTTPS进行
2. 除了公开接口外，所有请求必须携带有效的认证令牌
3. 敏感数据在传输和存储时必须加密
4. API访问频率限制，防止恶意请求
5. 请求参数必须进行严格验证，防止注入攻击
