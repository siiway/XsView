#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
import jwt
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# JWT配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))

# 模拟用户数据库，实际项目中应使用真实数据库
users_db = {}

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')
    phone = data.get('phone', '')
    
    # 检查用户名是否已存在
    if any(user['username'] == username for user in users_db.values()):
        return jsonify({
            'code': 1002,
            'msg': '用户名已存在',
            'data': None
        }), 400
    
    # 创建新用户
    user_id = str(uuid.uuid4())
    users_db[user_id] = {
        'id': user_id,
        'username': username,
        'password': generate_password_hash(password),
        'email': email,
        'phone': phone,
        'role_id': 3,  # 默认为学生角色
        'original_platform_id': None,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'last_login': None,
        'status': 1
    }
    
    # 生成访问令牌
    token = generate_access_token(user_id)
    
    return jsonify({
        'code': 0,
        'msg': '注册成功',
        'data': {
            'userId': user_id,
            'username': username,
            'token': token
        }
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    remember_me = data.get('rememberMe', False)
    
    # 查找用户
    user = None
    for u in users_db.values():
        if u['username'] == username:
            user = u
            break
    
    # 验证用户存在性和密码
    if not user:
        return jsonify({
            'code': 2001,
            'msg': '用户不存在',
            'data': None
        }), 401
    
    if not check_password_hash(user['password'], password):
        return jsonify({
            'code': 2002,
            'msg': '密码错误',
            'data': None
        }), 401
    
    if user['status'] != 1:
        return jsonify({
            'code': 2003,
            'msg': '账号已被禁用',
            'data': None
        }), 403
    
    # 更新最后登录时间
    user['last_login'] = datetime.datetime.now().isoformat()
    
    # 生成访问令牌和刷新令牌
    access_token = generate_access_token(user['id'])
    refresh_token = generate_refresh_token(user['id'])
    
    # 设置令牌过期时间
    expires_in = JWT_REFRESH_TOKEN_EXPIRES if remember_me else JWT_ACCESS_TOKEN_EXPIRES
    
    return jsonify({
        'code': 0,
        'msg': '登录成功',
        'data': {
            'userId': user['id'],
            'username': user['username'],
            'token': access_token,
            'refreshToken': refresh_token,
            'expiresIn': expires_in
        }
    })

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('refreshToken'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    refresh_token = data.get('refreshToken')
    
    try:
        # 验证刷新令牌
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=['HS256'])
        user_id = payload['sub']
        token_type = payload['type']
        
        # 检查令牌类型
        if token_type != 'refresh':
            raise jwt.InvalidTokenError('Invalid token type')
        
        # 检查用户是否存在
        if user_id not in users_db:
            raise jwt.InvalidTokenError('User not found')
        
        # 生成新的访问令牌和刷新令牌
        new_access_token = generate_access_token(user_id)
        new_refresh_token = generate_refresh_token(user_id)
        
        return jsonify({
            'code': 0,
            'msg': '刷新成功',
            'data': {
                'token': new_access_token,
                'refreshToken': new_refresh_token,
                'expiresIn': JWT_ACCESS_TOKEN_EXPIRES
            }
        })
    
    except jwt.ExpiredSignatureError:
        return jsonify({
            'code': 2004,
            'msg': '刷新令牌已过期',
            'data': None
        }), 401
    
    except jwt.InvalidTokenError:
        return jsonify({
            'code': 2004,
            'msg': '无效的刷新令牌',
            'data': None
        }), 401

@auth_bp.route('/bind-original-account', methods=['POST'])
def bind_original_account():
    # 获取请求头中的令牌
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
        
        # 获取请求数据
        data = request.get_json()
        
        # 验证请求数据
        if not data or not data.get('loginName') or not data.get('password'):
            return jsonify({
                'code': 1001,
                'msg': '参数错误',
                'data': None
            }), 400
        
        login_name = data.get('loginName')
        password = data.get('password')
        device_type = data.get('deviceType', 1)
        role_type = data.get('roleType', 1)
        
        # 这里应该调用原平台API进行验证
        # 由于我们无法实际调用，这里模拟成功响应
        
        # 更新用户信息
        original_platform_id = f"original_{user_id}"  # 模拟原平台ID
        users_db[user_id]['original_platform_id'] = original_platform_id
        
        return jsonify({
            'code': 0,
            'msg': '绑定成功',
            'data': {
                'originalPlatformId': original_platform_id,
                'bindStatus': True
            }
        })
    
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

def generate_access_token(user_id):
    """生成访问令牌"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'type': 'access'
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def generate_refresh_token(user_id):
    """生成刷新令牌"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRES),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'type': 'refresh'
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
