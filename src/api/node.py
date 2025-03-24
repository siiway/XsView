#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
import jwt
import os
import uuid
import datetime
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建蓝图
node_bp = Blueprint('node', __name__, url_prefix='/api/node')

# JWT配置
NODE_SECRET = os.getenv('EDGE_NODE_SECRET')
NODE_TOKEN_EXPIRES = int(os.getenv('EDGE_NODE_TOKEN_EXPIRES', 86400))

# 模拟边缘节点数据库
edge_nodes_db = {}

@node_bp.route('/register', methods=['POST'])
def register_node():
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('nodeId') or not data.get('nodeSecret'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    node_id = data.get('nodeId')
    node_secret = data.get('nodeSecret')
    node_ip = data.get('nodeIp', request.remote_addr)
    node_capacity = data.get('nodeCapacity', 100)
    node_status = data.get('nodeStatus', 'active')
    
    # 验证节点密钥
    if node_secret != NODE_SECRET:
        return jsonify({
            'code': 2005,
            'msg': '节点密钥无效',
            'data': None
        }), 403
    
    # 注册或更新节点信息
    edge_nodes_db[node_id] = {
        'id': node_id,
        'ip': node_ip,
        'capacity': node_capacity,
        'status': node_status,
        'current_load': 0,
        'active_connections': 0,
        'last_heartbeat': datetime.datetime.now().isoformat(),
        'registered_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    # 生成节点令牌
    node_token = generate_node_token(node_id)
    
    return jsonify({
        'code': 0,
        'msg': '注册成功',
        'data': {
            'nodeToken': node_token,
            'expiresIn': NODE_TOKEN_EXPIRES
        }
    })

@node_bp.route('/heartbeat', methods=['POST'])
def node_heartbeat():
    # 获取请求头中的令牌
    auth_header = request.headers.get('Node-Authorization')
    if not auth_header:
        return jsonify({
            'code': 2004,
            'msg': '未提供有效的节点认证令牌',
            'data': None
        }), 401
    
    node_token = auth_header
    
    try:
        # 验证节点令牌
        payload = jwt.decode(node_token, NODE_SECRET, algorithms=['HS256'])
        node_id = payload['sub']
        
        # 检查节点是否存在
        if node_id not in edge_nodes_db:
            raise jwt.InvalidTokenError('Node not found')
        
        # 获取请求数据
        data = request.get_json()
        
        # 验证请求数据
        if not data or not data.get('nodeId'):
            return jsonify({
                'code': 1001,
                'msg': '参数错误',
                'data': None
            }), 400
        
        # 确认节点ID匹配
        if data.get('nodeId') != node_id:
            return jsonify({
                'code': 1002,
                'msg': '节点ID不匹配',
                'data': None
            }), 400
        
        # 更新节点状态
        edge_nodes_db[node_id]['current_load'] = data.get('currentLoad', 0)
        edge_nodes_db[node_id]['active_connections'] = data.get('activeConnections', 0)
        edge_nodes_db[node_id]['status'] = data.get('nodeStatus', 'active')
        edge_nodes_db[node_id]['last_heartbeat'] = datetime.datetime.now().isoformat()
        edge_nodes_db[node_id]['updated_at'] = datetime.datetime.now().isoformat()
        
        # 返回心跳响应
        return jsonify({
            'code': 0,
            'msg': '心跳成功',
            'data': {
                'serverTime': datetime.datetime.now().isoformat(),
                'configUpdated': False,
                'newConfig': {}
            }
        })
    
    except jwt.ExpiredSignatureError:
        return jsonify({
            'code': 2004,
            'msg': '节点认证令牌已过期',
            'data': None
        }), 401
    
    except jwt.InvalidTokenError:
        return jsonify({
            'code': 2004,
            'msg': '无效的节点认证令牌',
            'data': None
        }), 401

def generate_node_token(node_id):
    """生成节点认证令牌"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=NODE_TOKEN_EXPIRES),
        'iat': datetime.datetime.utcnow(),
        'sub': node_id,
        'type': 'node'
    }
    return jwt.encode(payload, NODE_SECRET, algorithm='HS256')

# 节点认证装饰器
def node_token_required(f):
    def decorated(*args, **kwargs):
        # 获取请求头中的令牌
        auth_header = request.headers.get('Node-Authorization')
        if not auth_header:
            return jsonify({
                'code': 2004,
                'msg': '未提供有效的节点认证令牌',
                'data': None
            }), 401
        
        node_token = auth_header
        
        try:
            # 验证节点令牌
            payload = jwt.decode(node_token, NODE_SECRET, algorithms=['HS256'])
            node_id = payload['sub']
            
            # 检查节点是否存在
            if node_id not in edge_nodes_db:
                raise jwt.InvalidTokenError('Node not found')
            
            # 将节点ID添加到请求上下文
            request.node_id = node_id
            
            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({
                'code': 2004,
                'msg': '节点认证令牌已过期',
                'data': None
            }), 401
        
        except jwt.InvalidTokenError:
            return jsonify({
                'code': 2004,
                'msg': '无效的节点认证令牌',
                'data': None
            }), 401
    
    return decorated
