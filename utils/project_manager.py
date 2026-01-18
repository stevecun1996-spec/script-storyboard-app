"""
项目文件管理模块
用于保存、加载、管理分镜和提示词项目
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class ProjectManager:
    """项目管理器"""
    
    def __init__(self, projects_dir: str = None):
        """
        初始化项目管理器
        
        Args:
            projects_dir: 项目保存目录，默认在用户目录下的 .script_storyboard 文件夹
        """
        if projects_dir is None:
            # 默认保存在用户目录下
            home_dir = Path.home()
            self.projects_dir = home_dir / ".script_storyboard" / "projects"
        else:
            self.projects_dir = Path(projects_dir)
        
        # 确保目录存在
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def save_project(self, project_name: str, script: str, scenes: List[Dict], 
                    image_prompts: List[Dict] = None, metadata: Dict = None) -> str:
        """
        保存项目
        
        Args:
            project_name: 项目名称
            script: 剧本内容
            scenes: 分镜列表
            image_prompts: 提示词列表（可选）
            metadata: 元数据（可选）
        
        Returns:
            str: 保存的文件路径
        """
        # 生成文件名（去除特殊字符）
        safe_name = self._sanitize_filename(project_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.json"
        filepath = self.projects_dir / filename
        
        # 构建项目数据
        project_data = {
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "script": script,
            "scenes": scenes,
            "image_prompts": image_prompts or [],
            "metadata": metadata or {}
        }
        
        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def load_project(self, filepath: str) -> Dict[str, Any]:
        """
        加载项目
        
        Args:
            filepath: 项目文件路径
        
        Returns:
            Dict: 项目数据
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        return project_data
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """
        列出所有项目
        
        Returns:
            List[Dict]: 项目信息列表
        """
        projects = []
        
        # 遍历项目目录
        for filepath in self.projects_dir.glob("*.json"):
            try:
                # 读取项目信息（不加载完整内容）
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 获取文件修改时间
                stat = filepath.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime)
                
                projects.append({
                    "filename": filepath.name,
                    "filepath": str(filepath),
                    "project_name": data.get("project_name", filepath.stem),
                    "created_at": data.get("created_at", ""),
                    "updated_at": data.get("updated_at", mtime.isoformat()),
                    "script_length": len(data.get("script", "")),
                    "scene_count": len(data.get("scenes", [])),
                    "prompt_count": len(data.get("image_prompts", [])),
                    "file_size": stat.st_size,
                    "modified_time": mtime.isoformat()
                })
            except Exception as e:
                # 如果文件损坏，跳过
                print(f"Error loading project {filepath}: {e}")
                continue
        
        # 按修改时间排序（最新的在前）
        projects.sort(key=lambda x: x.get("modified_time", ""), reverse=True)
        
        return projects
    
    def delete_project(self, filepath: str) -> bool:
        """
        删除项目
        
        Args:
            filepath: 项目文件路径
        
        Returns:
            bool: 是否删除成功
        """
        try:
            path = Path(filepath)
            if path.exists() and path.parent == self.projects_dir:
                path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting project {filepath}: {e}")
            return False
    
    def rename_project(self, old_filepath: str, new_name: str) -> Optional[str]:
        """
        重命名项目
        
        Args:
            old_filepath: 原文件路径
            new_name: 新项目名称
        
        Returns:
            Optional[str]: 新文件路径，如果失败返回None
        """
        try:
            old_path = Path(old_filepath)
            if not old_path.exists() or old_path.parent != self.projects_dir:
                return None
            
            # 生成新文件名（保留时间戳）
            safe_name = self._sanitize_filename(new_name)
            # 尝试从旧文件名中提取时间戳
            old_stem = old_path.stem
            if "_" in old_stem:
                parts = old_stem.rsplit("_", 1)
                if len(parts) == 2 and len(parts[1]) == 15:  # 时间戳格式：YYYYMMDD_HHMMSS
                    timestamp = parts[1]
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            new_filename = f"{safe_name}_{timestamp}.json"
            new_path = self.projects_dir / new_filename
            
            # 重命名文件
            old_path.rename(new_path)
            
            # 更新项目数据中的名称
            project_data = self.load_project(str(new_path))
            project_data["project_name"] = new_name
            project_data["updated_at"] = datetime.now().isoformat()
            
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            
            return str(new_path)
        except Exception as e:
            print(f"Error renaming project {old_filepath}: {e}")
            return None
    
    def update_project(self, filepath: str, script: str = None, scenes: List[Dict] = None,
                      image_prompts: List[Dict] = None, metadata: Dict = None) -> bool:
        """
        更新项目
        
        Args:
            filepath: 项目文件路径
            script: 更新的剧本内容（可选）
            scenes: 更新的分镜列表（可选）
            image_prompts: 更新的提示词列表（可选）
            metadata: 更新的元数据（可选）
        
        Returns:
            bool: 是否更新成功
        """
        try:
            # 加载现有项目
            project_data = self.load_project(filepath)
            
            # 更新字段（只更新提供的字段）
            if script is not None:
                project_data["script"] = script
            if scenes is not None:
                project_data["scenes"] = scenes
            if image_prompts is not None:
                project_data["image_prompts"] = image_prompts
            if metadata is not None:
                project_data["metadata"].update(metadata)
            
            # 更新修改时间
            project_data["updated_at"] = datetime.now().isoformat()
            
            # 保存更新
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error updating project {filepath}: {e}")
            return False
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除特殊字符
        
        Args:
            filename: 原始文件名
        
        Returns:
            str: 清理后的文件名
        """
        # 移除或替换不允许的字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename.strip()
    
    def get_project_stats(self, filepath: str) -> Dict[str, Any]:
        """
        获取项目统计信息
        
        Args:
            filepath: 项目文件路径
        
        Returns:
            Dict: 统计信息
        """
        try:
            project_data = self.load_project(filepath)
            return {
                "project_name": project_data.get("project_name", ""),
                "script_length": len(project_data.get("script", "")),
                "scene_count": len(project_data.get("scenes", [])),
                "prompt_count": len(project_data.get("image_prompts", [])),
                "created_at": project_data.get("created_at", ""),
                "updated_at": project_data.get("updated_at", "")
            }
        except Exception as e:
            return {"error": str(e)}



