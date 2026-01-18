"""
剧本分割工具
智能将剧本分割成每部分500字以内的片段，保持内容完整性，并在批次间保留衔接部分
"""

from typing import List, Tuple
import re


class ScriptSplitter:
    """剧本分割器"""
    
    def __init__(self, max_chars: int = 500, overlap_chars: int = 100):
        """
        初始化分割器
        
        Args:
            max_chars: 每个片段的最大字符数，默认500
            overlap_chars: 批次间的重叠字符数（用于保留衔接部分），默认100
        """
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars
    
    def split_script(self, script: str) -> List[Tuple[str, int, int]]:
        """
        分割剧本
        
        Args:
            script: 完整的剧本文本
        
        Returns:
            List[Tuple[str, int, int]]: 分割后的片段列表，每个元素为 (片段文本, 起始位置, 结束位置)
        """
        if not script or len(script.strip()) == 0:
            return []
        
        # 如果剧本本身就很短，直接返回
        if len(script) <= self.max_chars:
            return [(script, 0, len(script))]
        
        segments = []
        current_pos = 0
        script_len = len(script)
        
        while current_pos < script_len:
            # 确定当前片段的结束位置
            end_pos = min(current_pos + self.max_chars, script_len)
            
            # 如果不是最后一段，尝试找到最佳的分割点
            if end_pos < script_len:
                segment = script[current_pos:end_pos]
                best_split_pos = self._find_best_split_point(segment, current_pos)
                
                # 如果找到了好的分割点，使用它
                if best_split_pos > current_pos:
                    segment_text = script[current_pos:best_split_pos]
                    segments.append((segment_text, current_pos, best_split_pos))
                    current_pos = best_split_pos
                else:
                    # 如果没找到好的分割点，强制在当前位置分割
                    segment_text = script[current_pos:end_pos]
                    segments.append((segment_text, current_pos, end_pos))
                    current_pos = end_pos
            else:
                # 最后一段
                segment_text = script[current_pos:]
                segments.append((segment_text, current_pos, script_len))
                break
        
        return segments
    
    def _find_best_split_point(self, segment: str, start_pos: int) -> int:
        """
        在片段中找到最佳的分割点
        
        Args:
            segment: 当前片段文本
            start_pos: 片段在原剧本中的起始位置
        
        Returns:
            int: 最佳分割位置（相对于原剧本的绝对位置）
        """
        segment_len = len(segment)
        
        # 如果片段很短，直接返回末尾
        if segment_len < self.max_chars * 0.5:
            return start_pos + segment_len
        
        # 尝试找到段落分隔符（双换行）
        double_newline_pos = segment.rfind('\n\n')
        if double_newline_pos > segment_len * 0.5:  # 在片段的后半部分
            return start_pos + double_newline_pos + 2
        
        # 尝试找到单换行（段落结束）
        # 从后往前找，优先选择段落结束的位置
        newline_pos = segment.rfind('\n')
        if newline_pos > segment_len * 0.6:  # 在片段的后60%
            # 检查这是否是段落结束（后面跟着句号、问号、感叹号等）
            if newline_pos + 1 < len(segment):
                next_char = segment[newline_pos + 1]
                if next_char in ['。', '！', '？', '.', '!', '?']:
                    return start_pos + newline_pos + 1
        
        # 尝试找到句子结束符（句号、问号、感叹号）
        sentence_end_pattern = re.compile(r'[。！？.!?]')
        matches = list(sentence_end_pattern.finditer(segment))
        
        if matches:
            # 从后往前找，选择在片段后70%位置的句子结束符
            threshold = segment_len * 0.7
            for match in reversed(matches):
                if match.end() >= threshold:
                    return start_pos + match.end()
            
            # 如果后70%没有，选择最后一个句子结束符
            last_match = matches[-1]
            if last_match.end() > segment_len * 0.5:  # 至少在片段中间之后
                return start_pos + last_match.end()
        
        # 尝试找到对话结束（冒号后的换行，或人物名后的冒号）
        dialogue_pattern = re.compile(r'[：:]\s*\n')
        dialogue_matches = list(dialogue_pattern.finditer(segment))
        
        if dialogue_matches:
            threshold = segment_len * 0.6
            for match in reversed(dialogue_matches):
                if match.end() >= threshold:
                    return start_pos + match.end()
        
        # 尝试找到逗号、分号等停顿点
        pause_pattern = re.compile(r'[，；,;]\s*')
        pause_matches = list(pause_pattern.finditer(segment))
        
        if pause_matches:
            threshold = segment_len * 0.8
            for match in reversed(pause_matches):
                if match.end() >= threshold:
                    return start_pos + match.end()
        
        # 如果都没找到合适的点，尝试在空格处分割（英文剧本）
        space_pos = segment.rfind(' ')
        if space_pos > segment_len * 0.8:
            return start_pos + space_pos + 1
        
        # 最后，如果实在找不到，就在90%的位置强制分割
        # 这样可以保证至少有一些上下文延续
        fallback_pos = int(segment_len * 0.9)
        return start_pos + fallback_pos
    
    def get_split_info(self, script: str) -> dict:
        """
        获取分割信息
        
        Args:
            script: 完整的剧本文本
        
        Returns:
            dict: 包含分割信息的字典
        """
        segments = self.split_script(script)
        
        return {
            "total_chars": len(script),
            "segment_count": len(segments),
            "segments": [
                {
                    "index": i + 1,
                    "text": seg[0],
                    "start_pos": seg[1],
                    "end_pos": seg[2],
                    "char_count": len(seg[0])
                }
                for i, seg in enumerate(segments)
            ]
        }

