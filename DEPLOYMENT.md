# 部署指南

## 📌 重要说明

**Vercel 不适合直接部署 Streamlit 应用**，因为：
- Vercel 主要支持静态网站和 serverless 函数
- Streamlit 需要长期运行的 Python 服务器进程
- Vercel 不支持 WebSocket（Streamlit 使用）

## 🚀 推荐部署方案

### 方案一：Streamlit Cloud（最简单，推荐）⭐

这是部署 Streamlit 应用最简单的方式。

#### 步骤：

1. **准备 GitHub 仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git push -u origin main
   ```

2. **创建 `packages.txt` 文件**（如果使用 conda）
   - 不需要，Streamlit Cloud 使用 pip

3. **访问 Streamlit Cloud**
   - 访问：https://share.streamlit.io/
   - 使用 GitHub 账号登录

4. **部署应用**
   - 点击 "New app"
   - 选择 GitHub 仓库
   - 选择分支（通常是 main）
   - 填写应用路径：`Script_to_Storyboard_Simple/app.py`
   - 点击 "Deploy"

5. **配置 Secrets（环境变量）**
   - 在 App settings 中添加 API Keys（如果需要）

**优点：**
- ✅ 完全免费
- ✅ 自动 HTTPS
- ✅ 自动更新（推送代码后自动部署）
- ✅ 简单易用

---

### 方案二：Railway（推荐）⭐

Railway 支持 Python 应用，适合部署 Streamlit。

#### 步骤：

1. **创建 `Procfile`**
   ```
   web: streamlit run Script_to_Storyboard_Simple/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **创建 `runtime.txt`**（可选）
   ```
   python-3.9.6
   ```

3. **部署到 Railway**
   - 访问：https://railway.app/
   - 使用 GitHub 登录
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择仓库
   - Railway 会自动检测并部署

4. **配置环境变量**
   - 在 Railway 项目中添加环境变量（如 API Keys）

**优点：**
- ✅ 支持 Python 应用
- ✅ 免费额度充足
- ✅ 自动 HTTPS
- ✅ 简单配置

---

### 方案三：Render（推荐）⭐

Render 也支持 Python 应用。

#### 步骤：

1. **创建 `render.yaml`**（可选）
   ```yaml
   services:
     - type: web
       name: script-storyboard
       env: python
       plan: free
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run Script_to_Storyboard_Simple/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **部署到 Render**
   - 访问：https://render.com/
   - 使用 GitHub 登录
   - 点击 "New" → "Web Service"
   - 连接 GitHub 仓库
   - 配置：
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `streamlit run Script_to_Storyboard_Simple/app.py --server.port=$PORT --server.address=0.0.0.0`
   - 点击 "Create Web Service"

**优点：**
- ✅ 免费套餐可用
- ✅ 自动 HTTPS
- ✅ 支持 Python

---

### 方案四：Vercel（需要重构）⚠️

如果一定要用 Vercel，需要将应用重构为：
- **后端 API**：使用 FastAPI/Flask 提供 API 端点
- **前端**：使用 React/Next.js 构建前端界面
- **部署**：API 部署为 Vercel Serverless Functions，前端部署为静态网站

这需要大量重构工作，**不推荐**。

---

## 📋 部署前准备

### 1. 创建 `.streamlit/config.toml`（可选）

创建 `Script_to_Storyboard_Simple/.streamlit/config.toml`：

```toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### 2. 更新 `requirements.txt`

确保包含所有依赖：

```txt
streamlit>=1.30.0
requests>=2.32.0
urllib3>=2.0.0
openai>=1.0.0
pandas>=2.0.0
openpyxl>=3.1.0
pillow>=10.0.0
```

### 3. 创建 `.gitignore`

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.log
.DS_Store
.streamlit/secrets.toml
```

### 4. 创建 `README.md`（如果还没有）

包含项目说明和部署信息。

---

## 🔧 环境变量配置

在部署平台上设置环境变量（如需要）：

- `OPENAI_API_KEY`（或其他 LLM API Key）
- `SKIP_SSL_VERIFY=true`（如果需要）

---

## ⚠️ 注意事项

1. **存储路径**：项目保存目录 `~/.script_storyboard` 在云服务器上可能无法持久化，建议使用数据库或云存储。

2. **API Key**：不要将 API Key 提交到代码仓库，使用环境变量或 Secrets。

3. **文件大小**：注意 Streamlit 上传文件的大小限制。

4. **免费额度**：
   - Streamlit Cloud：完全免费
   - Railway：$5 免费额度/月
   - Render：免费但有休眠机制

---

## 🎯 推荐选择

**首选：Streamlit Cloud**
- 专为 Streamlit 设计
- 零配置
- 完全免费

**备选：Railway 或 Render**
- 如果 Streamlit Cloud 不可用
- 需要更多控制

**不推荐：Vercel**
- 需要大量重构
- 工作量巨大

