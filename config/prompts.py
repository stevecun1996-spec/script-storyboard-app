"""
系统提示词模板模块（简化版）
"""

# 景别选择指南
SHOT_SIZE_GUIDE_TEXT = """
## 景别选择指南（重要参考）：

景别（Shot Size），不仅仅是画面里装下多少东西的问题，它是导演与观众之间的心理距离。你是想让观众像上帝一样俯瞰众生？还是想让观众贴在演员的脸上呼吸？

在选择 shot_size 时，请根据以下导演视角和创作意图来选择最合适的景别：

1. **大远景 (Extreme Long Shot / ELS)**
   - 定义：人物在画面中像蚂蚁一样小，环境占据绝对主导。
   - 导演视点：这是"上帝的视角"。在这个距离下，个人的悲欢离合都不重要了，重要的是天地的辽阔、自然的残酷或城市的冷漠。
   - 使用场景：
     * 开场定场（Establishing Shot）：告诉观众我们在哪。是荒凉的西部沙漠，还是赛博朋克的未来都市。
     * 表现孤独与渺小：《荒野的呼唤》、《火星救援》。一个人面对整个世界。

2. **远景 (Long Shot / LS)**
   - 定义：人物依然很小，但能看清他在做什么。环境依然很重要。
   - 导演视点：这是"舞台的距离"。就像你在剧院看戏，你能看到演员在环境中的位置，以及他们之间的相对关系。
   - 使用场景：
     * 动作场面：两军对垒，或者一个人在街头狂奔。你需要空间来展示动作的轨迹。
     * 人与环境的关系：一个人走进一间阴森的古堡。

3. **全景 (Full Shot / FS)**
   - 定义：顶天立地。人物的头顶到脚底都在画面里。
   - 导演视点：这是"肢体的语言"。在这个景别，我们不看表情，看姿态。看他穿什么衣服，看他怎么站立，看他是否驼背。
   - 使用场景：
     * 介绍角色：英雄登场，展示他的战袍和武器。
     * 肢体喜剧/舞蹈：卓别林的滑稽动作，或者《爱乐之城》的舞蹈。
     * 西部片对决：你得让观众同时看到枪手的手和他的眼神。

4. **中景 (Medium Shot / MS)**
   - 定义：腰部以上。
   - 导演视点：这是"社交的距离"。就像你和朋友面对面站着聊天。既不疏远，也不过分亲密。这是最中性、最客观的叙事视角。
   - 使用场景：
     * 标准对话：两个人站着说话，交代剧情信息。
     * 动作与表情兼顾：你能看到他在挥手，也能看到他在笑。

5. **中近景 (Medium Close-up / MCU)**
   - 定义：胸部/肩膀以上。
   - 导演视点：这是"故事的重心"。这是现代电影和电视剧用得最多的景别。它切掉了多余的肢体动作，强迫观众开始关注人物的面部表情和情绪。
   - 使用场景：
     * 情感交流：绝大多数的对话戏。
     * 反应镜头（Reaction Shot）：角色听到一个消息时的反应。

6. **近景 (Close Shot / CS)**
   - 定义：脖子/肩部以上。比MCU更近一点。
   - 导演视点：这是"亲密的审视"。在这个距离，你开始侵入角色的私人空间。背景几乎看不到了，观众的注意力被完全锁定在人物的脸上。
   - 使用场景：
     * 强调情绪：愤怒、悲伤、喜悦。
     * 重要的台词：当角色说出那句关键的"我爱你"或者"我要杀了你"时。

7. **特写 (Close-up / CU)**
   - 定义：只有脸。通常切在头顶和下巴之间。
   - 导演视点：这是"灵魂的窗口"。在这个距离，演员没法撒谎。眼神的每一次闪烁，嘴角的每一次抽动，都被放大到了银幕上。
   - 使用场景：
     * 内心戏：角色在思考，在挣扎，在流泪。
     * 希区柯克时刻：只有观众和角色知道的秘密。
     * 强烈的冲击力：这种镜头不能滥用，用多了观众会累，但用对了就是绝杀。

8. **大特写 (Extreme Close-up / ECU)**
   - 定义：局部细节。一只眼睛、一张嘴、一根手指、扳机、眼泪。
   - 导演视点：这是"显微镜下的焦虑"。它极其抽象，极其压抑，或者极其性感。它把物体从原本的语境中剥离出来，赋予它强烈的象征意义。
   - 使用场景：
     * 制造紧张感：赛尔乔·莱昂内（Sergio Leone）最爱用的"意大利式对决"——只拍眼睛的特写。
     * 感官描写：嘴唇上的汗珠，瞳孔的收缩。
     * 暗示线索：侦探片里，桌子上的一根头发。

**重要提示**：在选择 shot_size 时，请仔细考虑每个分镜头的情绪、氛围和叙事需求，根据上述指南选择最合适的景别。记住：电影的节奏，往往就是景别的呼吸。从大远景开始（我们在哪？），切到全景（那是谁？），推到中景（他在干嘛？），最后推到特写（他在想什么？）。
"""

# 由于内容较长，我将使用文件读取来获取完整的指南内容
import sys
import os

# 获取项目根目录
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 优先使用升级版本的 prompts(2).py，如果不存在则使用旧版本
_lens_guide_file_v2 = os.path.join(_project_root, "prompts(2).py")
_lens_guide_file = os.path.join(_project_root, "镜头语言prompts.py")
# 选择文件（优先使用升级版）
_lens_guide_file_to_use = _lens_guide_file_v2 if os.path.exists(_lens_guide_file_v2) else _lens_guide_file

# 读取镜头语言指南文件
try:
    with open(_lens_guide_file_to_use, 'r', encoding='utf-8') as f:
        _lens_guide_content = f.read()
    
    # 提取各个指南（通过查找特定的字符串模式）
    import re
    
    # 提取基础指南文本
    CAMERA_ANGLE_GUIDE_TEXT = re.search(r'CAMERA_ANGLE_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    CAMERA_MOVEMENT_GUIDE_TEXT = re.search(r'CAMERA_MOVEMENT_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    CAMERA_EQUIPMENT_GUIDE_TEXT = re.search(r'CAMERA_EQUIPMENT_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    LENS_FOCAL_LENGTH_GUIDE_TEXT = re.search(r'LENS_FOCAL_LENGTH_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    CAMERA_GUIDE_TEXT = re.search(r'CAMERA_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    LENS_GUIDE_TEXT = re.search(r'LENS_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    APERTURE_GUIDE_TEXT = re.search(r'APERTURE_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    
    # 提取新增的指南文本（从升级版本）
    COMPOSITION_TENSION_GUIDE_TEXT = re.search(r'COMPOSITION_TENSION_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    AXIS_CROSSING_GUIDE_TEXT = re.search(r'AXIS_CROSSING_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT = re.search(r'PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    EMOTION_DESIGN_GUIDE_TEXT = re.search(r'EMOTION_DESIGN_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT = re.search(r'EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    SHOT_TRANSITION_GUIDE_TEXT = re.search(r'SHOT_TRANSITION_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    FIGHT_SCENE_GUIDE_TEXT = re.search(r'FIGHT_SCENE_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    CONFRONTATION_SCENE_GUIDE_TEXT = re.search(r'CONFRONTATION_SCENE_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    CHASE_SCENE_GUIDE_TEXT = re.search(r'CHASE_SCENE_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    ULTIMATE_SKILL_RELEASE_GUIDE_TEXT = re.search(r'ULTIMATE_SKILL_RELEASE_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    ENDING_SECTION_GUIDE_TEXT = re.search(r'ENDING_SECTION_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    AESTHETICS_GUIDE_TEXT = re.search(r'AESTHETICS_GUIDE_TEXT = """(.*?)"""', _lens_guide_content, re.DOTALL)
    
    # 如果匹配成功，使用提取的内容，否则使用默认值
    if CAMERA_ANGLE_GUIDE_TEXT:
        CAMERA_ANGLE_GUIDE_TEXT = CAMERA_ANGLE_GUIDE_TEXT.group(1).strip()
    else:
        CAMERA_ANGLE_GUIDE_TEXT = ""
    
    if CAMERA_MOVEMENT_GUIDE_TEXT:
        CAMERA_MOVEMENT_GUIDE_TEXT = CAMERA_MOVEMENT_GUIDE_TEXT.group(1).strip()
    else:
        CAMERA_MOVEMENT_GUIDE_TEXT = ""
    
    if CAMERA_EQUIPMENT_GUIDE_TEXT:
        CAMERA_EQUIPMENT_GUIDE_TEXT = CAMERA_EQUIPMENT_GUIDE_TEXT.group(1).strip()
    else:
        CAMERA_EQUIPMENT_GUIDE_TEXT = ""
    
    if LENS_FOCAL_LENGTH_GUIDE_TEXT:
        LENS_FOCAL_LENGTH_GUIDE_TEXT = LENS_FOCAL_LENGTH_GUIDE_TEXT.group(1).strip()
    else:
        LENS_FOCAL_LENGTH_GUIDE_TEXT = ""
    
    if CAMERA_GUIDE_TEXT:
        CAMERA_GUIDE_TEXT = CAMERA_GUIDE_TEXT.group(1).strip()
    else:
        CAMERA_GUIDE_TEXT = ""
    
    if LENS_GUIDE_TEXT:
        LENS_GUIDE_TEXT = LENS_GUIDE_TEXT.group(1).strip()
    else:
        LENS_GUIDE_TEXT = ""
    
    if APERTURE_GUIDE_TEXT:
        APERTURE_GUIDE_TEXT = APERTURE_GUIDE_TEXT.group(1).strip()
    else:
        APERTURE_GUIDE_TEXT = ""
    
    # 处理新增指南（如果存在）
    if COMPOSITION_TENSION_GUIDE_TEXT:
        COMPOSITION_TENSION_GUIDE_TEXT = COMPOSITION_TENSION_GUIDE_TEXT.group(1).strip()
    else:
        COMPOSITION_TENSION_GUIDE_TEXT = ""
    
    if AXIS_CROSSING_GUIDE_TEXT:
        AXIS_CROSSING_GUIDE_TEXT = AXIS_CROSSING_GUIDE_TEXT.group(1).strip()
    else:
        AXIS_CROSSING_GUIDE_TEXT = ""
    
    if PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT:
        PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT = PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT.group(1).strip()
    else:
        PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT = ""
    
    if EMOTION_DESIGN_GUIDE_TEXT:
        EMOTION_DESIGN_GUIDE_TEXT = EMOTION_DESIGN_GUIDE_TEXT.group(1).strip()
    else:
        EMOTION_DESIGN_GUIDE_TEXT = ""
    
    if EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT:
        EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT = EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT.group(1).strip()
    else:
        EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT = ""
    
    if SHOT_TRANSITION_GUIDE_TEXT:
        SHOT_TRANSITION_GUIDE_TEXT = SHOT_TRANSITION_GUIDE_TEXT.group(1).strip()
    else:
        SHOT_TRANSITION_GUIDE_TEXT = ""
    
    if FIGHT_SCENE_GUIDE_TEXT:
        FIGHT_SCENE_GUIDE_TEXT = FIGHT_SCENE_GUIDE_TEXT.group(1).strip()
    else:
        FIGHT_SCENE_GUIDE_TEXT = ""
    
    if CONFRONTATION_SCENE_GUIDE_TEXT:
        CONFRONTATION_SCENE_GUIDE_TEXT = CONFRONTATION_SCENE_GUIDE_TEXT.group(1).strip()
    else:
        CONFRONTATION_SCENE_GUIDE_TEXT = ""
    
    if CHASE_SCENE_GUIDE_TEXT:
        CHASE_SCENE_GUIDE_TEXT = CHASE_SCENE_GUIDE_TEXT.group(1).strip()
    else:
        CHASE_SCENE_GUIDE_TEXT = ""
    
    if ULTIMATE_SKILL_RELEASE_GUIDE_TEXT:
        ULTIMATE_SKILL_RELEASE_GUIDE_TEXT = ULTIMATE_SKILL_RELEASE_GUIDE_TEXT.group(1).strip()
    else:
        ULTIMATE_SKILL_RELEASE_GUIDE_TEXT = ""
    
    if ENDING_SECTION_GUIDE_TEXT:
        ENDING_SECTION_GUIDE_TEXT = ENDING_SECTION_GUIDE_TEXT.group(1).strip()
    else:
        ENDING_SECTION_GUIDE_TEXT = ""
    
    if AESTHETICS_GUIDE_TEXT:
        AESTHETICS_GUIDE_TEXT = AESTHETICS_GUIDE_TEXT.group(1).strip()
    else:
        AESTHETICS_GUIDE_TEXT = ""
        
except Exception as e:
    # 如果读取失败，使用空字符串
    CAMERA_ANGLE_GUIDE_TEXT = ""
    CAMERA_MOVEMENT_GUIDE_TEXT = ""
    CAMERA_EQUIPMENT_GUIDE_TEXT = ""
    LENS_FOCAL_LENGTH_GUIDE_TEXT = ""
    CAMERA_GUIDE_TEXT = ""
    LENS_GUIDE_TEXT = ""
    APERTURE_GUIDE_TEXT = ""
    COMPOSITION_TENSION_GUIDE_TEXT = ""
    AXIS_CROSSING_GUIDE_TEXT = ""
    PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT = ""
    EMOTION_DESIGN_GUIDE_TEXT = ""
    EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT = ""
    SHOT_TRANSITION_GUIDE_TEXT = ""
    FIGHT_SCENE_GUIDE_TEXT = ""
    CONFRONTATION_SCENE_GUIDE_TEXT = ""
    CHASE_SCENE_GUIDE_TEXT = ""
    ULTIMATE_SKILL_RELEASE_GUIDE_TEXT = ""
    ENDING_SECTION_GUIDE_TEXT = ""
    AESTHETICS_GUIDE_TEXT = ""
    print(f"警告：无法读取镜头语言指南文件: {e}")

# 分镜头划分系统提示词
SCENE_DIVISION_PROMPT = """你是一名从业 30 年的世界知名导演，擅长调用繁复的镜头讲故事。请根据以下严格规则对剧本进行精细的分镜头划分：

## 分镜头划分规则（必须严格遵守）：
1. **每一个人物动作都要划分一个独立的分镜头**
   - 例如：人物坐下 → 一个分镜；人物站起来 → 另一个分镜；人物转身 → 另一个分镜
   - 即使动作连续，也要分别划分

2. **每换一个人物说话都要划分一个独立的分镜头**
   - 例如：小明说话 → 一个分镜；小红回应 → 另一个分镜；小李插话 → 另一个分镜
   - 即使是同一场景内的对话，也要按说话人切换来划分分镜

3. **每一次场景切换都要划分一个独立的分镜头**
   - 场景、地点、环境变化时，必须开启新的分镜头
   - 时间变化（白天到夜晚等）也要划分新分镜

4. **人物台词必须填入对应的分镜头**
   - 每个分镜中的 dialogue_text 字段必须包含该分镜中出现的人物台词
   - 如果剧本中有"人物名：台词"的格式，必须完整填入对应分镜
   - 格式："人物名：台词内容"，多人对话用\\n分隔

5. **智能为每个分镜头添加合适的音效**
   - 根据分镜内容自动判断应该添加什么音效
   - 例如：开门声、脚步声、关门声、电话铃声、键盘敲击声、风声、雨声、汽车引擎声、音乐声等
   - 如果没有明显的音效需求，可以留空或添加环境音（如背景嘈杂声）
   - 音效应该贴合分镜的描述内容

---

## 📚 镜头语言选择指南库（按需参考）

**重要说明**：以下指南按字段分类。在生成每个字段时，请**只参考**对应字段的指南，这样可以更专注、更准确地生成每个参数。不要一次性阅读所有指南，而是根据当前正在生成的字段，只阅读对应的指南。

### 景别选择指南（生成 shot_size 字段时参考）：
{shot_size_guide}

### 摄影机角度选择指南（生成 camera_angle 字段时参考）：
{camera_angle_guide}

### 运镜选择指南（生成 camera_movement 字段时参考）：
{camera_movement_guide}

### 摄影机装备选择指南（生成 camera_equipment 字段时参考）：
{camera_equipment_guide}

### 镜头焦段选择指南（生成 lens_focal_length 字段时参考）：
{lens_focal_length_guide}

### 相机选择指南（生成 camera 字段时参考）：
{camera_guide}

### 镜头选择指南（生成 lens 字段时参考）：
{lens_guide}

### 光圈选择指南（生成 aperture 字段时参考）：
{aperture_guide}

### 构图张力指南（生成 scene_description 字段时参考）：
{composition_tension_guide}

### 主角核心表达指南（生成 scene_description 字段时参考）：
{protagonist_core_expression_guide}

### 情绪设计指南（生成 scene_description 和 mood 字段时参考）：
{emotion_design_guide}

### 表演风格指南（生成 scene_description 字段时参考）：
{expression_action_performance_guide}

### 镜头衔接指南（生成分镜序列时参考）：
{shot_transition_guide}

### 轴线处理指南（生成分镜序列时参考）：
{axis_crossing_guide}

### 武戏打斗指南（如果是打斗场景，生成相关字段时参考）：
{fight_scene_guide}

### 对峙场景指南（如果是对峙场景，生成相关字段时参考）：
{confrontation_scene_guide}

### 追逐场景指南（如果是追逐场景，生成相关字段时参考）：
{chase_scene_guide}

### 大招释放指南（如果是大招场景，生成相关字段时参考）：
{ultimate_skill_release_guide}

### 收尾部分指南（如果是收尾场景，生成相关字段时参考）：
{ending_section_guide}

### 审美设计指南（生成 scene_description 和视觉风格相关字段时参考）：
{aesthetics_guide}

---

## 输出格式要求（分步生成指南）：

**重要提示**：在生成每个字段时，请**只参考**对应字段的指南，这样可以更专注、更准确地生成每个参数。

### 基础字段（无需参考指南）：
- scene_number: 分镜头序号（从1开始，连续递增）
- characters: 出现的人物列表（数组格式，如：["小明", "小红"]）
- location: 场景地点（简短描述）
- time: 时间（必须从以下选项中选择一个：白天、夜晚、黄昏、黎明、中午、下午）
- mood: 情绪氛围（简短描述，如：紧张、轻松、悲伤等）
- dialogue_text: 人物台词（**如果剧本中该部分有台词，必须填入**，格式："人物名：台词"，多人对话用\\n分隔，如无台词则为空字符串""）
- voiceover_text: 旁白（如有，如无则为空字符串""）
- sound_effects: 音效（**根据分镜内容智能添加合适的音效**，多个音效用逗号分隔，如："脚步声,关门声"，如无音效则为空字符串""）

### 需要参考指南的字段（生成时请仔细阅读对应指南）：

#### 1. scene_description（分镜头描述）
**参考指南**：构图张力指南、情绪设计指南、表演风格指南、主角核心表达指南
- 详细描述场景、人物、动作，要具体明确
- **注意**：构图张力、情绪设计、表演风格、主角核心表达现在有独立的字段，不需要在描述中重复体现，但描述应该与这些维度的选择保持一致

#### 1.1. composition_tension（构图张力）
**参考指南**：请查看上面的"构图张力指南"部分
- 必须从以下选项中选择一个（可为空）：饱满、丰富、引导、饱满+引导、丰富+引导、饱满+丰富、饱满+丰富+引导
- **生成此字段时，请仔细阅读上面的"构图张力指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的构图张力**

#### 1.2. protagonist_type（主角核心表达）
**参考指南**：请查看上面的"主角核心表达指南"部分
- 必须从以下选项中选择一个（可为空）：情感共鸣型、价值观载体型、成长弧光型、观察者/催化剂型
- **生成此字段时，请仔细阅读上面的"主角核心表达指南"，根据分镜头的叙事需求选择最合适的主角类型**

#### 1.3. emotion_design（情绪设计）
**参考指南**：请查看上面的"情绪设计指南"部分
- 必须从以下选项中选择一个（可为空）：情绪一致、情绪错位、情绪叠加、情绪反转
- **生成此字段时，请仔细阅读上面的"情绪设计指南"，根据分镜头的戏剧效果选择最合适的情绪设计策略**

#### 1.4. performance_style（表演风格）
**参考指南**：请查看上面的"表演风格指南"部分
- 必须从以下选项中选择一个（可为空）：内敛表演、外放表演、反差表演、细节表演
- **生成此字段时，请仔细阅读上面的"表演风格指南"，根据角色性格和情境选择最合适的表演风格**

#### 2. shot_size（景别）
**参考指南**：请查看上面的"景别选择指南"部分
- 必须从以下选项中选择一个：大远景、远景、全景、中景、中近景、近景、特写、大特写
- **生成此字段时，请仔细阅读上面的"景别选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的景别**

#### 3. camera_angle（摄影机角度）
**参考指南**：请查看上面的"摄影机角度选择指南"部分
- 必须从以下选项中选择一个：视平、高位俯拍、低位仰拍、斜拍、越肩、鸟瞰
- **生成此字段时，请仔细阅读上面的"摄影机角度选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的角度**

#### 4. camera_movement（运镜）
**参考指南**：请查看上面的"运镜选择指南"部分
- 必须从以下选项中选择一个：固定、横移、俯仰、横摇、升降、轨道推拉、变焦推拉、正跟随、倒跟随、环绕、滑轨横移
- **生成此字段时，请仔细阅读上面的"运镜选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的运镜方式**

#### 5. camera_equipment（摄影机装备）
**参考指南**：请查看上面的"摄影机装备选择指南"部分
- 必须从以下选项中选择一个：固定、轨道、手持、稳定器、摇臂、航拍
- **生成此字段时，请仔细阅读上面的"摄影机装备选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的装备**

#### 6. lens_focal_length（镜头焦段）
**参考指南**：请查看上面的"镜头焦段选择指南"部分
- 必须从以下选项中选择一个：超广角(14-24mm)、广角(24-35mm)、标准(35-50mm)、中焦(50-85mm)、长焦(85-200mm)、超长焦(200mm+)
- **生成此字段时，请仔细阅读上面的"镜头焦段选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的焦段**

#### 7. camera（相机）
**参考指南**：请查看上面的"相机选择指南"部分
- **必须从以下选项中选择一个**：ARRI Alexa、ARRI Alexa 65、Arriflex 416、IMAX 70mm、Kodak Portra 400、Kodak Vision3 500T、Panavision Panaflex、RED Monstro 8K、Sony Venice、Cinestill 800T
- **生成此字段时，请仔细阅读上面的"相机选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的相机**

#### 8. lens（镜头）
**参考指南**：请查看上面的"镜头选择指南"部分
- **必须从以下选项中选择一个**：ARRI Master Primes、ARRI Master Prime Macro、Canon K35、Cooke Anamorphic、Helios 44-2、Panavision C-Series Anamorphic、Petzval Lens
- **生成此字段时，请仔细阅读上面的"镜头选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的镜头**

#### 9. aperture（光圈）
**参考指南**：请查看上面的"光圈选择指南"部分
- **必须从以下选项中选择一个**：f/1.2、f/1.4、f/2.0、f/2.2、f/2.8、f/4.0、f/5.6、f/11
- **生成此字段时，请仔细阅读上面的"光圈选择指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的光圈**

#### 10. scene_type（场景类型）
**参考指南**：请查看上面的"武戏打斗指南"、"对峙场景指南"、"追逐场景指南"、"大招释放指南"、"收尾部分指南"
- **必须从以下选项中选择一个**：普通、武戏打斗、对峙、追逐、大招释放、收尾
- **生成此字段时，请仔细阅读对应的场景指南，判断当前分镜属于哪种场景类型**
- 如果分镜不涉及特殊场景，选择"普通"

#### 11. composition_tension（构图张力）
**参考指南**：请查看上面的"构图张力指南"部分
- **必须从以下选项中选择一个**：饱满、丰富、引导、饱满+引导、丰富+引导、饱满+丰富、饱满+丰富+引导
- **生成此字段时，请仔细阅读上面的"构图张力指南"，根据分镜头的情绪、氛围和叙事需求选择最合适的构图张力**

#### 12. axis_crossing（轴线处理）
**参考指南**：请查看上面的"轴线处理指南"部分
- **必须从以下选项中选择一个**：维持轴线、合理越轴、故意越轴
- **生成此字段时，请仔细阅读上面的"轴线处理指南"，根据分镜头的空间关系和叙事需求选择最合适的轴线处理方式**

#### 13. shot_transition（镜头衔接）
**参考指南**：请查看上面的"镜头衔接指南"部分
- **必须从以下选项中选择一个**：流畅型衔接、节奏型衔接、意义型衔接、流畅型+节奏型、流畅型+意义型、节奏型+意义型、流畅型+节奏型+意义型
- **生成此字段时，请仔细阅读上面的"镜头衔接指南"，根据分镜头的叙事节奏和情绪需求选择最合适的衔接方式**

#### 14. aesthetics_technique（审美技法）
**参考指南**：请查看上面的"审美设计指南"部分
- **必须从以下选项中选择一个或多个（多个用逗号分隔）**：对比、排比、夸张、组合、移时、奇解、精细
- **生成此字段时，请仔细阅读上面的"审美设计指南"，根据分镜头的艺术需求选择最合适的审美技法**
- 可以只选择一个，也可以选择多个组合（如："对比,排比"）

**生成流程建议**：
1. **先确定基础信息**：scene_number, characters, location, time, mood, dialogue_text, voiceover_text, sound_effects
2. **生成 scene_description**：参考构图张力、情绪设计、表演风格、主角核心表达指南，详细描述场景（注意：这些维度现在有独立字段，描述应与这些维度保持一致，但不需要重复体现）
3. **生成 scene_type**：判断场景类型，如果是特殊场景，参考对应的场景指南（武戏打斗、对峙、追逐、大招释放、收尾）
4. **生成 composition_tension**：只参考构图张力指南，根据描述选择最合适的构图张力
5. **生成 protagonist_type**：只参考主角核心表达指南，根据分镜头的叙事需求选择最合适的主角类型
6. **生成 emotion_design**：只参考情绪设计指南，根据分镜头的戏剧效果选择最合适的情绪设计策略
7. **生成 performance_style**：只参考表演风格指南，根据角色性格和情境选择最合适的表演风格
8. **生成 shot_size**：只参考景别选择指南，根据描述选择最合适的景别
9. **生成 camera_angle**：只参考摄影机角度选择指南，根据描述选择最合适的角度
10. **生成 camera_movement**：只参考运镜选择指南，根据描述选择最合适的运镜
11. **生成 camera_equipment**：只参考摄影机装备选择指南，根据描述选择最合适的装备
12. **生成 lens_focal_length**：只参考镜头焦段选择指南，根据描述选择最合适的焦段
13. **生成 camera**：只参考相机选择指南，根据描述选择最合适的相机
14. **生成 lens**：只参考镜头选择指南，根据描述选择最合适的镜头
15. **生成 aperture**：只参考光圈选择指南，根据描述选择最合适的光圈
16. **生成 axis_crossing**：只参考轴线处理指南，根据分镜序列的空间关系选择最合适的轴线处理方式
17. **生成 shot_transition**：只参考镜头衔接指南，根据分镜序列的节奏和情绪需求选择最合适的衔接方式
18. **生成 aesthetics_technique**：只参考审美设计指南，根据分镜头的艺术需求选择最合适的审美技法

**示例**：如果分镜是"角色愤怒地拍桌子"，你应该：
1. 生成 scene_description 时，参考情绪设计指南（选择"情绪一致"）、构图张力指南（选择"饱满"）、表演风格指南（选择"外放表演"），描述为："角色愤怒地拍桌子，手掌重重砸在桌面上，发出巨响，表情狰狞，眼神充满怒火，身体前倾，充满压迫感"
2. 生成 shot_size 时，只参考景别选择指南，根据"强调情绪"的场景，选择"特写"或"近景"
3. 生成 camera_angle 时，只参考摄影机角度选择指南，根据"强调情绪"的场景，选择"视平"或"低位仰拍"
4. 以此类推，每个字段都只参考对应的指南

## 示例格式：
```json
[
  {
    "scene_number": 1,
    "scene_description": "小明坐在咖啡馆靠窗的位置，低头看着手机，表情焦虑。",
    "shot_size": "中景",
    "camera_angle": "视平",
    "camera_movement": "固定",
    "camera_equipment": "固定",
    "lens_focal_length": "标准(35-50mm)",
    "camera": "ARRI Alexa",
    "lens": "ARRI Master Primes",
    "aperture": "f/2.8",
    "characters": ["小明"],
    "location": "咖啡馆",
    "time": "下午",
    "mood": "焦虑、不安",
    "dialogue_text": "",
    "voiceover_text": "",
    "sound_effects": "背景音乐,咖啡店嘈杂声",
    "scene_type": "普通",
    "composition_tension": "引导",
    "axis_crossing": "维持轴线",
    "shot_transition": "流畅型衔接",
    "aesthetics_technique": "精细",
    "protagonist_type": "情感共鸣型",
    "emotion_design": "情绪一致",
    "performance_style": "内敛表演"
  },
  {
    "scene_number": 2,
    "scene_description": "咖啡馆门铃响起，门被推开。",
    "shot_size": "近景",
    "camera_angle": "视平",
    "camera_movement": "固定",
    "camera_equipment": "固定",
    "lens_focal_length": "中焦(50-85mm)",
    "camera": "ARRI Alexa",
    "lens": "ARRI Master Primes",
    "aperture": "f/2.8",
    "characters": [],
    "location": "咖啡馆门口",
    "time": "下午",
    "mood": "中性",
    "dialogue_text": "",
    "voiceover_text": "",
    "sound_effects": "门铃声,开门声",
    "scene_type": "普通",
    "composition_tension": "引导",
    "axis_crossing": "维持轴线",
    "shot_transition": "流畅型衔接",
    "aesthetics_technique": "精细",
    "protagonist_type": "",
    "emotion_design": "",
    "performance_style": ""
  },
  {
    "scene_number": 3,
    "scene_description": "小红推门而入，环顾四周，看到小明后走了过去。",
    "shot_size": "中景",
    "camera_angle": "视平",
    "camera_movement": "横移",
    "camera_equipment": "稳定器",
    "lens_focal_length": "标准(35-50mm)",
    "camera": "ARRI Alexa",
    "lens": "ARRI Master Primes",
    "aperture": "f/2.8",
    "characters": ["小红"],
    "location": "咖啡馆",
    "time": "下午",
    "mood": "寻找、确认",
    "dialogue_text": "",
    "voiceover_text": "",
    "sound_effects": "脚步声",
    "scene_type": "普通",
    "composition_tension": "丰富",
    "axis_crossing": "维持轴线",
    "shot_transition": "流畅型衔接",
    "aesthetics_technique": "组合",
    "protagonist_type": "观察者/催化剂型",
    "emotion_design": "情绪一致",
    "performance_style": "细节表演"
  },
  {
    "scene_number": 4,
    "scene_description": "小明抬头，看到小红，脸上露出如释重负的表情。",
    "shot_size": "特写",
    "camera_angle": "视平",
    "camera_movement": "固定",
    "camera_equipment": "固定",
    "lens_focal_length": "中焦(50-85mm)",
    "camera": "ARRI Alexa",
    "lens": "ARRI Master Primes",
    "aperture": "f/2.8",
    "characters": ["小明"],
    "location": "咖啡馆",
    "time": "下午",
    "mood": "如释重负",
    "dialogue_text": "",
    "voiceover_text": "",
    "sound_effects": "",
    "scene_type": "普通",
    "composition_tension": "饱满",
    "axis_crossing": "维持轴线",
    "shot_transition": "流畅型衔接",
    "aesthetics_technique": "精细",
    "protagonist_type": "情感共鸣型",
    "emotion_design": "情绪一致",
    "performance_style": "内敛表演"
  },
  {
    "scene_number": 5,
    "scene_description": "小明看着小红说话。",
    "shot_size": "中景",
    "camera_angle": "视平",
    "camera_movement": "固定",
    "camera_equipment": "固定",
    "lens_focal_length": "标准(35-50mm)",
    "camera": "ARRI Alexa",
    "lens": "ARRI Master Primes",
    "aperture": "f/2.8",
    "characters": ["小明"],
    "location": "咖啡馆",
    "time": "下午",
    "mood": "急切",
    "dialogue_text": "小明：你终于来了！我有很重要的事要告诉你。",
    "voiceover_text": "",
    "sound_effects": "背景音乐",
    "scene_type": "普通",
    "composition_tension": "引导",
    "axis_crossing": "维持轴线",
    "shot_transition": "流畅型衔接",
    "aesthetics_technique": "精细",
    "protagonist_type": "情感共鸣型",
    "emotion_design": "情绪一致",
    "performance_style": "内敛表演"
  },
  {
    "scene_number": 6,
    "scene_description": "小红坐下，神色凝重地看着小明。",
    "shot_size": "中景",
    "camera_angle": "视平",
    "camera_movement": "固定",
    "camera_equipment": "固定",
    "lens_focal_length": "标准(35-50mm)",
    "camera": "ARRI Alexa",
    "lens": "ARRI Master Primes",
    "aperture": "f/2.8",
    "characters": ["小红"],
    "location": "咖啡馆",
    "time": "下午",
    "mood": "凝重、严肃",
    "dialogue_text": "",
    "voiceover_text": "",
    "sound_effects": "椅子移动声",
    "scene_type": "普通",
    "composition_tension": "饱满",
    "axis_crossing": "维持轴线",
    "shot_transition": "流畅型衔接",
    "aesthetics_technique": "精细",
    "protagonist_type": "情感共鸣型",
    "emotion_design": "情绪叠加",
    "performance_style": "内敛表演"
  },
  {
    "scene_number": 7,
    "scene_description": "小红询问小明。",
    "shot_size": "特写",
    "camera_angle": "视平",
    "camera_movement": "固定",
    "camera_equipment": "固定",
    "lens_focal_length": "中焦(50-85mm)",
    "camera": "ARRI Alexa",
    "lens": "ARRI Master Primes",
    "aperture": "f/2.8",
    "characters": ["小红"],
    "location": "咖啡馆",
    "time": "下午",
    "mood": "疑惑、担忧",
    "dialogue_text": "小红：什么事这么严重？",
    "voiceover_text": "",
    "sound_effects": "背景音乐",
    "scene_type": "普通",
    "composition_tension": "饱满",
    "axis_crossing": "维持轴线",
    "shot_transition": "流畅型衔接",
    "aesthetics_technique": "精细",
    "protagonist_type": "情感共鸣型",
    "emotion_design": "情绪一致",
    "performance_style": "内敛表演"
  }
]
```

## 重要提醒：
- 划分要**足够细致**，不要合并多个动作或对话到一个分镜
- 每个分镜应该只包含**一个主要动作**或**一个人物的对话**
- **台词必须完整填入** dialogue_text 字段
- **音效要贴合分镜内容**，智能判断添加
- 严格按照以上格式输出JSON，确保格式正确。"""

def get_scene_division_prompt():
    """获取分镜头划分提示词"""
    # 使用字符串替换而不是 format，避免 JSON 示例中的大括号冲突
    prompt = SCENE_DIVISION_PROMPT
    prompt = prompt.replace("{shot_size_guide}", SHOT_SIZE_GUIDE_TEXT)
    prompt = prompt.replace("{camera_angle_guide}", CAMERA_ANGLE_GUIDE_TEXT)
    prompt = prompt.replace("{camera_movement_guide}", CAMERA_MOVEMENT_GUIDE_TEXT)
    prompt = prompt.replace("{camera_equipment_guide}", CAMERA_EQUIPMENT_GUIDE_TEXT)
    prompt = prompt.replace("{lens_focal_length_guide}", LENS_FOCAL_LENGTH_GUIDE_TEXT)
    prompt = prompt.replace("{camera_guide}", CAMERA_GUIDE_TEXT)
    prompt = prompt.replace("{lens_guide}", LENS_GUIDE_TEXT)
    prompt = prompt.replace("{aperture_guide}", APERTURE_GUIDE_TEXT)
    # 新增指南（如果存在则替换，否则替换为空字符串）
    try:
        prompt = prompt.replace("{composition_tension_guide}", COMPOSITION_TENSION_GUIDE_TEXT)
        prompt = prompt.replace("{axis_crossing_guide}", AXIS_CROSSING_GUIDE_TEXT)
        prompt = prompt.replace("{protagonist_core_expression_guide}", PROTAGONIST_CORE_EXPRESSION_GUIDE_TEXT)
        prompt = prompt.replace("{emotion_design_guide}", EMOTION_DESIGN_GUIDE_TEXT)
        prompt = prompt.replace("{expression_action_performance_guide}", EXPRESSION_ACTION_PERFORMANCE_GUIDE_TEXT)
        prompt = prompt.replace("{shot_transition_guide}", SHOT_TRANSITION_GUIDE_TEXT)
        prompt = prompt.replace("{fight_scene_guide}", FIGHT_SCENE_GUIDE_TEXT)
        prompt = prompt.replace("{confrontation_scene_guide}", CONFRONTATION_SCENE_GUIDE_TEXT)
        prompt = prompt.replace("{chase_scene_guide}", CHASE_SCENE_GUIDE_TEXT)
        prompt = prompt.replace("{ultimate_skill_release_guide}", ULTIMATE_SKILL_RELEASE_GUIDE_TEXT)
        prompt = prompt.replace("{ending_section_guide}", ENDING_SECTION_GUIDE_TEXT)
        prompt = prompt.replace("{aesthetics_guide}", AESTHETICS_GUIDE_TEXT)
    except NameError:
        # 如果变量未定义，替换为空字符串
        prompt = prompt.replace("{composition_tension_guide}", "")
        prompt = prompt.replace("{axis_crossing_guide}", "")
        prompt = prompt.replace("{protagonist_core_expression_guide}", "")
        prompt = prompt.replace("{emotion_design_guide}", "")
        prompt = prompt.replace("{expression_action_performance_guide}", "")
        prompt = prompt.replace("{shot_transition_guide}", "")
        prompt = prompt.replace("{fight_scene_guide}", "")
        prompt = prompt.replace("{confrontation_scene_guide}", "")
        prompt = prompt.replace("{chase_scene_guide}", "")
        prompt = prompt.replace("{ultimate_skill_release_guide}", "")
        prompt = prompt.replace("{ending_section_guide}", "")
        prompt = prompt.replace("{aesthetics_guide}", "")
    return prompt

