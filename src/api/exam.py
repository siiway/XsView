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
exam_bp = Blueprint('exam', __name__, url_prefix='/api/exam')

# 从auth.py导入模拟用户数据库，实际项目中应使用真实数据库
from src.api.auth import users_db

# 模拟考试数据库
exams_db = {}
scores_db = {}
wrong_questions_db = {}

# 初始化一些模拟数据
def init_mock_data():
    # 创建一些模拟考试
    exam_ids = []
    subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
    
    for i in range(1, 6):
        exam_id = str(uuid.uuid4())
        exam_ids.append(exam_id)
        
        exams_db[exam_id] = {
            'id': exam_id,
            'original_exam_id': f'original_exam_{i}',
            'title': f'2025年第{i}次月考',
            'subject': '全科',
            'exam_time': (datetime.datetime.now() - datetime.timedelta(days=i*10)).isoformat(),
            'total_score': 750,
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
    
    # 为每个用户创建模拟成绩
    for user_id in users_db:
        for exam_id in exam_ids:
            score_id = str(uuid.uuid4())
            
            # 随机生成成绩数据
            import random
            total_score = exams_db[exam_id]['total_score']
            score = round(random.uniform(total_score * 0.6, total_score * 0.95), 1)
            rank = random.randint(1, 100)
            
            scores_db[score_id] = {
                'id': score_id,
                'user_id': user_id,
                'exam_id': exam_id,
                'score': score,
                'rank': rank,
                'original_score_data': '{}',
                'created_at': datetime.datetime.now().isoformat(),
                'updated_at': datetime.datetime.now().isoformat()
            }
            
            # 创建一些模拟错题
            for j in range(1, 6):
                question_id = str(uuid.uuid4())
                wrong_questions_db[question_id] = {
                    'id': question_id,
                    'user_id': user_id,
                    'exam_id': exam_id,
                    'question_id': f'q_{j}',
                    'knowledge_point_id': f'kp_{random.randint(1, 10)}',
                    'question_content': f'这是第{j}道题的内容',
                    'correct_answer': 'A',
                    'user_answer': chr(ord('A') + random.randint(1, 3)),
                    'created_at': datetime.datetime.now().isoformat(),
                    'updated_at': datetime.datetime.now().isoformat()
                }

# 初始化模拟数据
init_mock_data()

@exam_bp.route('/list', methods=['GET'])
@token_required
def get_exam_list():
    user_id = request.user_id
    
    # 获取分页参数
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    
    # 获取用户的所有考试成绩
    user_scores = [score for score in scores_db.values() if score['user_id'] == user_id]
    
    # 按考试时间排序
    user_scores.sort(key=lambda x: exams_db[x['exam_id']]['exam_time'], reverse=True)
    
    # 分页
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_scores = user_scores[start_idx:end_idx]
    
    # 构建响应数据
    exam_list = []
    for score in paginated_scores:
        exam_id = score['exam_id']
        exam = exams_db.get(exam_id)
        
        if exam:
            exam_list.append({
                'id': exam['id'],
                'title': exam['title'],
                'subject': exam['subject'],
                'examTime': exam['exam_time'],
                'totalScore': exam['total_score'],
                'score': score['score'],
                'rank': score['rank']
            })
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': {
            'total': len(user_scores),
            'list': exam_list
        }
    })

@exam_bp.route('/detail', methods=['GET'])
@token_required
def get_exam_detail():
    user_id = request.user_id
    exam_id = request.args.get('examId')
    
    if not exam_id:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
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
    
    # 模拟科目成绩
    import random
    subject_scores = []
    subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
    
    for subject in subjects:
        subject_total = 150 if subject in ['语文', '数学', '英语'] else 100
        subject_score = round(random.uniform(subject_total * 0.6, subject_total * 0.95), 1)
        subject_rank = random.randint(1, 100)
        
        subject_scores.append({
            'subject': subject,
            'score': subject_score,
            'totalScore': subject_total,
            'rank': subject_rank
        })
    
    # 模拟题目统计
    question_stats = {
        'correct': random.randint(100, 150),
        'wrong': random.randint(20, 50),
        'partial': random.randint(10, 30),
        'unanswered': random.randint(0, 10)
    }
    
    # 构建响应数据
    detail = {
        'id': exam['id'],
        'title': exam['title'],
        'subject': exam['subject'],
        'examTime': exam['exam_time'],
        'totalScore': exam['total_score'],
        'score': user_score['score'],
        'rank': user_score['rank'],
        'classRank': random.randint(1, 50),
        'gradeRank': user_score['rank'],
        'subjectScores': subject_scores,
        'questionStats': question_stats
    }
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': detail
    })

@exam_bp.route('/analysis', methods=['GET'])
@token_required
def get_exam_analysis():
    user_id = request.user_id
    exam_id = request.args.get('examId')
    
    if not exam_id:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
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
    
    # 模拟分数分布
    score_distribution = {
        'ranges': ['0-60', '60-70', '70-80', '80-90', '90-100'],
        'counts': [10, 20, 30, 25, 15]
    }
    
    # 模拟科目分析
    import random
    subject_analysis = []
    subjects = ['语文', '数学', '英语', '物理', '化学', '生物']
    
    for subject in subjects:
        subject_total = 150 if subject in ['语文', '数学', '英语'] else 100
        subject_score = round(random.uniform(subject_total * 0.6, subject_total * 0.95), 1)
        
        subject_analysis.append({
            'subject': subject,
            'score': subject_score,
            'averageScore': round(subject_total * 0.75, 1),
            'maxScore': round(subject_total * 0.98, 1),
            'minScore': round(subject_total * 0.45, 1),
            'standardDeviation': round(subject_total * 0.1, 1)
        })
    
    # 模拟知识点分析
    knowledge_point_analysis = []
    for i in range(1, 11):
        mastery_level = round(random.uniform(0.5, 1.0), 2)
        avg_mastery_level = round(random.uniform(0.6, 0.9), 2)
        
        knowledge_point_analysis.append({
            'knowledgePoint': f'知识点{i}',
            'masteryLevel': mastery_level,
            'averageMasteryLevel': avg_mastery_level
        })
    
    # 模拟排名趋势
    rank_trend = []
    for i in range(1, 6):
        trend_exam_id = list(exams_db.keys())[i-1]
        trend_exam = exams_db[trend_exam_id]
        
        rank_trend.append({
            'examId': trend_exam_id,
            'examTitle': trend_exam['title'],
            'rank': random.randint(1, 100),
            'totalStudents': 200
        })
    
    # 构建响应数据
    analysis = {
        'examId': exam_id,
        'scoreDistribution': score_distribution,
        'subjectAnalysis': subject_analysis,
        'knowledgePointAnalysis': knowledge_point_analysis,
        'rankTrend': rank_trend
    }
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': analysis
    })

@exam_bp.route('/wrong-questions', methods=['GET'])
@token_required
def get_wrong_questions():
    user_id = request.user_id
    exam_id = request.args.get('examId')
    
    if not exam_id:
        return jsonify({
            'code': 1001,
            'msg': '参数错误',
            'data': None
        }), 400
    
    # 获取考试信息
    exam = exams_db.get(exam_id)
    if not exam:
        return jsonify({
            'code': 1002,
            'msg': '考试不存在',
            'data': None
        }), 404
    
    # 获取用户在该考试中的错题
    user_wrong_questions = [q for q in wrong_questions_db.values() 
                           if q['user_id'] == user_id and q['exam_id'] == exam_id]
    
    # 构建响应数据
    wrong_questions = []
    for question in user_wrong_questions:
        wrong_questions.append({
            'id': question['id'],
            'questionId': question['question_id'],
            'content': question['question_content'],
            'correctAnswer': question['correct_answer'],
            'userAnswer': question['user_answer'],
            'knowledgePoint': f'知识点{question["knowledge_point_id"].split("_")[1]}'
        })
    
    return jsonify({
        'code': 0,
        'msg': '获取成功',
        'data': {
            'examId': exam_id,
            'wrongQuestions': wrong_questions
        }
    })
