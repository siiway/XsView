#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
import jwt
import os
import uuid
import datetime
from dotenv import load_dotenv
from src.api.user import token_required

# 加载环境变量
load_dotenv()

# 创建蓝图
notification_bp = Blueprint('notification', __name__, url_prefix='/api/notification')

# 从auth.py导入模拟用户数据库，实际项目中应使用真实数据库
from src.api.auth import users_db

# 模拟通知数据库
notifications_db = {}

# 初始化一些模拟数据
def init_mock_data():
    # 为每个用户创建一些模拟通知
    for user_id in users_db:
        # 系统通知
        notification_id = str(uuid.uuid4())
        notifications_db[notification_id] = {
            'id': notification_id,
            'user_id': user_id,
            'title': '欢迎使用ScoreX查分星',
            'content': '感谢您使用ScoreX查分星系统，我们将为您提供优质的考试成绩查询和分析服务。',
            'is_read': False,
            'type': 'system',
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        # 成绩更新通知
        notification_id = str(uuid.uuid4())
        notifications_db[notification_id] = {
            'id': notification_id,
            'user_id': user_id,
            'title': '新考试成绩已更新',
            'content': '您的2025年第1次月考成绩已更新，点击查看详情。',
            'is_read': False,
            'type': 'score',
            'created_at': (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat(),
            'updated_at': (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat()
        }
        
        # 诊断报告通知
        notification_id = str(uuid.uuid4())
        notifications_db[notification_id] = {
            'id': notification_id,
            'user_id': user_id,
            'title': '考试诊断报告已生成',
            'content': '您的2025年第1次月考诊断报告已生成，点击查看详情。',
            'is_read': True,
            'type': 'report',
            'created_at': (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
            'updated_at': (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        }
        
        # 学习资料推荐
        notification_id = str(uuid.uuid4())
        notifications_db[notification_id] = {
            'id': notification_id,
            'user_id': user_id,
            'title': '为您推荐学习资料',
            'content': '根据您的考试情况，我们为您推荐了一些学习资料，点击查看。',
            'is_read': False,
            'type': 'material',
            'created_at': (datetime.datetime.now() - datetime.timedelta(hours=12)).isoformat(),
            'updated_at': (datetime.datetime.now() - datetime.timedelta(hours=12)).isoformat()
        }

# 初始化模拟数据
init_mock_data()

@notification_bp.route('/list', methods=['GET'])
@token_required
def get_notification_list():
    user_id = request.user_id
    
    # 获取分页和筛选参数
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    is_read = request.args.get('isRead')
    
    # 获取用户的通知
    user_notifications = [n for n in notifications_db.values() if n['user_id'] == user_id]
    
    # 根据是否已读筛选
    if is_read is not None:
        is_read_bool = is_read.lower() == 'true'
        user_notifications = [n for n in user_notifications if n['is_read'] == is_read_bool]
    
    # 按创建时间排序
    user_notifications.sort(key=lambda x: x['created_at'], reverse=True)
    
    # 分页
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_notifications = user_notifications[start_idx:end_idx]
    
    # 计算未读通知数量
    unread_count = sum(1 for n in notifications_db.values() 
                      if n['user_id'] == user_id and not n['is_read'])
    
    # 构建响应数据
    notification_list = []
    for notification in paginated_notifications:
        notification_list.append({
            'id': notification['id'],
            'title': notification['title'],
            'content': notification['content'],
            'isRead': notification['is_read'],
            'type': notification['type'],
            'createdAt': notification['created_at']
        })
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': {
            'total': len(user_notifications),
            'unreadCount': unread_count,
            'list': notification_list
        }
    })

@notification_bp.route('/read', methods=['PUT'])
@token_required
def mark_notification_read():
    user_id = request.user_id
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('notificationId'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    notification_id = data.get('notificationId')
    
    # 获取通知
    notification = notifications_db.get(notification_id)
    
    if not notification:
        return jsonify({
            'code': 1002,
            'msg': '通知不存在',
            'data': None
        }), 404
    
    # 检查通知是否属于当前用户
    if notification['user_id'] != user_id:
        return jsonify({
            'code': 2005,
            'msg': '权限不足',
            'data': None
        }), 403
    
    # 标记为已读
    notification['is_read'] = True
    notification['updated_at'] = datetime.datetime.now().isoformat()
    
    return jsonify({
        'code': 0,
        'msg': '标记成功',
        'data': None
    })
