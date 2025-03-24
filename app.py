#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

# 导入API蓝图
from src.api.auth import auth_bp
from src.api.user import user_bp
from src.api.exam import exam_bp
from src.api.diagnostic import diagnostic_bp
from src.api.learning import learning_bp
from src.api.notification import notification_bp
from src.api.node import node_bp
from src.api.proxy import proxy_bp

# 加载环境变量
load_dotenv()

# 创建应用实例
app = Flask(__name__)

# 配置应用
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))

# 配置CORS
cors_origins = os.getenv('CORS_ORIGINS', '').split(',')
CORS(app, resources={r"/api/*": {"origins": cors_origins}})

# 配置日志
log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO'))
log_file = os.getenv('LOG_FILE', 'logs/server.log')

# 确保日志目录存在
os.makedirs(os.path.dirname(log_file), exist_ok=True)

handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
handler.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(log_level)

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(exam_bp)
app.register_blueprint(diagnostic_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(node_bp)
app.register_blueprint(proxy_bp)

@app.route('/')
def index():
    return {
        'name': 'ScoreX API Server',
        'version': '1.0.0',
        'status': 'running'
    }

if __name__ == '__main__':
    host = os.getenv('SERVER_HOST', '0.0.0.0')
    port = int(os.getenv('SERVER_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
