"""
文生图提示词生成模块（Nano Banana Pro 格式）
支持 LLM 辅助生成更准确的 JSON 提示词
"""

import json
from typing import Dict, List, Any, Optional
from config.image_prompt_templates import (
    NANO_BANANA_PROMPT_TEMPLATE,
    SHOT_SIZE_MAPPING,
    CAMERA_ANGLE_MAPPING,
    CAMERA_MOVEMENT_MAPPING,
    CAMERA_EQUIPMENT_MAPPING,
    CAMERA_MODEL_MAPPING,
    LENS_MAPPING,
    APERTURE_MAPPING,
    MOOD_MAPPING,
    TIME_MAPPING,
    DEFAULT_NEGATIVE_PROMPT,
    QUALITY_TAGS
)
from config.prompt_generation_prompts import (
    PROMPT_GENERATION_SYSTEM_PROMPT,
    get_visual_elements_extraction_prompt,
    get_translation_prompt
)

class ImagePromptGenerator:
    """文生图提示词生成器（Nano Banana Pro 格式）"""
    
    def __init__(self, config: Optional[Dict] = None, llm_service: Optional[Any] = None):
        """
        初始化生成器
        
        Args:
            config: 配置字典，包含：
                - language: "chinese", "english", "bilingual" (默认: "bilingual")
                - detail_level: "simple", "standard", "detailed" (默认: "standard")
                - include_technical: bool (默认: True)
                - include_mood: bool (默认: True)
                - include_characters: bool (默认: True)
                - include_dialogue: bool (默认: False)
                - use_llm: bool (默认: False) - 是否使用 LLM 辅助生成
            llm_service: LLMService 实例（可选），如果提供且 use_llm=True，将使用 LLM 辅助生成
        """
        self.config = config or {}
        self.language = self.config.get("language", "bilingual")
        self.detail_level = self.config.get("detail_level", "standard")
        self.include_technical = self.config.get("include_technical", True)
        self.include_mood = self.config.get("include_mood", True)
        self.include_characters = self.config.get("include_characters", True)
        self.include_dialogue = self.config.get("include_dialogue", False)
        self.use_llm = self.config.get("use_llm", False)
        self.llm_service = llm_service
        
        # 如果启用 LLM 但没有提供服务，发出警告
        if self.use_llm and not self.llm_service:
            import warnings
            warnings.warn("use_llm=True 但未提供 llm_service，将回退到规则处理模式")
            self.use_llm = False
    
    def generate_prompt(self, scene: Dict[str, Any], context_scenes: List[Dict] = None) -> Dict[str, Any]:
        """
        为单个分镜生成 Nano Banana Pro 格式的提示词
        
        Args:
            scene: 分镜数据字典
            context_scenes: 上下文分镜列表（用于分析姿势和表情）
            
        Returns:
            Dict: 包含 JSON 结构化提示词的字典
        """
        # 获取完整的分镜描述（作为核心内容）
        full_description = scene.get("scene_description", "")
        
        # 创建基础模板副本
        prompt = json.loads(json.dumps(NANO_BANANA_PROMPT_TEMPLATE))
        
        # 提取视觉元素（带上下文）
        visual_elements = self._extract_visual_elements(scene, context_scenes)
        
        # 填充主体信息（基于完整描述提取，但保留描述完整性）
        prompt["subject"] = self._build_subject(visual_elements, scene)
        # 将完整描述添加到主体信息中
        if full_description:
            if self.language == "bilingual":
                prompt["subject"]["full_description"] = f"{full_description} / {self._translate_scene_description(full_description)}"
            elif self.language == "english":
                prompt["subject"]["full_description"] = self._translate_scene_description(full_description)
            else:
                prompt["subject"]["full_description"] = full_description
        
        # 填充场景信息
        prompt["scene"] = self._build_scene(visual_elements, scene)
        # 将完整描述添加到场景信息中
        if full_description:
            prompt["scene"]["full_description"] = full_description
        
        # 填充构图信息
        prompt["composition"] = self._build_composition(scene)
        
        # 填充光照信息
        prompt["lighting"] = self._build_lighting(scene)
        
        # 填充技术参数
        if self.include_technical:
            prompt["camera_technical"] = self._build_camera_technical(scene)
        else:
            prompt.pop("camera_technical", None)
        
        # 填充视觉风格
        prompt["visual_style"] = self._build_visual_style(scene)
        
        # 构建空间锚点（根据构图需求）
        prompt["spatial_anchors"] = self._build_spatial_anchors(scene)
        
        # 构建负面约束
        prompt["negative_constraints"] = self._build_negative_constraints(scene)
        
        return {
            "scene_number": scene.get("scene_number", 0),
            "scene_description": full_description,
            "prompt_json": prompt,
            "prompt_text": self._format_prompt_text(prompt, full_description),
            "negative_prompt": self._format_negative_prompt(scene)
        }
    
    def generate_batch(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量生成提示词（支持上下文分析）
        
        Args:
            scenes: 分镜列表
            
        Returns:
            List[Dict]: 提示词列表
        """
        results = []
        for scene in scenes:
            try:
                # 传递所有分镜作为上下文，让 LLM 能够分析前后分镜
                result = self.generate_prompt(scene, context_scenes=scenes)
                results.append(result)
            except Exception as e:
                # 如果某个分镜生成失败，记录错误但继续处理其他分镜
                results.append({
                    "scene_number": scene.get("scene_number", 0),
                    "error": str(e),
                    "prompt_json": None,
                    "prompt_text": "",
                    "negative_prompt": ""
                })
        return results
    
    def _extract_visual_elements(self, scene: Dict, context_scenes: List[Dict] = None) -> Dict:
        """提取视觉元素（支持 LLM 辅助和上下文分析）"""
        description = scene.get("scene_description", "")
        characters = scene.get("characters", [])
        
        # 如果启用 LLM，尝试使用 LLM 提取（带上下文）
        if self.use_llm and self.llm_service:
            try:
                return self._extract_visual_elements_with_llm(scene, context_scenes)
            except Exception as e:
                # LLM 调用失败，回退到规则处理
                import warnings
                warnings.warn(f"LLM 提取失败，回退到规则处理: {str(e)}")
        
        # 规则处理（原有逻辑）
        return {
            "description": description,
            "characters": characters,
            "location": scene.get("location", ""),
            "time": scene.get("time", ""),
            "mood": scene.get("mood", ""),
            "dialogue": scene.get("dialogue_text", "")
        }
    
    def _extract_visual_elements_with_llm(self, scene: Dict, context_scenes: List[Dict] = None) -> Dict:
        """使用 LLM 提取视觉元素（支持上下文分析）"""
        description = scene.get("scene_description", "")
        characters = scene.get("characters", [])
        
        # 获取上下文信息
        previous_scene = None
        next_scene = None
        if context_scenes:
            current_index = None
            for idx, s in enumerate(context_scenes):
                if s.get("scene_number") == scene.get("scene_number"):
                    current_index = idx
                    break
            
            if current_index is not None:
                # 获取前一个分镜
                if current_index > 0:
                    prev_scene = context_scenes[current_index - 1]
                    previous_scene = prev_scene.get("scene_description", "")
                
                # 获取下一个分镜
                if current_index < len(context_scenes) - 1:
                    next_scene_obj = context_scenes[current_index + 1]
                    next_scene = next_scene_obj.get("scene_description", "")
        
        # 构建 LLM 提示词
        user_prompt = get_visual_elements_extraction_prompt(
            description,
            characters,
            self.language,
            previous_scene=previous_scene,
            next_scene=next_scene
        )
        
        messages = [
            {"role": "system", "content": PROMPT_GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        # 调用 LLM
        response = self.llm_service._call_llm(messages, temperature=0.3)  # 使用较低温度以获得更准确的结果
        
        # 提取 JSON
        try:
            # 尝试从响应中提取 JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                extracted_data = json.loads(json_str)
                
                # 转换为标准格式
                return {
                    "description": description,
                    "characters": characters,
                    "location": scene.get("location", ""),
                    "time": scene.get("time", ""),
                    "mood": scene.get("mood", ""),
                    "dialogue": scene.get("dialogue_text", ""),
                    # LLM 提取的数据
                    "llm_extracted": extracted_data
                }
        except json.JSONDecodeError:
            # JSON 解析失败，回退到规则处理
            pass
        
        # 如果 LLM 提取失败，返回基础数据
        return {
            "description": description,
            "characters": characters,
            "location": scene.get("location", ""),
            "time": scene.get("time", ""),
            "mood": scene.get("mood", ""),
            "dialogue": scene.get("dialogue_text", "")
        }
    
    def _build_subject(self, visual_elements: Dict, scene: Dict) -> Dict:
        """构建主体信息（支持 LLM 辅助）"""
        characters = visual_elements.get("characters", [])
        description = visual_elements.get("description", "")
        
        # 如果 LLM 已提取数据，优先使用
        full_description = description  # 默认值
        if "llm_extracted" in visual_elements:
            llm_data = visual_elements["llm_extracted"]
            subject_data = llm_data.get("subject", {})
            
            # 使用 LLM 提取的数据
            main_char = subject_data.get("main_character", characters[0] if characters else "人物")
            action = subject_data.get("action", "")
            pose = subject_data.get("pose", "")
            expression = subject_data.get("expression", "")
            clothing = subject_data.get("clothing", "")
            props = subject_data.get("props", "")
            full_description = subject_data.get("full_description", description)
            
            # 如果 LLM 没有提供某些字段，使用规则提取作为补充
            if not action:
                action = self._extract_action(description)
                action_detail = self._extract_action_detail(description, action)
            else:
                action_detail = action
            # 姿势：如果 LLM 没有提供，先尝试从描述中提取，如果还是没有且不是空镜，再推断
            if not pose:
                pose = self._extract_pose(description)
                # 如果提取失败且不是空镜，才进行推断（避免在最终检查时重复推断）
                if not pose and not self._is_empty_scene(description, characters):
                    pose = self._infer_pose_from_context(description, action_detail, scene)
            if not expression:
                expression = self._extract_expression(description)
            if not clothing:
                clothing = self._extract_clothing(description)
            if not props:
                props = self._extract_props(description)
        else:
            # 规则提取（原有逻辑）
            main_char = characters[0] if characters else "人物"
            action = self._extract_action(description)
            action_detail = self._extract_action_detail(description, action)
            # 姿势：先尝试提取，如果失败且不是空镜，再推断
            pose = self._extract_pose(description)
            if not pose and not self._is_empty_scene(description, characters):
                pose = self._infer_pose_from_context(description, action_detail, scene)
            expression = self._extract_expression(description)
            clothing = self._extract_clothing(description)
            props = self._extract_props(description)
        
        # 构建双语描述（如果 LLM 已提供翻译，直接使用；否则使用规则翻译）
        if "llm_extracted" in visual_elements:
            # LLM 已提供翻译，直接使用
            if self.language == "bilingual":
                main_character = f"{main_char} / {main_char}"
                # LLM 数据可能已经包含双语，检查格式
                action_text = action if "/" in action else f"{action} / {self._translate_to_english(action)}"
                pose_text = pose if (not pose or "/" in pose) else f"{pose} / {self._translate_to_english(pose)}"
                expression_text = expression if "/" in expression else f"{expression} / {self._translate_to_english(expression)}"
                clothing_text = clothing if (not clothing or "/" in clothing) else f"{clothing} / {self._translate_to_english(clothing)}"
                props_text = props if (not props or "/" in props) else f"{props} / {self._translate_to_english(props)}"
            elif self.language == "english":
                # 提取英文部分（如果存在）
                main_character = main_char
                action_text = action.split(" / ")[-1] if " / " in action else self._translate_to_english(action)
                pose_text = pose.split(" / ")[-1] if (pose and " / " in pose) else (self._translate_to_english(pose) if pose else "")
                expression_text = expression.split(" / ")[-1] if " / " in expression else self._translate_to_english(expression)
                clothing_text = clothing.split(" / ")[-1] if (clothing and " / " in clothing) else (self._translate_to_english(clothing) if clothing else "")
                props_text = props.split(" / ")[-1] if (props and " / " in props) else (self._translate_to_english(props) if props else "")
            else:
                # 中文模式，提取中文部分
                main_character = main_char
                action_text = action.split(" / ")[0] if " / " in action else action
                pose_text = pose.split(" / ")[0] if (pose and " / " in pose) else (pose if pose else "")
                expression_text = expression.split(" / ")[0] if " / " in expression else expression
                clothing_text = clothing.split(" / ")[0] if (clothing and " / " in clothing) else (clothing if clothing else "")
                props_text = props.split(" / ")[0] if (props and " / " in props) else (props if props else "")
        else:
            # 规则处理（原有逻辑）
            if self.language == "bilingual":
                main_character = f"{main_char} / {main_char}"
                action_text = f"{action_detail} / {self._translate_to_english(action_detail)}"
                pose_text = f"{pose} / {self._translate_to_english(pose)}" if pose else ""
                expression_text = f"{expression} / {self._translate_to_english(expression)}"
                clothing_text = f"{clothing} / {self._translate_to_english(clothing)}" if clothing else ""
                props_text = f"{props} / {self._translate_to_english(props)}" if props else ""
            elif self.language == "english":
                main_character = main_char
                action_text = self._translate_to_english(action_detail)
                pose_text = self._translate_to_english(pose) if pose else ""
                expression_text = self._translate_to_english(expression)
                clothing_text = self._translate_to_english(clothing) if clothing else ""
                props_text = self._translate_to_english(props) if props else ""
            else:
                main_character = main_char
                action_text = action_detail
                pose_text = pose if pose else ""
                expression_text = expression
                clothing_text = clothing if clothing else ""
                props_text = props if props else ""
        
        # 最终确保姿势字段被填充（除非是空镜）
        # 注意：这里只检查 pose_text 是否为空，如果为空且不是空镜才推断
        # 前面的逻辑已经处理了 pose 的提取和推断，这里只是确保最终输出不为空
        if not pose_text or pose_text.strip() == "":
            if not self._is_empty_scene(description, characters):
                # 不是空镜，必须填充姿势
                # 如果前面的逻辑已经推断过但 pose_text 仍为空，说明推断结果没有被正确格式化
                # 此时需要重新推断（这种情况应该很少发生）
                if not pose or pose.strip() == "":
                    inferred_pose = self._infer_pose_from_context(description, action_text, scene)
                else:
                    inferred_pose = pose
                
                if self.language == "bilingual":
                    pose_text = f"{inferred_pose} / {self._translate_to_english(inferred_pose)}"
                elif self.language == "english":
                    pose_text = self._translate_to_english(inferred_pose)
                else:
                    pose_text = inferred_pose
        
        result = {
            "main_character": main_character,
            "action": action_text,
            "pose": pose_text,
            "expression": expression_text,
            "clothing": clothing_text,
            "props": props_text
        }
        
        # 如果 LLM 提供了完整描述，添加它
        if "llm_extracted" in visual_elements and full_description:
            result["full_description"] = full_description
        
        return result
    
    def _build_scene(self, visual_elements: Dict, scene: Dict) -> Dict:
        """构建场景信息"""
        location = visual_elements.get("location", "")
        description = visual_elements.get("description", "")
        time = scene.get("time", "白天")
        characters = visual_elements.get("characters", [])
        
        # 获取时间映射
        time_info = TIME_MAPPING.get(time, TIME_MAPPING["白天"])
        
        # 提取场景细节和人物与背景的关系
        scene_details = self._extract_scene_details(description, location)
        character_background_relation = self._extract_character_background_relation(description, characters, location)
        weather = self._extract_weather(description)
        
        # 构建环境描述（包含人物与背景的关系）
        # 组合人物关系、场景细节和位置
        env_parts = []
        if character_background_relation:
            env_parts.append(character_background_relation)
        if scene_details:
            env_parts.append(scene_details)
        elif location:
            env_parts.append(location)
        
        if env_parts:
            env_combined = "，".join(env_parts)
            if self.language == "bilingual":
                environment_text = f"{env_combined} / {self._translate_to_english(env_combined)}"
            elif self.language == "english":
                environment_text = self._translate_to_english(env_combined)
            else:
                environment_text = env_combined
        else:
            environment_text = ""
        
        if self.language == "bilingual":
            location_text = f"{location} / {self._translate_to_english(location)}" if location else ""
            time_text = f"{time_info['chinese']} / {time_info['english']}"
            background_text = environment_text
            weather_text = f"{weather} / {self._translate_to_english(weather)}" if weather else ""
        elif self.language == "english":
            location_text = self._translate_to_english(location) if location else ""
            time_text = time_info["english"]
            background_text = environment_text
            weather_text = self._translate_to_english(weather) if weather else ""
        else:
            location_text = location
            time_text = time_info["chinese"]
            background_text = environment_text
            weather_text = weather if weather else ""
        
        return {
            "location": location_text,
            "environment": environment_text,
            "background": background_text,
            "time_of_day": time_text,
            "weather": weather_text
        }
    
    def _build_composition(self, scene: Dict) -> Dict:
        """构建构图信息"""
        shot_size = scene.get("shot_size", "中景")
        camera_angle = scene.get("camera_angle", "视平")
        composition_tension = scene.get("composition_tension", "")
        
        # 获取映射
        shot_info = SHOT_SIZE_MAPPING.get(shot_size, SHOT_SIZE_MAPPING["中景"])
        angle_info = CAMERA_ANGLE_MAPPING.get(camera_angle, CAMERA_ANGLE_MAPPING["视平"])
        
        if self.language == "bilingual":
            shot_text = f"{shot_info['chinese']} / {shot_info['english']}"
            angle_text = f"{angle_info['chinese']} / {angle_info['english']}"
            # 构图张力翻译
            if composition_tension:
                tension_mapping = {
                    "饱满": "饱满构图，主体占据显著比例 / full composition, subject dominates",
                    "丰富": "丰富构图，多层次信息 / rich composition, multi-layered information",
                    "引导": "引导构图，视线引导 / guiding composition, visual guidance",
                    "饱满+引导": "饱满引导构图 / full guiding composition",
                    "丰富+引导": "丰富引导构图 / rich guiding composition",
                    "饱满+丰富": "饱满丰富构图 / full rich composition",
                    "饱满+丰富+引导": "饱满丰富引导构图 / full rich guiding composition"
                }
                tension_text = tension_mapping.get(composition_tension, f"{composition_tension} / {composition_tension}")
            else:
                tension_text = ""
        elif self.language == "english":
            shot_text = shot_info["english"]
            angle_text = angle_info["english"]
            # 构图张力翻译
            if composition_tension:
                tension_mapping = {
                    "饱满": "full composition, subject dominates",
                    "丰富": "rich composition, multi-layered information",
                    "引导": "guiding composition, visual guidance",
                    "饱满+引导": "full guiding composition",
                    "丰富+引导": "rich guiding composition",
                    "饱满+丰富": "full rich composition",
                    "饱满+丰富+引导": "full rich guiding composition"
                }
                tension_text = tension_mapping.get(composition_tension, composition_tension)
            else:
                tension_text = ""
        else:
            shot_text = shot_info["chinese"]
            angle_text = angle_info["chinese"]
            tension_text = composition_tension if composition_tension else ""
        
        return {
            "shot_size": shot_text,
            "camera_angle": angle_text,
            "composition_tension": tension_text,
            "rule_of_thirds": "遵循三分法则 / rule of thirds",
            "leading_lines": ""  # 可以从描述中提取
        }
    
    def _build_lighting(self, scene: Dict) -> Dict:
        """构建光照信息"""
        time = scene.get("time", "白天")
        mood = scene.get("mood", "")
        
        # 时间决定基础光照
        time_info = TIME_MAPPING.get(time, TIME_MAPPING["白天"])
        
        # 情绪决定光照风格
        mood_info = MOOD_MAPPING.get(mood, {}) if mood else {}
        
        if self.language == "bilingual":
            time_light = f"{time_info['chinese']} / {time_info['english']}"
            mood_light = f"{mood_info.get('chinese', '')} / {mood_info.get('english', '')}" if mood_info else ""
        elif self.language == "english":
            time_light = time_info["english"]
            mood_light = mood_info.get("english", "") if mood_info else ""
        else:
            time_light = time_info["chinese"]
            mood_light = mood_info.get("chinese", "") if mood_info else ""
        
        return {
            "type": time_light,
            "direction": "",  # 可以从描述中提取
            "intensity": mood_light if mood_light else "自然 / natural",
            "color_temperature": time_light,
            "mood": mood_light if mood_light else ""
        }
    
    def _build_camera_technical(self, scene: Dict) -> Dict:
        """构建技术参数"""
        camera = scene.get("camera", "ARRI Alexa")
        lens = scene.get("lens", "ARRI Master Primes")
        aperture = scene.get("aperture", "f/2.8")
        lens_focal = scene.get("lens_focal_length", "标准(35-50mm)")
        
        # 获取映射
        camera_info = CAMERA_MODEL_MAPPING.get(camera, CAMERA_MODEL_MAPPING["ARRI Alexa"])
        lens_info = LENS_MAPPING.get(lens, LENS_MAPPING["ARRI Master Primes"])
        aperture_info = APERTURE_MAPPING.get(aperture, APERTURE_MAPPING["f/2.8"])
        
        if self.language == "bilingual":
            camera_text = f"{camera_info['chinese']} / {camera_info['english']}"
            lens_text = f"{lens_info['chinese']} / {lens_info['english']}"
            aperture_text = f"{aperture_info['chinese']} / {aperture_info['english']}"
            focal_text = f"{lens_focal} / {self._translate_focal_length(lens_focal)}"
        elif self.language == "english":
            camera_text = camera_info["english"]
            lens_text = lens_info["english"]
            aperture_text = aperture_info["english"]
            focal_text = self._translate_focal_length(lens_focal)
        else:
            camera_text = camera_info["chinese"]
            lens_text = lens_info["chinese"]
            aperture_text = aperture_info["chinese"]
            focal_text = lens_focal
        
        return {
            "camera_model": camera_text,
            "lens": lens_text,
            "aperture": aperture_text,
            "focal_length": focal_text,
            "depth_of_field": aperture_info["visual"]
        }
    
    def _build_visual_style(self, scene: Dict) -> Dict:
        """构建视觉风格"""
        camera = scene.get("camera", "ARRI Alexa")
        mood = scene.get("mood", "")
        
        camera_info = CAMERA_MODEL_MAPPING.get(camera, CAMERA_MODEL_MAPPING["ARRI Alexa"])
        mood_info = MOOD_MAPPING.get(mood, {}) if mood else {}
        
        if self.language == "bilingual":
            cinematic = f"{camera_info['visual']} / {camera_info['visual']}"
            color_grading = f"电影级调色 / cinematic color grading"
            atmosphere = f"{mood_info.get('visual', '电影感氛围')} / {mood_info.get('visual', 'cinematic atmosphere')}" if mood_info else "电影感氛围 / cinematic atmosphere"
        elif self.language == "english":
            cinematic = camera_info["visual"]
            color_grading = "cinematic color grading"
            atmosphere = mood_info.get("visual", "cinematic atmosphere") if mood_info else "cinematic atmosphere"
        else:
            cinematic = camera_info["visual"]
            color_grading = "电影级调色"
            atmosphere = mood_info.get("visual", "电影感氛围") if mood_info else "电影感氛围"
        
        return {
            "cinematic_style": cinematic,
            "color_grading": color_grading,
            "texture": "电影质感 / film texture",
            "atmosphere": atmosphere
        }
    
    def _build_spatial_anchors(self, scene: Dict) -> List[Dict]:
        """构建空间锚点"""
        anchors = []
        
        # 根据景别和角度创建空间锚点
        shot_size = scene.get("shot_size", "中景")
        camera_angle = scene.get("camera_angle", "视平")
        
        # 示例：如果是特写，锚定面部
        if "特写" in shot_size:
            anchors.append({
                "element": "面部 / face",
                "position": "画面中心 / center",
                "priority": "high"
            })
        
        # 根据构图张力指南，可以添加更多锚点
        # 这里可以根据 scene_description 分析添加
        
        return anchors
    
    def _build_negative_constraints(self, scene: Dict) -> List[str]:
        """构建负面约束"""
        constraints = []
        
        # 添加通用负面词
        if self.language == "bilingual":
            constraints.append(DEFAULT_NEGATIVE_PROMPT["chinese"])
            constraints.append(DEFAULT_NEGATIVE_PROMPT["english"])
        elif self.language == "english":
            constraints.append(DEFAULT_NEGATIVE_PROMPT["english"])
        else:
            constraints.append(DEFAULT_NEGATIVE_PROMPT["chinese"])
        
        # 根据场景添加特定负面词
        time = scene.get("time", "白天")
        if time == "夜晚":
            constraints.append("白天光线 / daytime lighting")
        elif time == "白天":
            constraints.append("夜晚黑暗 / nighttime darkness")
        
        return constraints
    
    def _format_prompt_text(self, prompt_json: Dict, scene_description: str = "") -> str:
        """将 JSON 格式转换为文本格式（用于显示和复制）"""
        parts = []
        
        # 首先添加完整的分镜描述（作为核心内容）
        if scene_description:
            # 保留原始描述，只做最小清理（移除多余空格）
            import re
            cleaned_desc = re.sub(r'\s+', ' ', scene_description).strip()
            
            if self.language == "bilingual":
                # 双语模式下，保留完整中文描述
                parts.append(cleaned_desc)
            elif self.language == "english":
                # 英文模式下，可以添加翻译（目前保留原样）
                parts.append(cleaned_desc)
            else:
                parts.append(cleaned_desc)
        
        # 然后添加提取的详细信息（作为补充）
        # 主体信息（如果分镜描述中没有完全包含）
        if prompt_json.get("subject", {}).get("pose"):
            pose = prompt_json["subject"]["pose"]
            if pose and pose not in scene_description:
                parts.append(pose)
        
        if prompt_json.get("subject", {}).get("props"):
            props = prompt_json["subject"]["props"]
            if props and props not in scene_description:
                parts.append(props)
        
        # 场景环境信息
        if prompt_json.get("scene", {}).get("environment"):
            env = prompt_json["scene"]["environment"]
            # 如果环境信息与描述不重复，添加
            if env and not any(word in scene_description for word in env.split()[:3]):
                parts.append(env)
        
        # 构图信息（镜头语言）
        if prompt_json.get("composition", {}).get("shot_size"):
            comp_parts = []
            if prompt_json["composition"]["shot_size"]:
                comp_parts.append(prompt_json["composition"]["shot_size"])
            if prompt_json["composition"]["camera_angle"]:
                comp_parts.append(prompt_json["composition"]["camera_angle"])
            if prompt_json["composition"].get("composition_tension"):
                comp_parts.append(prompt_json["composition"]["composition_tension"])
            if comp_parts:
                parts.append(", ".join(comp_parts))
        
        # 技术参数
        if prompt_json.get("camera_technical"):
            tech_parts = []
            if prompt_json["camera_technical"].get("camera_model"):
                tech_parts.append(prompt_json["camera_technical"]["camera_model"])
            if prompt_json["camera_technical"].get("lens"):
                tech_parts.append(prompt_json["camera_technical"]["lens"])
            if prompt_json["camera_technical"].get("aperture"):
                tech_parts.append(prompt_json["camera_technical"]["aperture"])
            if prompt_json["camera_technical"].get("depth_of_field"):
                tech_parts.append(prompt_json["camera_technical"]["depth_of_field"])
            if tech_parts:
                parts.append(", ".join(tech_parts))
        
        # 视觉风格
        if prompt_json.get("visual_style", {}).get("cinematic_style"):
            style_parts = []
            if prompt_json["visual_style"]["cinematic_style"]:
                style_parts.append(prompt_json["visual_style"]["cinematic_style"])
            if prompt_json["visual_style"]["color_grading"]:
                style_parts.append(prompt_json["visual_style"]["color_grading"])
            if style_parts:
                parts.append(", ".join(style_parts))
        
        # 质量标签
        if self.language == "bilingual":
            parts.append(QUALITY_TAGS["chinese"] + " / " + QUALITY_TAGS["english"])
        elif self.language == "english":
            parts.append(QUALITY_TAGS["english"])
        else:
            parts.append(QUALITY_TAGS["chinese"])
        
        return ", ".join(parts)
    
    def _translate_scene_description(self, description: str) -> str:
        """翻译分镜描述（支持 LLM 辅助和字典翻译）"""
        if not description or not description.strip():
            return description
        
        # 如果启用 LLM，优先使用 LLM 翻译
        if self.use_llm and self.llm_service:
            try:
                return self._translate_with_llm(description)
            except Exception as e:
                # LLM 翻译失败，回退到字典翻译
                import warnings
                warnings.warn(f"LLM 翻译失败，回退到字典翻译: {str(e)}")
        
        # 使用字典进行基础翻译
        return self._translate_with_dict(description)
    
    def _translate_with_dict(self, text: str) -> str:
        """使用字典进行翻译（智能匹配）"""
        if not text or not text.strip():
            return text
        
        translations = self._get_basic_translations()
        result = text
        
        # 按长度排序，优先匹配长词
        sorted_keys = sorted(translations.keys(), key=len, reverse=True)
        
        # 替换所有匹配的词汇
        for chinese in sorted_keys:
            english = translations[chinese]
            if chinese in result:
                # 替换所有出现的位置
                result = result.replace(chinese, english)
        
        # 如果完全没有匹配到，返回原文本
        # 如果部分匹配，返回混合结果（保留未匹配的部分）
        if result == text:
            # 尝试简单的逐词翻译
            words = text.split()
            translated_words = []
            for word in words:
                if word in translations:
                    translated_words.append(translations[word])
                else:
                    translated_words.append(word)
            result = " ".join(translated_words)
        
        return result
    
    def _translate_with_llm(self, text: str) -> str:
        """使用 LLM 进行翻译"""
        if not text or not text.strip():
            return text
        
        user_prompt = get_translation_prompt(text, "english")
        
        messages = [
            {"role": "system", "content": "你是一个专业的翻译专家，擅长将中文电影术语准确翻译成英文。"},
            {"role": "user", "content": user_prompt}
        ]
        
        # 调用 LLM
        response = self.llm_service._call_llm(messages, temperature=0.3)
        
        # 清理响应（移除可能的说明文字）
        translation = response.strip()
        # 如果响应包含引号，提取引号内的内容
        if translation.startswith('"') and translation.endswith('"'):
            translation = translation[1:-1]
        elif translation.startswith("'") and translation.endswith("'"):
            translation = translation[1:-1]
        
        return translation if translation else text
    
    def _format_negative_prompt(self, scene: Dict) -> str:
        """格式化负面提示词"""
        constraints = self._build_negative_constraints(scene)
        return ", ".join(constraints)
    
    def _extract_action(self, description: str) -> str:
        """从描述中提取动作关键词"""
        # 扩展的动作关键词
        action_keywords = [
            "坐", "站", "走", "跑", "看", "说", "笑", "哭", "转身", "抬头", "低头",
            "推", "拉", "拿", "放", "举", "握", "抓", "扔", "踢", "跳",
            "进入", "离开", "靠近", "远离", "跟随", "追逐", "躲避",
            "环顾", "张望", "凝视", "注视", "扫视", "瞥见",
            "点头", "摇头", "挥手", "摆手", "指向", "指向",
            "蹲下", "站起", "躺下", "趴下", "跪下", "弯腰",
            "拥抱", "握手", "拍", "打", "推门", "开门", "关门",
            "拿起", "放下", "递给", "接过", "翻开", "合上"
        ]
        
        # 按长度排序，优先匹配长词
        action_keywords.sort(key=len, reverse=True)
        
        for keyword in action_keywords:
            if keyword in description:
                return keyword
        
        # 如果没有找到，尝试提取动词
        import re
        # 匹配常见的中文动词模式
        verb_patterns = [
            r"([^，。！？\s]+(?:着|了|过|在))",  # 带助词的动词
            r"([^，。！？\s]+(?:中|时))",  # 进行时
        ]
        
        for pattern in verb_patterns:
            matches = re.findall(pattern, description)
            if matches:
                return matches[0]
        
        return "动作"
    
    def _extract_action_detail(self, description: str, base_action: str) -> str:
        """提取详细的动作描述（包含动作的完整信息）"""
        # 如果描述中包含动作，提取动作及其上下文
        if base_action in description:
            # 找到动作在描述中的位置
            idx = description.find(base_action)
            # 提取动作前后的上下文（各12个字符）
            start = max(0, idx - 12)
            end = min(len(description), idx + len(base_action) + 12)
            context = description[start:end]
            
            # 清理上下文，保留关键信息
            import re
            # 移除标点符号，但保留关键信息
            context = re.sub(r'[，。！？、]', ' ', context)
            # 移除多余空格
            context = re.sub(r'\s+', ' ', context).strip()
            
            # 如果上下文有意义且长度合理，返回更详细的描述
            # 限制在30个字符以内，避免过长
            if len(context) > len(base_action) and len(context) <= 30:
                return context
            else:
                # 如果太长，只返回动作本身加上紧邻的2-3个词
                words = context.split()
                if len(words) > 1:
                    # 找到动作词的位置
                    try:
                        action_idx = words.index(base_action) if base_action in words else -1
                        if action_idx >= 0:
                            # 取动作前后各1-2个词
                            start_word = max(0, action_idx - 1)
                            end_word = min(len(words), action_idx + 2)
                            return ' '.join(words[start_word:end_word])
                    except:
                        pass
                return base_action
        
        return base_action
    
    def _is_empty_scene(self, description: str, characters: List[str]) -> bool:
        """
        判断是否是空镜（完全不涉及人物）
        
        Args:
            description: 分镜描述
            characters: 人物列表
            
        Returns:
            bool: 如果是空镜返回 True，否则返回 False
        """
        # 如果有人物列表且不为空，不是空镜
        if characters and len(characters) > 0:
            return False
        
        # 如果描述为空，可能是空镜
        if not description or len(description.strip()) == 0:
            return True
        
        # 检查描述中是否包含人物相关词汇（去重并优化）
        person_keywords = [
            "人物", "角色", "人", "主角", "演员", "他", "她", "他们", "她们",
            "配角", "反派", "英雄", "主角", "人物", "角色", "主角",
            "主角", "主角", "主角", "主角", "主角", "主角", "主角", "主角",  # 移除重复
            "主角", "主角", "主角", "主角", "主角", "主角", "主角", "主角"
        ]
        # 去重
        person_keywords = list(set(person_keywords))
        
        description_lower = description.lower()
        for keyword in person_keywords:
            if keyword in description or keyword in description_lower:
                return False
        
        # 检查动作词汇（如果有明显的动作，通常不是空镜）
        action_keywords = ["走", "跑", "坐", "站", "看", "说", "笑", "哭", "转身", "抬头", "低头"]
        for keyword in action_keywords:
            if keyword in description:
                return False
        
        # 检查是否是纯环境描述（只包含环境、风景、建筑等词汇）
        environment_keywords = [
            "风景", "环境", "建筑", "天空", "云", "山", "海", "树", "街道", "城市", "房屋",
            "空镜", "空景", "空镜头", "空场景", "无人物", "没有人", "纯环境", "纯风景"
        ]
        has_environment = any(keyword in description for keyword in environment_keywords)
        has_person = any(keyword in description for keyword in person_keywords)
        
        # 如果明确标注为空镜相关词汇，直接返回 True
        empty_scene_keywords = ["空镜", "空景", "空镜头", "空场景", "无人物", "没有人", "纯环境", "纯风景"]
        if any(keyword in description for keyword in empty_scene_keywords):
            return True
        
        # 如果只有环境词汇，没有人物词汇和动作词汇，可能是空镜
        if has_environment and not has_person:
            # 进一步检查：如果描述很短且只包含环境词汇，更可能是空镜
            if len(description.strip()) < 20:
                return True
        
        return False
    
    def _infer_pose_from_context(self, description: str, action: str, scene: Dict) -> str:
        """
        根据上下文推断姿势（当描述中没有明确姿势时）
        
        Args:
            description: 分镜描述
            action: 动作描述
            scene: 分镜数据字典
            
        Returns:
            str: 推断的姿势描述
        """
        # 根据动作推断姿势
        if action:
            action_lower = action.lower()
            if "跑" in action or "奔跑" in action or "running" in action_lower:
                return "身体前倾、双腿交替、手臂摆动"
            elif "走" in action or "步行" in action or "walking" in action_lower:
                return "自然站立、双腿交替、手臂自然摆动"
            elif "停" in action or "停下" in action or "stop" in action_lower:
                return "急停、身体前倾、双手撑膝"
            elif "坐" in action or "sitting" in action_lower:
                return "盘腿而坐、身体前倾"
            elif "站" in action or "站立" in action or "standing" in action_lower:
                return "昂首站立、双手自然下垂"
            elif "蹲" in action or "crouching" in action_lower:
                return "蹲下、身体前倾、双手撑地"
            elif "躺" in action or "lying" in action_lower:
                return "平躺、身体放松"
            elif "转身" in action or "turn" in action_lower:
                return "转身、背对镜头、肩膀紧绷"
            elif "看" in action or "look" in action_lower or "凝视" in action:
                return "站立、头部转向、眼神专注"
            elif "握" in action or "grip" in action_lower or "握拳" in action:
                return "握拳、挺胸、身体前倾"
        
        # 根据情绪推断姿势
        mood = scene.get("mood", "")
        if mood:
            mood_lower = mood.lower()
            if "愤怒" in mood or "angry" in mood_lower or "愤怒" in mood:
                return "握拳、挺胸、身体前倾"
            elif "悲伤" in mood or "sad" in mood_lower or "悲伤" in mood:
                return "低头、肩膀下垂、双手无力"
            elif "紧张" in mood or "nervous" in mood_lower or "紧张" in mood:
                return "身体紧绷、双手握拳、肩膀高耸"
            elif "放松" in mood or "relaxed" in mood_lower or "放松" in mood:
                return "身体放松、双手自然下垂、肩膀放松"
        
        # 根据景别推断姿势
        shot_size = scene.get("shot_size", "")
        if shot_size:
            if "特写" in shot_size or "close" in shot_size.lower():
                return "头部特写、颈部以上"
            elif "近景" in shot_size or "close shot" in shot_size.lower():
                return "肩部以上、头部和肩膀"
            elif "中景" in shot_size or "medium" in shot_size.lower():
                return "腰部以上、上半身"
            elif "全景" in shot_size or "full" in shot_size.lower():
                return "全身站立、双手自然下垂"
        
        # 默认姿势
        return "自然站立、双手自然下垂"
    
    def _extract_pose(self, description: str) -> str:
        """从描述中提取姿势"""
        pose_keywords = [
            "坐", "站", "蹲", "跪", "躺", "趴", "靠", "倚",
            "弯腰", "挺胸", "抬头", "低头", "侧身", "转身",
            "双手叉腰", "双手抱胸", "双手背后", "单手扶墙",
            "双腿交叉", "单腿站立", "盘腿", "翘腿"
        ]
        
        # 按长度排序
        pose_keywords.sort(key=len, reverse=True)
        
        for keyword in pose_keywords:
            if keyword in description:
                return keyword
        
        # 从动作中推断姿势
        if "坐" in description:
            return "坐着"
        elif "站" in description:
            return "站着"
        elif "躺" in description:
            return "躺着"
        
        return ""
    
    def _extract_expression(self, description: str) -> str:
        """从描述中提取表情"""
        expression_keywords = [
            "焦虑", "紧张", "轻松", "悲伤", "高兴", "愤怒", "疑惑", "微笑",
            "严肃", "冷漠", "兴奋", "恐惧", "惊讶", "失望", "满意", "不满",
            "痛苦", "快乐", "忧郁", "开朗", "疲惫", "精神", "专注", "分心",
            "面无表情", "眉头紧锁", "嘴角上扬", "眼神坚定", "眼神闪烁",
            "如释重负", "愁眉苦脸", "喜笑颜开", "怒目而视"
        ]
        
        # 按长度排序
        expression_keywords.sort(key=len, reverse=True)
        
        for keyword in expression_keywords:
            if keyword in description:
                return keyword
        
        return "自然表情"
    
    def _extract_clothing(self, description: str) -> str:
        """从描述中提取服装信息"""
        clothing_keywords = [
            "西装", "衬衫", "T恤", "裙子", "裤子", "外套", "大衣", "风衣",
            "制服", "工作服", "运动服", "休闲服", "正装", "便装",
            "红色", "蓝色", "黑色", "白色", "灰色", "彩色"
        ]
        
        for keyword in clothing_keywords:
            if keyword in description:
                return keyword
        
        return ""
    
    def _extract_props(self, description: str) -> str:
        """从描述中提取道具信息"""
        props_keywords = [
            "手机", "电脑", "书", "笔", "杯子", "包", "钥匙", "钱包",
            "文件", "文件夹", "报纸", "杂志", "相机", "眼镜",
            "门", "窗", "桌子", "椅子", "沙发", "床",
            "车", "自行车", "摩托车", "包", "行李箱"
        ]
        
        for keyword in props_keywords:
            if keyword in description:
                return keyword
        
        return ""
    
    def _extract_scene_details(self, description: str, location: str) -> str:
        """提取场景细节"""
        # 提取描述中关于场景的详细信息
        # 移除人物相关的描述，保留环境描述
        
        # 场景特征关键词
        scene_features = [
            "宽敞", "狭窄", "明亮", "昏暗", "整洁", "凌乱", "安静", "嘈杂",
            "现代", "古典", "豪华", "简陋", "温馨", "冷清", "热闹", "空旷"
        ]
        
        details = []
        for feature in scene_features:
            if feature in description:
                details.append(feature)
        
        # 如果有位置信息，结合位置和特征
        if details and location:
            return f"{location}，{''.join(details)}"
        elif details:
            return ''.join(details)
        elif location:
            return location
        else:
            return ""
    
    def _extract_character_background_relation(self, description: str, characters: List[str], location: str) -> str:
        """提取人物与背景的关系"""
        if not characters or not description:
            return ""
        
        main_char = characters[0]
        import re
        
        # 位置关系关键词（按优先级排序，长词优先）
        position_keywords = [
            "坐在", "站在", "躺在", "靠在", "倚在", "位于",
            "窗边", "桌边", "门口", "角落", "中央", "中间",
            "旁边", "前方", "后方", "左侧", "右侧", "边缘",
            "面对", "背对", "面向", "背向", "靠近", "远离"
        ]
        
        # 尝试提取完整的位置关系短语
        # 模式：人物 + 位置动词 + 位置描述
        patterns = [
            rf"{main_char}(?:坐在|站在|躺在|靠在|倚在)([^，。！？]+?)(?:，|。|$)",
            rf"{main_char}[^，。！？]*(?:在|位于)([^，。！？]+?)(?:，|。|$)",
            rf"{main_char}([^，。！？]*(?:窗边|桌边|门口|角落|中央|中间|旁边))",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, description)
            if matches:
                # 清理匹配结果，提取位置描述
                for match in matches[:1]:  # 只取第一个匹配
                    # 移除标点，保留关键信息
                    cleaned = re.sub(r'[，。！？、]', '', match).strip()
                    if cleaned and len(cleaned) > 1:
                        # 如果包含位置信息，返回完整关系
                        if any(kw in cleaned for kw in ["窗", "桌", "门", "角", "中", "旁", "边"]):
                            return f"{main_char}在{cleaned}"
                        elif location and location in cleaned:
                            return f"{main_char}在{cleaned}"
                        elif len(cleaned) <= 15:  # 限制长度
                            return f"{main_char}在{cleaned}"
        
        # 如果没有找到，尝试简单匹配
        for keyword in sorted(position_keywords, key=len, reverse=True):
            if keyword in description:
                idx = description.find(keyword)
                # 检查前面是否有人物名称
                char_start = max(0, idx - 10)
                char_snippet = description[char_start:idx]
                
                if main_char in char_snippet:
                    # 提取位置描述（向后15个字符）
                    pos_end = min(len(description), idx + len(keyword) + 15)
                    pos_snippet = description[idx:pos_end]
                    # 清理位置描述
                    pos_cleaned = re.sub(r'[，。！？、]', '', pos_snippet).strip()
                    if pos_cleaned and len(pos_cleaned) <= 20:
                        return pos_cleaned
        
        return ""
    
    def _extract_weather(self, description: str) -> str:
        """从描述中提取天气信息"""
        weather_keywords = [
            "晴天", "阴天", "雨天", "雪天", "雾天", "大风", "微风",
            "阳光", "月光", "星光", "灯光", "霓虹灯"
        ]
        
        for keyword in weather_keywords:
            if keyword in description:
                return keyword
        
        return ""
    
    def _translate_to_english(self, text: str) -> str:
        """中文到英文翻译（支持 LLM 辅助）"""
        if not text or not text.strip():
            return text
        
        # 如果启用 LLM 且文本较长或不在字典中，使用 LLM 翻译
        if self.use_llm and self.llm_service and (len(text) > 5 or text not in self._get_basic_translations()):
            try:
                return self._translate_with_llm(text)
            except Exception:
                # LLM 翻译失败，回退到字典
                pass
        
        # 规则处理（字典映射）
        translations = self._get_basic_translations()
        return translations.get(text, text)
    
    def _get_basic_translations(self) -> Dict[str, str]:
        """获取基础翻译字典（扩展版）"""
        return {
            # 基础动作
            "坐": "sitting", "站": "standing", "走": "walking", "跑": "running",
            "看": "looking", "说": "speaking", "笑": "smiling", "哭": "crying",
            "转身": "turning", "抬头": "looking up", "低头": "looking down",
            "蹲": "crouching", "跪": "kneeling", "躺": "lying", "趴": "lying face down",
            "靠": "leaning", "倚": "leaning against", "弯腰": "bending over",
            "挺胸": "chest out", "侧身": "sideways", "转身": "turning around",
            "推": "pushing", "拉": "pulling", "拿": "holding", "放": "placing",
            "举": "raising", "握": "gripping", "抓": "grabbing", "扔": "throwing",
            "踢": "kicking", "跳": "jumping", "进入": "entering", "离开": "leaving",
            "靠近": "approaching", "远离": "moving away", "跟随": "following",
            "追逐": "chasing", "躲避": "avoiding", "环顾": "looking around",
            "张望": "peering", "凝视": "gazing", "注视": "staring", "扫视": "scanning",
            "瞥见": "glimpsing", "点头": "nodding", "摇头": "shaking head",
            "挥手": "waving", "摆手": "gesturing", "指向": "pointing",
            "蹲下": "squatting", "站起": "standing up", "躺下": "lying down",
            "趴下": "lying face down", "跪下": "kneeling", "弯腰": "bending",
            "拥抱": "hugging", "握手": "shaking hands", "拍": "patting",
            "打": "hitting", "推门": "pushing door", "开门": "opening door",
            "关门": "closing door", "拿起": "picking up", "放下": "putting down",
            "递给": "handing", "接过": "receiving", "翻开": "opening", "合上": "closing",
            
            # 表情和情绪
            "焦虑": "anxious", "紧张": "tense", "轻松": "relaxed", "悲伤": "sad",
            "高兴": "happy", "愤怒": "angry", "疑惑": "confused", "微笑": "smiling",
            "严肃": "serious", "冷漠": "indifferent", "兴奋": "excited", "恐惧": "fearful",
            "惊讶": "surprised", "失望": "disappointed", "满意": "satisfied", "不满": "dissatisfied",
            "痛苦": "painful", "快乐": "joyful", "忧郁": "melancholic", "开朗": "cheerful",
            "疲惫": "tired", "精神": "energetic", "专注": "focused", "分心": "distracted",
            "面无表情": "expressionless", "眉头紧锁": "frowning", "嘴角上扬": "smiling",
            "眼神坚定": "determined eyes", "眼神闪烁": "shifty eyes", "如释重负": "relieved",
            "愁眉苦脸": "worried", "喜笑颜开": "beaming", "怒目而视": "glaring",
            
            # 姿势相关
            "双手叉腰": "hands on hips", "双手抱胸": "arms crossed", "双手背后": "hands behind back",
            "单手扶墙": "one hand on wall", "双腿交叉": "legs crossed", "单腿站立": "standing on one leg",
            "盘腿": "cross-legged", "翘腿": "legs crossed", "身体前倾": "leaning forward",
            "身体后仰": "leaning back", "肩膀下垂": "shoulders drooping", "肩膀高耸": "shoulders raised",
            "双手撑膝": "hands on knees", "双手撑地": "hands on ground", "握拳": "clenched fists",
            "自然站立": "standing naturally", "双手自然下垂": "arms hanging naturally",
            
            # 服装相关
            "西装": "suit", "衬衫": "shirt", "T恤": "T-shirt", "裙子": "skirt",
            "裤子": "pants", "外套": "jacket", "大衣": "coat", "风衣": "trench coat",
            "制服": "uniform", "工作服": "work clothes", "运动服": "sportswear",
            "休闲服": "casual wear", "正装": "formal wear", "便装": "casual clothes",
            
            # 场景和环境
            "宽敞": "spacious", "狭窄": "narrow", "明亮": "bright", "昏暗": "dim",
            "整洁": "tidy", "凌乱": "messy", "安静": "quiet", "嘈杂": "noisy",
            "现代": "modern", "古典": "classical", "豪华": "luxurious", "简陋": "simple",
            "温馨": "cozy", "冷清": "desolate", "热闹": "lively", "空旷": "empty",
            
            # 时间和天气
            "白天": "daytime", "夜晚": "night", "黄昏": "dusk", "黎明": "dawn",
            "中午": "noon", "下午": "afternoon", "早晨": "morning", "傍晚": "evening",
            "晴天": "sunny", "雨天": "rainy", "阴天": "cloudy", "雪天": "snowy",
            "大风": "windy", "雾天": "foggy", "雷雨": "thunderstorm",
            
            # 通用词汇
            "动作": "action", "自然表情": "natural expression", "人物": "character",
            "主角": "protagonist", "角色": "character", "场景": "scene", "环境": "environment",
            "背景": "background", "地点": "location", "氛围": "atmosphere", "情绪": "emotion",
            "表情": "expression", "姿势": "pose", "服装": "clothing", "道具": "props",
            "特写": "close-up", "中景": "medium shot", "远景": "wide shot", "全景": "full shot",
            "镜头": "shot", "画面": "frame", "构图": "composition", "光影": "lighting",
            "色彩": "color", "色调": "tone", "质感": "texture", "风格": "style"
        }
    
    def _translate_focal_length(self, focal: str) -> str:
        """翻译镜头焦段"""
        translations = {
            "超广角(14-24mm)": "ultra wide angle 14-24mm",
            "广角(24-35mm)": "wide angle 24-35mm",
            "标准(35-50mm)": "standard 35-50mm",
            "中焦(50-85mm)": "medium telephoto 50-85mm",
            "长焦(85-200mm)": "telephoto 85-200mm",
            "超长焦(200mm+)": "super telephoto 200mm+"
        }
        return translations.get(focal, focal)
