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
learning_bp = Blueprint('learning', __name__, url_prefix='/api/learning')

# 从auth.py导入模拟用户数据库，实际项目中应使用真实数据库
from src.api.auth import users_db
from src.api.diagnostic import diagnostic_reports_db

# 模拟学习资料数据库
learning_materials_db = {}

# 初始化一些模拟数据
def init_mock_data():
    # 创建一些模拟学习资料
    knowledge_points = [
        '函数与导数', '概率统计', '立体几何', '解析几何', 
        '语法与修辞', '阅读理解', '物理力学', '化学反应原理',
        '生物遗传学', '英语写作'
    ]
    
    for i, kp in enumerate(knowledge_points):
        for j in range(1, 4):
            material_id = str(uuid.uuid4())
            material_type = ['文档', '视频', '习题'][j % 3]
            
            learning_materials_db[material_id] = {
                'id': material_id,
                'knowledge_point_id': f'kp_{i+1}',
                'knowledge_point': kp,
                'title': f'{kp}专项{material_type}{j}',
                'content': f'这是关于{kp}的学习资料，包含了重要知识点和练习题。',
                'file_path': f'/materials/{kp.replace(" ", "_")}_{j}.pdf',
                'type': material_type,
                'description': f'{kp}的核心概念讲解和例题分析，适合{["基础", "提高", "拔高"][j % 3]}阶段学习。',
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            }

# 初始化模拟数据
init_mock_data()

@learning_bp.route('/recommended', methods=['GET'])
@token_required
def get_recommended_materials():
    user_id = request.user_id
    
    # 获取用户的诊断报告
    user_reports = [report for report in diagnostic_reports_db.values() if report['user_id'] == user_id]
    
    # 如果没有诊断报告，返回随机推荐
    if not user_reports:
        import random
        recommended_materials = random.sample(list(learning_materials_db.values()), min(5, len(learning_materials_db)))
    else:
        # 按创建时间排序，获取最新的诊断报告
        user_reports.sort(key=lambda x: x['created_at'], reverse=True)
        latest_report = user_reports[0]
        
        # 从弱点分析中获取知识点
        weak_knowledge_points = [item['knowledgePoint'] for item in latest_report['weakness_analysis']]
        
        # 查找相关学习资料
        recommended_materials = []
        for material in learning_materials_db.values():
            if material['knowledge_point'] in weak_knowledge_points:
                recommended_materials.append(material)
        
        # 如果相关资料不足5个，添加一些随机资料
        if len(recommended_materials) < 5:
            import random
            other_materials = [m for m in learning_materials_db.values() if m not in recommended_materials]
            additional_materials = random.sample(other_materials, min(5 - len(recommended_materials), len(other_materials)))
            recommended_materials.extend(additional_materials)
    
    # 构建响应数据
    materials_list = []
    for material in recommended_materials:
        materials_list.append({
            'id': material['id'],
            'title': material['title'],
            'knowledgePoint': material['knowledge_point'],
            'type': material['type'],
            'description': material['description']
        })
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': {
            'materials': materials_list
        }
    })

@learning_bp.route('/material', methods=['GET'])
@token_required
def get_material_detail():
    material_id = request.args.get('materialId')
    
    if not material_id:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 获取学习资料
    material = learning_materials_db.get(material_id)
    
    if not material:
        return jsonify({
            'code': 1002,
            'msg': '学习资料不存在',
            'data': None
        }), 404
    
    # 构建响应数据
    material_data = {
        'id': material['id'],
        'title': material['title'],
        'knowledgePoint': material['knowledge_point'],
        'content': material['content'],
        'filePath': material['file_path']
    }
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': material_data
    })
