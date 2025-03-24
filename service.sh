#!/bin/bash

# 启动中心服务器
start_center_server() {
  echo "启动中心服务器..."
  cd /home/ubuntu/ScoreX/backend/center-server
  source venv/bin/activate
  python app.py &
  echo $! > center_server.pid
  echo "中心服务器已启动，PID: $(cat center_server.pid)"
}

# 启动边缘节点服务
start_edge_node() {
  echo "启动边缘节点服务..."
  cd /home/ubuntu/ScoreX/backend/edge-node
  node index.js &
  echo $! > edge_node.pid
  echo "边缘节点服务已启动，PID: $(cat edge_node.pid)"
}

# 停止中心服务器
stop_center_server() {
  echo "停止中心服务器..."
  cd /home/ubuntu/ScoreX/backend/center-server
  if [ -f center_server.pid ]; then
    kill $(cat center_server.pid)
    rm center_server.pid
    echo "中心服务器已停止"
  else
    echo "中心服务器未运行"
  fi
}

# 停止边缘节点服务
stop_edge_node() {
  echo "停止边缘节点服务..."
  cd /home/ubuntu/ScoreX/backend/edge-node
  if [ -f edge_node.pid ]; then
    kill $(cat edge_node.pid)
    rm edge_node.pid
    echo "边缘节点服务已停止"
  else
    echo "边缘节点服务未运行"
  fi
}

# 启动所有服务
start_all() {
  start_center_server
  sleep 2
  start_edge_node
  echo "所有服务已启动"
}

# 停止所有服务
stop_all() {
  stop_edge_node
  stop_center_server
  echo "所有服务已停止"
}

# 重启所有服务
restart_all() {
  stop_all
  sleep 2
  start_all
}

# 检查服务状态
check_status() {
  echo "检查服务状态..."
  
  # 检查中心服务器
  cd /home/ubuntu/ScoreX/backend/center-server
  if [ -f center_server.pid ] && ps -p $(cat center_server.pid) > /dev/null; then
    echo "中心服务器正在运行，PID: $(cat center_server.pid)"
  else
    echo "中心服务器未运行"
  fi
  
  # 检查边缘节点服务
  cd /home/ubuntu/ScoreX/backend/edge-node
  if [ -f edge_node.pid ] && ps -p $(cat edge_node.pid) > /dev/null; then
    echo "边缘节点服务正在运行，PID: $(cat edge_node.pid)"
  else
    echo "边缘节点服务未运行"
  fi
}

# 显示帮助信息
show_help() {
  echo "ScoreX 服务管理脚本"
  echo "用法: $0 [选项]"
  echo "选项:"
  echo "  start       启动所有服务"
  echo "  stop        停止所有服务"
  echo "  restart     重启所有服务"
  echo "  status      检查服务状态"
  echo "  center      仅启动中心服务器"
  echo "  edge        仅启动边缘节点服务"
  echo "  stop-center 仅停止中心服务器"
  echo "  stop-edge   仅停止边缘节点服务"
  echo "  help        显示此帮助信息"
}

# 主函数
case "$1" in
  start)
    start_all
    ;;
  stop)
    stop_all
    ;;
  restart)
    restart_all
    ;;
  status)
    check_status
    ;;
  center)
    start_center_server
    ;;
  edge)
    start_edge_node
    ;;
  stop-center)
    stop_center_server
    ;;
  stop-edge)
    stop_edge_node
    ;;
  help|*)
    show_help
    ;;
esac

exit 0
