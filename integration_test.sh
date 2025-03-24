#!/bin/bash

# 集成测试脚本
# 用于测试ScoreX系统的各个组件是否正常工作

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 测试结果统计
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 打印测试结果
print_result() {
  local test_name=$1
  local result=$2
  local message=$3
  
  TOTAL_TESTS=$((TOTAL_TESTS + 1))
  
  if [ "$result" = "PASS" ]; then
    echo -e "${GREEN}[PASS]${NC} $test_name"
    PASSED_TESTS=$((PASSED_TESTS + 1))
  else
    echo -e "${RED}[FAIL]${NC} $test_name: $message"
    FAILED_TESTS=$((FAILED_TESTS + 1))
  fi
}

# 测试中心服务器是否启动
test_center_server() {
  echo -e "\n${YELLOW}测试中心服务器...${NC}"
  
  # 启动中心服务器
  cd /home/ubuntu/ScoreX
  ./service.sh center
  sleep 3
  
  # 检查服务是否运行
  cd /home/ubuntu/ScoreX/backend/center-server
  if [ -f center_server.pid ] && ps -p $(cat center_server.pid) > /dev/null; then
    print_result "中心服务器启动" "PASS"
  else
    print_result "中心服务器启动" "FAIL" "服务未能成功启动"
    return 1
  fi
  
  # 测试API接口
  response=$(curl -s http://localhost:5000/api/health)
  if [[ "$response" == *"status"*:"ok"* ]]; then
    print_result "中心服务器健康检查" "PASS"
  else
    print_result "中心服务器健康检查" "FAIL" "健康检查接口未返回预期结果"
  fi
  
  return 0
}

# 测试边缘节点服务是否启动
test_edge_node() {
  echo -e "\n${YELLOW}测试边缘节点服务...${NC}"
  
  # 启动边缘节点服务
  cd /home/ubuntu/ScoreX
  ./service.sh edge
  sleep 3
  
  # 检查服务是否运行
  cd /home/ubuntu/ScoreX/backend/edge-node
  if [ -f edge_node.pid ] && ps -p $(cat edge_node.pid) > /dev/null; then
    print_result "边缘节点服务启动" "PASS"
  else
    print_result "边缘节点服务启动" "FAIL" "服务未能成功启动"
    return 1
  fi
  
  # 测试API接口
  response=$(curl -s http://localhost:3000/api/health)
  if [[ "$response" == *"status"*:"ok"* ]]; then
    print_result "边缘节点服务健康检查" "PASS"
  else
    print_result "边缘节点服务健康检查" "FAIL" "健康检查接口未返回预期结果"
  fi
  
  return 0
}

# 测试中心服务器和边缘节点之间的通信
test_communication() {
  echo -e "\n${YELLOW}测试服务间通信...${NC}"
  
  # 测试中心服务器到边缘节点的通信
  response=$(curl -s http://localhost:5000/api/node/status)
  if [[ "$response" == *"status"*:"ok"* ]]; then
    print_result "中心服务器到边缘节点通信" "PASS"
  else
    print_result "中心服务器到边缘节点通信" "FAIL" "通信测试失败"
  fi
  
  return 0
}

# 测试用户认证功能
test_authentication() {
  echo -e "\n${YELLOW}测试用户认证功能...${NC}"
  
  # 测试登录功能
  response=$(curl -s -X POST http://localhost:5000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"test_user","password":"test_password"}')
  
  if [[ "$response" == *"error"* ]]; then
    print_result "用户登录（无效凭据）" "PASS" "正确拒绝了无效凭据"
  else
    print_result "用户登录（无效凭据）" "FAIL" "未能正确拒绝无效凭据"
  fi
  
  return 0
}

# 测试API代理功能
test_api_proxy() {
  echo -e "\n${YELLOW}测试API代理功能...${NC}"
  
  # 测试API代理
  response=$(curl -s http://localhost:5000/api/proxy/status)
  if [[ "$response" == *"status"* ]]; then
    print_result "API代理功能" "PASS"
  else
    print_result "API代理功能" "FAIL" "代理接口未返回预期结果"
  fi
  
  return 0
}

# 性能测试
test_performance() {
  echo -e "\n${YELLOW}执行性能测试...${NC}"
  
  # 简单的负载测试
  start_time=$(date +%s.%N)
  for i in {1..50}; do
    curl -s http://localhost:5000/api/health > /dev/null
  done
  end_time=$(date +%s.%N)
  
  duration=$(echo "$end_time - $start_time" | bc)
  requests_per_second=$(echo "50 / $duration" | bc)
  
  if (( $(echo "$requests_per_second > 10" | bc -l) )); then
    print_result "API性能测试" "PASS" "每秒处理请求数: $requests_per_second"
  else
    print_result "API性能测试" "FAIL" "性能不达标，每秒处理请求数: $requests_per_second"
  fi
  
  return 0
}

# 清理测试环境
cleanup() {
  echo -e "\n${YELLOW}清理测试环境...${NC}"
  
  cd /home/ubuntu/ScoreX
  ./service.sh stop
  
  echo "测试环境已清理"
}

# 打印测试摘要
print_summary() {
  echo -e "\n${YELLOW}测试摘要${NC}"
  echo "总测试数: $TOTAL_TESTS"
  echo -e "${GREEN}通过: $PASSED_TESTS${NC}"
  echo -e "${RED}失败: $FAILED_TESTS${NC}"
  
  if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}所有测试通过!${NC}"
    exit 0
  else
    echo -e "\n${RED}测试失败!${NC}"
    exit 1
  fi
}

# 主函数
main() {
  echo "===== ScoreX 系统集成测试 ====="
  echo "开始时间: $(date)"
  
  # 运行测试
  test_center_server
  test_edge_node
  test_communication
  test_authentication
  test_api_proxy
  test_performance
  
  # 清理环境
  cleanup
  
  # 打印摘要
  print_summary
}

# 执行主函数
main
