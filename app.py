"""
剧本分镜生成系统 - 简化版
核心功能：剧本输入 → 分镜划分 → 编辑 → 导出
"""

import streamlit as st
import pandas as pd
import copy
from typing import List, Dict, Any
from pathlib import Path

# 导入模块
from config.llm_config import get_available_brands, get_models_by_brand
from config.prompts import get_scene_division_prompt
from services.llm_service import LLMService
from utils.scene_parser import SceneParser
from utils.export_utils import ExportUtils
from utils.prompt_generator import ImagePromptGenerator
from utils.project_manager import ProjectManager

# 页面配置
st.set_page_config(
    page_title="剧本分镜生成系统（简化版）",
    page_icon="🎬",
    layout="wide"
)

# 可选：添加简单的密码验证（如需小范围分享，取消下面的注释）
# import os
# 
# # 获取密码：优先从 Streamlit Cloud Secrets 获取，其次从环境变量获取
# def get_secret(key: str, default: str = ""):
#     """获取配置值，优先从 st.secrets 获取，其次从环境变量"""
#     try:
#         # 尝试从 Streamlit Cloud Secrets 获取
#         return st.secrets.get(key, default)
#     except (AttributeError, KeyError, FileNotFoundError):
#         # 如果不在 Streamlit Cloud 或 secrets 不存在，使用环境变量
#         return os.environ.get(key, default)
# 
# PASSWORD = get_secret("APP_PASSWORD", "")  # 在 Streamlit Cloud Secrets 中设置
# 
# if PASSWORD:  # 只有在设置了密码时才启用验证
#     if "authenticated" not in st.session_state:
#         st.session_state.authenticated = False
#     
#     if not st.session_state.authenticated:
#         st.title("🔒 访问验证")
#         st.info("请输入访问密码以继续")
#         password_input = st.text_input("访问密码", type="password", key="password_input")
#         if st.button("确认", type="primary"):
#             if password_input == PASSWORD:
#                 st.session_state.authenticated = True
#                 st.rerun()
#             else:
#                 st.error("❌ 密码错误，请重试")
#         st.stop()

# 初始化服务
@st.cache_resource
def init_services():
    """初始化服务"""
    return {
        "llm_service": LLMService(),
        "scene_parser": SceneParser(),
        "export_utils": ExportUtils(),
        "project_manager": ProjectManager()
    }

# 初始化会话状态
def init_session_state():
    """初始化会话状态"""
    if "script" not in st.session_state:
        st.session_state.script = ""
    if "scenes" not in st.session_state:
        st.session_state.scenes = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    if "fetched_models" not in st.session_state:
        st.session_state.fetched_models = {}
    if "image_prompts" not in st.session_state:
        st.session_state.image_prompts = []
    if "prompt_config" not in st.session_state:
        st.session_state.prompt_config = {
            "language": "bilingual",
            "detail_level": "standard",
            "include_technical": True,
            "include_mood": True,
            "include_characters": True,
            "use_llm": False  # 默认不启用 LLM，用户可选择启用
        }
    if "current_project" not in st.session_state:
        st.session_state.current_project = None  # 当前打开的项目文件路径
    if "project_name" not in st.session_state:
        st.session_state.project_name = ""  # 当前项目名称

def render_sidebar():
    """渲染侧边栏配置"""
    st.sidebar.title("🎬 配置设置")
    
    # LLM配置
    st.sidebar.subheader("📝 LLM模型配置")
    brands = get_available_brands()
    selected_brand = st.sidebar.selectbox("选择LLM品牌", brands, key="llm_brand")
    
    # 获取模型列表（优先使用已获取的模型）
    if selected_brand in st.session_state.fetched_models:
        models = st.session_state.fetched_models[selected_brand]
    else:
        models = get_models_by_brand(selected_brand)
    
    models_with_custom = models + ["🔧 自定义模型"]
    selected_model = st.sidebar.selectbox("选择模型", models_with_custom, key="llm_model")
    
    # 自定义模型输入
    if selected_model == "🔧 自定义模型":
        custom_model = st.sidebar.text_input(
            "输入模型名称",
            value=st.session_state.get("custom_model_name", ""),
            placeholder="例如: glm-4-plus, gpt-4o-2024-11-20",
            help="输入完整的模型名称",
            key="custom_model_input"
        )
        final_model = custom_model if custom_model else models[0]
        
        if custom_model:
            st.session_state.custom_model_name = custom_model
            st.sidebar.info(f"📌 当前模型: {custom_model}")
    else:
        final_model = selected_model
    
    api_key = st.sidebar.text_input("API Key", type="password", key="api_key")
    
    # 刷新模型列表按钮（LM Studio可不填key）
    if api_key or selected_brand == "LM Studio":
        if st.sidebar.button("🔄 刷新模型列表", help="从API获取最新可用模型"):
            try:
                with st.spinner("正在获取模型列表..."):
                    services = init_services()
                    fetched_models = services["llm_service"].fetch_available_models(
                        selected_brand, api_key
                    )
                    st.session_state.fetched_models[selected_brand] = fetched_models
                    st.sidebar.success(f"✅ 成功获取 {len(fetched_models)} 个模型")
                    st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ 获取失败: {str(e)}")
                st.sidebar.info("💡 某些品牌可能不支持此功能，请使用自定义模型输入")
    
    # 显示配置状态
    if api_key or selected_brand == "LM Studio":
        st.sidebar.success("✅ 配置完成")
        if selected_model == "🔧 自定义模型" and final_model:
            st.sidebar.caption(f"使用模型: {final_model}")
    else:
        st.sidebar.warning("⚠️ 请输入API Key")
    
    return {
        "brand": selected_brand,
        "model": final_model,
        "api_key": api_key
    }

def render_project_manager(services):
    """渲染项目管理界面"""
    project_manager = services["project_manager"]
    
    st.sidebar.markdown("---")
    st.sidebar.title("📁 项目管理")
    
    # 当前项目信息
    if st.session_state.current_project:
        st.sidebar.success(f"✅ 当前项目：{st.session_state.project_name}")
    else:
        st.sidebar.info("📝 新项目")
    
    # 项目管理选项卡
    tab1, tab2 = st.sidebar.tabs(["💾 保存/加载", "📋 项目管理"])
    
    with tab1:
        # 保存项目
        st.markdown("#### 💾 保存项目")
        project_name_input = st.text_input(
            "项目名称",
            value=st.session_state.project_name or "我的项目",
            key="save_project_name",
            placeholder="输入项目名称"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 保存", key="save_project_btn", use_container_width=True):
                if not project_name_input.strip():
                    st.sidebar.error("请输入项目名称")
                elif not st.session_state.script:
                    st.sidebar.warning("请先输入剧本")
                elif not st.session_state.scenes:
                    st.sidebar.warning("请先生成分镜")
                else:
                    try:
                        filepath = project_manager.save_project(
                            project_name=project_name_input.strip(),
                            script=st.session_state.script,
                            scenes=st.session_state.scenes,
                            image_prompts=st.session_state.image_prompts,
                            metadata={
                                "current_step": st.session_state.current_step,
                                "prompt_config": st.session_state.prompt_config
                            }
                        )
                        st.session_state.current_project = filepath
                        st.session_state.project_name = project_name_input.strip()
                        st.sidebar.success(f"✅ 保存成功！\n{Path(filepath).name}")
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"保存失败：{str(e)}")
        
        with col2:
            if st.session_state.current_project:
                if st.button("🔄 更新", key="update_project_btn", use_container_width=True):
                    try:
                        success = project_manager.update_project(
                            filepath=st.session_state.current_project,
                            script=st.session_state.script,
                            scenes=st.session_state.scenes,
                            image_prompts=st.session_state.image_prompts,
                            metadata={
                                "current_step": st.session_state.current_step,
                                "prompt_config": st.session_state.prompt_config
                            }
                        )
                        if success:
                            st.sidebar.success("✅ 更新成功！")
                            st.rerun()
                        else:
                            st.sidebar.error("更新失败")
                    except Exception as e:
                        st.sidebar.error(f"更新失败：{str(e)}")
        
        st.markdown("---")
        
        # 加载项目
        st.markdown("#### 📂 加载项目")
        projects = project_manager.list_projects()
        
        if projects:
            # 选择项目下拉框
            project_options = [f"{p['project_name']} ({p['scene_count']}个分镜)" for p in projects]
            selected_index = st.selectbox(
                "选择项目",
                options=range(len(projects)),
                format_func=lambda x: project_options[x] if x < len(project_options) else "",
                key="load_project_select"
            )
            
            if selected_index is not None and selected_index < len(projects):
                selected_project = projects[selected_index]
                
                if st.button("📂 加载项目", key="load_project_btn", use_container_width=True):
                    try:
                        project_data = project_manager.load_project(selected_project["filepath"])
                        
                        # 加载数据到 session_state
                        st.session_state.script = project_data.get("script", "")
                        st.session_state.scenes = project_data.get("scenes", [])
                        st.session_state.image_prompts = project_data.get("image_prompts", [])
                        
                        # 恢复元数据
                        metadata = project_data.get("metadata", {})
                        if "current_step" in metadata:
                            st.session_state.current_step = metadata["current_step"]
                        if "prompt_config" in metadata:
                            st.session_state.prompt_config.update(metadata["prompt_config"])
                        
                        # 更新当前项目信息
                        st.session_state.current_project = selected_project["filepath"]
                        st.session_state.project_name = project_data.get("project_name", selected_project["project_name"])
                        
                        st.sidebar.success(f"✅ 加载成功！\n{selected_project['scene_count']}个分镜")
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"加载失败：{str(e)}")
        else:
            st.info("暂无保存的项目")
    
    with tab2:
        # 项目列表和管理
        st.markdown("#### 📋 项目列表")
        projects = project_manager.list_projects()
        
        if projects:
            for i, project in enumerate(projects[:10]):  # 只显示最近10个
                with st.expander(f"📄 {project['project_name']}", expanded=False):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.caption(f"**创建时间：** {project.get('created_at', '')[:19]}")
                        st.caption(f"**修改时间：** {project.get('modified_time', '')[:19]}")
                        st.caption(f"**分镜数：** {project['scene_count']} | **提示词：** {project['prompt_count']} | **字数：** {project['script_length']}")
                    
                    with col2:
                        # 加载按钮
                        if st.button("📂 加载", key=f"quick_load_{i}", use_container_width=True):
                            try:
                                project_data = project_manager.load_project(project["filepath"])
                                st.session_state.script = project_data.get("script", "")
                                st.session_state.scenes = project_data.get("scenes", [])
                                st.session_state.image_prompts = project_data.get("image_prompts", [])
                                metadata = project_data.get("metadata", {})
                                if "current_step" in metadata:
                                    st.session_state.current_step = metadata["current_step"]
                                if "prompt_config" in metadata:
                                    st.session_state.prompt_config.update(metadata["prompt_config"])
                                st.session_state.current_project = project["filepath"]
                                st.session_state.project_name = project_data.get("project_name", project["project_name"])
                                st.sidebar.success("✅ 加载成功！")
                                st.rerun()
                            except Exception as e:
                                st.sidebar.error(f"加载失败：{str(e)}")
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        # 重命名
                        new_name = st.text_input(
                            "重命名",
                            value=project["project_name"],
                            key=f"rename_{i}",
                            label_visibility="collapsed"
                        )
                        if new_name != project["project_name"] and st.button("✏️ 重命名", key=f"rename_btn_{i}", use_container_width=True):
                            try:
                                new_path = project_manager.rename_project(project["filepath"], new_name)
                                if new_path:
                                    if st.session_state.current_project == project["filepath"]:
                                        st.session_state.current_project = new_path
                                        st.session_state.project_name = new_name
                                    st.sidebar.success("✅ 重命名成功！")
                                    st.rerun()
                                else:
                                    st.sidebar.error("重命名失败")
                            except Exception as e:
                                st.sidebar.error(f"重命名失败：{str(e)}")
                    
                    with col4:
                        # 删除按钮
                        if st.button("🗑️ 删除", key=f"project_delete_{i}", use_container_width=True, type="secondary"):
                            try:
                                if project_manager.delete_project(project["filepath"]):
                                    if st.session_state.current_project == project["filepath"]:
                                        st.session_state.current_project = None
                                        st.session_state.project_name = ""
                                    st.sidebar.success("✅ 删除成功！")
                                    st.rerun()
                                else:
                                    st.sidebar.error("删除失败")
                            except Exception as e:
                                st.sidebar.error(f"删除失败：{str(e)}")
        else:
            st.info("暂无保存的项目")

def render_step1_script_input():
    """步骤1：剧本输入"""
    st.header("📝 步骤1：输入剧本")
    
    script = st.text_area(
        "请输入剧本内容",
        value=st.session_state.script,
        height=400,
        placeholder="请输入您的剧本内容...\n\n建议包含：场景、人物、动作、对话等详细信息",
        key="script_input"
    )
    
    if script:
        st.session_state.script = script
        
        # 显示剧本统计
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("字数", len(script))
        with col2:
            st.metric("行数", len(script.split('\n')))
        with col3:
            st.metric("预估分镜", f"{len(script)//200 + 1}~{len(script)//100 + 1}")
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🎬 开始分镜", type="primary", key="start_division"):
                if not script.strip():
                    st.error("请输入剧本内容")
                    return False
                if len(script.strip()) < 50:
                    st.warning("剧本内容过短，建议至少50个字符")
                return True
        with col2:
            st.info("点击按钮使用AI自动划分分镜头")
    
    return False

def render_step2_scene_editing(services):
    """步骤2：分镜头编辑"""
    st.header("✂️ 步骤2：分镜头编辑")
    
    if not st.session_state.scenes:
        st.warning("请先完成分镜头划分")
        return False
    
    # 统计信息
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总分镜数", len(st.session_state.scenes))
    with col2:
        unique_locations = len(set(s.get('location', '') for s in st.session_state.scenes))
        st.metric("场景数", unique_locations)
    with col3:
        all_characters = set()
        for s in st.session_state.scenes:
            all_characters.update(s.get('characters', []))
        st.metric("人物数", len(all_characters))
    with col4:
        dialogue_count = sum(1 for s in st.session_state.scenes if s.get('dialogue_text', ''))
        st.metric("对话镜头", dialogue_count)
    
    st.markdown("---")
    
    # 显示分镜头
    for i, scene in enumerate(st.session_state.scenes):
        with st.expander(f"分镜头 {i+1}: {scene['scene_description'][:50]}...", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # 分镜描述
                new_desc = st.text_area(
                    "分镜描述",
                    value=scene["scene_description"],
                    height=120,
                    key=f"desc_{i}"
                )
                
                # 镜头参数（独立字段）
                st.markdown("**镜头参数**")
                # 兼容旧格式：如果存在组合格式，尝试解析
                shot_size_val = scene.get("shot_size", "")
                camera_angle_val = scene.get("camera_angle", "")
                camera_movement_val = scene.get("camera_movement", "")
                camera_equipment_val = scene.get("camera_equipment", "")
                lens_focal_val = scene.get("lens_focal_length", "")
                camera_val = scene.get("camera", "")
                lens_val = scene.get("lens", "")
                aperture_val = scene.get("aperture", "")
                
                # 如果字段为空，尝试从组合格式解析（兼容旧数据）
                if not shot_size_val and "/" in str(camera_angle_val):
                    angle_parts = str(camera_angle_val).split("/")
                    if len(angle_parts) == 5:
                        shot_size_val = angle_parts[0]
                        camera_angle_val = angle_parts[1]
                        camera_movement_val = angle_parts[2]
                        camera_equipment_val = angle_parts[3]
                        lens_focal_val = angle_parts[4]
                
                # 设置默认值
                if not shot_size_val:
                    shot_size_val = "中景"
                if not camera_angle_val or camera_angle_val not in ["视平", "高位俯拍", "低位仰拍", "斜拍", "越肩", "鸟瞰"]:
                    camera_angle_val = "视平"
                if not camera_movement_val:
                    camera_movement_val = "固定"
                if not camera_equipment_val:
                    camera_equipment_val = "固定"
                if not lens_focal_val:
                    lens_focal_val = "标准(35-50mm)"
                
                col_angle_1, col_angle_2, col_angle_3, col_angle_4, col_angle_5 = st.columns(5)
                with col_angle_1:
                    shot_size = st.selectbox(
                        "景别",
                        ["大远景", "远景", "全景", "中景", "中近景", "近景", "特写", "大特写"],
                        index=["大远景", "远景", "全景", "中景", "中近景", "近景", "特写", "大特写"].index(shot_size_val) if shot_size_val in ["大远景", "远景", "全景", "中景", "中近景", "近景", "特写", "大特写"] else 3,
                        key=f"shot_size_{i}"
                    )
                with col_angle_2:
                    camera_angle = st.selectbox(
                        "摄影机角度",
                        ["视平", "高位俯拍", "低位仰拍", "斜拍", "越肩", "鸟瞰"],
                        index=["视平", "高位俯拍", "低位仰拍", "斜拍", "越肩", "鸟瞰"].index(camera_angle_val) if camera_angle_val in ["视平", "高位俯拍", "低位仰拍", "斜拍", "越肩", "鸟瞰"] else 0,
                        key=f"camera_angle_{i}"
                    )
                with col_angle_3:
                    camera_movement = st.selectbox(
                        "运镜",
                        ["固定", "横移", "俯仰", "横摇", "升降", "轨道推拉", "变焦推拉", "正跟随", "倒跟随", "环绕", "滑轨横移"],
                        index=["固定", "横移", "俯仰", "横摇", "升降", "轨道推拉", "变焦推拉", "正跟随", "倒跟随", "环绕", "滑轨横移"].index(camera_movement_val) if camera_movement_val in ["固定", "横移", "俯仰", "横摇", "升降", "轨道推拉", "变焦推拉", "正跟随", "倒跟随", "环绕", "滑轨横移"] else 0,
                        key=f"camera_movement_{i}"
                    )
                with col_angle_4:
                    camera_equipment = st.selectbox(
                        "摄影机装备",
                        ["固定", "轨道", "手持", "稳定器", "摇臂", "航拍"],
                        index=["固定", "轨道", "手持", "稳定器", "摇臂", "航拍"].index(camera_equipment_val) if camera_equipment_val in ["固定", "轨道", "手持", "稳定器", "摇臂", "航拍"] else 0,
                        key=f"camera_equipment_{i}"
                    )
                with col_angle_5:
                    lens_focal = st.selectbox(
                        "镜头焦段",
                        ["超广角(14-24mm)", "广角(24-35mm)", "标准(35-50mm)", "中焦(50-85mm)", "长焦(85-200mm)", "超长焦(200mm+)"],
                        index=["超广角(14-24mm)", "广角(24-35mm)", "标准(35-50mm)", "中焦(50-85mm)", "长焦(85-200mm)", "超长焦(200mm+)"].index(lens_focal_val) if lens_focal_val in ["超广角(14-24mm)", "广角(24-35mm)", "标准(35-50mm)", "中焦(50-85mm)", "长焦(85-200mm)", "超长焦(200mm+)"] else 2,
                        key=f"lens_focal_{i}"
                    )
                
                # 相机、镜头、光圈参数（必选）
                # 设置默认值
                if not camera_val:
                    camera_val = "ARRI Alexa"
                if not lens_val:
                    lens_val = "ARRI Master Primes"
                if not aperture_val:
                    aperture_val = "f/2.8"
                
                col_camera_1, col_camera_2, col_camera_3 = st.columns(3)
                with col_camera_1:
                    camera_options = ["ARRI Alexa", "ARRI Alexa 65", "Arriflex 416", "IMAX 70mm", "Kodak Portra 400", "Kodak Vision3 500T", "Panavision Panaflex", "RED Monstro 8K", "Sony Venice", "Cinestill 800T"]
                    camera_index = camera_options.index(camera_val) if camera_val in camera_options else 0
                    camera = st.selectbox(
                        "相机 *",
                        camera_options,
                        index=camera_index,
                        key=f"camera_{i}"
                    )
                with col_camera_2:
                    lens_options = ["ARRI Master Primes", "ARRI Master Prime Macro", "Canon K35", "Cooke Anamorphic", "Helios 44-2", "Panavision C-Series Anamorphic", "Petzval Lens"]
                    lens_index = lens_options.index(lens_val) if lens_val in lens_options else 0
                    lens = st.selectbox(
                        "镜头 *",
                        lens_options,
                        index=lens_index,
                        key=f"lens_{i}"
                    )
                with col_camera_3:
                    aperture_options = ["f/1.2", "f/1.4", "f/2.0", "f/2.2", "f/2.8", "f/4.0", "f/5.6", "f/11"]
                    aperture_index = aperture_options.index(aperture_val) if aperture_val in aperture_options else 4
                    aperture = st.selectbox(
                        "光圈 *",
                        aperture_options,
                        index=aperture_index,
                        key=f"aperture_{i}"
                    )
                
                # 基础信息
                col1_1, col1_2, col1_3 = st.columns(3)
                
                with col1_2:
                    new_location = st.text_input(
                        "地点",
                        value=scene.get("location", ""),
                        key=f"location_{i}"
                    )
                
                with col1_3:
                    new_time = st.selectbox(
                        "时间",
                        ["白天", "夜晚", "黄昏", "黎明", "中午", "下午"],
                        index=["白天", "夜晚", "黄昏", "黎明", "中午", "下午"].index(
                            scene.get("time", "白天")
                        ),
                        key=f"time_{i}"
                    )
                
                # 情绪和人物
                col1_4, col1_5 = st.columns(2)
                with col1_4:
                    new_mood = st.text_input(
                        "情绪氛围",
                        value=scene.get("mood", ""),
                        key=f"mood_{i}"
                    )
                
                with col1_5:
                    new_characters = st.text_input(
                        "人物（逗号分隔）",
                        value=", ".join(scene.get("characters", [])),
                        key=f"characters_{i}"
                    )
                
                # 创作维度字段
                st.markdown("**创作维度**")
                col_dim_1, col_dim_2, col_dim_3, col_dim_4 = st.columns(4)
                
                with col_dim_1:
                    composition_tension_options = ["", "饱满", "丰富", "引导", "饱满+引导", "丰富+引导", "饱满+丰富", "饱满+丰富+引导"]
                    composition_tension_val = scene.get("composition_tension", "")
                    composition_tension_index = composition_tension_options.index(composition_tension_val) if composition_tension_val in composition_tension_options else 0
                    composition_tension = st.selectbox(
                        "构图张力",
                        composition_tension_options,
                        index=composition_tension_index,
                        key=f"composition_tension_{i}"
                    )
                
                with col_dim_2:
                    protagonist_type_options = ["", "情感共鸣型", "价值观载体型", "成长弧光型", "观察者/催化剂型"]
                    protagonist_type_val = scene.get("protagonist_type", "")
                    protagonist_type_index = protagonist_type_options.index(protagonist_type_val) if protagonist_type_val in protagonist_type_options else 0
                    protagonist_type = st.selectbox(
                        "主角核心表达",
                        protagonist_type_options,
                        index=protagonist_type_index,
                        key=f"protagonist_type_{i}"
                    )
                
                with col_dim_3:
                    emotion_design_options = ["", "情绪一致", "情绪错位", "情绪叠加", "情绪反转"]
                    emotion_design_val = scene.get("emotion_design", "")
                    emotion_design_index = emotion_design_options.index(emotion_design_val) if emotion_design_val in emotion_design_options else 0
                    emotion_design = st.selectbox(
                        "情绪设计",
                        emotion_design_options,
                        index=emotion_design_index,
                        key=f"emotion_design_{i}"
                    )
                
                with col_dim_4:
                    performance_style_options = ["", "内敛表演", "外放表演", "反差表演", "细节表演"]
                    performance_style_val = scene.get("performance_style", "")
                    performance_style_index = performance_style_options.index(performance_style_val) if performance_style_val in performance_style_options else 0
                    performance_style = st.selectbox(
                        "表演风格",
                        performance_style_options,
                        index=performance_style_index,
                        key=f"performance_style_{i}"
                    )
                
                # 对话和音效
                st.markdown("**对话与音效**")
                col1_6, col1_7 = st.columns(2)
                with col1_6:
                    new_dialogue = st.text_area(
                        "台词",
                        value=scene.get("dialogue_text", ""),
                        height=60,
                        placeholder="人物名：台词内容",
                        key=f"dialogue_{i}"
                    )
                
                with col1_7:
                    new_voiceover = st.text_area(
                        "旁白",
                        value=scene.get("voiceover_text", ""),
                        height=60,
                        key=f"voiceover_{i}"
                    )
                
                new_sound = st.text_input(
                    "音效（逗号分隔）",
                    value=scene.get("sound_effects", ""),
                    key=f"sound_{i}"
                )
            
            with col2:
                st.write("")  # 空行对齐
                st.write("")
                
                if st.button("💾 保存", key=f"save_{i}", use_container_width=True):
                    st.session_state.scenes[i]["scene_description"] = new_desc
                    st.session_state.scenes[i]["shot_size"] = shot_size
                    st.session_state.scenes[i]["camera_angle"] = camera_angle
                    st.session_state.scenes[i]["camera_movement"] = camera_movement
                    st.session_state.scenes[i]["camera_equipment"] = camera_equipment
                    st.session_state.scenes[i]["lens_focal_length"] = lens_focal
                    st.session_state.scenes[i]["camera"] = camera
                    st.session_state.scenes[i]["lens"] = lens
                    st.session_state.scenes[i]["aperture"] = aperture
                    st.session_state.scenes[i]["location"] = new_location
                    st.session_state.scenes[i]["time"] = new_time
                    st.session_state.scenes[i]["mood"] = new_mood
                    st.session_state.scenes[i]["characters"] = [c.strip() for c in new_characters.split(",") if c.strip()]
                    # 保存创作维度字段
                    st.session_state.scenes[i]["composition_tension"] = composition_tension if composition_tension else ""
                    st.session_state.scenes[i]["protagonist_type"] = protagonist_type if protagonist_type else ""
                    st.session_state.scenes[i]["emotion_design"] = emotion_design if emotion_design else ""
                    st.session_state.scenes[i]["performance_style"] = performance_style if performance_style else ""
                    st.session_state.scenes[i]["dialogue_text"] = new_dialogue
                    st.session_state.scenes[i]["voiceover_text"] = new_voiceover
                    st.session_state.scenes[i]["sound_effects"] = new_sound
                    st.success(f"✅ 分镜 {i+1} 已保存")
                    st.rerun()
                
                if st.button("🗑️ 删除", key=f"scene_delete_{i}", use_container_width=True):
                    del st.session_state.scenes[i]
                    # 重新编号
                    for idx, s in enumerate(st.session_state.scenes):
                        s["scene_number"] = idx + 1
                    st.success(f"✅ 分镜 {i+1} 已删除")
                    st.rerun()
    
    # 导出按钮
    st.markdown("---")
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📊 导出Excel", type="primary", key="export"):
            return True
    with col2:
        st.info("导出所有分镜头到Excel文件（自动保存到桌面）")
    
    return False

# JSON提示词编辑器下拉选项配置
JSON_PROMPT_DROPDOWN_OPTIONS = {
    "shot_size": ["大远景", "远景", "全景", "中景", "中近景", "近景", "特写", "大特写"],
    "camera_angle": ["视平", "高位俯拍", "低位仰拍", "斜拍", "越肩", "鸟瞰"],
    "camera_model": ["ARRI Alexa", "ARRI Alexa 65", "Arriflex 416", "IMAX 70mm", "Kodak Portra 400", "Kodak Vision3 500T", "Panavision Panaflex", "RED Monstro 8K", "Sony Venice", "Cinestill 800T"],
    "lens": ["ARRI Master Primes", "ARRI Master Prime Macro", "Canon K35", "Cooke Anamorphic", "Helios 44-2", "Panavision C-Series Anamorphic", "Petzval Lens"],
    "aperture": ["f/1.2", "f/1.4", "f/2.0", "f/2.2", "f/2.8", "f/4.0", "f/5.6", "f/11"],
    "focal_length": ["超广角(14-24mm)", "广角(24-35mm)", "标准(35-50mm)", "中焦(50-85mm)", "长焦(85-200mm)", "超长焦(200mm+)"],
    "time_of_day": ["白天", "夜晚", "黄昏", "黎明", "中午", "下午"],
    "lighting_type": ["自然光", "人工光", "混合光", "环境光", "点光源", "面光源"],
    "lighting_direction": ["正面光", "侧光", "逆光", "顶光", "底光", "45度侧光", "背光"],
    "lighting_color_temperature": ["暖光(2700K-3000K)", "中性光(4000K-4500K)", "冷光(5000K-6500K)", "日光(5500K)", "钨丝灯(3200K)", "荧光灯(4000K)"],
    "cinematic_style": ["现实主义", "超现实主义", "黑色电影", "科幻风格", "复古风格", "现代风格", "史诗风格", "文艺风格"],
    "color_grading": ["暖色调", "冷色调", "高对比度", "低饱和度", "高饱和度", "单色调", "电影级调色", "自然调色"],
    "composition_tension": ["", "饱满", "丰富", "引导", "饱满+引导", "丰富+引导", "饱满+丰富", "饱满+丰富+引导"],
    "protagonist_type": ["", "情感共鸣型", "价值观载体型", "成长弧光型", "观察者/催化剂型"],
    "emotion_design": ["", "情绪一致", "情绪错位", "情绪叠加", "情绪反转"],
    "performance_style": ["", "内敛表演", "外放表演", "反差表演", "细节表演"]
}

def render_json_prompt_editor(prompt_json: Dict, scene_num: int, key_prefix: str) -> Dict:
    """
    渲染JSON提示词的可视化编辑器
    
    Args:
        prompt_json: 当前的JSON提示词字典
        scene_num: 分镜编号
        key_prefix: Streamlit key的前缀
        
    Returns:
        编辑后的JSON字典
    """
    # 深拷贝原始JSON，确保所有字段都被保留
    edited_json = copy.deepcopy(prompt_json)
    
    # 使用tabs按JSON的顶层键分组
    tabs = st.tabs(["主体 (Subject)", "场景 (Scene)", "构图 (Composition)", "光照 (Lighting)", "技术参数 (Camera)", "视觉风格 (Style)", "其他 (Others)"])
    
    # 确保所有必需的顶层键存在
    if "subject" not in edited_json:
        edited_json["subject"] = {}
    if "scene" not in edited_json:
        edited_json["scene"] = {}
    if "composition" not in edited_json:
        edited_json["composition"] = {}
    if "lighting" not in edited_json:
        edited_json["lighting"] = {}
    if "camera_technical" not in edited_json:
        edited_json["camera_technical"] = {}
    if "visual_style" not in edited_json:
        edited_json["visual_style"] = {}
    if "spatial_anchors" not in edited_json:
        edited_json["spatial_anchors"] = []
    if "negative_constraints" not in edited_json:
        edited_json["negative_constraints"] = []
    
    # Tab 1: Subject
    with tabs[0]:
        st.markdown("#### 主体信息")
        subject = edited_json.get("subject", {})
        
        col1, col2 = st.columns(2)
        with col1:
            edited_json["subject"]["main_character"] = st.text_input(
                "主要角色",
                value=subject.get("main_character", ""),
                key=f"{key_prefix}_subject_main_character"
            )
            edited_json["subject"]["action"] = st.text_area(
                "动作",
                value=subject.get("action", ""),
                height=80,
                key=f"{key_prefix}_subject_action"
            )
            edited_json["subject"]["pose"] = st.text_input(
                "姿势",
                value=subject.get("pose", ""),
                key=f"{key_prefix}_subject_pose"
            )
            edited_json["subject"]["expression"] = st.text_input(
                "表情",
                value=subject.get("expression", ""),
                key=f"{key_prefix}_subject_expression"
            )
        with col2:
            edited_json["subject"]["clothing"] = st.text_input(
                "服装",
                value=subject.get("clothing", ""),
                key=f"{key_prefix}_subject_clothing"
            )
            edited_json["subject"]["props"] = st.text_input(
                "道具",
                value=subject.get("props", ""),
                key=f"{key_prefix}_subject_props"
            )
            edited_json["subject"]["full_description"] = st.text_area(
                "完整描述",
                value=subject.get("full_description", ""),
                height=100,
                key=f"{key_prefix}_subject_full_description"
            )
    
    # Tab 2: Scene
    with tabs[1]:
        st.markdown("#### 场景信息")
        scene = edited_json.get("scene", {})
        
        col1, col2 = st.columns(2)
        with col1:
            edited_json["scene"] = {}
            edited_json["scene"]["location"] = st.text_input(
                "地点",
                value=scene.get("location", ""),
                key=f"{key_prefix}_scene_location"
            )
            edited_json["scene"]["environment"] = st.text_input(
                "环境",
                value=scene.get("environment", ""),
                key=f"{key_prefix}_scene_environment"
            )
            edited_json["scene"]["background"] = st.text_area(
                "背景",
                value=scene.get("background", ""),
                height=80,
                key=f"{key_prefix}_scene_background"
            )
        with col2:
            # 时间使用下拉框
            time_options = JSON_PROMPT_DROPDOWN_OPTIONS["time_of_day"]
            current_time = scene.get("time_of_day", "")
            time_index = time_options.index(current_time) if current_time in time_options else 0
            edited_json["scene"]["time_of_day"] = st.selectbox(
                "时间",
                time_options,
                index=time_index,
                key=f"{key_prefix}_scene_time_of_day"
            )
            edited_json["scene"]["weather"] = st.text_input(
                "天气",
                value=scene.get("weather", ""),
                key=f"{key_prefix}_scene_weather"
            )
            edited_json["scene"]["full_description"] = st.text_area(
                "完整描述",
                value=scene.get("full_description", ""),
                height=100,
                key=f"{key_prefix}_scene_full_description"
            )
    
    # Tab 3: Composition
    with tabs[2]:
        st.markdown("#### 构图信息")
        composition = edited_json.get("composition", {})
        
        col1, col2 = st.columns(2)
        with col1:
            edited_json["composition"] = {}
            # 景别使用下拉框
            shot_size_options = JSON_PROMPT_DROPDOWN_OPTIONS["shot_size"]
            current_shot_size = composition.get("shot_size", "")
            shot_size_index = shot_size_options.index(current_shot_size) if current_shot_size in shot_size_options else 3
            edited_json["composition"]["shot_size"] = st.selectbox(
                "景别",
                shot_size_options,
                index=shot_size_index,
                key=f"{key_prefix}_composition_shot_size"
            )
            # 摄影机角度使用下拉框
            camera_angle_options = JSON_PROMPT_DROPDOWN_OPTIONS["camera_angle"]
            current_camera_angle = composition.get("camera_angle", "")
            camera_angle_index = camera_angle_options.index(current_camera_angle) if current_camera_angle in camera_angle_options else 0
            edited_json["composition"]["camera_angle"] = st.selectbox(
                "摄影机角度",
                camera_angle_options,
                index=camera_angle_index,
                key=f"{key_prefix}_composition_camera_angle"
            )
            edited_json["composition"]["framing"] = st.text_input(
                "取景",
                value=composition.get("framing", ""),
                key=f"{key_prefix}_composition_framing"
            )
            # 构图张力使用下拉框
            composition_tension_options = JSON_PROMPT_DROPDOWN_OPTIONS["composition_tension"]
            current_composition_tension = composition.get("composition_tension", "")
            # 处理双语格式（可能包含 " / " 分隔符）
            if " / " in str(current_composition_tension):
                current_composition_tension = str(current_composition_tension).split(" / ")[0]
            composition_tension_index = composition_tension_options.index(current_composition_tension) if current_composition_tension in composition_tension_options else 0
            edited_json["composition"]["composition_tension"] = st.selectbox(
                "构图张力",
                composition_tension_options,
                index=composition_tension_index,
                key=f"{key_prefix}_composition_tension"
            )
        with col2:
            edited_json["composition"]["rule_of_thirds"] = st.text_input(
                "三分法则",
                value=composition.get("rule_of_thirds", ""),
                key=f"{key_prefix}_composition_rule_of_thirds"
            )
            edited_json["composition"]["leading_lines"] = st.text_input(
                "引导线",
                value=composition.get("leading_lines", ""),
                key=f"{key_prefix}_composition_leading_lines"
            )
    
    # Tab 4: Lighting
    with tabs[3]:
        st.markdown("#### 光照信息")
        lighting = edited_json.get("lighting", {})
        
        col1, col2 = st.columns(2)
        with col1:
            edited_json["lighting"] = {}
            # 光照类型使用下拉框
            lighting_type_options = JSON_PROMPT_DROPDOWN_OPTIONS["lighting_type"]
            current_lighting_type = lighting.get("type", "")
            lighting_type_index = lighting_type_options.index(current_lighting_type) if current_lighting_type in lighting_type_options else 0
            edited_json["lighting"]["type"] = st.selectbox(
                "光照类型",
                lighting_type_options,
                index=lighting_type_index,
                key=f"{key_prefix}_lighting_type"
            )
            # 光照方向使用下拉框
            lighting_direction_options = JSON_PROMPT_DROPDOWN_OPTIONS["lighting_direction"]
            current_lighting_direction = lighting.get("direction", "")
            lighting_direction_index = lighting_direction_options.index(current_lighting_direction) if current_lighting_direction in lighting_direction_options else 0
            edited_json["lighting"]["direction"] = st.selectbox(
                "光照方向",
                lighting_direction_options,
                index=lighting_direction_index,
                key=f"{key_prefix}_lighting_direction"
            )
            edited_json["lighting"]["intensity"] = st.text_input(
                "光照强度",
                value=lighting.get("intensity", ""),
                key=f"{key_prefix}_lighting_intensity"
            )
        with col2:
            # 色温使用下拉框
            color_temp_options = JSON_PROMPT_DROPDOWN_OPTIONS["lighting_color_temperature"]
            current_color_temp = lighting.get("color_temperature", "")
            color_temp_index = color_temp_options.index(current_color_temp) if current_color_temp in color_temp_options else 0
            edited_json["lighting"]["color_temperature"] = st.selectbox(
                "色温",
                color_temp_options,
                index=color_temp_index,
                key=f"{key_prefix}_lighting_color_temperature"
            )
            edited_json["lighting"]["mood"] = st.text_input(
                "氛围",
                value=lighting.get("mood", ""),
                key=f"{key_prefix}_lighting_mood"
            )
    
    # Tab 5: Camera Technical
    with tabs[4]:
        st.markdown("#### 技术参数")
        camera_technical = edited_json.get("camera_technical", {})
        
        col1, col2 = st.columns(2)
        with col1:
            edited_json["camera_technical"] = {}
            # 相机型号使用下拉框
            camera_model_options = JSON_PROMPT_DROPDOWN_OPTIONS["camera_model"]
            current_camera_model = camera_technical.get("camera_model", "")
            camera_model_index = camera_model_options.index(current_camera_model) if current_camera_model in camera_model_options else 0
            edited_json["camera_technical"]["camera_model"] = st.selectbox(
                "相机型号",
                camera_model_options,
                index=camera_model_index,
                key=f"{key_prefix}_camera_technical_camera_model"
            )
            # 镜头使用下拉框
            lens_options = JSON_PROMPT_DROPDOWN_OPTIONS["lens"]
            current_lens = camera_technical.get("lens", "")
            lens_index = lens_options.index(current_lens) if current_lens in lens_options else 0
            edited_json["camera_technical"]["lens"] = st.selectbox(
                "镜头",
                lens_options,
                index=lens_index,
                key=f"{key_prefix}_camera_technical_lens"
            )
            # 光圈使用下拉框
            aperture_options = JSON_PROMPT_DROPDOWN_OPTIONS["aperture"]
            current_aperture = camera_technical.get("aperture", "")
            aperture_index = aperture_options.index(current_aperture) if current_aperture in aperture_options else 4
            edited_json["camera_technical"]["aperture"] = st.selectbox(
                "光圈",
                aperture_options,
                index=aperture_index,
                key=f"{key_prefix}_camera_technical_aperture"
            )
        with col2:
            # 焦段使用下拉框
            focal_length_options = JSON_PROMPT_DROPDOWN_OPTIONS["focal_length"]
            current_focal_length = camera_technical.get("focal_length", "")
            focal_length_index = focal_length_options.index(current_focal_length) if current_focal_length in focal_length_options else 2
            edited_json["camera_technical"]["focal_length"] = st.selectbox(
                "焦段",
                focal_length_options,
                index=focal_length_index,
                key=f"{key_prefix}_camera_technical_focal_length"
            )
            edited_json["camera_technical"]["depth_of_field"] = st.text_input(
                "景深",
                value=camera_technical.get("depth_of_field", ""),
                key=f"{key_prefix}_camera_technical_depth_of_field"
            )
    
    # Tab 6: Visual Style
    with tabs[5]:
        st.markdown("#### 视觉风格")
        visual_style = edited_json.get("visual_style", {})
        
        col1, col2 = st.columns(2)
        with col1:
            edited_json["visual_style"] = {}
            # 电影风格使用下拉框
            cinematic_style_options = JSON_PROMPT_DROPDOWN_OPTIONS["cinematic_style"]
            current_cinematic_style = visual_style.get("cinematic_style", "")
            cinematic_style_index = cinematic_style_options.index(current_cinematic_style) if current_cinematic_style in cinematic_style_options else 0
            edited_json["visual_style"]["cinematic_style"] = st.selectbox(
                "电影风格",
                cinematic_style_options,
                index=cinematic_style_index,
                key=f"{key_prefix}_visual_style_cinematic_style"
            )
            # 色彩分级使用下拉框
            color_grading_options = JSON_PROMPT_DROPDOWN_OPTIONS["color_grading"]
            current_color_grading = visual_style.get("color_grading", "")
            color_grading_index = color_grading_options.index(current_color_grading) if current_color_grading in color_grading_options else 0
            edited_json["visual_style"]["color_grading"] = st.selectbox(
                "色彩分级",
                color_grading_options,
                index=color_grading_index,
                key=f"{key_prefix}_visual_style_color_grading"
            )
        with col2:
            edited_json["visual_style"]["texture"] = st.text_input(
                "纹理",
                value=visual_style.get("texture", ""),
                key=f"{key_prefix}_visual_style_texture"
            )
            edited_json["visual_style"]["atmosphere"] = st.text_input(
                "氛围",
                value=visual_style.get("atmosphere", ""),
                key=f"{key_prefix}_visual_style_atmosphere"
            )
            # 主角核心表达使用下拉框
            protagonist_type_options = JSON_PROMPT_DROPDOWN_OPTIONS["protagonist_type"]
            current_protagonist_type = visual_style.get("protagonist_type", "")
            # 处理双语格式
            if " / " in str(current_protagonist_type):
                current_protagonist_type = str(current_protagonist_type).split(" / ")[0]
            protagonist_type_index = protagonist_type_options.index(current_protagonist_type) if current_protagonist_type in protagonist_type_options else 0
            edited_json["visual_style"]["protagonist_type"] = st.selectbox(
                "主角核心表达",
                protagonist_type_options,
                index=protagonist_type_index,
                key=f"{key_prefix}_visual_style_protagonist_type"
            )
            # 情绪设计使用下拉框
            emotion_design_options = JSON_PROMPT_DROPDOWN_OPTIONS["emotion_design"]
            current_emotion_design = visual_style.get("emotion_design", "")
            # 处理双语格式
            if " / " in str(current_emotion_design):
                current_emotion_design = str(current_emotion_design).split(" / ")[0]
            emotion_design_index = emotion_design_options.index(current_emotion_design) if current_emotion_design in emotion_design_options else 0
            edited_json["visual_style"]["emotion_design"] = st.selectbox(
                "情绪设计",
                emotion_design_options,
                index=emotion_design_index,
                key=f"{key_prefix}_visual_style_emotion_design"
            )
            # 表演风格使用下拉框
            performance_style_options = JSON_PROMPT_DROPDOWN_OPTIONS["performance_style"]
            current_performance_style = visual_style.get("performance_style", "")
            # 处理双语格式
            if " / " in str(current_performance_style):
                current_performance_style = str(current_performance_style).split(" / ")[0]
            performance_style_index = performance_style_options.index(current_performance_style) if current_performance_style in performance_style_options else 0
            edited_json["visual_style"]["performance_style"] = st.selectbox(
                "表演风格",
                performance_style_options,
                index=performance_style_index,
                key=f"{key_prefix}_visual_style_performance_style"
            )
    
    # Tab 7: Others (spatial_anchors, negative_constraints)
    with tabs[6]:
        st.markdown("#### 其他参数")
        
        # 空间锚点（数组）
        st.markdown("**空间锚点 (Spatial Anchors)**")
        spatial_anchors_original = edited_json.get("spatial_anchors", [])
        # 过滤掉被标记删除的项（使用原始索引）
        filtered_anchors = []
        anchor_index_map = {}  # 映射：过滤后索引 -> 原始索引
        original_idx = 0
        for i, anchor in enumerate(spatial_anchors_original):
            if not st.session_state.get(f"{key_prefix}_delete_anchor_{i}", False):
                filtered_anchors.append(anchor)
                anchor_index_map[len(filtered_anchors) - 1] = i
        edited_json["spatial_anchors"] = filtered_anchors.copy()
        
        # 显示现有锚点
        for display_idx, anchor in enumerate(edited_json["spatial_anchors"]):
            col1, col2 = st.columns([4, 1])
            with col1:
                anchor_value = st.text_input(
                    f"锚点 {display_idx+1}",
                    value=str(anchor) if anchor else "",
                    key=f"{key_prefix}_spatial_anchor_{display_idx}"
                )
                edited_json["spatial_anchors"][display_idx] = anchor_value
            with col2:
                if st.button("删除", key=f"{key_prefix}_delete_anchor_btn_{display_idx}"):
                    # 使用映射找到原始索引
                    original_index = anchor_index_map.get(display_idx, display_idx)
                    st.session_state[f"{key_prefix}_delete_anchor_{original_index}"] = True
                    st.rerun()
        
        # 添加新锚点按钮
        if st.button("➕ 添加空间锚点", key=f"{key_prefix}_add_anchor"):
            if f"{key_prefix}_spatial_anchors_count" not in st.session_state:
                st.session_state[f"{key_prefix}_spatial_anchors_count"] = len(edited_json["spatial_anchors"])
            st.session_state[f"{key_prefix}_spatial_anchors_count"] += 1
            st.rerun()
        
        # 处理新添加的锚点
        anchor_count = st.session_state.get(f"{key_prefix}_spatial_anchors_count", len(edited_json["spatial_anchors"]))
        for i in range(len(edited_json["spatial_anchors"]), anchor_count):
            anchor_value = st.text_input(
                f"新锚点 {i+1}",
                value="",
                key=f"{key_prefix}_new_spatial_anchor_{i}"
            )
            if anchor_value:
                edited_json["spatial_anchors"].append(anchor_value)
        
        st.markdown("---")
        
        # 负面约束（数组）
        st.markdown("**负面约束 (Negative Constraints)**")
        negative_constraints_original = edited_json.get("negative_constraints", [])
        # 过滤掉被标记删除的项（使用原始索引）
        filtered_constraints = []
        constraint_index_map = {}  # 映射：过滤后索引 -> 原始索引
        for i, constraint in enumerate(negative_constraints_original):
            if not st.session_state.get(f"{key_prefix}_delete_constraint_{i}", False):
                filtered_constraints.append(constraint)
                constraint_index_map[len(filtered_constraints) - 1] = i
        edited_json["negative_constraints"] = filtered_constraints.copy()
        
        # 显示现有约束
        for display_idx, constraint in enumerate(edited_json["negative_constraints"]):
            col1, col2 = st.columns([4, 1])
            with col1:
                constraint_value = st.text_input(
                    f"约束 {display_idx+1}",
                    value=str(constraint) if constraint else "",
                    key=f"{key_prefix}_negative_constraint_{display_idx}"
                )
                edited_json["negative_constraints"][display_idx] = constraint_value
            with col2:
                if st.button("删除", key=f"{key_prefix}_delete_constraint_btn_{display_idx}"):
                    # 使用映射找到原始索引
                    original_index = constraint_index_map.get(display_idx, display_idx)
                    st.session_state[f"{key_prefix}_delete_constraint_{original_index}"] = True
                    st.rerun()
        
        # 添加新约束按钮
        if st.button("➕ 添加负面约束", key=f"{key_prefix}_add_constraint"):
            if f"{key_prefix}_negative_constraints_count" not in st.session_state:
                st.session_state[f"{key_prefix}_negative_constraints_count"] = len(edited_json["negative_constraints"])
            st.session_state[f"{key_prefix}_negative_constraints_count"] += 1
            st.rerun()
        
        # 处理新添加的约束
        constraint_count = st.session_state.get(f"{key_prefix}_negative_constraints_count", len(edited_json["negative_constraints"]))
        for i in range(len(edited_json["negative_constraints"]), constraint_count):
            constraint_value = st.text_input(
                f"新约束 {i+1}",
                value="",
                key=f"{key_prefix}_new_negative_constraint_{i}"
            )
            if constraint_value:
                edited_json["negative_constraints"].append(constraint_value)
    
    return edited_json

def render_step3_prompt_generation(services):
    """步骤3：生成文生图提示词"""
    st.header("🎨 步骤3：生成文生图提示词（Nano Banana Pro）")
    
    if not st.session_state.scenes:
        st.warning("⚠️ 请先完成分镜编辑")
        return
    
    # 配置区域
    with st.expander("⚙️ 提示词生成配置", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                "提示词语言",
                ["bilingual", "chinese", "english"],
                index=0 if st.session_state.prompt_config["language"] == "bilingual" else (1 if st.session_state.prompt_config["language"] == "chinese" else 2),
                key="prompt_language"
            )
            
            detail_level = st.selectbox(
                "详细程度",
                ["simple", "standard", "detailed"],
                index=1 if st.session_state.prompt_config["detail_level"] == "standard" else (0 if st.session_state.prompt_config["detail_level"] == "simple" else 2),
                key="prompt_detail"
            )
        
        with col2:
            include_technical = st.checkbox(
                "包含技术参数（相机、镜头、光圈）",
                value=st.session_state.prompt_config["include_technical"],
                key="prompt_technical"
            )
            
            include_mood = st.checkbox(
                "包含情绪氛围",
                value=st.session_state.prompt_config["include_mood"],
                key="prompt_mood"
            )
        
        # LLM 辅助选项
        st.markdown("---")
        use_llm = st.checkbox(
            "🤖 使用 LLM 辅助生成（更准确但需要 API 调用）",
            value=st.session_state.prompt_config.get("use_llm", False),
            key="prompt_use_llm",
            help="启用后，将使用 LLM 模型来更准确地提取视觉元素和翻译文本，生成更准确的 JSON 提示词。需要配置 API Key。"
        )
        
        if use_llm:
            st.info("💡 LLM 辅助模式：将使用已配置的 LLM 模型来提升提示词生成的准确性。")
        
        # 更新配置
        st.session_state.prompt_config = {
            "language": language,
            "detail_level": detail_level,
            "include_technical": include_technical,
            "include_mood": include_mood,
            "include_characters": True,
            "use_llm": use_llm
        }
    
    # 批量生成区域
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        scene_range = st.radio(
            "选择分镜范围",
            ["全部", "选中", "自定义"],
            key="scene_range"
        )
    
    with col2:
        if scene_range == "自定义":
            start_idx = st.number_input("起始分镜", min_value=1, max_value=len(st.session_state.scenes), value=1, key="start_idx")
            end_idx = st.number_input("结束分镜", min_value=1, max_value=len(st.session_state.scenes), value=len(st.session_state.scenes), key="end_idx")
        else:
            start_idx = 1
            end_idx = len(st.session_state.scenes)
    
    with col3:
        if st.button("🚀 生成提示词", type="primary", use_container_width=True, key="generate_prompts"):
            # 确定要生成的分镜范围
            if scene_range == "全部":
                selected_scenes = st.session_state.scenes
            elif scene_range == "选中":
                # 这里可以添加选中逻辑，暂时使用全部
                selected_scenes = st.session_state.scenes
            else:
                selected_scenes = st.session_state.scenes[start_idx-1:end_idx]
            
            # 生成提示词
            try:
                # 检查是否需要 LLM 服务
                use_llm = st.session_state.prompt_config.get("use_llm", False)
                llm_service = None
                
                if use_llm:
                    # 检查 API 配置
                    config = st.session_state.get("llm_config", {})
                    if not config.get("api_key") and config.get("brand") != "LM Studio":
                        st.warning("⚠️ 已启用 LLM 辅助，但未配置 API Key，将使用规则处理模式")
                        st.session_state.prompt_config["use_llm"] = False
                        use_llm = False
                    else:
                        # 配置 LLM 服务
                        llm_service = services["llm_service"]
                        llm_service.set_model(
                            config.get("brand", "Deepseek"),
                            config.get("model", "deepseek-chat"),
                            config.get("api_key", "")
                        )
                
                spinner_text = "正在使用 LLM 生成提示词（可能需要一些时间）..." if use_llm else "正在生成提示词..."
                with st.spinner(spinner_text):
                    generator = ImagePromptGenerator(
                        st.session_state.prompt_config,
                        llm_service=llm_service if use_llm else None
                    )
                    prompts = generator.generate_batch(selected_scenes)
                    st.session_state.image_prompts = prompts
                    
                    mode_text = "（LLM 辅助）" if use_llm else "（规则处理）"
                    st.success(f"✅ 成功生成 {len(prompts)} 个提示词{mode_text}！")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")
                with st.expander("🔍 查看详细错误"):
                    st.code(str(e))
    
    # 预览区域
    st.markdown("---")
    st.subheader("📋 提示词预览")
    
    if st.session_state.image_prompts:
        # 显示统计信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("已生成提示词", len(st.session_state.image_prompts))
        with col2:
            avg_length = sum(len(p.get("prompt_text", "")) for p in st.session_state.image_prompts) / len(st.session_state.image_prompts) if st.session_state.image_prompts else 0
            st.metric("平均长度", f"{avg_length:.0f} 字符")
        with col3:
            if st.button("📋 复制全部提示词", key="copy_all"):
                all_prompts = "\n\n".join([
                    f"分镜 {p['scene_number']}:\n{p['prompt_text']}" 
                    for p in st.session_state.image_prompts 
                    if p.get("prompt_text")
                ])
                st.code(all_prompts, language="text")
                st.success("✅ 提示词已显示，请手动复制")
        
        # 显示每个分镜的提示词
        for idx, prompt_data in enumerate(st.session_state.image_prompts):
            if "error" in prompt_data:
                st.error(f"❌ 分镜 {prompt_data['scene_number']} 生成失败: {prompt_data['error']}")
                continue
            
            scene_num = prompt_data["scene_number"]
            scene_desc = prompt_data.get("scene_description", "")
            
            with st.expander(f"分镜 {scene_num}: {scene_desc[:50]}..." if len(scene_desc) > 50 else f"分镜 {scene_num}: {scene_desc}"):
                # 初始化编辑状态
                edit_key_prefix = f"edit_prompt_{scene_num}"
                
                # 使用session_state存储编辑后的内容
                if f"{edit_key_prefix}_text" not in st.session_state:
                    st.session_state[f"{edit_key_prefix}_text"] = prompt_data.get("prompt_text", "")
                if f"{edit_key_prefix}_negative" not in st.session_state:
                    st.session_state[f"{edit_key_prefix}_negative"] = prompt_data.get("negative_prompt", "")
                if f"{edit_key_prefix}_json_edited" not in st.session_state:
                    st.session_state[f"{edit_key_prefix}_json_edited"] = prompt_data.get("prompt_json", {})
                
                # 文本格式提示词（可编辑）
                st.markdown("**📝 文本格式提示词（可编辑）:**")
                edited_text = st.text_area(
                    "编辑文本提示词",
                    value=st.session_state[f"{edit_key_prefix}_text"],
                    height=150,
                    key=f"{edit_key_prefix}_text_area",
                    help="可以直接修改提示词文本，修改后点击下方的「保存修改」按钮"
                )
                st.session_state[f"{edit_key_prefix}_text"] = edited_text
                
                # 负面提示词（可编辑）
                st.markdown("**📝 负面提示词（可编辑）:**")
                edited_negative = st.text_area(
                    "编辑负面提示词",
                    value=st.session_state[f"{edit_key_prefix}_negative"],
                    height=100,
                    key=f"{edit_key_prefix}_negative_area",
                    help="可以直接修改负面提示词，修改后点击下方的「保存修改」按钮"
                )
                st.session_state[f"{edit_key_prefix}_negative"] = edited_negative
                
                # JSON 可视化编辑器
                st.markdown("**📝 JSON 结构化提示词（Nano Banana Pro 格式，可视化编辑）:**")
                current_json = st.session_state.get(f"{edit_key_prefix}_json_edited", prompt_data.get("prompt_json", {}))
                edited_json = render_json_prompt_editor(current_json, scene_num, edit_key_prefix)
                # 保存编辑后的JSON到session_state
                st.session_state[f"{edit_key_prefix}_json_edited"] = edited_json
                
                # 操作按钮
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"💾 保存修改", key=f"save_{scene_num}", type="primary"):
                        try:
                            # 获取编辑后的JSON（从session_state）
                            edited_json_obj = st.session_state.get(f"{edit_key_prefix}_json_edited", edited_json)
                            
                            # 更新session_state中的提示词数据
                            st.session_state.image_prompts[idx]["prompt_text"] = edited_text
                            st.session_state.image_prompts[idx]["negative_prompt"] = edited_negative
                            st.session_state.image_prompts[idx]["prompt_json"] = edited_json_obj
                            
                            st.success(f"✅ 分镜 {scene_num} 的提示词已保存！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ 保存失败: {str(e)}")
                
                with col2:
                    if st.button(f"🔄 重置为原始", key=f"reset_{scene_num}"):
                        # 重置为原始值
                        st.session_state[f"{edit_key_prefix}_text"] = prompt_data.get("prompt_text", "")
                        st.session_state[f"{edit_key_prefix}_negative"] = prompt_data.get("negative_prompt", "")
                        st.session_state[f"{edit_key_prefix}_json_edited"] = prompt_data.get("prompt_json", {})
                        # 清除数组计数
                        if f"{edit_key_prefix}_spatial_anchors_count" in st.session_state:
                            del st.session_state[f"{edit_key_prefix}_spatial_anchors_count"]
                        if f"{edit_key_prefix}_negative_constraints_count" in st.session_state:
                            del st.session_state[f"{edit_key_prefix}_negative_constraints_count"]
                        # 清除所有删除标记
                        keys_to_delete = [k for k in st.session_state.keys() if k.startswith(f"{edit_key_prefix}_delete_")]
                        for key in keys_to_delete:
                            del st.session_state[key]
                        st.success(f"✅ 已重置为原始提示词")
                        st.rerun()
                
                with col3:
                    if st.button(f"📋 复制文本提示词", key=f"copy_text_{scene_num}"):
                        st.code(edited_text, language="text")
                        st.success("✅ 提示词已显示，请手动复制")
                
                with col4:
                    if st.button(f"📋 复制JSON", key=f"copy_json_{scene_num}"):
                        import json
                        json_str = json.dumps(edited_json, ensure_ascii=False, indent=2)
                        st.code(json_str, language="json")
                        st.success("✅ JSON已显示，请手动复制")
    else:
        st.info("👆 请先点击「生成提示词」按钮")
    
    # 导出区域
    st.markdown("---")
    st.subheader("💾 导出提示词")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 导出为TXT", key="export_txt"):
            if st.session_state.image_prompts:
                try:
                    import os
                    from datetime import datetime
                    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"分镜提示词_{timestamp}.txt"
                    filepath = os.path.join(desktop, filename)
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        for prompt_data in st.session_state.image_prompts:
                            if prompt_data.get("prompt_text"):
                                f.write(f"=== 分镜 {prompt_data['scene_number']} ===\n")
                                f.write(f"描述: {prompt_data.get('scene_description', '')}\n")
                                f.write(f"提示词: {prompt_data['prompt_text']}\n")
                                f.write(f"负面提示词: {prompt_data.get('negative_prompt', '')}\n")
                                f.write("\n")
                    
                    st.success(f"✅ 已保存到: {filepath}")
                except Exception as e:
                    st.error(f"❌ 导出失败: {str(e)}")
            else:
                st.warning("⚠️ 请先生成提示词")
    
    with col2:
        if st.button("📦 导出为JSON", key="export_json"):
            if st.session_state.image_prompts:
                try:
                    import os
                    import json
                    from datetime import datetime
                    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"分镜提示词_{timestamp}.json"
                    filepath = os.path.join(desktop, filename)
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(st.session_state.image_prompts, f, ensure_ascii=False, indent=2)
                    
                    st.success(f"✅ 已保存到: {filepath}")
                except Exception as e:
                    st.error(f"❌ 导出失败: {str(e)}")
            else:
                st.warning("⚠️ 请先生成提示词")
    
    with col3:
        if st.button("📊 导出Excel（含提示词）", key="export_excel_prompts"):
            if st.session_state.image_prompts:
                try:
                    # 更新导出工具以支持提示词
                    filepath = services["export_utils"].export_to_excel_with_prompts(
                        st.session_state.scenes,
                        st.session_state.image_prompts,
                        st.session_state.script
                    )
                    st.success(f"✅ 已保存到: {filepath}")
                except Exception as e:
                    st.error(f"❌ 导出失败: {str(e)}")
            else:
                st.warning("⚠️ 请先生成提示词")

def main():
    """主函数"""
    # 初始化
    init_session_state()
    services = init_services()
    config = render_sidebar()
    
    # 渲染项目管理（在侧边栏）
    render_project_manager(services)
    
    # 主标题
    st.title("🎬 剧本分镜生成系统（简化版）")
    st.caption("剧本输入 → AI自动分镜 → 编辑完善 → 生成提示词 → Excel导出")
    st.markdown("---")
    
    # 步骤导航
    steps = ["📝 输入剧本", "✂️ 分镜编辑", "🎨 生成提示词"]
    current_step = st.session_state.current_step
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if i + 1 == current_step:
                st.button(f"✅ {step}", disabled=True, use_container_width=True)
            elif i + 1 < current_step:
                if st.button(f"✓ {step}", use_container_width=True, key=f"nav_{i}"):
                    st.session_state.current_step = i + 1
                    st.rerun()
            else:
                st.button(f"{step}", disabled=True, use_container_width=True)
    
    st.markdown("---")
    
    # 根据步骤渲染界面
    if current_step == 1:
        if render_step1_script_input():
            # 开始分镜
            if not config["api_key"] and config["brand"] != "LM Studio":
                st.error("❌ 请先在侧边栏配置API Key")
            else:
                # 估算剧本长度
                script_length = len(st.session_state.script)
                estimated_time = "约1-3分钟"
                if script_length > 2000:
                    estimated_time = "约3-10分钟（长剧本需要更长时间）"
                
                try:
                    # 显示提示信息
                    st.info(f"⏳ 正在使用AI划分分镜头，预计需要{estimated_time}，请耐心等待...\n\n提示：由于需要精细划分（每个动作、每次对话切换），响应时间可能较长。")
                    
                    with st.spinner("正在精细划分分镜头，请稍候..."):
                        services["llm_service"].set_model(
                            config["brand"],
                            config["model"],
                            config["api_key"]
                        )
                        
                        scenes = services["llm_service"].divide_script(
                            st.session_state.script,
                            get_scene_division_prompt()
                        )
                        
                        validated_scenes = services["scene_parser"].validate_scenes(scenes)
                        st.session_state.scenes = validated_scenes
                        st.session_state.current_step = 2
                        st.success(f"✅ 成功划分出 {len(validated_scenes)} 个分镜头！")
                        st.rerun()
                
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"❌ 分镜划分失败: {error_msg}")
                    
                    # 针对不同错误类型给出特别提示
                    if "超时" in error_msg or "timeout" in error_msg.lower():
                        st.warning("💡 处理建议：")
                        st.markdown("""
                        1. **缩短剧本长度**：尝试将剧本分成几段分别处理
                        2. **检查网络**：确保网络连接稳定
                        3. **稍后重试**：API服务可能繁忙，稍后再试
                        4. **更换API服务**：尝试使用其他LLM服务（如Deepseek、通义千问等）
                        """)
                    elif "429" in error_msg or "负载已饱和" in error_msg or "rate limit" in error_msg.lower():
                        st.warning("💡 API服务繁忙，建议：")
                        st.markdown("""
                        1. **等待1-2分钟**：服务器负载饱和，稍等片刻后重试
                        2. **更换API服务**：尝试使用其他LLM服务
                           - Deepseek（推荐，性价比高）
                           - 通义千问
                           - 智谱GLM
                           - 月之暗面
                        3. **检查账户配额**：如果使用OpenAI，检查是否有足够配额
                        4. **分时段使用**：避开高峰期使用
                        """)
                        # 添加重试按钮
                        if st.button("🔄 立即重试", key="retry_division"):
                            st.rerun()
                    elif "401" in error_msg or "认证失败" in error_msg:
                        st.warning("💡 API Key问题，请检查：")
                        st.markdown("""
                        1. **API Key是否正确**：检查侧边栏中的API Key
                        2. **API Key是否过期**：某些服务商的Key有有效期
                        3. **是否有使用权限**：确认账户有访问该模型的权限
                        """)
                    elif "403" in error_msg or "权限不足" in error_msg:
                        st.warning("💡 权限问题，请检查：")
                        st.markdown("""
                        1. **账户余额**：检查账户是否有足够余额
                        2. **模型权限**：确认API Key可以访问所选模型
                        3. **服务状态**：检查服务商是否正常服务
                        """)
                    
                    with st.expander("🔍 查看详细错误"):
                        st.code(str(e))
    
    elif current_step == 2:
        render_step2_scene_editing(services)
    
    elif current_step == 3:
        render_step3_prompt_generation(services)
    
    # 底部导航
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ 上一步", disabled=current_step <= 1):
            st.session_state.current_step -= 1
            st.rerun()
    
    with col2:
        if st.button("➡️ 下一步", disabled=current_step >= 3 or not st.session_state.scenes):
            st.session_state.current_step += 1
            st.rerun()
    
    with col3:
        if st.button("🔄 重置所有"):
            for key in ["script", "scenes"]:
                if key == "scenes":
                    st.session_state[key] = []
                else:
                    st.session_state[key] = ""
            st.session_state.current_step = 1
            st.success("✅ 已重置")
            st.rerun()

if __name__ == "__main__":
    main()
