#!/bin/bash

# Apigather API 测试脚本
# 用于测试 Apigather API 的连接和功能

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Apigather API 测试脚本"
echo "=========================================="
echo ""

# 配置
API_BASE="https://apigather.com/v1/chat/completions"
API_KEY="sk-XrJFGSaZRmjWSSt6cs5tNchNOaWR0VHD7wzz9LtonWewqr15"
MODEL="gemini-3-pro-preview"

echo -e "${BLUE}API 端点: ${API_BASE}${NC}"
echo -e "${BLUE}模型: ${MODEL}${NC}"
echo ""

# 测试 1: 简单对话测试
echo -e "${YELLOW}测试 1: 简单对话测试${NC}"
echo "----------------------------------------"

RESPONSE=$(curl -k -s -X POST "${API_BASE}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{
    \"model\": \"${MODEL}\",
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"你好，请回复'测试成功'\"
      }
    ],
    \"temperature\": 0.7
  }" \
  --connect-timeout 30 \
  --max-time 60 \
  -w "\nHTTP_CODE:%{http_code}\nTIME:%{time_total}")

HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
TIME_TOTAL=$(echo "$RESPONSE" | grep "TIME:" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d' | sed '/TIME:/d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ 请求成功 (HTTP $HTTP_CODE)${NC}"
    echo -e "${GREEN}响应时间: ${TIME_TOTAL}秒${NC}"
    echo ""
    echo "响应内容:"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    
    # 提取回复内容
    CONTENT=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['message']['content'])" 2>/dev/null)
    if [ ! -z "$CONTENT" ]; then
        echo ""
        echo -e "${GREEN}AI 回复: ${CONTENT}${NC}"
    fi
else
    echo -e "${RED}❌ 请求失败 (HTTP $HTTP_CODE)${NC}"
    echo "响应内容:"
    echo "$BODY"
fi

echo ""
echo "=========================================="

# 测试 2: 获取模型列表（如果支持）
echo -e "${YELLOW}测试 2: 获取模型列表${NC}"
echo "----------------------------------------"

MODELS_RESPONSE=$(curl -k -s -X GET "https://apigather.com/v1/models" \
  -H "Authorization: Bearer ${API_KEY}" \
  --connect-timeout 30 \
  --max-time 30 \
  -w "\nHTTP_CODE:%{http_code}")

MODELS_HTTP_CODE=$(echo "$MODELS_RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
MODELS_BODY=$(echo "$MODELS_RESPONSE" | sed '/HTTP_CODE:/d')

if [ "$MODELS_HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ 获取模型列表成功${NC}"
    echo "可用模型:"
    echo "$MODELS_BODY" | python3 -m json.tool 2>/dev/null || echo "$MODELS_BODY"
else
    echo -e "${YELLOW}⚠️  获取模型列表失败或未支持 (HTTP $MODELS_HTTP_CODE)${NC}"
    echo "响应: $MODELS_BODY"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}测试完成${NC}"
