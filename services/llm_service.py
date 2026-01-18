"""
LLM服务模块（简化版）
参照完整版实现，支持多种LLM服务
"""

import json
import os
import platform
import requests
import urllib3
from typing import List, Dict, Any
from config.llm_config import get_llm_config

# 禁用SSL警告（当使用verify=False时）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 对于 macOS 系统，在模块级别设置 SSL 上下文以解决权限问题
if platform.system() == "Darwin":
    # 设置环境变量，让底层库也跳过 SSL 验证
    os.environ.setdefault("PYTHONHTTPSVERIFY", "0")
    # 修改默认的 SSL 上下文，禁用验证（解决 macOS 权限问题）
    try:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
    except Exception:
        pass  # 如果设置失败，继续使用 requests 的 verify=False

class LLMService:
    """LLM服务类"""
    
    def __init__(self):
        self.brand = None
        self.model = None
        self.api_key = None
        self.api_base = None
        self.request_format = None
    
    def set_model(self, brand: str, model: str, api_key: str):
        """设置LLM模型配置"""
        config = get_llm_config(brand, model)
        self.brand = brand
        self.model = model
        self.api_key = api_key
        self.api_base = config["api_base"]
        self.request_format = config["request_format"]
    
    def divide_script(self, script: str, system_prompt: str) -> List[Dict[str, Any]]:
        """
        使用LLM划分剧本为分镜头
        
        Args:
            script: 剧本文本
            system_prompt: 系统提示词
        
        Returns:
            List[Dict]: 分镜头列表
        """
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请对以下剧本进行分镜头划分：\n\n{script}"}
            ]
            
            # 调用LLM
            content = self._call_llm(messages, temperature=0.7)
            
            # 提取JSON
            scenes = self._extract_json_from_response(content)
            
            return scenes
            
        except Exception as e:
            raise Exception(f"LLM服务调用失败: {str(e)}")
    
    def _call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        调用LLM API
        
        Args:
            messages: 消息列表
            temperature: 温度参数
        
        Returns:
            str: LLM响应内容
        """
        if not self.api_base:
            raise ValueError("请先设置LLM模型")
        
        try:
            if self.request_format == "openai":
                return self._call_openai_format(messages, temperature)
            else:
                raise ValueError(f"不支持的请求格式: {self.request_format}")
        
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower() or "timed out" in error_msg.lower() or isinstance(e, requests.exceptions.Timeout):
                raise Exception(f"LLM调用超时（已等待10分钟）。可能原因：1. 剧本过长；2. 网络较慢；3. API服务繁忙。建议：1. 尝试缩短剧本长度；2. 稍后重试；3. 检查网络连接；4. 使用更快的API服务。")
            raise Exception(f"LLM调用失败: {error_msg}")
    
    def _call_openai_format(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """调用OpenAI格式的API"""
        headers = {
            "Content-Type": "application/json"
        }
        
        # LM Studio等本地服务可无需密钥
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        # 处理SSL错误：对于 macOS 系统，直接使用 verify=False 避免权限问题
        is_macos = platform.system() == "Darwin"
        skip_ssl_verify = is_macos or os.environ.get("SKIP_SSL_VERIFY", "").lower() == "true"
        
        try:
            # 根据系统决定是否验证SSL
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=600,  # 增加到10分钟，适应长剧本的精细划分
                verify=not skip_ssl_verify  # macOS 使用 False，其他系统使用 True
            )
        except requests.exceptions.SSLError as ssl_error:
            # 如果标准验证失败（非 macOS 系统），尝试备用方案
            if not skip_ssl_verify:
                try:
                    response = requests.post(
                        f"{self.api_base}/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=600,
                        verify=False  # 备用方案：不验证SSL证书
                    )
                except Exception as e2:
                    error_msg = str(ssl_error)
                    if "Operation not permitted" in error_msg or "PermissionError" in error_msg:
                        raise Exception(
                            f"SSL连接权限错误：系统阻止了网络连接。\n\n"
                            f"💡 解决方案：\n"
                            f"1. 在系统设置中，允许Python/Streamlit访问网络\n"
                            f"2. 系统设置 → 安全性与隐私 → 防火墙 → 允许Python访问\n"
                            f"3. 或者设置环境变量：export SKIP_SSL_VERIFY=true\n"
                            f"4. 如果问题持续，可以尝试使用其他LLM服务（如LM Studio本地服务）\n\n"
                            f"原始错误：{error_msg}\n备用方案也失败：{str(e2)}"
                        )
                    else:
                        raise Exception(f"SSL连接失败: {error_msg}\n尝试跳过验证也失败: {str(e2)}")
            else:
                # macOS 系统使用 verify=False 仍然失败
                error_msg = str(ssl_error)
                raise Exception(
                    f"SSL连接失败（即使跳过验证）：{error_msg}\n\n"
                    f"💡 这可能是系统级别的网络权限问题。\n"
                    f"请检查系统设置中的网络权限配置。"
                )
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout("请求超时：API响应时间超过10分钟")
        except Exception as e:
            raise Exception(f"API连接失败: {str(e)}")
        
        if response.status_code != 200:
            error_detail = response.text
            # 尝试解析错误信息
            try:
                error_json = response.json()
                error_msg = error_json.get("error", {}).get("message", error_detail)
                error_code = error_json.get("error", {}).get("code", "")
                
                # 针对常见错误提供友好提示
                if response.status_code == 429:
                    if "负载已饱和" in error_msg or "rate limit" in error_msg.lower():
                        raise Exception(f"API服务繁忙（429）：当前请求过多，服务器负载已饱和。\n\n💡 建议：\n1. 等待 1-2 分钟后重试\n2. 尝试使用其他LLM服务（如Deepseek、通义千问等）\n3. 如果使用OpenAI，考虑升级到更高配额\n\n原始错误：{error_msg}")
                    else:
                        raise Exception(f"API限流（429）：请求频率过高。\n\n💡 建议：\n1. 等待几分钟后重试\n2. 减少请求频率\n\n原始错误：{error_msg}")
                elif response.status_code == 401:
                    raise Exception(f"API认证失败（401）：API Key无效或已过期。\n\n💡 请检查：\n1. API Key是否正确\n2. API Key是否已过期\n3. 是否有使用权限\n\n原始错误：{error_msg}")
                elif response.status_code == 403:
                    raise Exception(f"API权限不足（403）：当前API Key没有访问权限。\n\n💡 请检查：\n1. API Key是否有访问该模型的权限\n2. 账户余额是否充足\n\n原始错误：{error_msg}")
                else:
                    raise Exception(f"API调用失败 ({response.status_code}): {error_msg}")
            except:
                # 如果无法解析JSON，使用原始错误信息
                raise Exception(f"API调用失败 ({response.status_code}): {error_detail}")
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # 检查是否被截断
        finish_reason = result["choices"][0].get("finish_reason", "")
        if finish_reason == "length":
            raise Exception("响应被截断（超过最大token限制），请尝试缩短输入或使用支持更长上下文的模型")
        
        return content
    
    def _extract_json_from_response(self, response: str) -> List[Dict]:
        """从响应中提取JSON"""
        import re
        
        # 尝试提取JSON代码块
        patterns = [
            r"```json\s*(.*?)\s*```",
            r"```\s*(.*?)\s*```",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                try:
                    return json.loads(matches[0])
                except:
                    continue
        
        # 直接解析
        try:
            return json.loads(response)
        except:
            # 尝试查找数组
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(response[start:end])
                except:
                    pass
        
        raise Exception("无法从响应中提取有效的JSON数据")
    
    def fetch_available_models(self, brand: str, api_key: str) -> List[str]:
        """
        从API获取可用模型列表
        
        Args:
            brand: LLM品牌
            api_key: API密钥
        
        Returns:
            List[str]: 模型列表
        """
        try:
            config = get_llm_config(brand)
            
            # LM Studio本地服务无需API密钥
            if brand == "LM Studio":
                headers = {"Content-Type": "application/json"}
            else:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            
            # 构建 models 接口 URL
            # 确保 api_base 格式正确（去除末尾的斜杠，然后添加 /models）
            api_base = config['api_base'].rstrip('/')
            models_url = f"{api_base}/models"
            
            # 处理SSL错误：对于 macOS 系统，直接使用 verify=False 避免权限问题
            is_macos = platform.system() == "Darwin"
            skip_ssl_verify = is_macos or os.environ.get("SKIP_SSL_VERIFY", "").lower() == "true"
            
            # 根据系统决定是否验证SSL
            # macOS 系统直接使用 verify=False，避免权限问题
            try:
                # 对于 macOS，始终使用 verify=False
                # 对于其他系统，先尝试标准验证，失败后使用 verify=False
                use_verify = not skip_ssl_verify
                
                response = requests.get(
                    models_url,
                    headers=headers,
                    timeout=30,
                    verify=use_verify
                )
            except requests.exceptions.SSLError as ssl_error:
                # 如果标准验证失败，尝试备用方案
                if use_verify:
                    try:
                        response = requests.get(
                            models_url,
                            headers=headers,
                            timeout=30,
                            verify=False  # 备用方案：不验证SSL证书
                        )
                    except requests.exceptions.SSLError as ssl_error2:
                        # 备用方案也失败
                        error_msg = str(ssl_error2)
                        if "Operation not permitted" in error_msg or "PermissionError" in error_msg:
                            raise Exception(
                                f"SSL连接权限错误：系统阻止了网络连接。\n\n"
                                f"💡 解决方案：\n"
                                f"1. 在macOS系统设置中，允许Python/Streamlit访问网络\n"
                                f"2. 系统设置 → 安全性与隐私 → 防火墙 → 允许Python访问\n"
                                f"3. 或者使用终端运行：sudo spctl --master-disable（需要管理员权限）\n"
                                f"4. 如果问题持续，可以尝试使用其他LLM服务（如LM Studio本地服务）\n\n"
                                f"原始错误：{error_msg}"
                            )
                        else:
                            raise Exception(f"SSL连接失败: {error_msg}")
                else:
                    # macOS 使用 verify=False 仍然失败
                    error_msg = str(ssl_error)
                    if "Operation not permitted" in error_msg or "PermissionError" in error_msg:
                        raise Exception(
                            f"SSL连接权限错误：macOS系统阻止了网络连接（即使跳过SSL验证）。\n\n"
                            f"💡 这是系统级别的权限问题，需要：\n"
                            f"1. 在macOS系统设置中，允许Python/Streamlit访问网络\n"
                            f"2. 系统设置 → 安全性与隐私 → 防火墙 → 允许Python访问\n"
                            f"3. 或者使用终端运行：sudo spctl --master-disable（需要管理员权限）\n"
                            f"4. 如果问题持续，可以尝试使用其他LLM服务（如LM Studio本地服务）\n\n"
                            f"原始错误：{error_msg}"
                        )
                    else:
                        raise Exception(f"SSL连接失败: {error_msg}")
            except Exception as e:
                # 其他类型的错误
                raise Exception(f"API连接失败: {str(e)}")
            
            # 检查 HTTP 状态码
            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get("error", {}).get("message", error_detail)
                    error_code = error_json.get("error", {}).get("code", "")
                    
                    if response.status_code == 401:
                        raise Exception(f"API认证失败（401）：API Key无效或已过期。\n\n💡 请检查：\n1. API Key是否正确\n2. API Key是否已过期\n3. 是否有使用权限\n\n原始错误：{error_msg}")
                    elif response.status_code == 403:
                        raise Exception(f"API权限不足（403）：当前API Key没有访问权限。\n\n💡 请检查：\n1. API Key是否有访问该模型的权限\n2. 账户余额是否充足\n\n原始错误：{error_msg}")
                    elif response.status_code == 404:
                        raise Exception(f"API端点不存在（404）：该品牌可能不支持 /models 接口。\n\n💡 建议：\n1. 使用自定义模型输入\n2. 或使用配置文件中预定义的模型列表\n\n原始错误：{error_msg}")
                    else:
                        raise Exception(f"API调用失败 ({response.status_code}): {error_msg}")
                except:
                    # 如果无法解析JSON，使用原始错误信息
                    raise Exception(f"API调用失败 ({response.status_code}): {error_detail}")
            
            result = response.json()
            
            # 提取模型ID
            if "data" in result and isinstance(result["data"], list):
                models = []
                for model in result["data"]:
                    if isinstance(model, dict) and "id" in model:
                        models.append(model["id"])
                if models:
                    return models
                else:
                    raise Exception("API返回的模型列表为空")
            else:
                # 某些 API 可能使用不同的响应格式，尝试其他格式
                if "models" in result and isinstance(result["models"], list):
                    models = []
                    for model in result["models"]:
                        if isinstance(model, dict) and "id" in model:
                            models.append(model["id"])
                        elif isinstance(model, str):
                            models.append(model)
                    if models:
                        return models
                
                raise Exception(f"API响应格式不正确。响应内容：{json.dumps(result, ensure_ascii=False, indent=2)}")
        
        except Exception as e:
            raise Exception(f"获取模型列表失败: {str(e)}")
