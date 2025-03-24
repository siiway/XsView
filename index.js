// 边缘节点服务实现
// index.js

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const dotenv = require('dotenv');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

// 加载环境变量
dotenv.config();

// 创建应用实例
const app = express();

// 配置中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

// 配置变量
const PORT = process.env.PORT || 3000;
const CENTER_SERVER_URL = process.env.CENTER_SERVER_URL || 'http://localhost:5000';
const NODE_ID = process.env.NODE_ID || `node_${uuidv4()}`;
const NODE_SECRET = process.env.NODE_SECRET || 'your_edge_node_secret_here';
const ORIGINAL_API_BASE_URL = process.env.ORIGINAL_API_BASE_URL || 'https://hfs-be.yunxiao.com';

// 存储节点令牌
let nodeToken = null;
let nodeTokenExpires = 0;

// 注册节点
async function registerNode() {
    try {
        const response = await axios.post(`${CENTER_SERVER_URL}/api/node/register`, {
            nodeId: NODE_ID,
            nodeSecret: NODE_SECRET,
            nodeCapacity: 100,
            nodeStatus: 'active'
        });

        if (response.data.code === 0) {
            nodeToken = response.data.data.nodeToken;
            nodeTokenExpires = Date.now() + (response.data.data.expiresIn * 1000);
            console.log(`节点 ${NODE_ID} 注册成功，令牌有效期至 ${new Date(nodeTokenExpires)}`);
            return true;
        } else {
            console.error('节点注册失败:', response.data.msg);
            return false;
        }
    } catch (error) {
        console.error('节点注册请求异常:', error.message);
        return false;
    }
}

// 发送心跳
async function sendHeartbeat() {
    if (!nodeToken || Date.now() >= nodeTokenExpires) {
        const registered = await registerNode();
        if (!registered) {
            console.error('无法发送心跳，节点未注册');
            return;
        }
    }

    try {
        const response = await axios.post(
            `${CENTER_SERVER_URL}/api/node/heartbeat`,
            {
                nodeId: NODE_ID,
                currentLoad: Math.floor(Math.random() * 50),  // 模拟负载
                activeConnections: Math.floor(Math.random() * 10),  // 模拟连接数
                nodeStatus: 'active'
            },
            {
                headers: {
                    'Node-Authorization': nodeToken
                }
            }
        );

        if (response.data.code === 0) {
            console.log(`心跳发送成功，服务器时间: ${response.data.data.serverTime}`);
            
            // 检查配置更新
            if (response.data.data.configUpdated) {
                console.log('收到新配置:', response.data.data.newConfig);
                // 实际项目中应该应用新配置
            }
        } else {
            console.error('心跳发送失败:', response.data.msg);
        }
    } catch (error) {
        console.error('心跳请求异常:', error.message);
    }
}

// 代理原平台登录接口
app.post('/api/login', async (req, res) => {
    if (!nodeToken || Date.now() >= nodeTokenExpires) {
        const registered = await registerNode();
        if (!registered) {
            return res.status(500).json({
                code: 3002,
                msg: '边缘节点未注册',
                data: null
            });
        }
    }

    const { loginName, password, deviceType, rememberMe, roleType, userId } = req.body;

    try {
        const response = await axios.post(
            `${CENTER_SERVER_URL}/api/proxy/login`,
            {
                userId,
                loginName,
                password,
                deviceType: deviceType || 1,
                rememberMe: rememberMe || 1,
                roleType: roleType || 1
            },
            {
                headers: {
                    'Node-Authorization': nodeToken
                }
            }
        );

        return res.json(response.data);
    } catch (error) {
        console.error('登录代理请求异常:', error.message);
        return res.status(500).json({
            code: 3001,
            msg: '登录代理请求异常',
            data: null
        });
    }
});

// 代理原平台用户信息接口
app.get('/api/user-info', async (req, res) => {
    if (!nodeToken || Date.now() >= nodeTokenExpires) {
        const registered = await registerNode();
        if (!registered) {
            return res.status(500).json({
                code: 3002,
                msg: '边缘节点未注册',
                data: null
            });
        }
    }

    const { userId, token } = req.query;

    if (!userId || !token) {
        return res.status(400).json({
            code: 1001,
            msg: '参数错误',
            data: null
        });
    }

    try {
        const response = await axios.get(
            `${CENTER_SERVER_URL}/api/proxy/user-info`,
            {
                params: { userId, token },
                headers: {
                    'Node-Authorization': nodeToken
                }
            }
        );

        return res.json(response.data);
    } catch (error) {
        console.error('用户信息代理请求异常:', error.message);
        return res.status(500).json({
            code: 3001,
            msg: '用户信息代理请求异常',
            data: null
        });
    }
});

// 代理原平台考试列表接口
app.get('/api/exam-list', async (req, res) => {
    if (!nodeToken || Date.now() >= nodeTokenExpires) {
        const registered = await registerNode();
        if (!registered) {
            return res.status(500).json({
                code: 3002,
                msg: '边缘节点未注册',
                data: null
            });
        }
    }

    const { userId, token } = req.query;

    if (!userId || !token) {
        return res.status(400).json({
            code: 1001,
            msg: '参数错误',
            data: null
        });
    }

    try {
        const response = await axios.get(
            `${CENTER_SERVER_URL}/api/proxy/exam-list`,
            {
                params: { userId, token },
                headers: {
                    'Node-Authorization': nodeToken
                }
            }
        );

        return res.json(response.data);
    } catch (error) {
        console.error('考试列表代理请求异常:', error.message);
        return res.status(500).json({
            code: 3001,
            msg: '考试列表代理请求异常',
            data: null
        });
    }
});

// 代理原平台考试详情接口
app.get('/api/exam-detail', async (req, res) => {
    if (!nodeToken || Date.now() >= nodeTokenExpires) {
        const registered = await registerNode();
        if (!registered) {
            return res.status(500).json({
                code: 3002,
                msg: '边缘节点未注册',
                data: null
            });
        }
    }

    const { userId, token, examId } = req.query;

    if (!userId || !token || !examId) {
        return res.status(400).json({
            code: 1001,
            msg: '参数错误',
            data: null
        });
    }

    try {
        const response = await axios.get(
            `${CENTER_SERVER_URL}/api/proxy/exam-detail`,
            {
                params: { userId, token, examId },
                headers: {
                    'Node-Authorization': nodeToken
                }
            }
        );

        return res.json(response.data);
    } catch (error) {
        console.error('考试详情代理请求异常:', error.message);
        return res.status(500).json({
            code: 3001,
            msg: '考试详情代理请求异常',
            data: null
        });
    }
});

// 健康检查接口
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        nodeId: NODE_ID,
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

// 启动应用
app.listen(PORT, () => {
    console.log(`边缘节点服务已启动，监听端口 ${PORT}`);
    
    // 注册节点
    registerNode().then(registered => {
        if (registered) {
            // 设置定期心跳
            setInterval(sendHeartbeat, 60000);  // 每分钟发送一次心跳
        }
    });
});
