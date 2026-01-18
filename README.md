# 🎬 剧本分镜生成系统

<div align="center">

一个基于 AI 的智能剧本分镜生成工具，帮助影视创作者快速将剧本转换为专业的分镜头脚本和文生图提示词。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[功能特性](#-核心功能) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [部署](#-部署) • [常见问题](#-常见问题)

</div>

---

## ✨ 核心功能

### 🎯 主要功能

- **📝 剧本输入** - 支持长文本剧本输入，自动识别场景和对话
- **🤖 AI 自动分镜** - 基于大语言模型智能划分分镜头，包含场景、镜头、人物、对话等信息
- **✏️ 分镜编辑** - 可视化编辑每个分镜头，支持修改描述、镜头角度、地点、时间、情绪、台词、旁白、音效等
- **🎨 文生图提示词生成** - 将分镜转换为 Nano Banana Pro 格式的 JSON 提示词，支持多种语言和详细程度配置
- **💾 项目管理** - 保存和加载项目，支持分镜和提示词的持久化存储
- **📊 Excel 导出** - 一键导出完整的分镜头脚本为 Excel 文件，包含分镜头表和原始剧本表

### 🌟 特色亮点

- ✅ **10 种 LLM 品牌支持** - OpenAI、Deepseek、通义千问、智谱 GLM、月之暗面、Claude、讯飞星火、百川智能、MiniMax、LM Studio
- ✅ **自定义模型支持** - 支持输入自定义模型名称，适配最新发布的模型
- ✅ **模型列表刷新** - 自动获取账户可用的所有模型列表
- ✅ **多语言提示词** - 支持中文、英文、双语模式的文生图提示词生成
- ✅ **灵活配置** - 可配置提示词详细程度、技术参数、情绪氛围等
- ✅ **云端部署** - 支持 Streamlit Cloud 一键部署，支持密码保护

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 网络连接（用于 API 调用）
- 任一支持的 LLM API 密钥（推荐使用 Deepseek，性价比高）

### 安装步骤

1. **克隆或下载项目**

```bash
git clone <repository-url>
cd Script_to_Storyboard_Simple
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

如果安装速度慢，可以使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. **启动应用**

**方式一：使用启动脚本（推荐）**

- Windows: 双击 `run.bat`
- macOS/Linux: 运行 `bash run.sh` 或 `chmod +x run.sh && ./run.sh`

**方式二：使用命令行**

```bash
streamlit run app.py
```

4. **访问应用**

打开浏览器访问：http://localhost:8501

---

## 📋 使用指南

### 基本工作流程

#### 步骤 1：配置 API

在侧边栏中配置 LLM 服务：

1. **选择 LLM 品牌** - 从 10 种主流 LLM 中选择
2. **选择模型** - 选择具体模型，或使用"🔧 自定义模型"输入模型名称
3. **输入 API Key** - 输入对应服务的 API 密钥
4. **（可选）刷新模型列表** - 点击"刷新模型列表"获取账户可用的所有模型

#### 步骤 2：输入剧本

在主界面中：

1. 粘贴或输入你的剧本内容
2. 点击「开始分镜」按钮
3. 等待 AI 自动划分分镜头（根据剧本长度可能需要几分钟）

#### 步骤 3：编辑分镜

在分镜编辑界面中：

- ✅ 查看 AI 自动划分的分镜头列表
- ✏️ 编辑每个分镜的详细信息：
  - 分镜描述
  - 镜头角度（远景、中景、近景、特写等）
  - 人物
  - 地点
  - 时间
  - 情绪
  - 台词
  - 旁白
  - 音效
- ➕ 添加新分镜
- 🗑️ 删除不需要的分镜

#### 步骤 4：生成文生图提示词（可选）

1. 进入「步骤 3：生成文生图提示词」页面
2. 配置提示词选项：
   - **提示词语言**：中文 / 英文 / 双语
   - **详细程度**：简洁 / 标准 / 详细
   - **包含技术参数**：相机、镜头、光圈等
   - **包含情绪氛围**：场景情绪描述
   - **包含人物信息**：角色外观、服装等
   - **使用 LLM 辅助**：使用 AI 优化提示词（可选）
3. 选择分镜范围（全部 / 选中 / 自定义）
4. 点击「生成提示词」
5. 预览和复制提示词

#### 步骤 5：保存和导出

- **保存项目**：点击「保存项目」按钮，输入项目名称保存
- **加载项目**：从项目列表中选择已保存的项目加载
- **导出 Excel**：点击「导出 Excel」按钮，文件将保存到桌面

---

## 💡 支持的 LLM 模型

### OpenAI
- `gpt-4o` - 最新旗舰模型（推荐用于高质量分镜）
- `gpt-4o-mini` - 轻量级版本
- `gpt-4-turbo` - 高性能版本
- `gpt-3.5-turbo` - 经济型选择

### Deepseek（⭐ 推荐）
- `deepseek-chat` - 高性价比，中文理解优秀
- `deepseek-coder` - 代码理解能力强

### 通义千问
- `qwen-plus` - 高性能版本
- `qwen-turbo` - 快速响应
- `qwen-max` - 最强性能

### 智谱 GLM
- `glm-4` - 最新版本
- `glm-4v` - 视觉理解版本
- `glm-3-turbo` - 快速版本

### 月之暗面
- `moonshot-v1-8k` - 8K 上下文
- `moonshot-v1-32k` - 32K 上下文
- `moonshot-v1-128k` - 128K 超长上下文（适合长剧本）

### Claude
- `claude-3-5-sonnet-20241022` - 最新版本
- `claude-3-opus-20240229` - 最强性能
- `claude-3-haiku-20240307` - 快速版本

### 讯飞星火
- `spark-v3.5` - 最新版本
- `spark-v3.0` - 稳定版本
- `spark-v2.0` - 经典版本

### 百川智能
- `Baichuan2-Turbo` - 快速版本
- `Baichuan2-53B` - 高性能版本

### MiniMax
- `abab6-chat` - 最新版本
- `abab5.5-chat` - 稳定版本

### LM Studio（本地）
- `lmstudio-local` - 本地部署，无需 API Key

### Apigather
- `gemini-3-pro-preview` - Gemini 3 Pro 预览版
- `gemini-3-flash-preview` - Gemini 3 Flash 预览版
- `gemini-3-pro-image-preview` - 图像理解版本
- `gemini-3-pro-preview-thinking` - 思考模式版本

**✨ 提示**：所有品牌都支持自定义模型输入，你可以直接输入模型名称使用最新发布的模型。

---

## 📁 项目结构

```
Script_to_Storyboard_Simple/
├── app.py                          # 主应用文件
├── requirements.txt                # Python 依赖包
├── README.md                       # 项目说明文档
│
├── config/                         # 配置模块
│   ├── __init__.py
│   ├── llm_config.py              # LLM 配置（10 种品牌）
│   ├── prompts.py                  # 分镜划分提示词模板
│   ├── image_prompt_templates.py  # 文生图提示词模板
│   └── prompt_generation_prompts.py # 提示词生成提示词
│
├── services/                       # 服务层
│   ├── __init__.py
│   └── llm_service.py              # LLM 服务（API 调用封装）
│
├── utils/                          # 工具模块
│   ├── __init__.py
│   ├── scene_parser.py             # 分镜解析器
│   ├── script_splitter.py          # 剧本分割器
│   ├── export_utils.py             # Excel 导出工具
│   ├── prompt_generator.py         # 文生图提示词生成器
│   └── project_manager.py          # 项目管理器
│
├── run.bat                         # Windows 启动脚本
├── run.sh                          # macOS/Linux 启动脚本
│
└── 文档/                           # 文档目录
    ├── README_DEPLOY.md            # 部署指南
    ├── STREAMLIT_CLOUD_DEPLOY.md   # Streamlit Cloud 部署指南
    ├── STREAMLIT_SECRETS_GUIDE.md  # Secrets 配置指南
    ├── SHARING_GUIDE.md            # 分享指南
    └── 功能规划-分镜转文生图提示词.md
```

---

## 📊 导出格式

### Excel 文件结构

导出的 Excel 文件包含两个工作表：

#### 1. 分镜头表

包含以下列：

| 列名 | 说明 |
|------|------|
| 序号 | 分镜顺序编号 |
| 分镜描述 | 场景和动作描述 |
| 镜头角度 | 远景/中景/近景/特写等 |
| 人物 | 出场人物 |
| 地点 | 场景地点 |
| 时间 | 时间设定（日/夜/黄昏等） |
| 情绪 | 场景情绪氛围 |
| 台词 | 人物对话 |
| 旁白 | 旁白内容 |
| 音效 | 音效说明 |

#### 2. 原始剧本表

包含完整的原始剧本文本，便于对照和追溯。

---

## 🚀 部署

### 本地部署

按照 [快速开始](#-快速开始) 部分的说明即可在本地运行。

### Streamlit Cloud 部署

项目支持一键部署到 Streamlit Cloud，详细步骤请参考：

- 📖 [Streamlit Cloud 部署指南](STREAMLIT_CLOUD_DEPLOY.md)
- 📖 [Secrets 配置指南](STREAMLIT_SECRETS_GUIDE.md)

**快速部署步骤**：

1. 将代码推送到 GitHub 仓库
2. 访问 https://share.streamlit.io/
3. 使用 GitHub 账号登录
4. 点击 "New app"，选择仓库和分支
5. 设置 Main file path 为 `app.py`
6. 点击 "Deploy" 等待部署完成

**配置 Secrets（可选）**：

如果需要密码保护，在 Streamlit Cloud 的 Settings → Secrets 中添加：

```toml
APP_PASSWORD = "你的密码"
```

然后在 `app.py` 中取消注释密码验证代码。

---

## 📝 使用技巧

### 提升分镜质量

1. **剧本要详细** - 包含场景描述、动作说明、对话内容
2. **格式要规范** - 使用清晰的段落和场景标记
3. **模型要选好** - 推荐使用 GPT-4o、Deepseek 或 GLM-4
4. **多次生成** - 不满意可以重新生成，或手动编辑优化

### 节省 API 成本

1. **使用 Deepseek** - 性价比最高，中文理解优秀（⭐ 推荐）
2. **先短后长** - 先用短剧本测试效果
3. **减少重试** - 优化剧本后再生成，避免重复调用
4. **使用本地模型** - LM Studio 支持本地部署，完全免费

### 提升工作效率

1. **自定义模型** - 使用最新发布的模型获得更好效果
2. **刷新列表** - 获取账户可用的所有模型
3. **批量编辑** - 使用项目管理功能保存和复用分镜
4. **标准化输出** - Excel 格式便于后续导入其他工具

### 文生图提示词优化

1. **选择合适的语言** - 根据使用的文生图模型选择中文或英文
2. **调整详细程度** - 简洁模式适合快速预览，详细模式适合最终输出
3. **启用 LLM 辅助** - 使用 AI 优化提示词，获得更准确的结果
4. **包含技术参数** - 如果需要精确控制镜头效果，启用技术参数

---

## 🔧 常见问题

### 安装和启动

**Q: 安装依赖时报错？**

A: 
- 确保 Python 版本 ≥ 3.8
- 尝试使用国内镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
- 如果仍有问题，尝试升级 pip：`pip install --upgrade pip`

**Q: 启动后无法访问？**

A:
- 检查端口 8501 是否被占用
- 尝试使用其他端口：`streamlit run app.py --server.port 8502`
- 查看终端是否有错误信息

### API 调用

**Q: API 调用失败？**

A:
- 检查 API Key 是否正确
- 确认账户余额是否充足
- 检查网络连接是否正常
- 某些服务可能需要代理，检查是否需要配置代理

**Q: 某些模型无法使用？**

A:
- 确认模型名称是否正确
- 检查账户是否有权限使用该模型
- 尝试使用自定义模型输入功能
- 某些模型可能需要特定的 API 版本

### 功能使用

**Q: 分镜结果不理想？**

A:
- 完善剧本细节，添加更多场景和动作描述
- 尝试使用更强的模型（如 GPT-4o）
- 生成后手动编辑优化
- 检查提示词模板是否适合你的剧本类型

**Q: 找不到导出的 Excel 文件？**

A:
- 文件自动保存在桌面
- 文件名格式：`分镜头脚本_YYYYMMDD_HHMMSS.xlsx`
- 检查桌面文件夹
- 某些系统可能保存到下载文件夹

**Q: 如何使用自定义模型？**

A:
1. 在模型选择下拉框中选择 "🔧 自定义模型"
2. 在输入框中输入模型名称（如：`gpt-4-turbo-2024-04-09`）
3. 输入对应的 API Key
4. 点击 "开始分镜" 使用

**Q: 刷新模型列表失败？**

A:
- 某些品牌可能不支持此功能
- 直接使用自定义模型输入功能
- 检查 API Key 是否有查询模型列表的权限

### 部署相关

**Q: Streamlit Cloud 部署失败？**

A:
- 检查 `requirements.txt` 是否包含所有依赖
- 确认 Main file path 配置正确（`app.py`）
- 查看部署日志了解具体错误
- 参考 [部署指南](STREAMLIT_CLOUD_DEPLOY.md)

**Q: 如何配置 Secrets？**

A:
- 参考 [Secrets 配置指南](STREAMLIT_SECRETS_GUIDE.md)
- 使用 TOML 格式编写配置
- 确保字符串值用双引号括起来

---

## 🎯 适用场景

- 🎬 **电影/电视剧分镜设计** - 快速生成专业分镜头脚本
- 🎨 **动画分镜制作** - 将文字剧本转换为可视化分镜
- 🎮 **游戏剧情可视化** - 游戏过场动画和剧情分镜设计
- 📺 **短视频脚本规划** - 短视频拍摄前的分镜规划
- 📖 **漫画分镜设计** - 漫画创作前的分镜设计
- 🎓 **影视教学演示** - 影视教学中的分镜制作演示
- 🎪 **广告创意分镜** - 广告拍摄前的分镜设计

---

## 🛠️ 技术栈

- **前端框架**: Streamlit
- **后端语言**: Python 3.8+
- **数据处理**: Pandas
- **文件导出**: openpyxl
- **HTTP 请求**: requests, openai
- **其他**: urllib3, Pillow

---

## 📄 许可证

本项目供学习和研究使用。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 获取帮助

- 📖 查看项目文档
- 🐛 提交 Issue 报告问题
- 💬 参与讨论

---

## 🎉 致谢

感谢所有支持本项目的用户和贡献者！

---

<div align="center">

**让剧本快速转化为专业分镜头脚本！** 🎬✨

Made with ❤️ by the community

</div>
