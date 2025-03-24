#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
import jwt
import os
import requests
from dotenv import load_dotenv
from src.api.node import node_token_required

# 加载环境变量
load_dotenv()

# 创建蓝图
proxy_bp = Blueprint('proxy', __name__, url_prefix='/api/proxy')

# 原平台API基础URL
ORIGINAL_API_BASE_URL = os.getenv('ORIGINAL_API_BASE_URL')
ORIGINAL_API_TIMEOUT = int(os.getenv('ORIGINAL_API_TIMEOUT', 30))

@proxy_bp.route('/login', methods=['POST'])
@node_token_required
def proxy_login():
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('loginName') or not data.get('password'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 构建请求参数
    login_params = {
        'deviceType': data.get('deviceType', 1),
        'loginName': data.get('loginName'),
        'password': data.get('password'),
        'rememberMe': data.get('rememberMe', 1),
        'roleType': data.get('roleType', 1)
    }
    
    # 构建请求头
    headers = {
        'User-Agent': 'Android 13',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # 调用原平台登录接口
        response = requests.post(
            f"{ORIGINAL_API_BASE_URL}/v2/users/sessions",
            data=login_params,
            headers=headers,
            timeout=ORIGINAL_API_TIMEOUT
        )
        
        # 解析响应
        result = response.json()
        
        # 记录用户ID和请求信息
        user_id = data.get('userId')
        node_id = request.node_id
        
        # 实际项目中应该将这些信息记录到数据库
        print(f"用户 {user_id} 通过节点 {node_id} 登录原平台")
        
        # 返回响应
        return jsonify({
            'code': result.get('code', 0),
            'msg': result.get('msg', '登录成功'),
            'data': result.get('data')
        })
    
    except requests.RequestException as e:
        return jsonify({
            'code': 3001,
            'msg': f'原平台API调用失败: {str(e)}',
            'data': None
        }), 500

@proxy_bp.route('/user-info', methods=['GET'])
@node_token_required
def proxy_user_info():
    # 获取请求参数
    user_id = request.args.get('userId')
    token = request.args.get('token')
    
    if not user_id or not token:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 构建请求头
    headers = {
        'User-Agent': 'Android 13',
        'Authorization': token
    }
    
    try:
        # 调用原平台用户信息接口
        response = requests.get(
            f"{ORIGINAL_API_BASE_URL}/v2/user-center/user-snapshot",
            headers=headers,
            timeout=ORIGINAL_API_TIMEOUT
        )
        
        # 解析响应
        result = response.json()
        
        # 记录节点ID
        node_id = request.node_id
        
        # 实际项目中应该将这些信息记录到数据库
        print(f"用户 {user_id} 通过节点 {node_id} 获取用户信息")
        
        # 返回响应
        return jsonify({
            'code': result.get('code', 0),
            'msg': result.get('msg', '获取成功'),
            'data': {
                'userInfo': result.get('data')
            }
        })
    
    except requests.RequestException as e:
        return jsonify({
            'code': 3001,
            'msg': f'原平台API调用失败: {str(e)}',
            'data': None
        }), 500

@proxy_bp.route('/exam-list', methods=['GET'])
@node_token_required
def proxy_exam_list():
    # 获取请求参数
    user_id = request.args.get('userId')
    token = request.args.get('token')
    
    if not user_id or not token:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 构建请求头
    headers = {
        'User-Agent': 'Android 13',
        'Authorization': token
    }
    
    try:
        # 调用原平台考试列表接口
        response = requests.get(
            f"{ORIGINAL_API_BASE_URL}/v4/exam/list",
            headers=headers,
            timeout=ORIGINAL_API_TIMEOUT
        )
        
        # 解析响应
        result = response.json()
        
        # 记录节点ID
        node_id = request.node_id
        
        # 实际项目中应该将这些信息记录到数据库
        print(f"用户 {user_id} 通过节点 {node_id} 获取考试列表")
        
        # 返回响应
        return jsonify({
            'code': result.get('code', 0),
            'msg': result.get('msg', '获取成功'),
            'data': {
                'examList': result.get('data', {}).get('list', [])
            }
        })
    
    except requests.RequestException as e:
        return jsonify({
            'code': 3001,
            'msg': f'原平台API调用失败: {str(e)}',
            'data': None
        }), 500

@proxy_bp.route('/exam-detail', methods=['GET'])
@node_token_required
def proxy_exam_detail():
    # 获取请求参数
    user_id = request.args.get('userId')
    token = request.args.get('token')
    exam_id = request.args.get('examId')
    
    if not user_id or not token or not exam_id:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 构建请求头
    headers = {
        'User-Agent': 'Android 13',
        'Authorization': token
    }
    
    try:
        # 调用原平台考试详情接口
        response = requests.get(
            f"{ORIGINAL_API_BASE_URL}/v4/exam/detail",
            params={'id': exam_id},
            headers=headers,
            timeout=ORIGINAL_API_TIMEOUT
        )
        
        # 解析响应
        result = response.json()
        
        # 记录节点ID
        node_id = request.node_id
        
        # 实际项目中应该将这些信息记录到数据库
        print(f"用户 {user_id} 通过节点 {node_id} 获取考试详情 {exam_id}")
        
        # 返回响应
        return jsonify({
            'code': result.get('code', 0),
            'msg': result.get('msg', '获取成功'),
            'data': {
                'examDetail': result.get('data')
            }
        })
    
    except requests.RequestException as e:
        return jsonify({
            'code': 3001,
            'msg': f'原平台API调用失败: {str(e)}',
            'data': None
        }), 500
