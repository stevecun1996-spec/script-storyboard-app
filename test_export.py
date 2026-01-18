#!/usr/bin/env python3
"""
导出功能自检程序
检查所有新字段是否正确导出到Excel
"""

import os
import sys
import pandas as pd
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_parser import SceneParser
from utils.export_utils import ExportUtils

def test_export():
    """测试导出功能"""
    print("=" * 80)
    print("导出功能自检程序")
    print("=" * 80)
    
    # 测试数据1：新格式（独立字段）
    print("\n【测试1】新格式数据（独立字段）")
    print("-" * 80)
    test_scenes_new = [
        {
            "scene_number": 1,
            "scene_description": "测试分镜1 - 新格式",
            "shot_size": "中景",
            "camera_angle": "视平",
            "camera_movement": "固定",
            "camera_equipment": "固定",
            "lens_focal_length": "标准(35-50mm)",
            "characters": ["小明"],
            "location": "咖啡馆",
            "time": "下午",
            "mood": "焦虑",
            "dialogue_text": "",
            "voiceover_text": "",
            "sound_effects": "背景音乐"
        },
        {
            "scene_number": 2,
            "scene_description": "测试分镜2 - 特写",
            "shot_size": "特写",
            "camera_angle": "高位俯拍",
            "camera_movement": "横移",
            "camera_equipment": "稳定器",
            "lens_focal_length": "中焦(50-85mm)",
            "characters": ["小红"],
            "location": "室外",
            "time": "白天",
            "mood": "紧张",
            "dialogue_text": "小红：你好",
            "voiceover_text": "",
            "sound_effects": "脚步声"
        }
    ]
    
    # 通过解析器处理
    parser = SceneParser()
    validated = parser.validate_scenes(test_scenes_new)
    
    print(f"解析后的场景数量: {len(validated)}")
    print(f"\n第一个场景的字段:")
    scene1 = validated[0]
    required_fields = ['shot_size', 'camera_angle', 'camera_movement', 'camera_equipment', 'lens_focal_length']
    for field in required_fields:
        value = scene1.get(field, "❌ 缺失")
        print(f"  {field:20s}: {value}")
    
    # 导出
    export_utils = ExportUtils()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_file = f"/tmp/test_export_{timestamp}.xlsx"
    filepath = export_utils.export_to_excel(validated, "测试剧本内容")
    
    print(f"\n✅ 导出文件: {filepath}")
    
    # 读取并检查
    try:
        df = pd.read_excel(filepath, sheet_name='分镜头')
        print(f"\n导出的列数: {len(df.columns)}")
        print(f"\n所有列名:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # 检查必需字段
        print(f"\n【字段检查】")
        print("-" * 80)
        required_export_fields = ['景别', '摄影机角度', '运镜', '摄影机装备', '镜头焦段']
        all_present = True
        missing_fields = []
        
        for field in required_export_fields:
            if field in df.columns:
                print(f"  ✅ {field:15s}: 存在")
            else:
                print(f"  ❌ {field:15s}: 缺失")
                all_present = False
                missing_fields.append(field)
        
        if all_present:
            print(f"\n✅ 所有新字段都已正确导出！")
            print(f"\n【数据示例】")
            print("-" * 80)
            print(f"第一行数据:")
            for field in required_export_fields:
                value = df.iloc[0][field]
                print(f"  {field:15s}: {value}")
            
            print(f"\n第二行数据:")
            if len(df) > 1:
                for field in required_export_fields:
                    value = df.iloc[1][field]
                    print(f"  {field:15s}: {value}")
        else:
            print(f"\n❌ 以下字段缺失: {', '.join(missing_fields)}")
            print(f"\n请检查 export_utils.py 中的导出逻辑")
        
        # 检查是否有旧的"镜头角度"列
        if "镜头角度" in df.columns:
            print(f"\n⚠️  警告: 发现旧的'镜头角度'列，应该已被新字段替代")
        
    except Exception as e:
        print(f"\n❌ 读取Excel文件时出错: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 测试2：旧格式（组合格式）
    print(f"\n\n【测试2】旧格式数据（组合格式，兼容性测试）")
    print("-" * 80)
    test_scenes_old = [
        {
            "scene_number": 1,
            "scene_description": "测试分镜 - 旧格式",
            "camera_angle": "中景/视平/固定/固定/标准(35-50mm)",  # 组合格式
            "characters": ["小明"],
            "location": "咖啡馆",
            "time": "下午",
            "mood": "焦虑",
            "dialogue_text": "",
            "voiceover_text": "",
            "sound_effects": "背景音乐"
        }
    ]
    
    validated_old = parser.validate_scenes(test_scenes_old)
    filepath_old = export_utils.export_to_excel(validated_old, "测试剧本内容（旧格式）")
    
    print(f"✅ 导出文件: {filepath_old}")
    
    try:
        df_old = pd.read_excel(filepath_old, sheet_name='分镜头')
        print(f"\n旧格式转换后的列:")
        for i, col in enumerate(df_old.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # 检查是否成功转换
        all_old_present = all(field in df_old.columns for field in required_export_fields)
        if all_old_present:
            print(f"\n✅ 旧格式已成功转换为新格式")
        else:
            print(f"\n❌ 旧格式转换失败")
        
        os.remove(filepath_old)
    except Exception as e:
        print(f"\n❌ 读取旧格式文件时出错: {str(e)}")
    
    print(f"\n" + "=" * 80)
    print("自检完成")
    print("=" * 80)
    
    return all_present

if __name__ == "__main__":
    try:
        success = test_export()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 自检程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

