# API 测试脚本使用说明

## 概述

这些脚本用于测试和诊断 LLM API 的连接问题，特别是 SSL 和网络连接问题。

## 脚本文件

1. **test_api.sh** - 通用 API 测试脚本，支持所有 LLM 提供商
2. **test_api_apigather.sh** - Apigather API 专用诊断脚本

## 使用方法

### 通用测试脚本 (test_api.sh)

```bash
# 设置 API Key 并测试 Apigather
export API_KEY=your_api_key_here
./test_api.sh Apigather

# 或者直接传入 API Key
API_KEY=your_api_key_here ./test_api.sh Apigather

# 测试其他提供商
API_KEY=your_key ./test_api.sh OpenAI
API_KEY=your_key ./test_api.sh Deepseek
API_KEY=your_key ./test_api.sh 通义千问

# LM Studio 本地服务（不需要 API Key）
./test_api.sh LM\ Studio
```

### Apigather 专用诊断脚本

```bash
# 交互式输入 API Key
./test_api_apigather.sh

# 或使用环境变量
export API_KEY=your_api_key_here
./test_api_apigather.sh
```

## 测试内容

### test_api.sh 测试项目：

1. **获取模型列表** (`GET /models`)
   - 测试 API 连接
   - 验证 API Key
   - 检查响应格式

2. **简单对话测试** (`POST /chat/completions`)
   - 测试完整的对话流程
   - 验证模型可用性
   - 检查响应内容

### test_api_apigather.sh 测试项目：

1. **基本连接测试（跳过 SSL 验证）**
   - 使用 `-k` 选项跳过 SSL 证书验证
   - 用于诊断 SSL 问题

2. **完整 SSL 验证测试**
   - 使用标准 SSL 验证
   - 如果失败，说明存在 SSL 证书问题

3. **详细 SSL 信息**
   - 显示 SSL/TLS 握手详情
   - 帮助诊断证书问题

4. **对话测试**
   - 测试完整的 API 调用流程

## 常见问题诊断

### SSL 错误 (Operation not permitted)

**症状：**
```
SSLError: PermissionError(1, 'Operation not permitted')
```

**解决方案：**

1. **macOS 系统权限**
   ```bash
   # 在系统设置中允许 Python/Streamlit 访问网络
   # 系统设置 → 安全性与隐私 → 防火墙
   ```

2. **使用跳过 SSL 验证的脚本**
   ```bash
   # 脚本已自动添加 -k 选项（macOS）
   ./test_api.sh Apigather
   ```

3. **临时禁用系统完整性保护（不推荐）**
   ```bash
   sudo spctl --master-disable
   ```

### HTTP 401 (未授权)

**症状：**
```
HTTP状态码: 401
```

**解决方案：**
- 检查 API Key 是否正确
- 确认 API Key 是否已过期
- 验证 API Key 是否有访问权限

### HTTP 429 (请求过多)

**症状：**
```
HTTP状态码: 429
错误信息: 当前分组上游负载已饱和
```

**解决方案：**
- 等待 1-2 分钟后重试
- 减少请求频率
- 考虑使用其他 LLM 服务

### 连接超时

**症状：**
```
curl: (28) Operation timed out
```

**解决方案：**
- 检查网络连接
- 确认防火墙设置
- 验证 API 端点是否可访问

## 输出说明

- ✅ **绿色** - 测试成功
- ⚠️ **黄色** - 警告信息
- ❌ **红色** - 错误信息

## 示例输出

### 成功示例

```
==========================================
测试 1: 获取模型列表
==========================================
✓ 成功获取模型列表
{
  "data": [
    {
      "id": "gemini-3-pro-preview",
      "object": "model"
    }
  ]
}

==========================================
测试 2: 简单对话测试
==========================================
✓ 对话测试成功
AI 回复: 测试成功
```

### 失败示例

```
==========================================
测试 1: 获取模型列表
==========================================
✗ 获取模型列表失败 (HTTP 401)
{
  "error": {
    "message": "Invalid API Key"
  }
}
```

## 注意事项

1. **API Key 安全**
   - 不要将 API Key 提交到版本控制系统
   - 使用环境变量存储 API Key
   - 测试后及时清除终端历史

2. **SSL 验证**
   - 生产环境应启用 SSL 验证
   - 测试环境可以临时跳过验证（使用 `-k` 选项）

3. **网络环境**
   - 某些网络环境可能阻止 API 访问
   - 检查代理设置
   - 验证防火墙规则

## 故障排除步骤

1. **运行诊断脚本**
   ```bash
   ./test_api_apigather.sh
   ```

2. **检查网络连接**
   ```bash
   ping apigather.com
   ```

3. **测试 DNS 解析**
   ```bash
   nslookup apigather.com
   ```

4. **检查 SSL 证书**
   ```bash
   openssl s_client -connect apigather.com:443
   ```

5. **查看详细错误**
   ```bash
   curl -v -k -H "Authorization: Bearer $API_KEY" https://apigather.com/v1/models
   ```

## 支持

如果问题持续存在，请：
1. 保存测试脚本的完整输出
2. 检查系统日志
3. 联系 API 提供商支持
