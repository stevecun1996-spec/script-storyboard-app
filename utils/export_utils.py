"""
导出工具模块（简化版）
"""

import os
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any

class ExportUtils:
    """导出工具类"""
    
    def export_to_excel(self, scenes: List[Dict[str, Any]], script: str) -> str:
        """
        导出分镜头到Excel文件
        
        Args:
            scenes: 分镜头列表
            script: 原始剧本
        
        Returns:
            str: 导出文件路径
        """
        # 准备数据
        data = []
        for i, scene in enumerate(scenes):
            # 优先使用独立字段（新格式）
            shot_size = scene.get("shot_size", "")
            camera_angle = scene.get("camera_angle", "")
            camera_movement = scene.get("camera_movement", "")
            camera_equipment = scene.get("camera_equipment", "")
            lens_focal = scene.get("lens_focal_length", "")
            
            # 兼容旧格式：如果字段为空，尝试从组合格式解析
            if not shot_size:
                camera_angle_full = scene.get("camera_angle", "")
                if "/" in str(camera_angle_full) and len(str(camera_angle_full).split("/")) == 5:
                    angle_parts = str(camera_angle_full).split("/")
                    shot_size = angle_parts[0]
                    camera_angle = angle_parts[1]
                    camera_movement = angle_parts[2]
                    camera_equipment = angle_parts[3]
                    lens_focal = angle_parts[4]
                else:
                    # 默认值
                    shot_size = "中景"
                    camera_angle = "视平"
                    camera_movement = "固定"
                    camera_equipment = "固定"
                    lens_focal = "标准(35-50mm)"
            
            # 获取相机、镜头、光圈参数，如果为空则使用默认值
            camera = scene.get("camera", "")
            if not camera:
                camera = "ARRI Alexa"  # 默认值
            
            lens = scene.get("lens", "")
            if not lens:
                lens = "ARRI Master Primes"  # 默认值
            
            aperture = scene.get("aperture", "")
            if not aperture:
                aperture = "f/2.8"  # 默认值
            
            # 获取新增的特殊场景字段
            scene_type = scene.get("scene_type", "普通")
            composition_tension = scene.get("composition_tension", "")
            axis_crossing = scene.get("axis_crossing", "")
            shot_transition = scene.get("shot_transition", "")
            aesthetics_technique = scene.get("aesthetics_technique", "")
            # 获取新增的创作维度字段
            protagonist_type = scene.get("protagonist_type", "")
            emotion_design = scene.get("emotion_design", "")
            performance_style = scene.get("performance_style", "")
            
            row = {
                "序号": scene.get("scene_number", i + 1),
                "分镜描述": scene.get("scene_description", ""),
                "景别": shot_size,
                "摄影机角度": camera_angle,
                "运镜": camera_movement,
                "摄影机装备": camera_equipment,
                "镜头焦段": lens_focal,
                "相机": camera,
                "镜头": lens,
                "光圈": aperture,
                "场景类型": scene_type,
                "构图张力": composition_tension,
                "轴线处理": axis_crossing,
                "镜头衔接": shot_transition,
                "审美技法": aesthetics_technique,
                "主角核心表达": protagonist_type,
                "情绪设计": emotion_design,
                "表演风格": performance_style,
                "人物": ", ".join(scene.get("characters", [])),
                "地点": scene.get("location", ""),
                "时间": scene.get("time", ""),
                "情绪": scene.get("mood", ""),
                "台词": scene.get("dialogue_text", ""),
                "旁白": scene.get("voiceover_text", ""),
                "音效": scene.get("sound_effects", "")
            }
            data.append(row)
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 确保列的顺序（将相机、镜头、光圈放在镜头焦段后面，特殊场景字段放在光圈后面，创作维度字段放在特殊场景字段后面）
        column_order = [
            "序号", "分镜描述", "景别", "摄影机角度", "运镜", "摄影机装备", 
            "镜头焦段", "相机", "镜头", "光圈",
            "场景类型", "构图张力", "轴线处理", "镜头衔接", "审美技法",
            "主角核心表达", "情绪设计", "表演风格",
            "人物", "地点", "时间", "情绪", "台词", "旁白", "音效"
        ]
        # 只保留实际存在的列
        column_order = [col for col in column_order if col in df.columns]
        # 添加其他可能存在的列
        other_cols = [col for col in df.columns if col not in column_order]
        df = df[column_order + other_cols]
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"分镜头脚本_{timestamp}.xlsx"
        filepath = os.path.join(desktop, filename)
        
        # 导出Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 写入分镜头表
            df.to_excel(writer, sheet_name='分镜头', index=False)
            
            # 写入原始剧本
            script_df = pd.DataFrame({"原始剧本": [script]})
            script_df.to_excel(writer, sheet_name='原始剧本', index=False)
        
        return filepath
    
    def export_to_excel_with_prompts(self, scenes: List[Dict[str, Any]], prompts: List[Dict[str, Any]], script: str) -> str:
        """
        导出分镜头到Excel文件（包含提示词）
        
        Args:
            scenes: 分镜头列表
            prompts: 提示词列表
            script: 原始剧本
        
        Returns:
            str: 导出文件路径
        """
        # 创建提示词映射（按scene_number）
        prompt_map = {p.get("scene_number", 0): p for p in prompts}
        
        # 准备数据
        data = []
        for i, scene in enumerate(scenes):
            scene_num = scene.get("scene_number", i + 1)
            
            # 优先使用独立字段（新格式）
            shot_size = scene.get("shot_size", "")
            camera_angle = scene.get("camera_angle", "")
            camera_movement = scene.get("camera_movement", "")
            camera_equipment = scene.get("camera_equipment", "")
            lens_focal = scene.get("lens_focal_length", "")
            
            # 兼容旧格式
            if not shot_size:
                camera_angle_full = scene.get("camera_angle", "")
                if "/" in str(camera_angle_full) and len(str(camera_angle_full).split("/")) == 5:
                    angle_parts = str(camera_angle_full).split("/")
                    shot_size = angle_parts[0]
                    camera_angle = angle_parts[1]
                    camera_movement = angle_parts[2]
                    camera_equipment = angle_parts[3]
                    lens_focal = angle_parts[4]
                else:
                    shot_size = "中景"
                    camera_angle = "视平"
                    camera_movement = "固定"
                    camera_equipment = "固定"
                    lens_focal = "标准(35-50mm)"
            
            # 获取相机、镜头、光圈参数
            camera = scene.get("camera", "ARRI Alexa")
            lens = scene.get("lens", "ARRI Master Primes")
            aperture = scene.get("aperture", "f/2.8")
            
            # 获取新增的特殊场景字段
            scene_type = scene.get("scene_type", "普通")
            composition_tension = scene.get("composition_tension", "")
            axis_crossing = scene.get("axis_crossing", "")
            shot_transition = scene.get("shot_transition", "")
            aesthetics_technique = scene.get("aesthetics_technique", "")
            # 获取新增的创作维度字段
            protagonist_type = scene.get("protagonist_type", "")
            emotion_design = scene.get("emotion_design", "")
            performance_style = scene.get("performance_style", "")
            
            # 获取对应的提示词
            prompt_data = prompt_map.get(scene_num, {})
            prompt_text = prompt_data.get("prompt_text", "")
            negative_prompt = prompt_data.get("negative_prompt", "")
            prompt_json = prompt_data.get("prompt_json", {})
            
            # 格式化JSON为字符串
            import json
            prompt_json_str = json.dumps(prompt_json, ensure_ascii=False, indent=2) if prompt_json else ""
            
            row = {
                "序号": scene_num,
                "分镜描述": scene.get("scene_description", ""),
                "景别": shot_size,
                "摄影机角度": camera_angle,
                "运镜": camera_movement,
                "摄影机装备": camera_equipment,
                "镜头焦段": lens_focal,
                "相机": camera,
                "镜头": lens,
                "光圈": aperture,
                "场景类型": scene_type,
                "构图张力": composition_tension,
                "轴线处理": axis_crossing,
                "镜头衔接": shot_transition,
                "审美技法": aesthetics_technique,
                "主角核心表达": protagonist_type,
                "情绪设计": emotion_design,
                "表演风格": performance_style,
                "人物": ", ".join(scene.get("characters", [])),
                "地点": scene.get("location", ""),
                "时间": scene.get("time", ""),
                "情绪": scene.get("mood", ""),
                "台词": scene.get("dialogue_text", ""),
                "旁白": scene.get("voiceover_text", ""),
                "音效": scene.get("sound_effects", ""),
                "提示词（文本）": prompt_text,
                "负面提示词": negative_prompt,
                "提示词（JSON）": prompt_json_str
            }
            data.append(row)
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 确保列的顺序（特殊场景字段放在光圈后面，创作维度字段放在特殊场景字段后面）
        column_order = [
            "序号", "分镜描述", "景别", "摄影机角度", "运镜", "摄影机装备", 
            "镜头焦段", "相机", "镜头", "光圈",
            "场景类型", "构图张力", "轴线处理", "镜头衔接", "审美技法",
            "主角核心表达", "情绪设计", "表演风格",
            "人物", "地点", "时间", "情绪", "台词", "旁白", "音效",
            "提示词（文本）", "负面提示词", "提示词（JSON）"
        ]
        column_order = [col for col in column_order if col in df.columns]
        other_cols = [col for col in df.columns if col not in column_order]
        df = df[column_order + other_cols]
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"分镜头脚本_含提示词_{timestamp}.xlsx"
        filepath = os.path.join(desktop, filename)
        
        # 导出Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 写入分镜头表
            df.to_excel(writer, sheet_name='分镜头', index=False)
            
            # 写入原始剧本
            script_df = pd.DataFrame({"原始剧本": [script]})
            script_df.to_excel(writer, sheet_name='原始剧本', index=False)
        
        return filepath

