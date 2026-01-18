"""
提示词生成专用系统提示词
用于 LLM 辅助生成更准确的 JSON 提示词
"""

PROMPT_GENERATION_SYSTEM_PROMPT = """你是一个专业的电影分镜转文生图提示词生成专家。你的任务是根据分镜描述和剧本上下文，提取视觉元素并生成结构化的 JSON 提示词。

## 任务要求

1. **准确提取视觉元素**：
   - 从分镜描述中提取人物的动作、姿势、表情、服装、道具
   - 提取场景环境、地点、天气、时间
   - 提取人物与背景的关系

2. **基于上下文分析姿势和表情**（重要）：
   - **姿势分析**：根据前后分镜的剧情发展，推断人物在当前分镜中的姿势
     * 如果前一个分镜是"奔跑"，当前分镜是"停下"，姿势应该是"急停、身体前倾、双手撑膝"
     * 如果前一个分镜是"对话"，当前分镜是"转身离开"，姿势应该是"转身、背对镜头、肩膀紧绷"
     * 考虑情绪状态：愤怒时可能是"握拳、挺胸、身体前倾"；悲伤时可能是"低头、肩膀下垂、双手无力"
   - **表情分析**：根据剧情上下文和情绪设计，推断人物的表情
     * 如果前一个分镜是"收到坏消息"，当前分镜是"反应"，表情应该是"震惊、瞳孔放大、嘴巴微张"
     * 如果前一个分镜是"对峙"，当前分镜是"特写"，表情应该是"紧张、眼神锐利、眉头紧锁"
     * 考虑情绪设计：如果是"情绪错位"，表情可能与表面情绪不一致；如果是"情绪叠加"，表情可能混合多种情绪

3. **生成准确的翻译**：
   - 将中文描述准确翻译成英文
   - 保持专业术语的准确性（如镜头语言、摄影术语）

4. **结构化输出**：
   - 严格按照 JSON 格式输出
   - 确保所有字段都有合理的值

## 输出格式

请严格按照以下 JSON 格式输出，不要添加任何额外的说明文字：

```json
{
  "subject": {
    "main_character": "主要人物名称",
    "action": "动作描述（中文 / English）",
    "pose": "姿势描述（中文 / English）",
    "expression": "表情描述（中文 / English）",
    "clothing": "服装描述（中文 / English）",
    "props": "道具描述（中文 / English）",
    "full_description": "完整分镜描述（中文 / English）"
  },
  "scene": {
    "environment": "环境描述（中文 / English）",
    "location": "地点（中文 / English）",
    "weather": "天气（中文 / English）",
    "time": "时间（中文 / English）",
    "full_description": "完整场景描述"
  },
  "character_background_relation": "人物与背景的关系描述（中文 / English）"
}
```

## 注意事项

1. **姿势字段是必填项**（重要）：
   - **除非是纯空镜**（画面中完全不涉及任何人物，只有环境、风景、建筑等），否则必须填写姿势字段
   - 如果分镜描述中没有明确说明姿势，必须根据以下信息推断：
     * 根据动作推断：如果描述是"奔跑"，姿势应该是"身体前倾、双腿交替、手臂摆动"
     * 根据景别推断：如果是"特写"，姿势可能是"头部特写、颈部以上"；如果是"全景"，姿势可能是"全身站立、双手自然下垂"
     * 根据情绪推断：如果是"愤怒"，姿势可能是"握拳、挺胸、身体前倾"；如果是"悲伤"，姿势可能是"低头、肩膀下垂"
     * 根据前后分镜推断：结合剧情发展，推断当前分镜的姿势
   - **空镜判断标准**：如果分镜描述中完全没有提到人物、角色、人、主角等词汇，且只描述环境、风景、建筑、物品等，则可以留空姿势字段
   - 姿势描述要具体：不要只写"站立"、"坐着"，要写"昂首站立、双手叉腰"、"盘腿而坐、身体前倾"

2. **姿势和表情必须基于上下文分析**：不要只从当前分镜描述中提取，要结合前后分镜的剧情发展来推断
3. 如果某个字段在分镜描述中没有明确信息，使用合理的默认值或留空（但姿势除外，必须推断）
4. 双语模式下，确保中英文都准确
5. 保持专业术语的准确性
6. 只输出 JSON，不要添加任何解释文字
"""

def get_visual_elements_extraction_prompt(
    scene_description: str, 
    characters: list, 
    language: str = "bilingual",
    previous_scene: str = None,
    next_scene: str = None,
    emotion_design: str = None,
    performance_style: str = None
) -> str:
    """
    生成视觉元素提取的提示词
    
    Args:
        scene_description: 分镜描述
        characters: 人物列表
        language: 语言模式（bilingual/chinese/english）
        previous_scene: 前一个分镜的描述（用于上下文分析）
        next_scene: 下一个分镜的描述（用于上下文分析）
        emotion_design: 情绪设计（如"情绪一致"、"情绪错位"等）
        performance_style: 表演风格（如"内敛表演"、"外放表演"等）
    
    Returns:
        str: 用户提示词
    """
    chars_text = "、".join(characters) if characters else "人物"
    
    # 构建上下文信息
    context_parts = []
    if previous_scene:
        context_parts.append(f"**前一个分镜**：{previous_scene}")
    if next_scene:
        context_parts.append(f"**下一个分镜**：{next_scene}")
    context_text = "\n".join(context_parts) if context_parts else "无"
    
    # 构建创作维度信息
    creative_parts = []
    if emotion_design:
        creative_parts.append(f"**情绪设计**：{emotion_design}")
    if performance_style:
        creative_parts.append(f"**表演风格**：{performance_style}")
    creative_text = "\n".join(creative_parts) if creative_parts else "无特殊要求"
    
    prompt = f"""请分析以下分镜描述，结合上下文信息，提取视觉元素并生成结构化的 JSON 提示词。

## 当前分镜信息

**人物**：{chars_text}
**描述**：{scene_description}

## 上下文信息（用于分析姿势和表情）

{context_text}

## 创作维度

{creative_text}

## 分析要求

1. **姿势分析**（必填项，除非是纯空镜）：
   - **姿势字段是必填项**：除非当前分镜是纯空镜（完全不涉及人物），否则必须填写姿势
   - 根据前后分镜的剧情发展，推断人物在当前分镜中的姿势
   - 考虑动作的连贯性：如果前一个分镜是"奔跑"，当前是"停下"，姿势应该是"急停、身体前倾、双手撑膝"
   - 考虑情绪状态：愤怒时可能是"握拳、挺胸、身体前倾"；悲伤时可能是"低头、肩膀下垂、双手无力"
   - 如果表演风格是"内敛表演"，姿势应该更克制；如果是"外放表演"，姿势应该更夸张
   - 姿势描述要具体：不要只写"站立"、"坐着"，要写"昂首站立、双手叉腰"、"盘腿而坐、身体前倾"
   - **空镜判断**：如果分镜描述中完全没有提到人物、角色、人、主角等词汇，且只描述环境、风景、建筑、物品等，则可以留空姿势字段

2. **表情分析**（重要）：
   - 根据剧情上下文和情绪设计，推断人物的表情
   - 如果前一个分镜是"收到坏消息"，当前分镜是"反应"，表情应该是"震惊、瞳孔放大"
   - 如果情绪设计是"情绪错位"，表情可能与表面情绪不一致（如表面平静但眼神紧张）
   - 如果情绪设计是"情绪叠加"，表情可能混合多种情绪（如"决绝中带着痛苦"）
   - 如果表演风格是"内敛表演"，表情应该更微妙；如果是"外放表演"，表情应该更明显

3. 仔细分析分镜描述，提取所有视觉元素
4. 准确翻译为英文（如果是双语模式）
5. 如果某些信息不明确，使用合理的推断
6. 严格按照 JSON 格式输出，不要添加任何说明文字

请开始分析并输出 JSON："""
    
    return prompt

def get_translation_prompt(text: str, target_language: str = "english") -> str:
    """
    生成翻译提示词
    
    Args:
        text: 要翻译的文本
        target_language: 目标语言
    
    Returns:
        str: 用户提示词
    """
    prompt = f"""请将以下中文文本准确翻译成{target_language}，保持专业术语的准确性。

**原文**：{text}

**要求**：
1. 准确翻译，不要遗漏信息
2. 保持专业术语的准确性（如镜头语言、摄影术语）
3. 如果涉及电影术语，使用标准的英文表达
4. 只输出翻译结果，不要添加任何说明

请翻译："""
    
    return prompt
