# 🚀 Streamlit Cloud 快速部署指南

## ✅ 部署步骤（5分钟完成）

### 步骤 1：准备代码（1分钟）

在终端中执行：

```bash
cd "/Users/Zhuanz/Desktop/cursor 工程/剧本到分镜-github/Script_to_Storyboard_Simple-main/Script_to_Storyboard_Simple"

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: 剧本分镜生成系统"
```

### 步骤 2：创建 GitHub 仓库（1分钟）

1. 访问：https://github.com/new
2. 填写信息：
   - **Repository name**: `script-storyboard-app`（或你喜欢的名称）
   - **Description**: `剧本分镜生成系统`
   - **Visibility**: 选择 **Public**（Public 仓库才能免费使用 Streamlit Cloud）
   - **不要勾选** "Initialize this repository with a README"
3. 点击 **"Create repository"**

### 步骤 3：推送代码到 GitHub（1分钟）

在终端中执行（替换为你的仓库地址）：

```bash
# 添加远程仓库
git remote add origin https://github.com/你的用户名/script-storyboard-app.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 步骤 4：部署到 Streamlit Cloud（2分钟）

1. **访问 Streamlit Cloud**
   - 打开：https://share.streamlit.io/
   - 点击右上角 **"Sign in"**
   - 选择 **"Continue with GitHub"**
   - 授权 Streamlit Cloud 访问 GitHub

2. **创建新应用**
   - 点击 **"New app"** 按钮
   - 填写信息：
     - **Repository**: 选择你刚创建的仓库
     - **Branch**: `main`
     - **Main file path**: `app.py` ⚠️ **重要：只写 `app.py`，不是完整路径**
     - **App URL**: 可以自定义（如：`script-storyboard`）
   - 点击 **"Deploy"**

3. **等待部署**
   - Streamlit Cloud 会自动安装依赖
   - 部署需要 2-5 分钟
   - 可以在日志中查看进度

4. **完成！**
   - 部署完成后，你会获得应用 URL：
     ```
     https://script-storyboard.streamlit.app
     ```

### 步骤 5：配置 Secrets（可选，如果需要密码保护）

1. 在 Streamlit Cloud 应用页面，点击右上角 ⚙️ **"Settings"**
2. 找到 **"Secrets"** 选项
3. 点击 **"Edit secrets"**
4. 添加密码（可选）：
   ```toml
   APP_PASSWORD = "你的密码"
   ```
5. 点击 **"Save"**
6. 如果需要启用密码保护，编辑 `app.py`，取消注释第 28-43 行的密码验证代码
7. 提交并推送代码：
   ```bash
   git add app.py
   git commit -m "Enable password protection"
   git push
   ```

---

## 📋 部署配置说明

### Main file path 配置

⚠️ **重要**：由于 `app.py` 在 `Script_to_Storyboard_Simple` 目录下，有两种配置方式：

**方式一（推荐）**：使用相对路径
- Main file path: `app.py`
- 如果 app.py 在仓库根目录，这样配置即可

**方式二**：如果 app.py 在子目录
- Main file path: `Script_to_Storyboard_Simple/app.py`

**建议**：检查你的仓库结构，确保 `app.py` 在正确的位置。

---

## 🔧 部署后检查

部署完成后，检查以下功能：

- [ ] ✅ 应用可以正常访问
- [ ] ✅ 侧边栏配置正常显示
- [ ] ✅ 可以输入剧本
- [ ] ✅ 可以配置 API Key
- [ ] ✅ 分镜生成功能正常
- [ ] ✅ 分镜编辑功能正常
- [ ] ✅ 提示词生成功能正常
- [ ] ✅ 导出功能正常
- [ ] ✅ 项目管理功能正常

---

## 📱 分享应用

部署完成后，你可以：

1. **直接分享链接**
   ```
   https://你的应用名.streamlit.app
   ```

2. **分享给朋友**
   - 发送应用链接
   - 如果有密码，一并提供
   - 建议朋友使用自己的 API Key

---

## ⚠️ 注意事项

1. **API Key 安全**
   - ✅ 不要在代码中硬编码 API Key
   - ✅ 建议用户使用自己的 API Key
   - ✅ 如果使用 Secrets，确保不要泄露

2. **数据隐私**
   - ⚠️ Streamlit Cloud 免费版应用是公开的
   - ⚠️ 任何获得链接的人都可以访问
   - ⚠️ 建议使用密码保护（已提供代码）

3. **文件存储**
   - ⚠️ 项目管理功能保存的文件在服务器本地
   - ⚠️ 可能无法持久化（免费版）
   - 💡 建议定期导出 Excel 保存

4. **更新应用**
   - 推送代码到 GitHub 后，Streamlit Cloud 会自动重新部署
   - 通常在 1-2 分钟内完成更新

---

## 🔍 常见问题

### Q1: 部署失败，提示找不到 app.py

**A**: 检查 Main file path 配置：
- 如果 `app.py` 在根目录：填写 `app.py`
- 如果 `app.py` 在子目录：填写 `Script_to_Storyboard_Simple/app.py`

### Q2: 依赖安装失败

**A**: 
1. 检查 `requirements.txt` 是否完整
2. 查看部署日志了解具体错误
3. 尝试简化版本要求

### Q3: 应用启动后显示错误

**A**: 
1. 在 Streamlit Cloud 点击 "Manage app"
2. 查看 "Logs" 标签页
3. 根据错误信息修复代码

### Q4: 如何查看访问统计？

**A**: 在 Streamlit Cloud：
- 进入应用 Settings
- 查看 "Usage statistics"

---

## 🎯 下一步

部署完成后：

1. ✅ 测试所有功能
2. ✅ 配置 Secrets（如需要）
3. ✅ 启用密码保护（如需要）
4. ✅ 分享给朋友使用
5. ✅ 定期检查应用状态

---

## 📞 需要帮助？

- Streamlit Cloud 文档：https://docs.streamlit.io/streamlit-community-cloud
- Streamlit 社区：https://discuss.streamlit.io/
- 详细部署指南：查看 `STREAMLIT_CLOUD_DEPLOY.md`

---

**祝你部署顺利！** 🎉

