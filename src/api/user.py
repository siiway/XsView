#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
import jwt
import os
from dotenv import load_dotenv
from functools import wraps

# 加载环境变量
load_dotenv()

# 创建蓝图
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# JWT配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# 从auth.py导入模拟用户数据库，实际项目中应使用真实数据库
from src.api.auth import users_db

# 认证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'code': 2004,
                'msg': '未提供有效的认证令牌',
                'data': None
            }), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            # 验证访问令牌
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['sub']
            
            # 检查用户是否存在
            if user_id not in users_db:
                raise jwt.InvalidTokenError('User not found')
            
            # 将用户ID添加到请求上下文
            request.user_id = user_id
            
            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({
                'code': 2004,
                'msg': '认证令牌已过期',
                'data': None
            }), 401
        
        except jwt.InvalidTokenError:
            return jsonify({
                'code': 2004,
                'msg': '无效的认证令牌',
                'data': None
            }), 401
    
    return decorated

@user_bp.route('/info', methods=['GET'])
@token_required
def get_user_info():
    user_id = request.user_id
    user = users_db.get(user_id)
    
    if not user:
        return jsonify({
            'code': 2001,
            'msg': '用户不存在',
            'data': None
        }), 404
    
    # 构建用户信息响应
    user_info = {
        'userId': user['id'],
        'username': user['username'],
        'email': user['email'],
        'phone': user['phone'],
        'role': {
            'id': user['role_id'],
            'name': get_role_name(user['role_id'])
        },
        'originalPlatformId': user['original_platform_id'],
        'lastLogin': user['last_login']
    }
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': user_info
    })

@user_bp.route('/update', methods=['PUT'])
@token_required
def update_user_info():
    user_id = request.user_id
    user = users_db.get(user_id)
    
    if not user:
        return jsonify({
            'code': 2001,
            'msg': '用户不存在',
            'data': None
        }), 404
    
    data = request.get_json()
    
    # 验证请求数据
    if not data:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 更新用户信息
    if 'email' in data:
        user['email'] = data['email']
    
    if 'phone' in data:
        user['phone'] = data['phone']
    
    # 返回更新后的用户信息
    updated_info = {
        'userId': user['id'],
        'email': user['email'],
        'phone': user['phone']
    }
    
    return jsonify({
        'code': 0,
        'msg': '更新成功',
        'data': updated_info
    })

@user_bp.route('/change-password', methods=['PUT'])
@token_required
def change_password():
    from werkzeug.security import check_password_hash, generate_password_hash
    
    user_id = request.user_id
    user = users_db.get(user_id)
    
    if not user:
        return jsonify({
            'code': 2001,
            'msg': '用户不存在',
            'data': None
        }), 404
    
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('oldPassword') or not data.get('newPassword'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    
    # 验证旧密码
    if not check_password_hash(user['password'], old_password):
        return jsonify({
            'code': 2002,
            'msg': '旧密码错误',
            'data': None
        }), 401
    
    # 更新密码
    user['password'] = generate_password_hash(new_password)
    
    return jsonify({
        'code': 0,
        'msg': '密码修改成功',
        'data': None
    })

def get_role_name(role_id):
    """根据角色ID获取角色名称"""
    roles = {
        1: '管理员',
        2: '教师',
        3: '学生'
    }
    return roles.get(role_id, '未知角色')
