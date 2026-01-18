#!/bin/bash

# Streamlit Cloud 部署准备脚本

echo "========================================"
echo "  Streamlit Cloud 部署准备"
echo "========================================"
echo ""

# 获取当前目录
CURRENT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "当前目录: $CURRENT_DIR"
echo ""

# 检查 app.py 是否存在
if [ ! -f "app.py" ]; then
    echo "❌ 错误：找不到 app.py 文件"
    echo "请确保在正确的目录下运行此脚本"
    exit 1
fi

echo "✅ 找到 app.py"
echo ""

# 检查 requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误：找不到 requirements.txt 文件"
    exit 1
fi

echo "✅ 找到 requirements.txt"
echo ""

# 初始化 Git 仓库（如果还没有）
if [ ! -d ".git" ]; then
    echo "正在初始化 Git 仓库..."
    git init
    echo "✅ Git 仓库已初始化"
    echo ""
else
    echo "✅ Git 仓库已存在"
    echo ""
fi

# 显示部署步骤
echo "========================================"
echo "  部署步骤"
echo "========================================"
echo ""
echo "1️⃣  提交代码到 Git："
echo "   git add ."
echo "   git commit -m \"Initial commit: 剧本分镜生成系统\""
echo ""
echo "2️⃣  创建 GitHub 仓库："
echo "   - 访问：https://github.com/new"
echo "   - 创建新仓库（建议选择 Public）"
echo "   - 不要初始化 README"
echo ""
echo "3️⃣  连接并推送代码："
echo "   git remote add origin https://github.com/你的用户名/仓库名.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4️⃣  部署到 Streamlit Cloud："
echo "   - 访问：https://share.streamlit.io/"
echo "   - 使用 GitHub 登录"
echo "   - 点击 \"New app\""
echo "   - Repository: 选择你的仓库"
echo "   - Branch: main"
echo "   - Main file path: app.py"
echo "   - 点击 \"Deploy\""
echo ""
echo "5️⃣  配置 Secrets（可选）："
echo "   - 进入应用 Settings"
echo "   - 找到 \"Secrets\""
echo "   - 添加 APP_PASSWORD（如果需要密码保护）"
echo ""
echo "========================================"
echo ""
echo "详细说明请查看：STREAMLIT_CLOUD_DEPLOY.md"
echo ""

