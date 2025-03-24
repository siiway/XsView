# ScoreX（查分星）API文档分析

## 已识别的API接口

1. **HOA-登录接口**
   - 路径: `https://hfs-be.yunxiao.com/v2/users/sessions`
   - 方法: POST
   - 参数:
     - deviceType: 数字类型，设备类型
     - loginName: 用户名/手机号/邮箱
     - password: 账号密码
     - rememberMe: 数字类型，是否记住登录状态
     - roleType: 数字类型，角色类型
   - 返回:
     - token: 用于认证的令牌
     - fdToken: 另一种认证令牌
     - userId: 用户ID
     - studentId: 学生ID

2. **HOA-用户信息**
   - 路径: `https://hfs-be.yunxiao.com/v2/user-center/user-snapshot`
   - 方法: GET
   - 认证: 需要认证头（具体格式待确认）

3. **HOA-考试列表**
   - 路径: `https://hfs-be.yunxiao.com/v4/exam/list`
   - 方法: GET
   - 认证: 需要认证头（具体格式待确认）

4. **HOA-考试详情**
   - 路径: `https://hfs-be.yunxiao.com/v4/exam/detail`
   - 方法: GET
   - 参数:
     - id: 考试ID
   - 认证: 需要认证头（具体格式待确认）

5. **其他已识别API**
   - HOA-邮件接口
   - HOA-单科详答
   - HOA-校级屏蔽
   - HOA-考试简要
   - HOA-拉小题分
   - HOA-拉答题卡和主观题
   - HOA-查可交易券
   - HOA-查个人剩余券
   - HOA-成长等级信息
   - HOA-成长等级排名
   - HOA-积分明细
   - HOA-周常任务
   - HOA-考试档案
   - HOA-分析成绩
   - HOA-得分分布

## 认证机制

API认证需要在请求头中包含认证信息，但具体格式尚未确认。登录接口返回两种token：
- token: 普通认证令牌
- fdToken: 另一种认证令牌，可能用于特定接口

## 数据结构

API返回的数据结构通常包含以下字段：
- code: 状态码，0表示成功
- msg: 状态消息
- data: 返回的数据内容

## 注意事项

1. 所有API调用前必须先调用登录接口获取认证令牌
2. API认证机制需要进一步研究
3. 部分API可能需要特定的参数格式或额外的请求头
4. 系统设计需要考虑API调用的频率限制和超时处理
