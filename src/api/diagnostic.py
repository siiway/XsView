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
diagnostic_bp = Blueprint('diagnostic', __name__, url_prefix='/api/diagnostic')

# 从auth.py导入模拟用户数据库，实际项目中应使用真实数据库
from src.api.auth import users_db
from src.api.exam import exams_db, scores_db, wrong_questions_db

# 模拟诊断报告数据库
diagnostic_reports_db = {}

@diagnostic_bp.route('/generate', methods=['POST'])
@token_required
def generate_diagnostic_report():
    user_id = request.user_id
    data = request.get_json()
    
    # 验证请求数据
    if not data or not data.get('examId'):
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    exam_id = data.get('examId')
    
    # 获取考试信息
    exam = exams_db.get(exam_id)
    if not exam:
        return jsonify({
            'code': 1002,
            'msg': '考试不存在',
            'data': None
        }), 404
    
    # 获取用户在该考试中的成绩
    user_score = None
    for score in scores_db.values():
        if score['user_id'] == user_id and score['exam_id'] == exam_id:
            user_score = score
            break
    
    if not user_score:
        return jsonify({
            'code': 1002,
            'msg': '成绩不存在',
            'data': None
        }), 404
    
    # 获取用户在该考试中的错题
    user_wrong_questions = [q for q in wrong_questions_db.values() 
                           if q['user_id'] == user_id and q['exam_id'] == exam_id]
    
    # 生成诊断报告
    report_id = str(uuid.uuid4())
    
    # 模拟生成诊断报告内容
    import random
    
    # 科目分析
    subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
    subject_analysis = []
    
    for subject in subjects:
        analysis = f"{subject}科目表现{random.choice(['优秀', '良好', '一般', '需要提升'])}，"
        analysis += f"得分率{random.randint(60, 95)}%，"
        analysis += f"相比班级平均水平{random.choice(['高出', '低于'])}约{random.randint(1, 15)}个百分点。"
        
        suggestions = f"建议{random.choice(['加强基础知识掌握', '提高解题速度', '注重知识点连接', '多做综合题训练', '加强错题复习'])}"
        
        subject_analysis.append({
            'subject': subject,
            'analysis': analysis,
            'suggestions': suggestions
        })
    
    # 弱点分析
    weakness_analysis = []
    knowledge_points = [
        '函数与导数', '概率统计', '立体几何', '解析几何', 
        '语法与修辞', '阅读理解', '物理力学', '化学反应原理',
        '生物遗传学', '英语写作'
    ]
    
    for i in range(3):
        kp = random.choice(knowledge_points)
        knowledge_points.remove(kp)
        
        mastery_level = round(random.uniform(0.3, 0.6), 2)
        suggestions = f"建议{random.choice(['回归课本，夯实基础', '多做专项练习', '系统梳理知识点', '寻求老师指导', '参加专题辅导'])}"
        
        learning_materials = []
        for j in range(2):
            learning_materials.append({
                'id': f"material_{uuid.uuid4()}",
                'title': f"{kp}专项训练资料{j+1}"
            })
        
        weakness_analysis.append({
            'knowledgePoint': kp,
            'masteryLevel': mastery_level,
            'suggestions': suggestions,
            'learningMaterials': learning_materials
        })
    
    # 整体分析
    overall_analysis = f"本次考试总体表现{random.choice(['优秀', '良好', '一般', '需要提升'])}，"
    overall_analysis += f"总分{user_score['score']}分，排名第{user_score['rank']}名。"
    overall_analysis += f"相比上次考试{random.choice(['有所进步', '略有下滑', '基本持平'])}。"
    overall_analysis += f"优势学科为{random.sample(subjects, 2)}，薄弱学科为{random.sample(subjects, 2)}。"
    
    # 改进建议
    improvement_suggestions = "1. " + random.choice([
        "制定合理的学习计划，注重时间管理",
        "加强薄弱科目的针对性训练",
        "建立错题本，定期复习",
        "提高解题效率，合理分配考试时间",
        "加强基础知识掌握，注重知识点连接"
    ])
    improvement_suggestions += "\n2. " + random.choice([
        "多做综合题训练，提高应用能力",
        "参加小组讨论，加深理解",
        "向老师同学请教不懂的问题",
        "保持良好的学习状态和心态",
        "适当放松，劳逸结合"
    ])
    improvement_suggestions += "\n3. " + random.choice([
        "关注考点变化，把握命题规律",
        "多角度思考问题，提高解题灵活性",
        "加强实验操作能力",
        "提高阅读理解能力",
        "注重知识的实际应用"
    ])
    
    # 保存诊断报告
    diagnostic_reports_db[report_id] = {
        'id': report_id,
        'user_id': user_id,
        'exam_id': exam_id,
        'exam_title': exam['title'],
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'overall_analysis': overall_analysis,
        'subject_analysis': subject_analysis,
        'weakness_analysis': weakness_analysis,
        'improvement_suggestions': improvement_suggestions
    }
    
    return jsonify({
        'code': 0,
        'msg': '生成成功',
        'data': {
            'reportId': report_id
        }
    })

@diagnostic_bp.route('/report', methods=['GET'])
@token_required
def get_diagnostic_report():
    user_id = request.user_id
    report_id = request.args.get('reportId')
    
    if not report_id:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 获取诊断报告
    report = diagnostic_reports_db.get(report_id)
    
    if not report:
        return jsonify({
            'code': 1002,
            'msg': '报告不存在',
            'data': None
        }), 404
    
    # 检查报告是否属于当前用户
    if report['user_id'] != user_id:
        return jsonify({
            'code': 2005,
            'msg': '权限不足',
            'data': None
        }), 403
    
    # 构建响应数据
    report_data = {
        'id': report['id'],
        'examId': report['exam_id'],
        'examTitle': report['exam_title'],
        'createdAt': report['created_at'],
        'overallAnalysis': report['overall_analysis'],
        'subjectAnalysis': report['subject_analysis'],
        'weaknessAnalysis': report['weakness_analysis'],
        'improvementSuggestions': report['improvement_suggestions']
    }
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': report_data
    })

@diagnostic_bp.route('/history', methods=['GET'])
@token_required
def get_history_reports():
    user_id = request.user_id
    
    # 获取分页参数
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    
    # 获取用户的所有诊断报告
    user_reports = [report for report in diagnostic_reports_db.values() if report['user_id'] == user_id]
    
    # 按创建时间排序
    user_reports.sort(key=lambda x: x['created_at'], reverse=True)
    
    # 分页
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_reports = user_reports[start_idx:end_idx]
    
    # 构建响应数据
    report_list = []
    for report in paginated_reports:
        report_list.append({
            'id': report['id'],
            'examId': report['exam_id'],
            'examTitle': report['exam_title'],
            'createdAt': report['created_at']
        })
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': {
            'total': len(user_reports),
            'list': report_list
        }
    })
