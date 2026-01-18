# 🔐 Streamlit Cloud Secrets 设置指南

## 📖 什么是 Secrets？

Secrets 是 Streamlit Cloud 提供的安全存储环境变量和敏感信息的方式。这些信息会被加密存储，并在应用运行时安全地提供给应用。

## 🎯 如何设置 Secrets

### 步骤 1：进入应用设置

1. 访问你的 Streamlit Cloud 应用页面
2. 点击右上角的 **⚙️ Settings**（设置）按钮
3. 在左侧菜单中找到 **"Secrets"** 选项
4. 点击 **"Edit secrets"**（编辑 secrets）按钮

### 步骤 2：编写 TOML 格式的配置

在编辑框中，使用 **TOML 格式**编写你的配置。TOML 是一种简单的配置文件格式。

#### 基本格式示例：

```toml
# 这是注释，以 # 开头

# 字符串值（用双引号）
APP_PASSWORD = "你的密码123"

# 数字值（不需要引号）
MAX_RETRIES = 3

# 布尔值
ENABLE_LOGGING = true

# 嵌套配置（使用方括号）
[database]
host = "localhost"
port = 5432
username = "admin"
```

### 步骤 3：本项目推荐的 Secrets 配置

根据本项目，你可以设置以下 Secrets：

#### 选项 1：仅设置密码保护（推荐）

```toml
# 应用访问密码（用于密码保护功能）
APP_PASSWORD = "你的安全密码"
```

#### 选项 2：完整配置（如果需要预设 API Key）

```toml
# 应用访问密码
APP_PASSWORD = "你的安全密码"

# SSL 验证设置（可选）
SKIP_SSL_VERIFY = "false"

# 预设的 API Keys（可选，不推荐在 Secrets 中存储）
# 建议用户通过界面输入自己的 API Key
# OPENAI_API_KEY = "sk-..."
# DEEPSEEK_API_KEY = "sk-..."
```

### 步骤 4：保存配置

1. 点击 **"Save"**（保存）按钮
2. 等待约 1 分钟让配置生效
3. 应用会自动重新部署

## 💻 在代码中如何使用 Secrets

### 方法 1：使用 `st.secrets`（推荐，Streamlit Cloud 专用）

```python
import streamlit as st

# 获取简单的字符串值
password = st.secrets.get("APP_PASSWORD", "")

# 或者直接访问（如果确定存在）
password = st.secrets["APP_PASSWORD"]

# 获取嵌套配置
# database_host = st.secrets["database"]["host"]
```

### 方法 2：兼容方式（同时支持本地和云端）

```python
import streamlit as st
import os

# 优先使用 st.secrets，如果不存在则使用环境变量
def get_secret(key: str, default: str = ""):
    """获取配置值，优先从 st.secrets 获取，其次从环境变量"""
    try:
        # 尝试从 Streamlit Cloud Secrets 获取
        return st.secrets.get(key, default)
    except (AttributeError, KeyError, FileNotFoundError):
        # 如果不在 Streamlit Cloud 或 secrets 不存在，使用环境变量
        return os.environ.get(key, default)

# 使用示例
PASSWORD = get_secret("APP_PASSWORD", "")
```

## 📝 本项目中的 Secrets 使用

### 当前支持的 Secrets：

1. **APP_PASSWORD**
   - 用途：应用访问密码
   - 类型：字符串
   - 是否必需：否（可选）
   - 示例：`APP_PASSWORD = "mypassword123"`

2. **SKIP_SSL_VERIFY**
   - 用途：是否跳过 SSL 验证
   - 类型：字符串（"true" 或 "false"）
   - 是否必需：否（可选）
   - 示例：`SKIP_SSL_VERIFY = "false"`

### 启用密码保护：

1. 在 Secrets 中设置 `APP_PASSWORD`
2. 编辑 `app.py`，取消注释第 28-46 行的密码验证代码
3. 提交并推送代码到 GitHub
4. Streamlit Cloud 会自动重新部署

## ⚠️ 重要注意事项

### 1. 安全性

- ✅ **DO（应该做）**：
  - 使用强密码
  - 定期更换密码
  - 不要将 Secrets 内容分享给他人
  - 不要在代码中硬编码敏感信息

- ❌ **DON'T（不应该做）**：
  - 不要在代码仓库中提交包含真实密码的文件
  - 不要在公开场合分享 Secrets 内容
  - 不要使用弱密码（如 "123456"）

### 2. 格式要求

- 必须使用 **TOML 格式**
- 字符串值必须用**双引号**括起来
- 每行一个配置项
- 可以使用 `#` 添加注释

### 3. 生效时间

- Secrets 更改后需要约 **1 分钟**才能生效
- 应用会自动重新部署
- 如果更改后出现问题，可以查看应用日志

## 🔍 常见问题

### Q1: 如何检查 Secrets 是否设置成功？

**A**: 在代码中添加临时调试代码：

```python
import streamlit as st

# 临时调试（记得删除）
st.write("Password set:", bool(st.secrets.get("APP_PASSWORD", "")))
```

### Q2: Secrets 设置后应用报错？

**A**: 
1. 检查 TOML 格式是否正确
2. 检查是否有语法错误（如缺少引号）
3. 查看应用日志了解具体错误
4. 确保键名与代码中使用的一致

### Q3: 如何删除 Secrets？

**A**: 
1. 进入 Secrets 编辑页面
2. 删除或注释掉不需要的配置项
3. 点击 "Save" 保存

### Q4: 可以在 Secrets 中存储 API Key 吗？

**A**: 
- 技术上可以，但不推荐
- 建议让用户通过应用界面输入自己的 API Key
- 如果必须预设，确保 Secrets 配置是私有的

### Q5: 本地开发时如何使用 Secrets？

**A**: 
- 在项目根目录创建 `.streamlit/secrets.toml` 文件
- 使用相同的 TOML 格式
- 注意：`.streamlit/secrets.toml` 应该添加到 `.gitignore` 中

## 📚 参考资源

- [Streamlit Secrets 官方文档](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [TOML 格式规范](https://toml.io/)
- [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-community-cloud)

---

**提示**：设置 Secrets 后，记得测试应用功能是否正常！

