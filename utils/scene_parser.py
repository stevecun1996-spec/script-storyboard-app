"""
分镜头解析工具（简化版）
"""

from typing import List, Dict, Any

class SceneParser:
    """分镜头解析器"""
    
    def __init__(self):
        # 保留旧格式兼容性
        self.valid_camera_angles = ["特写", "近景", "中景", "远景", "全景", "俯视", "仰视", "平视"]
        # 新的景别选项
        self.valid_shot_sizes = ["大远景", "远景", "全景", "中景", "中近景", "近景", "特写", "大特写"]
        # 新的摄影机角度选项
        self.valid_camera_angles_new = ["视平", "高位俯拍", "低位仰拍", "斜拍", "越肩", "鸟瞰"]
        # 运镜选项
        self.valid_camera_movements = ["固定", "横移", "俯仰", "横摇", "升降", "轨道推拉", "变焦推拉", "正跟随", "倒跟随", "环绕", "滑轨横移"]
        # 摄影机装备选项
        self.valid_camera_equipments = ["固定", "轨道", "手持", "稳定器", "摇臂", "航拍"]
        # 镜头焦段选项
        self.valid_lens_focals = ["超广角(14-24mm)", "广角(24-35mm)", "标准(35-50mm)", "中焦(50-85mm)", "长焦(85-200mm)", "超长焦(200mm+)"]
        # 相机选项（必选）
        self.valid_cameras = ["ARRI Alexa", "ARRI Alexa 65", "Arriflex 416", "IMAX 70mm", "Kodak Portra 400", "Kodak Vision3 500T", "Panavision Panaflex", "RED Monstro 8K", "Sony Venice", "Cinestill 800T"]
        # 镜头选项（必选）
        self.valid_lenses = ["ARRI Master Primes", "ARRI Master Prime Macro", "Canon K35", "Cooke Anamorphic", "Helios 44-2", "Panavision C-Series Anamorphic", "Petzval Lens"]
        # 光圈选项（必选）
        self.valid_apertures = ["f/1.2", "f/1.4", "f/2.0", "f/2.2", "f/2.8", "f/4.0", "f/5.6", "f/11"]
        # 场景类型选项
        self.valid_scene_types = ["普通", "武戏打斗", "对峙", "追逐", "大招释放", "收尾"]
        # 构图张力选项
        self.valid_composition_tensions = ["饱满", "丰富", "引导", "饱满+引导", "丰富+引导", "饱满+丰富", "饱满+丰富+引导"]
        # 轴线处理选项
        self.valid_axis_crossings = ["维持轴线", "合理越轴", "故意越轴"]
        # 镜头衔接选项
        self.valid_shot_transitions = ["流畅型衔接", "节奏型衔接", "意义型衔接", "流畅型+节奏型", "流畅型+意义型", "节奏型+意义型", "流畅型+节奏型+意义型"]
        # 审美技法选项（可以多选，用逗号分隔）
        self.valid_aesthetics_techniques = ["对比", "排比", "夸张", "组合", "移时", "奇解", "精细"]
        # 主角核心表达选项
        self.valid_protagonist_types = ["情感共鸣型", "价值观载体型", "成长弧光型", "观察者/催化剂型"]
        # 情绪设计选项
        self.valid_emotion_designs = ["情绪一致", "情绪错位", "情绪叠加", "情绪反转"]
        # 表演风格选项
        self.valid_performance_styles = ["内敛表演", "外放表演", "反差表演", "细节表演"]
        self.valid_times = ["白天", "夜晚", "黄昏", "黎明", "中午", "下午"]
    
    def validate_scenes(self, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        验证和规范化分镜头数据
        
        Args:
            scenes: 原始分镜头列表
        
        Returns:
            List[Dict]: 验证后的分镜头列表
        """
        if not isinstance(scenes, list):
            raise ValueError("分镜头数据应该是列表格式")
        
        validated_scenes = []
        
        for i, scene in enumerate(scenes):
            # 处理独立字段（新格式）
            shot_size = self._normalize_value(
                scene.get("shot_size", ""),
                self.valid_shot_sizes,
                "中景"
            )
            camera_angle = self._normalize_value(
                scene.get("camera_angle", ""),
                self.valid_camera_angles_new,
                "视平"
            )
            camera_movement = self._normalize_value(
                scene.get("camera_movement", ""),
                self.valid_camera_movements,
                "固定"
            )
            camera_equipment = self._normalize_value(
                scene.get("camera_equipment", ""),
                self.valid_camera_equipments,
                "固定"
            )
            lens_focal_length = self._normalize_value(
                scene.get("lens_focal_length", ""),
                self.valid_lens_focals,
                "标准(35-50mm)"
            )
            
            # 相机、镜头、光圈（必选字段）
            camera = self._normalize_value(
                scene.get("camera", ""),
                self.valid_cameras,
                "ARRI Alexa"
            )
            lens = self._normalize_value(
                scene.get("lens", ""),
                self.valid_lenses,
                "ARRI Master Primes"
            )
            aperture = self._normalize_value(
                scene.get("aperture", ""),
                self.valid_apertures,
                "f/2.8"
            )
            
            # 兼容旧格式：如果提供了组合格式的 camera_angle，尝试解析
            camera_angle_raw = scene.get("camera_angle", "")
            if "/" in str(camera_angle_raw) and len(str(camera_angle_raw).split("/")) == 5:
                parts = str(camera_angle_raw).split("/")
                shot_size = self._normalize_value(parts[0], self.valid_shot_sizes, "中景")
                camera_angle = self._normalize_value(parts[1], self.valid_camera_angles_new, "视平")
                camera_movement = self._normalize_value(parts[2], self.valid_camera_movements, "固定")
                camera_equipment = self._normalize_value(parts[3], self.valid_camera_equipments, "固定")
                lens_focal_length = self._normalize_value(parts[4], self.valid_lens_focals, "标准(35-50mm)")
            # 兼容更旧的格式：单个 camera_angle 值
            elif camera_angle_raw and camera_angle_raw not in self.valid_camera_angles_new and camera_angle_raw in self.valid_camera_angles:
                shot_size_map = {
                    "特写": "特写", "近景": "近景", "中景": "中景", 
                    "远景": "远景", "全景": "全景"
                }
                shot_size = shot_size_map.get(camera_angle_raw, "中景")
                camera_angle = "视平"
            
            # 验证新增的特殊场景字段
            scene_type = self._normalize_value(
                scene.get("scene_type", "普通"),
                self.valid_scene_types,
                "普通"
            )
            composition_tension = self._normalize_value(
                scene.get("composition_tension", "引导"),
                self.valid_composition_tensions,
                "引导"
            )
            axis_crossing = self._normalize_value(
                scene.get("axis_crossing", "维持轴线"),
                self.valid_axis_crossings,
                "维持轴线"
            )
            shot_transition = self._normalize_value(
                scene.get("shot_transition", "流畅型衔接"),
                self.valid_shot_transitions,
                "流畅型衔接"
            )
            # 验证新增的创作维度字段
            protagonist_type = self._normalize_value(
                scene.get("protagonist_type", ""),
                self.valid_protagonist_types,
                ""
            )
            emotion_design = self._normalize_value(
                scene.get("emotion_design", ""),
                self.valid_emotion_designs,
                ""
            )
            performance_style = self._normalize_value(
                scene.get("performance_style", ""),
                self.valid_performance_styles,
                ""
            )
            # 审美技法可以多选，验证每个技法是否有效
            aesthetics_technique_raw = scene.get("aesthetics_technique", "精细")
            if isinstance(aesthetics_technique_raw, str):
                # 如果是字符串，可能是逗号分隔的多个技法
                techniques = [t.strip() for t in aesthetics_technique_raw.split(",")]
                valid_techniques = [t for t in techniques if t in self.valid_aesthetics_techniques]
                aesthetics_technique = ",".join(valid_techniques) if valid_techniques else "精细"
            else:
                aesthetics_technique = "精细"
            
            validated_scene = {
                "scene_number": i + 1,
                "scene_description": scene.get("scene_description", f"分镜头 {i + 1}"),
                "shot_size": shot_size,
                "camera_angle": camera_angle,
                "camera_movement": camera_movement,
                "camera_equipment": camera_equipment,
                "lens_focal_length": lens_focal_length,
                "camera": camera,
                "lens": lens,
                "aperture": aperture,
                "characters": scene.get("characters", []) if isinstance(scene.get("characters"), list) else [],
                "location": scene.get("location", "未知"),
                "time": self._normalize_value(
                    scene.get("time", "白天"),
                    self.valid_times,
                    "白天"
                ),
                "mood": scene.get("mood", "中性"),
                "dialogue_text": scene.get("dialogue_text", ""),
                "voiceover_text": scene.get("voiceover_text", ""),
                "sound_effects": scene.get("sound_effects", ""),
                # 新增的特殊场景字段
                "scene_type": scene_type,
                "composition_tension": composition_tension,
                "axis_crossing": axis_crossing,
                "shot_transition": shot_transition,
                "aesthetics_technique": aesthetics_technique,
                # 新增的创作维度字段
                "protagonist_type": protagonist_type,
                "emotion_design": emotion_design,
                "performance_style": performance_style
            }
            
            # 保留其他可选的创作指导字段（如果AI生成了这些字段，保留它们但不强制要求）
            optional_fields = [
                "fight_scene_type", "confrontation_type", "chase_type",
                "ultimate_skill_stage", "ending_type"
            ]
            for field in optional_fields:
                if field in scene:
                    validated_scene[field] = scene[field]
            
            validated_scenes.append(validated_scene)
        
        return validated_scenes
    
    def _normalize_value(self, value: str, valid_options: List[str], default: str) -> str:
        """规范化值"""
        if not value:
            return default
        
        # 如果在有效选项中
        if value in valid_options:
            return value
        
        # 尝试匹配
        for option in valid_options:
            if option in value:
                return option
        
        return default

