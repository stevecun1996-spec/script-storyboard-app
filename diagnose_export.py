#!/usr/bin/env python3
"""
详细诊断导出功能
检查实际导出的Excel文件内容
"""

import os
import sys
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scene_parser import SceneParser
from utils.export_utils import ExportUtils

def diagnose_export():
    """详细诊断导出功能"""
    print("=" * 80)
    print("导出功能详细诊断")
    print("=" * 80)
    
    # 创建测试数据
    test_scenes = [
        {
            "scene_number": 1,
            "scene_description": "诊断测试分镜1",
            "shot_size": "中景",
            "camera_angle": "视平",
            "camera_movement": "固定",
            "camera_equipment": "固定",
            "lens_focal_length": "标准(35-50mm)",
            "characters": ["测试人物"],
            "location": "测试地点",
            "time": "下午",
            "mood": "测试情绪",
            "dialogue_text": "测试台词",
            "voiceover_text": "测试旁白",
            "sound_effects": "测试音效"
        }
    ]
    
    # 检查解析器
    print("\n【步骤1】检查场景解析器")
    print("-" * 80)
    parser = SceneParser()
    validated = parser.validate_scenes(test_scenes)
    
    scene = validated[0]
    print(f"解析后的场景字段:")
    print(f"  scene_number: {scene.get('scene_number')}")
    print(f"  scene_description: {scene.get('scene_description')}")
    print(f"  shot_size: {scene.get('shot_size')}")
    print(f"  camera_angle: {scene.get('camera_angle')}")
    print(f"  camera_movement: {scene.get('camera_movement')}")
    print(f"  camera_equipment: {scene.get('camera_equipment')}")
    print(f"  lens_focal_length: {scene.get('lens_focal_length')}")
    
    # 检查导出工具
    print(f"\n【步骤2】检查导出工具")
    print("-" * 80)
    export_utils = ExportUtils()
    
    # 检查导出工具的方法
    print(f"导出工具类: {type(export_utils)}")
    print(f"导出方法存在: {hasattr(export_utils, 'export_to_excel')}")
    
    # 执行导出
    print(f"\n【步骤3】执行导出")
    print("-" * 80)
    filepath = export_utils.export_to_excel(validated, "诊断测试剧本")
    print(f"导出文件路径: {filepath}")
    print(f"文件存在: {os.path.exists(filepath)}")
    
    if not os.path.exists(filepath):
        print("❌ 导出文件不存在！")
        return False
    
    # 读取Excel文件
    print(f"\n【步骤4】读取Excel文件")
    print("-" * 80)
    try:
        df = pd.read_excel(filepath, sheet_name='分镜头')
        print(f"✅ 成功读取Excel文件")
        print(f"行数: {len(df)}")
        print(f"列数: {len(df.columns)}")
    except Exception as e:
        print(f"❌ 读取Excel文件失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # 详细检查列
    print(f"\n【步骤5】详细检查列")
    print("-" * 80)
    print(f"所有列名 ({len(df.columns)} 列):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. '{col}'")
    
    # 检查必需字段
    print(f"\n【步骤6】检查必需字段")
    print("-" * 80)
    required_fields = {
        '景别': 'shot_size',
        '摄影机角度': 'camera_angle',
        '运镜': 'camera_movement',
        '摄影机装备': 'camera_equipment',
        '镜头焦段': 'lens_focal_length'
    }
    
    all_ok = True
    for export_name, scene_key in required_fields.items():
        if export_name in df.columns:
            value = df.iloc[0][export_name]
            expected = scene.get(scene_key, '')
            status = "✅" if str(value) == str(expected) else "⚠️"
            print(f"  {status} {export_name:15s}: '{value}' (期望: '{expected}')")
        else:
            print(f"  ❌ {export_name:15s}: 缺失")
            all_ok = False
    
    # 检查数据内容
    print(f"\n【步骤7】检查第一行完整数据")
    print("-" * 80)
    for col in df.columns:
        value = df.iloc[0][col]
        if pd.isna(value):
            value = "(空)"
        print(f"  {col:15s}: {value}")
    
    # 检查是否有旧字段
    print(f"\n【步骤8】检查是否有旧字段")
    print("-" * 80)
    old_fields = ['镜头角度']
    for field in old_fields:
        if field in df.columns:
            print(f"  ⚠️  发现旧字段: '{field}'")
        else:
            print(f"  ✅ 未发现旧字段: '{field}'")
    
    print(f"\n" + "=" * 80)
    if all_ok:
        print("✅ 诊断完成：所有字段都正确导出")
    else:
        print("❌ 诊断完成：发现问题，请检查上述输出")
    print("=" * 80)
    
    # 保留文件供用户检查
    print(f"\n导出文件已保存，请手动检查: {filepath}")
    
    return all_ok

if __name__ == "__main__":
    try:
        success = diagnose_export()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 诊断程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

