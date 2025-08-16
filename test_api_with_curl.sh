#!/bin/bash

# 培训管理API测试脚本 (使用curl)
# 用法: ./test_api_with_curl.sh [服务器地址] [认证Token]

# 默认配置
BASE_URL="${1:-http://localhost:8080}"
TOKEN="${2}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 设置请求头
HEADERS="Content-Type: application/json"
if [ -n "$TOKEN" ]; then
    HEADERS="$HEADERS -H Authorization: Bearer $TOKEN -H Sa-Token: $TOKEN"
fi

echo -e "${BLUE}🚀 培训管理API测试脚本${NC}"
echo -e "${BLUE}服务器地址: $BASE_URL${NC}"
echo "=================================="

# 测试1: 获取培训类型列表
echo -e "\n${YELLOW}📋 测试1: 获取培训类型列表${NC}"
curl -s -X GET "$BASE_URL/training/types" \
     -H "$HEADERS" | jq '.' 2>/dev/null || echo "请求失败或需要安装jq"

# 测试2: 新增培训记录
echo -e "\n${YELLOW}📝 测试2: 新增培训记录${NC}"
RECORD_DATA='{
  "name": "测试用户",
  "team": "测试班组", 
  "score": 95.0,
  "remark": "curl测试数据",
  "absent": 0,
  "trainingType": "笔试"
}'

RESPONSE=$(curl -s -X POST "$BASE_URL/training/" \
     -H "$HEADERS" \
     -d "$RECORD_DATA")

echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"

# 提取创建的记录ID
RECORD_ID=$(echo "$RESPONSE" | jq -r '.data // empty' 2>/dev/null)

# 测试3: 分页查询
echo -e "\n${YELLOW}📊 测试3: 分页查询培训记录${NC}"
curl -s -X GET "$BASE_URL/training/page?pageNum=1&pageSize=5" \
     -H "$HEADERS" | jq '.data | {total: .total, count: (.list | length)}' 2>/dev/null || echo "查询失败"

# 测试4: 关键字搜索
echo -e "\n${YELLOW}🔍 测试4: 关键字搜索${NC}"
curl -s -X GET "$BASE_URL/training/page?keywords=测试" \
     -H "$HEADERS" | jq '.data | {total: .total, records: [.list[] | {name: .name, team: .team, score: .score}]}' 2>/dev/null || echo "搜索失败"

# 测试5: 班组排名
echo -e "\n${YELLOW}🏆 测试5: 班组排名${NC}"
for training_type in "笔试" "仿真机" "其它"; do
    echo -e "${BLUE}  $training_type 班组排名:${NC}"
    curl -s -X GET "$BASE_URL/training/team-ranking?trainingType=$training_type" \
         -H "$HEADERS" | jq '.data[]? | {team: .team, averageScore: .averageScore, ranking: .ranking}' 2>/dev/null || echo "  获取排名失败"
done

# 测试6: 获取单条记录（如果有创建成功的记录）
if [ -n "$RECORD_ID" ] && [ "$RECORD_ID" != "null" ]; then
    echo -e "\n${YELLOW}📄 测试6: 获取单条记录 (ID: $RECORD_ID)${NC}"
    curl -s -X GET "$BASE_URL/training/$RECORD_ID" \
         -H "$HEADERS" | jq '.data' 2>/dev/null || echo "获取记录失败"
         
    # 测试7: 更新记录
    echo -e "\n${YELLOW}✏️  测试7: 更新培训记录${NC}"
    UPDATE_DATA='{
      "name": "测试用户(已更新)",
      "team": "测试班组",
      "score": 98.0,
      "remark": "curl更新测试",
      "absent": 0,
      "trainingType": "笔试"
    }'
    
    curl -s -X PUT "$BASE_URL/training/$RECORD_ID" \
         -H "$HEADERS" \
         -d "$UPDATE_DATA" | jq '.' 2>/dev/null || echo "更新失败"
fi

# 测试8: 更新排名
echo -e "\n${YELLOW}🔄 测试8: 更新排名${NC}"
curl -s -X PUT "$BASE_URL/training/update-ranking?trainingType=笔试" \
     -H "$HEADERS" | jq '.' 2>/dev/null || echo "更新排名失败"

echo -e "\n${GREEN}✅ 所有测试完成!${NC}"

# 清理测试数据（如果创建成功）
if [ -n "$RECORD_ID" ] && [ "$RECORD_ID" != "null" ]; then
    echo -e "\n${YELLOW}🗑️  清理测试数据${NC}"
    curl -s -X DELETE "$BASE_URL/training/$RECORD_ID" \
         -H "$HEADERS" | jq '.' 2>/dev/null || echo "删除失败"
fi

echo -e "\n${BLUE}💡 提示:${NC}"
echo "- 如果看到 'jq: command not found'，请安装jq工具来格式化JSON输出"
echo "- 如果认证失败，请检查Token是否正确"
echo "- 如果连接失败，请检查服务器地址和端口"

