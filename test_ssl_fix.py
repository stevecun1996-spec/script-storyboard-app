#!/usr/bin/env python3
"""
测试 SSL 修复是否生效
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.llm_service import LLMService
import platform

print("=" * 50)
print("SSL 修复测试")
print("=" * 50)
print(f"系统: {platform.system()}")
print(f"是否为 macOS: {platform.system() == 'Darwin'}")
print()

# 测试 API Key（需要用户提供）
api_key = os.environ.get("API_KEY", "")
if not api_key:
    print("⚠️  未设置 API_KEY 环境变量")
    print("使用方法: API_KEY=your_key python3 test_ssl_fix.py")
    print()
    api_key = input("请输入 API Key (或按 Enter 跳过): ").strip()
    if not api_key:
        print("跳过测试（需要 API Key）")
        sys.exit(0)

print("测试 1: 获取模型列表")
print("-" * 50)
try:
    service = LLMService()
    models = service.fetch_available_models("Apigather", api_key)
    print(f"✅ 成功！获取到 {len(models)} 个模型")
    print(f"前5个模型: {models[:5]}")
except Exception as e:
    print(f"❌ 失败: {str(e)}")
    print()
    print("错误详情:")
    import traceback
    traceback.print_exc()

print()
print("=" * 50)
print("测试完成")
print("=" * 50)
