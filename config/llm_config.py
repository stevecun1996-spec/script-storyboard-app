"""
LLM模型配置模块（简化版）
"""

# LLM模型配置字典
LLM_MODELS = {
    "OpenAI": {
        "api_base": "https://api.openai.com/v1",
        "models": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ],
        "request_format": "openai"
    },
    "通义千问": {
        "api_base": "https://dashscope.aliyuncs.com/api/v1",
        "models": [
            "qwen-plus",
            "qwen-turbo",
            "qwen-max"
        ],
        "request_format": "openai"
    },
    "智谱GLM": {
        "api_base": "https://open.bigmodel.cn/api/paas/v4",
        "models": [
            "glm-4",
            "glm-4v",
            "glm-3-turbo"
        ],
        "request_format": "openai"
    },
    "Deepseek": {
        "api_base": "https://api.deepseek.com/v1",
        "models": [
            "deepseek-chat",
            "deepseek-coder"
        ],
        "request_format": "openai"
    },
    "月之暗面": {
        "api_base": "https://api.moonshot.cn/v1",
        "models": [
            "moonshot-v1-8k",
            "moonshot-v1-32k",
            "moonshot-v1-128k"
        ],
        "request_format": "openai"
    },
    "Claude": {
        "api_base": "https://api.anthropic.com/v1",
        "models": [
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-haiku-20240307"
        ],
        "request_format": "openai"
    },
    "讯飞星火": {
        "api_base": "https://spark-api.xf-yun.com/v1",
        "models": [
            "spark-v3.5",
            "spark-v3.0",
            "spark-v2.0"
        ],
        "request_format": "openai"
    },
    "百川智能": {
        "api_base": "https://api.baichuan-ai.com/v1",
        "models": [
            "Baichuan2-Turbo",
            "Baichuan2-53B"
        ],
        "request_format": "openai"
    },
    "MiniMax": {
        "api_base": "https://api.minimax.chat/v1",
        "models": [
            "abab6-chat",
            "abab5.5-chat"
        ],
        "request_format": "openai"
    },
    "LM Studio": {
        "api_base": "http://127.0.0.1:1234/v1",
        "models": [
            "lmstudio-local"
        ],
        "request_format": "openai"
    },
    "Apigather": {
        "api_base": "https://apigather.com/v1",
        "models": [
            "gemini-3-pro-preview",
            "gemini-3-flash-preview",
            "gemini-3-pro-image-preview",
            "gemini-3-pro-preview-thinking"
        ],
        "request_format": "openai"
    }
}

def get_llm_config(brand: str, model: str = None):
    """获取指定品牌的LLM配置"""
    if brand not in LLM_MODELS:
        raise ValueError(f"不支持的LLM品牌: {brand}")
    
    config = LLM_MODELS[brand].copy()
    
    if model:
        config["selected_model"] = model
    else:
        config["selected_model"] = config["models"][0]
    
    return config

def get_available_brands():
    """获取所有可用的LLM品牌"""
    return list(LLM_MODELS.keys())

def get_models_by_brand(brand: str):
    """获取指定品牌的所有模型"""
    if brand not in LLM_MODELS:
        return []
    return LLM_MODELS[brand]["models"]

