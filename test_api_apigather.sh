#!/bin/bash

# Apigather API 专用测试脚本
# 用于诊断 SSL 和连接问题

echo "=========================================="
echo "Apigather API 诊断测试"
echo "=========================================="
echo ""

# 检查 API Key
if [ -z "$API_KEY" ]; then
    echo "请输入 API Key:"
    read -s API_KEY
    echo ""
fi

if [ -z "$API_KEY" ]; then
    echo "错误: API Key 不能为空"
    exit 1
fi

API_BASE="https://apigather.com/v1"

echo "测试 1: 基本连接测试（跳过 SSL 验证）"
echo "----------------------------------------"
curl -k -s -w "\nHTTP状态码: %{http_code}\n" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  "$API_BASE/models" | python3 -m json.tool 2>/dev/null || echo "响应不是有效的 JSON"
echo ""

echo "测试 2: 完整 SSL 验证测试"
echo "----------------------------------------"
curl -s -w "\nHTTP状态码: %{http_code}\n" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  "$API_BASE/models" | python3 -m json.tool 2>/dev/null || echo "响应不是有效的 JSON 或 SSL 验证失败"
echo ""

echo "测试 3: 详细 SSL 信息"
echo "----------------------------------------"
curl -v -k -s \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  "$API_BASE/models" 2>&1 | grep -E "(SSL|TLS|certificate|verify)"
echo ""

echo "测试 4: 对话测试"
echo "----------------------------------------"
curl -k -s -w "\nHTTP状态码: %{http_code}\n" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-pro-preview",
    "messages": [
      {
        "role": "user",
        "content": "你好"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 50
  }' \
  "$API_BASE/chat/completions" | python3 -m json.tool 2>/dev/null || echo "响应不是有效的 JSON"
echo ""

echo "测试完成"
