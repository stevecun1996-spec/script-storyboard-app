# Streamlit Cloud 分享指南

## ✅ 是的，可以小范围分享给朋友！

Streamlit Cloud 完全支持将应用分享给朋友使用。以下是详细的分享方式和注意事项。

---

## 🔗 分享方式

### 方式一：直接分享链接（最简单）

1. **部署到 Streamlit Cloud 后**，你会获得一个公开 URL：
   ```
   https://你的应用名.streamlit.app
   ```

2. **直接分享这个链接**给朋友
   - 朋友点击链接即可访问
   - 无需登录或注册
   - 无需任何权限验证

3. **优点**：
   - ✅ 最简单直接
   - ✅ 朋友无需安装任何软件
   - ✅ 跨平台使用（手机、平板、电脑）

---

## 🔒 访问控制

### 当前限制：

⚠️ **Streamlit Cloud 的免费版不支持密码保护或私有访问**

- 所有应用都是公开的
- 任何人获得链接都可以访问
- 无法设置密码或限制访问

### 解决方案：

#### 1. **使用非公开链接**（推荐）⭐

虽然无法完全私有化，但你可以：
- **不要公开分享链接**，只私下发给朋友
- 使用复杂的应用名称，不容易被猜到
- 定期更换应用名称（需要重新部署）

**步骤**：
```python
# 在 Streamlit Cloud 部署时，使用不易猜测的应用名称
# 例如：my-storyboard-app-xk9p2m 而不是 storyboard-app
```

#### 2. **添加简单的密码验证**（代码层面）

可以在应用开始时添加简单的密码验证：

```python
# 在 app.py 开头添加
import streamlit as st

# 密码验证（简单版本）
PASSWORD = "你的密码"  # 建议使用环境变量

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("请输入访问密码", type="password", key="password_input")
    if st.button("确认"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("密码错误，请重试")
    st.stop()  # 未验证时停止运行后续代码

# 后续应用代码...
```

**更好的方式**（使用环境变量）：
```python
import os

# 从环境变量读取密码（在 Streamlit Cloud 的 Secrets 中设置）
PASSWORD = os.environ.get("APP_PASSWORD", "")
```

**在 Streamlit Cloud 设置 Secrets**：
1. 进入应用的 Settings
2. 找到 "Secrets" 选项
3. 添加：
   ```toml
   APP_PASSWORD = "你的密码"
   ```

---

## 📋 分享前准备清单

### 1. ✅ 清理敏感信息

- [ ] 检查代码中是否有硬编码的 API Key
- [ ] 移除测试数据或个人信息
- [ ] 确保所有 API Key 都使用环境变量

### 2. ✅ 配置环境变量

在 Streamlit Cloud 的 **Secrets** 中配置：

```toml
# .streamlit/secrets.toml (在 Streamlit Cloud 中设置)

# LLM API Keys（示例）
OPENAI_API_KEY = "your-key-here"
DEEPSEEK_API_KEY = "your-key-here"

# 应用密码（如果使用）
APP_PASSWORD = "your-password-here"
```

### 3. ✅ 测试应用

- [ ] 确保所有功能正常工作
- [ ] 测试不同设备上的访问
- [ ] 检查加载速度

### 4. ✅ 准备使用说明

建议创建一个简单的使用说明文档，包含：
- 应用功能简介
- 使用步骤
- 常见问题
- 注意事项

---

## 🎯 最佳实践

### 1. **限制使用场景**

- ✅ 适合：小范围朋友间分享
- ✅ 适合：团队内部测试
- ❌ 不适合：完全私密的商业项目
- ❌ 不适合：需要严格访问控制的场景

### 2. **定期更新密码**

如果使用密码验证：
- 定期更换密码
- 在 Streamlit Cloud 的 Secrets 中更新
- 通知朋友新密码

### 3. **监控使用情况**

- 定期检查应用日志（Streamlit Cloud 提供）
- 注意异常访问
- 如果发现滥用，可以暂停应用

### 4. **数据隐私**

- ⚠️ **注意**：用户输入的数据（剧本、分镜）会存储在 Streamlit Cloud 的服务器上
- 如果使用项目管理功能，文件保存在服务器本地
- 建议告知朋友数据存储情况

---

## 🔐 如果需要更强的隐私保护

### 方案一：升级到 Streamlit Cloud 付费版

- 查看 Streamlit Cloud 是否有付费版提供私有部署
- 联系 Streamlit 团队了解企业版功能

### 方案二：使用其他平台

1. **Railway 私有部署**
   - 可以设置应用为私有
   - 通过 IP 白名单限制访问

2. **自建服务器**
   - 部署在自己的服务器上
   - 完全控制访问权限

3. **内网部署**
   - 部署在公司或家庭内网
   - 通过 VPN 访问

---

## 📱 分享示例

### 分享链接模板：

```
你好！

我开发了一个剧本分镜生成工具，想分享给你试试：

🔗 访问链接：https://your-app.streamlit.app
🔑 访问密码：xxxxxx（如果设置了密码）

功能：
- 输入剧本自动生成分镜
- 支持多种 LLM 模型
- 导出 Excel 格式

使用步骤：
1. 打开链接
2. 输入访问密码（如需要）
3. 在侧边栏配置 API Key
4. 输入剧本开始使用

如果有问题随时联系我！
```

---

## ⚠️ 注意事项

1. **API 费用**：
   - 如果朋友使用你的 API Key，会产生费用
   - 建议朋友使用自己的 API Key
   - 或者设置使用限制

2. **免费额度**：
   - Streamlit Cloud 免费版有使用限制
   - 注意应用是否会因为使用量过大而暂停

3. **数据安全**：
   - 朋友输入的剧本会经过服务器
   - 确保了解数据流向
   - 如果涉及敏感内容，建议本地使用

4. **版本控制**：
   - 更新应用后，所有用户都会看到新版本
   - 重大更新前建议通知朋友

---

## 🚀 快速分享步骤

1. **部署到 Streamlit Cloud**（见 DEPLOYMENT.md）

2. **（可选）添加密码验证**
   ```python
   # 在 app.py 开头添加密码验证代码
   ```

3. **在 Streamlit Cloud 设置 Secrets**
   - 添加 API Keys
   - 添加应用密码（如使用）

4. **测试访问**
   - 使用无痕浏览器测试
   - 确保所有功能正常

5. **分享链接**
   - 将应用 URL 分享给朋友
   - 提供使用说明和密码（如有）

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 Streamlit Cloud 官方文档
2. 检查应用日志
3. 查看 GitHub Issues

---

**总结**：Streamlit Cloud 非常适合小范围分享，虽然无法完全私有化，但通过非公开链接和密码验证可以实现基本的访问控制。

