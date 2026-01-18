#!/bin/bash

echo "========================================"
echo "  剧本分镜生成系统（简化版）"
echo "========================================"
echo ""
echo "正在启动应用..."
echo ""

cd "$(dirname "$0")"
streamlit run app.py


