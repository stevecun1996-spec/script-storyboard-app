#!/bin/bash

# 剧本分镜生成系统 - 启动脚本
# 双击此文件即可启动项目（macOS）

cd "$(dirname "$0")"

echo "========================================"
echo "  剧本分镜生成系统（简化版）"
echo "========================================"
echo ""
echo "正在检查依赖..."

# 检查 streamlit 是否已安装
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo ""
    echo "⚠️  检测到依赖未安装，正在安装..."
    echo ""
    pip3 install --user -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ 自动安装失败，请手动执行以下命令："
        echo ""
        echo "   pip3 install -r requirements.txt"
        echo ""
        echo "或者使用国内镜像："
        echo ""
        echo "   pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
        echo ""
        read -p "按回车键退出..."
        exit 1
    fi
    
    echo ""
    echo "✅ 依赖安装完成！"
    echo ""
fi

echo "正在启动应用..."
echo ""
echo "应用将在浏览器中自动打开"
echo "如果没有自动打开，请手动访问：http://localhost:8501"
echo ""
echo "按 Ctrl+C 可停止应用"
echo ""
echo "========================================"
echo ""

# 启动应用
python3 -m streamlit run app.py



