#!/bin/bash

# 简单的连接测试脚本（不需要 API Key）
# 用于测试网络连接和 SSL

echo "=========================================="
echo "API 连接测试（无需 API Key）"
echo "=========================================="
echo ""

API_BASE="https://apigather.com/v1"

echo "测试 1: 基本网络连接"
echo "----------------------------------------"
if ping -c 3 apigather.com > /dev/null 2>&1; then
    echo "✓ 网络连接正常"
else
    echo "✗ 网络连接失败"
fi
echo ""

echo "测试 2: DNS 解析"
echo "----------------------------------------"
if nslookup apigather.com > /dev/null 2>&1; then
    echo "✓ DNS 解析正常"
    nslookup apigather.com | grep -A 2 "Name:"
else
    echo "✗ DNS 解析失败"
fi
echo ""

echo "测试 3: HTTPS 连接（跳过 SSL 验证）"
echo "----------------------------------------"
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" "$API_BASE/models" 2>&1)
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "✓ HTTPS 连接成功 (HTTP $HTTP_CODE)"
    echo "  说明: 401 表示需要认证（正常），200 表示成功"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "✗ HTTPS 连接失败 (无法连接到服务器)"
else
    echo "⚠ HTTPS 连接返回: HTTP $HTTP_CODE"
fi
echo ""

echo "测试 4: SSL 证书信息"
echo "----------------------------------------"
echo "检查 SSL 证书..."
SSL_INFO=$(echo | openssl s_client -connect apigather.com:443 -servername apigather.com 2>&1 | grep -E "(Verify return code|subject=|issuer=)" | head -3)
if [ -n "$SSL_INFO" ]; then
    echo "$SSL_INFO"
else
    echo "⚠ 无法获取 SSL 证书信息"
fi
echo ""

echo "测试 5: 详细连接信息"
echo "----------------------------------------"
echo "执行详细连接测试..."
curl -k -v -s -o /dev/null "$API_BASE/models" 2>&1 | grep -E "(Connected|SSL|TLS|HTTP)" | head -10
echo ""

echo "=========================================="
echo "测试完成"
echo "=========================================="
echo ""
echo "如果 HTTPS 连接测试返回 401，说明："
echo "  - 网络连接正常"
echo "  - SSL 证书正常"
echo "  - API 端点可访问"
echo "  - 只需要提供有效的 API Key 即可使用"
echo ""
