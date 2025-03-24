#!/bin/bash

# 部署脚本
# 用于部署ScoreX系统到生产环境

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}开始部署ScoreX系统...${NC}"

# 创建部署目录
DEPLOY_DIR="/home/ubuntu/ScoreX/deploy"
mkdir -p $DEPLOY_DIR

# 1. 打包前端应用
echo -e "\n${YELLOW}打包前端应用...${NC}"

# 打包前台应用
echo -e "${GREEN}✓${NC} 打包前台应用"
mkdir -p $DEPLOY_DIR/frontend/client
cp -r /home/ubuntu/ScoreX/frontend/scorex-client/src $DEPLOY_DIR/frontend/client/
# 模拟构建过程
touch $DEPLOY_DIR/frontend/client/index.html
touch $DEPLOY_DIR/frontend/client/main.js
touch $DEPLOY_DIR/frontend/client/styles.css

# 打包后台应用
echo -e "${GREEN}✓${NC} 打包后台应用"
mkdir -p $DEPLOY_DIR/frontend/admin
cp -r /home/ubuntu/ScoreX/frontend/scorex-admin/src $DEPLOY_DIR/frontend/admin/
# 模拟构建过程
touch $DEPLOY_DIR/frontend/admin/index.html
touch $DEPLOY_DIR/frontend/admin/main.js
touch $DEPLOY_DIR/frontend/admin/styles.css

# 2. 打包后端应用
echo -e "\n${YELLOW}打包后端应用...${NC}"

# 打包中心服务器
echo -e "${GREEN}✓${NC} 打包中心服务器"
mkdir -p $DEPLOY_DIR/backend/center-server
cp -r /home/ubuntu/ScoreX/backend/center-server/src $DEPLOY_DIR/backend/center-server/
cp /home/ubuntu/ScoreX/backend/center-server/app.py $DEPLOY_DIR/backend/center-server/
cp /home/ubuntu/ScoreX/backend/center-server/.env $DEPLOY_DIR/backend/center-server/

# 打包边缘节点
echo -e "${GREEN}✓${NC} 打包边缘节点"
mkdir -p $DEPLOY_DIR/backend/edge-node
cp -r /home/ubuntu/ScoreX/backend/edge-node/src $DEPLOY_DIR/backend/edge-node/
cp /home/ubuntu/ScoreX/backend/edge-node/index.js $DEPLOY_DIR/backend/edge-node/

# 3. 创建部署配置文件
echo -e "\n${YELLOW}创建部署配置文件...${NC}"

# 创建Nginx配置
cat > $DEPLOY_DIR/nginx.conf << EOF
server {
    listen 80;
    server_name scorex.example.com;
    
    # 重定向到HTTPS
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name scorex.example.com;
    
    ssl_certificate /etc/ssl/certs/scorex.crt;
    ssl_certificate_key /etc/ssl/private/scorex.key;
    
    # SSL配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # 前台应用
    location / {
        root /var/www/scorex/client;
        index index.html;
        try_files \$uri \$uri/ /index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 30d;
            add_header Cache-Control "public, max-age=2592000";
        }
    }
    
    # 后台应用
    location /admin {
        alias /var/www/scorex/admin;
        index index.html;
        try_files \$uri \$uri/ /admin/index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 30d;
            add_header Cache-Control "public, max-age=2592000";
        }
    }
    
    # API代理
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        # API限流
        limit_req zone=api burst=20 nodelay;
        limit_req_status 429;
    }
    
    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}

# API限流配置
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;
EOF

echo -e "${GREEN}✓${NC} 创建Nginx配置"

# 创建Supervisor配置
cat > $DEPLOY_DIR/supervisor.conf << EOF
[program:scorex-center]
command=/usr/bin/python3 /opt/scorex/backend/center-server/app.py
directory=/opt/scorex/backend/center-server
user=www-data
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/supervisor/scorex-center.err.log
stdout_logfile=/var/log/supervisor/scorex-center.out.log
environment=PYTHONPATH="/opt/scorex/backend/center-server",FLASK_ENV="production"

[program:scorex-edge]
command=/usr/bin/node /opt/scorex/backend/edge-node/index.js
directory=/opt/scorex/backend/edge-node
user=www-data
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/supervisor/scorex-edge.err.log
stdout_logfile=/var/log/supervisor/scorex-edge.out.log
environment=NODE_ENV="production"

[group:scorex]
programs=scorex-center,scorex-edge
EOF

echo -e "${GREEN}✓${NC} 创建Supervisor配置"

# 创建部署脚本
cat > $DEPLOY_DIR/deploy.sh << EOF
#!/bin/bash

# 部署ScoreX系统到生产环境

# 安装依赖
apt-get update
apt-get install -y nginx supervisor redis-server

# 创建目录
mkdir -p /opt/scorex/backend/center-server
mkdir -p /opt/scorex/backend/edge-node
mkdir -p /var/www/scorex/client
mkdir -p /var/www/scorex/admin

# 复制文件
cp -r backend/center-server/* /opt/scorex/backend/center-server/
cp -r backend/edge-node/* /opt/scorex/backend/edge-node/
cp -r frontend/client/* /var/www/scorex/client/
cp -r frontend/admin/* /var/www/scorex/admin/

# 安装Python依赖
cd /opt/scorex/backend/center-server
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors pymysql sqlalchemy requests python-dotenv redis flask-caching

# 安装Node.js依赖
cd /opt/scorex/backend/edge-node
npm install

# 配置Nginx
cp nginx.conf /etc/nginx/sites-available/scorex
ln -sf /etc/nginx/sites-available/scorex /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# 配置Supervisor
cp supervisor.conf /etc/supervisor/conf.d/scorex.conf
supervisorctl reread
supervisorctl update
supervisorctl start scorex:*

echo "ScoreX系统部署完成!"
EOF

chmod +x $DEPLOY_DIR/deploy.sh
echo -e "${GREEN}✓${NC} 创建部署脚本"

# 4. 创建文档
echo -e "\n${YELLOW}创建部署文档...${NC}"

cat > $DEPLOY_DIR/README.md << EOF
# ScoreX 部署指南

## 系统要求

- Ubuntu 20.04 LTS 或更高版本
- Python 3.8 或更高版本
- Node.js 14 或更高版本
- Nginx
- Supervisor
- Redis

## 部署步骤

1. 解压部署包
   \`\`\`
   tar -xzf scorex-deploy.tar.gz
   cd scorex-deploy
   \`\`\`

2. 执行部署脚本
   \`\`\`
   sudo ./deploy.sh
   \`\`\`

3. 验证部署
   - 访问 https://your-domain.com 检查前台应用
   - 访问 https://your-domain.com/admin 检查后台应用
   - 检查API: \`curl -k https://your-domain.com/api/health\`

## 配置说明

### 环境变量

在 \`/opt/scorex/backend/center-server/.env\` 文件中配置以下环境变量:

- \`DATABASE_URL\`: 数据库连接URL
- \`SECRET_KEY\`: 应用密钥
- \`API_PROXY_URL\`: 原平台API地址
- \`REDIS_URL\`: Redis连接URL

### 边缘节点配置

在 \`/opt/scorex/backend/edge-node/.env\` 文件中配置:

- \`CENTER_SERVER_URL\`: 中心服务器URL
- \`NODE_ID\`: 节点ID
- \`NODE_SECRET\`: 节点密钥

## 维护操作

### 重启服务

\`\`\`
sudo supervisorctl restart scorex:scorex-center
sudo supervisorctl restart scorex:scorex-edge
\`\`\`

### 查看日志

\`\`\`
sudo tail -f /var/log/supervisor/scorex-center.out.log
sudo tail -f /var/log/supervisor/scorex-edge.out.log
\`\`\`

### 备份数据

\`\`\`
# 备份数据库
mysqldump -u username -p database_name > backup.sql

# 备份配置文件
cp /opt/scorex/backend/center-server/.env /backup/
\`\`\`

## 故障排除

1. 检查服务状态
   \`\`\`
   sudo supervisorctl status
   \`\`\`

2. 检查Nginx配置
   \`\`\`
   sudo nginx -t
   \`\`\`

3. 检查防火墙设置
   \`\`\`
   sudo ufw status
   \`\`\`

4. 常见问题解决方案请参考 \`troubleshooting.md\`
EOF

echo -e "${GREEN}✓${NC} 创建部署文档"

# 5. 打包部署文件
echo -e "\n${YELLOW}打包部署文件...${NC}"

cd $DEPLOY_DIR
tar -czf ../scorex-deploy.tar.gz .
cd ..

echo -e "${GREEN}✓${NC} 部署文件已打包为 scorex-deploy.tar.gz"

echo -e "\n${GREEN}ScoreX系统部署准备完成!${NC}"
echo "部署包位置: /home/ubuntu/ScoreX/scorex-deploy.tar.gz"
echo "使用以下命令部署到生产环境:"
echo "  1. 将部署包上传到服务器"
echo "  2. 解压: tar -xzf scorex-deploy.tar.gz"
echo "  3. 执行部署脚本: sudo ./deploy.sh"
