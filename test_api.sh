#!/bin/bash

# API 测试脚本
# 用于测试不同 LLM 提供商的 API 调用

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "LLM API 测试脚本"
echo "=========================================="
echo ""

# 配置
API_KEY="${API_KEY:-}"
BRAND="${1:-Apigather}"

# 根据品牌设置 API 端点
case "$BRAND" in
    "OpenAI")
        API_BASE="https://api.openai.com/v1"
        ;;
    "通义千问"|"qwen")
        API_BASE="https://dashscope.aliyuncs.com/api/v1"
        ;;
    "智谱GLM"|"glm")
        API_BASE="https://open.bigmodel.cn/api/paas/v4"
        ;;
    "Deepseek"|"deepseek")
        API_BASE="https://api.deepseek.com/v1"
        ;;
    "月之暗面"|"moonshot")
        API_BASE="https://api.moonshot.cn/v1"
        ;;
    "Claude"|"claude")
        API_BASE="https://api.anthropic.com/v1"
        ;;
    "Apigather"|"apigather")
        API_BASE="https://apigather.com/v1"
        ;;
    "LM Studio"|"lmstudio")
        API_BASE="http://127.0.0.1:1234/v1"
        API_KEY=""  # LM Studio 不需要 API Key
        ;;
    *)
        echo -e "${RED}错误: 不支持的品牌: $BRAND${NC}"
        echo "支持的品牌: OpenAI, 通义千问, 智谱GLM, Deepseek, 月之暗面, Claude, Apigather, LM Studio"
        exit 1
        ;;
esac

echo -e "${YELLOW}测试品牌: $BRAND${NC}"
echo -e "${YELLOW}API 端点: $API_BASE${NC}"
echo ""

# 检查 API Key
if [ -z "$API_KEY" ] && [ "$BRAND" != "LM Studio" ]; then
    echo -e "${YELLOW}警告: 未设置 API_KEY 环境变量${NC}"
    echo "使用方法: API_KEY=your_key ./test_api.sh [品牌]"
    echo "或者: export API_KEY=your_key && ./test_api.sh [品牌]"
    echo ""
    read -p "请输入 API Key (或按 Enter 跳过): " API_KEY
    if [ -z "$API_KEY" ] && [ "$BRAND" != "LM Studio" ]; then
        echo -e "${RED}错误: API Key 是必需的${NC}"
        exit 1
    fi
fi

echo "=========================================="
echo "测试 1: 获取模型列表"
echo "=========================================="

# 构建 curl 命令
CURL_CMD="curl -s -w '\nHTTP状态码: %{http_code}\n'"

if [ -n "$API_KEY" ]; then
    CURL_CMD="$CURL_CMD -H 'Authorization: Bearer $API_KEY'"
fi

CURL_CMD="$CURL_CMD -H 'Content-Type: application/json'"

# 对于 macOS SSL 问题，添加 -k 选项跳过证书验证
if [[ "$OSTYPE" == "darwin"* ]]; then
    CURL_CMD="$CURL_CMD -k"
fi

CURL_CMD="$CURL_CMD '$API_BASE/models'"

echo "执行命令:"
echo "$CURL_CMD"
echo ""
echo "响应:"
echo "----------------------------------------"

# 执行 curl 命令
RESPONSE=$(eval $CURL_CMD)
HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP状态码" | awk '{print $2}')
BODY=$(echo "$RESPONSE" | sed '/HTTP状态码/d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ 成功获取模型列表${NC}"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
else
    echo -e "${RED}✗ 获取模型列表失败 (HTTP $HTTP_CODE)${NC}"
    echo "$BODY"
fi

echo ""
echo "=========================================="
echo "测试 2: 简单对话测试"
echo "=========================================="

# 根据品牌选择模型
case "$BRAND" in
    "OpenAI")
        MODEL="gpt-4o-mini"
        ;;
    "通义千问"|"qwen")
        MODEL="qwen-turbo"
        ;;
    "智谱GLM"|"glm")
        MODEL="glm-4"
        ;;
    "Deepseek"|"deepseek")
        MODEL="deepseek-chat"
        ;;
    "月之暗面"|"moonshot")
        MODEL="moonshot-v1-8k"
        ;;
    "Claude"|"claude")
        MODEL="claude-3-5-sonnet-20241022"
        ;;
    "Apigather"|"apigather")
        MODEL="gemini-3-pro-preview"
        ;;
    "LM Studio"|"lmstudio")
        MODEL="lmstudio-local"
        ;;
esac

echo "使用模型: $MODEL"
echo ""

# 构建请求体
REQUEST_BODY=$(cat <<EOF
{
  "model": "$MODEL",
  "messages": [
    {
      "role": "user",
      "content": "你好，请回复'测试成功'"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 100
}
EOF
)

echo "执行对话测试..."
echo ""

# 构建 curl 命令
CURL_CMD="curl -s -w '\nHTTP状态码: %{http_code}\n'"

if [ -n "$API_KEY" ]; then
    CURL_CMD="$CURL_CMD -H 'Authorization: Bearer $API_KEY'"
fi

CURL_CMD="$CURL_CMD -H 'Content-Type: application/json'"

# 对于 macOS SSL 问题，添加 -k 选项
if [[ "$OSTYPE" == "darwin"* ]]; then
    CURL_CMD="$CURL_CMD -k"
fi

CURL_CMD="$CURL_CMD -d '$REQUEST_BODY'"
CURL_CMD="$CURL_CMD '$API_BASE/chat/completions'"

# 执行 curl 命令
RESPONSE=$(eval $CURL_CMD)
HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP状态码" | awk '{print $2}')
BODY=$(echo "$RESPONSE" | sed '/HTTP状态码/d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ 对话测试成功${NC}"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    
    # 提取回复内容
    CONTENT=$(echo "$BODY" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['choices'][0]['message']['content'])" 2>/dev/null)
    if [ -n "$CONTENT" ]; then
        echo ""
        echo -e "${GREEN}AI 回复: $CONTENT${NC}"
    fi
else
    echo -e "${RED}✗ 对话测试失败 (HTTP $HTTP_CODE)${NC}"
    echo "$BODY"
    
    # 尝试解析错误信息
    ERROR_MSG=$(echo "$BODY" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('error', {}).get('message', ''))" 2>/dev/null)
    if [ -n "$ERROR_MSG" ]; then
        echo ""
        echo -e "${RED}错误信息: $ERROR_MSG${NC}"
    fi
fi

echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
