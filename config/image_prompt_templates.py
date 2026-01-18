"""
文生图提示词模板配置（Nano Banana Pro 格式）
"""

# Nano Banana Pro JSON 结构化提示词模板
NANO_BANANA_PROMPT_TEMPLATE = {
    "subject": {
        "main_character": "",
        "action": "",
        "pose": "",
        "expression": "",
        "clothing": "",
        "props": ""
    },
    "scene": {
        "location": "",
        "environment": "",
        "background": "",
        "time_of_day": "",
        "weather": ""
    },
    "composition": {
        "shot_size": "",
        "camera_angle": "",
        "framing": "",
        "composition_tension": "",
        "rule_of_thirds": "",
        "leading_lines": ""
    },
    "lighting": {
        "type": "",
        "direction": "",
        "intensity": "",
        "color_temperature": "",
        "mood": ""
    },
    "camera_technical": {
        "camera_model": "",
        "lens": "",
        "aperture": "",
        "focal_length": "",
        "depth_of_field": ""
    },
    "visual_style": {
        "cinematic_style": "",
        "color_grading": "",
        "texture": "",
        "atmosphere": "",
        "protagonist_type": "",
        "emotion_design": "",
        "performance_style": ""
    },
    "spatial_anchors": [],
    "negative_constraints": []
}

# 镜头语言到视觉描述的映射
SHOT_SIZE_MAPPING = {
    "大远景": {
        "chinese": "大远景，人物极小，环境占据主导",
        "english": "extreme wide shot, tiny figure, vast landscape dominates",
        "visual": "extreme wide shot, establishing shot, vast scale, tiny human figure"
    },
    "远景": {
        "chinese": "远景，人物较小，环境重要",
        "english": "wide shot, small figure, environment important",
        "visual": "wide shot, full body visible, environmental context"
    },
    "全景": {
        "chinese": "全景，人物全身可见",
        "english": "full shot, full body visible",
        "visual": "full body shot, head to toe, complete figure"
    },
    "中景": {
        "chinese": "中景，腰部以上",
        "english": "medium shot, waist up",
        "visual": "medium shot, waist up, balanced composition"
    },
    "中近景": {
        "chinese": "中近景，胸部以上",
        "english": "medium close-up, chest up",
        "visual": "medium close-up, chest and above, focus on upper body"
    },
    "近景": {
        "chinese": "近景，肩部以上",
        "english": "close shot, shoulders up",
        "visual": "close shot, shoulders and above, intimate framing"
    },
    "特写": {
        "chinese": "特写，面部表情",
        "english": "close-up, facial expression",
        "visual": "close-up, face only, detailed facial expression, shallow depth of field"
    },
    "大特写": {
        "chinese": "大特写，局部细节",
        "english": "extreme close-up, detail",
        "visual": "extreme close-up, extreme detail, macro shot, very shallow depth of field"
    }
}

CAMERA_ANGLE_MAPPING = {
    "视平": {
        "chinese": "视平角度，自然视角",
        "english": "eye level, natural perspective",
        "visual": "eye level angle, natural perspective, neutral camera height"
    },
    "高位俯拍": {
        "chinese": "高位俯拍，向下视角",
        "english": "high angle, looking down",
        "visual": "high angle shot, top-down view, looking down, overhead perspective"
    },
    "低位仰拍": {
        "chinese": "低位仰拍，向上视角",
        "english": "low angle, looking up",
        "visual": "low angle shot, looking up, dramatic perspective, heroic angle"
    },
    "斜拍": {
        "chinese": "斜拍，倾斜构图",
        "english": "dutch angle, tilted frame",
        "visual": "dutch angle, canted frame, tilted composition, dynamic angle"
    },
    "越肩": {
        "chinese": "越肩镜头，过肩视角",
        "english": "over the shoulder, OTS",
        "visual": "over the shoulder shot, OTS, shoulder in foreground, depth"
    },
    "鸟瞰": {
        "chinese": "鸟瞰，垂直俯视",
        "english": "bird's eye view, vertical top-down",
        "visual": "bird's eye view, vertical top-down, 90 degree angle, god's eye view"
    }
}

CAMERA_MOVEMENT_MAPPING = {
    "固定": {
        "chinese": "固定镜头，稳定构图",
        "english": "static camera, locked frame",
        "visual": "static camera, locked frame, stable composition, no camera movement"
    },
    "横移": {
        "chinese": "横移，水平移动",
        "english": "truck shot, horizontal movement",
        "visual": "truck shot, horizontal camera movement, parallax effect"
    },
    "俯仰": {
        "chinese": "俯仰，上下转动",
        "english": "tilt, vertical pan",
        "visual": "tilt shot, vertical camera movement, up and down scanning"
    },
    "横摇": {
        "chinese": "横摇，左右转动",
        "english": "pan, horizontal rotation",
        "visual": "pan shot, horizontal camera rotation, side to side movement"
    },
    "升降": {
        "chinese": "升降，垂直移动",
        "english": "crane shot, vertical movement",
        "visual": "crane shot, vertical camera movement, rising or descending"
    },
    "轨道推拉": {
        "chinese": "轨道推拉，前后移动",
        "english": "dolly shot, forward/backward movement",
        "visual": "dolly shot, smooth forward or backward movement, perspective change"
    },
    "变焦推拉": {
        "chinese": "变焦推拉，焦距变化",
        "english": "zoom, focal length change",
        "visual": "zoom shot, focal length change, compressed space, optical zoom"
    },
    "正跟随": {
        "chinese": "正跟随，背后跟随",
        "english": "following shot, tracking behind",
        "visual": "following shot, camera tracking behind subject, third-person view"
    },
    "倒跟随": {
        "chinese": "倒跟随，前方后退",
        "english": "leading shot, tracking forward",
        "visual": "leading shot, camera tracking forward, subject approaching"
    },
    "环绕": {
        "chinese": "环绕，圆周运动",
        "english": "arc shot, circular movement",
        "visual": "arc shot, circular camera movement, orbiting around subject"
    },
    "滑轨横移": {
        "chinese": "滑轨横移，平滑横移",
        "english": "slider shot, smooth horizontal",
        "visual": "slider shot, smooth horizontal movement, subtle parallax"
    }
}

CAMERA_EQUIPMENT_MAPPING = {
    "固定": {
        "chinese": "三脚架固定，稳定拍摄",
        "english": "tripod, stable",
        "visual": "tripod mounted, stable camera, locked off, professional setup"
    },
    "轨道": {
        "chinese": "轨道拍摄，平滑移动",
        "english": "dolly track, smooth movement",
        "visual": "dolly track, smooth mechanical movement, cinematic quality"
    },
    "手持": {
        "chinese": "手持拍摄，真实感",
        "english": "handheld, documentary style",
        "visual": "handheld camera, slight camera shake, documentary style, realistic"
    },
    "稳定器": {
        "chinese": "稳定器，平滑跟随",
        "english": "stabilizer, smooth following",
        "visual": "stabilizer, smooth floating movement, steadicam style"
    },
    "摇臂": {
        "chinese": "摇臂拍摄，升降运动",
        "english": "crane, vertical movement",
        "visual": "crane shot, vertical camera movement, epic scale"
    },
    "航拍": {
        "chinese": "航拍，高空视角",
        "english": "aerial, high altitude",
        "visual": "aerial shot, drone perspective, high altitude view, bird's eye"
    }
}

CAMERA_MODEL_MAPPING = {
    "ARRI Alexa": {
        "chinese": "ARRI Alexa 电影质感",
        "english": "ARRI Alexa cinematic quality",
        "visual": "ARRI Alexa color science, cinematic color grading, film-like quality, professional cinematography"
    },
    "ARRI Alexa 65": {
        "chinese": "ARRI Alexa 65 大画幅",
        "english": "ARRI Alexa 65 large format",
        "visual": "ARRI Alexa 65, large format sensor, epic cinematic quality, shallow depth of field"
    },
    "Arriflex 416": {
        "chinese": "Arriflex 416 胶片质感",
        "english": "Arriflex 416 film grain",
        "visual": "16mm film grain, Arriflex 416, vintage film look, textured quality"
    },
    "IMAX 70mm": {
        "chinese": "IMAX 70mm 极致清晰",
        "english": "IMAX 70mm extreme clarity",
        "visual": "IMAX 70mm, extreme clarity, massive scale, immersive quality"
    },
    "Kodak Portra 400": {
        "chinese": "Kodak Portra 400 温暖色调",
        "english": "Kodak Portra 400 warm tones",
        "visual": "Kodak Portra 400 film stock, warm color tones, soft contrast, portrait quality"
    },
    "Kodak Vision3 500T": {
        "chinese": "Kodak Vision3 500T 电影胶片",
        "english": "Kodak Vision3 500T cinema film",
        "visual": "Kodak Vision3 500T, cinema film stock, organic colors, high dynamic range"
    },
    "Panavision Panaflex": {
        "chinese": "Panavision Panaflex 经典电影",
        "english": "Panavision Panaflex classic cinema",
        "visual": "Panavision Panaflex, classic cinema look, 35mm film aesthetic"
    },
    "RED Monstro 8K": {
        "chinese": "RED Monstro 8K 锐利清晰",
        "english": "RED Monstro 8K sharp clarity",
        "visual": "RED Monstro 8K, ultra sharp, clean digital look, high resolution"
    },
    "Sony Venice": {
        "chinese": "Sony Venice 现代数字",
        "english": "Sony Venice modern digital",
        "visual": "Sony Venice, modern digital cinema, neutral color science, high ISO capability"
    },
    "Cinestill 800T": {
        "chinese": "Cinestill 800T 霓虹风格",
        "english": "Cinestill 800T neon style",
        "visual": "Cinestill 800T, neon halation, cinematic night photography, vibrant colors"
    }
}

LENS_MAPPING = {
    "ARRI Master Primes": {
        "chinese": "ARRI Master Primes 极致清晰",
        "english": "ARRI Master Primes extreme sharpness",
        "visual": "ARRI Master Primes, T1.3, extreme sharpness, edge to edge clarity, professional optics"
    },
    "ARRI Master Prime Macro": {
        "chinese": "ARRI Master Prime Macro 微距",
        "english": "ARRI Master Prime Macro macro",
        "visual": "ARRI Master Prime Macro, extreme close-up capability, macro photography"
    },
    "Canon K35": {
        "chinese": "Canon K35 复古柔美",
        "english": "Canon K35 vintage soft",
        "visual": "Canon K35, vintage lens character, soft glow, low contrast, dreamy quality"
    },
    "Cooke Anamorphic": {
        "chinese": "Cooke Anamorphic 宽银幕",
        "english": "Cooke Anamorphic widescreen",
        "visual": "Cooke Anamorphic, widescreen format, oval bokeh, warm skin tones, cinematic"
    },
    "Helios 44-2": {
        "chinese": "Helios 44-2 旋焦效果",
        "english": "Helios 44-2 swirly bokeh",
        "visual": "Helios 44-2, swirly bokeh, vintage character, unique optical quality"
    },
    "Panavision C-Series Anamorphic": {
        "chinese": "Panavision C-Series 科幻风格",
        "english": "Panavision C-Series sci-fi style",
        "visual": "Panavision C-Series Anamorphic, blue streak flares, sci-fi aesthetic, classic Hollywood"
    },
    "Petzval Lens": {
        "chinese": "Petzval Lens 隧道效果",
        "english": "Petzval Lens tunnel effect",
        "visual": "Petzval lens, tunnel effect, sharp center, swirly edges, vintage portrait"
    }
}

APERTURE_MAPPING = {
    "f/1.2": {
        "chinese": "f/1.2 超大光圈，极浅景深",
        "english": "f/1.2 ultra wide aperture, extreme shallow depth",
        "visual": "f/1.2, ultra wide aperture, extreme shallow depth of field, strong bokeh, dreamy focus"
    },
    "f/1.4": {
        "chinese": "f/1.4 大光圈，浅景深",
        "english": "f/1.4 wide aperture, shallow depth",
        "visual": "f/1.4, wide aperture, shallow depth of field, beautiful bokeh, selective focus"
    },
    "f/2.0": {
        "chinese": "f/2.0 大光圈，柔和虚化",
        "english": "f/2.0 wide aperture, soft bokeh",
        "visual": "f/2.0, wide aperture, shallow depth of field, soft background blur, portrait quality"
    },
    "f/2.2": {
        "chinese": "f/2.2 大光圈，背景分离",
        "english": "f/2.2 wide aperture, background separation",
        "visual": "f/2.2, wide aperture, good subject separation, pleasing bokeh"
    },
    "f/2.8": {
        "chinese": "f/2.8 标准光圈，平衡景深",
        "english": "f/2.8 standard aperture, balanced depth",
        "visual": "f/2.8, standard aperture, balanced depth of field, moderate bokeh, cinematic"
    },
    "f/4.0": {
        "chinese": "f/4.0 中等光圈，较深景深",
        "english": "f/4.0 medium aperture, deeper depth",
        "visual": "f/4.0, medium aperture, deeper depth of field, background visible, action photography"
    },
    "f/5.6": {
        "chinese": "f/5.6 中等光圈，清晰背景",
        "english": "f/5.6 medium aperture, clear background",
        "visual": "f/5.6, medium aperture, deeper depth of field, background in focus, environmental context"
    },
    "f/11": {
        "chinese": "f/11 小光圈，深景深",
        "english": "f/11 small aperture, deep focus",
        "visual": "f/11, small aperture, deep focus, everything sharp, landscape photography, wide depth of field"
    }
}

# 情绪氛围映射（扩展版）
MOOD_MAPPING = {
    "紧张": {
        "chinese": "紧张氛围，高对比度",
        "english": "tense atmosphere, high contrast",
        "visual": "tense atmosphere, dramatic lighting, high contrast, suspenseful mood, dark shadows"
    },
    "轻松": {
        "chinese": "轻松氛围，柔和光线",
        "english": "relaxed atmosphere, soft light",
        "visual": "relaxed atmosphere, soft lighting, warm tones, comfortable mood, gentle shadows"
    },
    "悲伤": {
        "chinese": "悲伤氛围，低饱和度",
        "english": "sad atmosphere, low saturation",
        "visual": "melancholic atmosphere, muted colors, low saturation, soft shadows, emotional depth"
    },
    "兴奋": {
        "chinese": "兴奋氛围，明亮色彩",
        "english": "excited atmosphere, bright colors",
        "visual": "energetic atmosphere, bright colors, vibrant lighting, dynamic mood, high energy"
    },
    "神秘": {
        "chinese": "神秘氛围，阴影丰富",
        "english": "mysterious atmosphere, rich shadows",
        "visual": "mysterious atmosphere, dramatic shadows, low key lighting, enigmatic mood, chiaroscuro"
    },
    "浪漫": {
        "chinese": "浪漫氛围，温暖色调",
        "english": "romantic atmosphere, warm tones",
        "visual": "romantic atmosphere, warm color tones, soft lighting, intimate mood, golden hour"
    },
    "愤怒": {
        "chinese": "愤怒氛围，强烈对比",
        "english": "angry atmosphere, strong contrast",
        "visual": "angry atmosphere, harsh lighting, strong contrast, intense shadows, aggressive mood"
    },
    "恐惧": {
        "chinese": "恐惧氛围，低光阴影",
        "english": "fearful atmosphere, low light shadows",
        "visual": "fearful atmosphere, low key lighting, deep shadows, ominous mood, dark tones"
    },
    "喜悦": {
        "chinese": "喜悦氛围，明亮温暖",
        "english": "joyful atmosphere, bright and warm",
        "visual": "joyful atmosphere, bright lighting, warm colors, cheerful mood, vibrant tones"
    },
    "平静": {
        "chinese": "平静氛围，柔和平衡",
        "english": "calm atmosphere, soft and balanced",
        "visual": "calm atmosphere, even lighting, balanced composition, peaceful mood, harmonious tones"
    },
    "焦虑": {
        "chinese": "焦虑氛围，不稳定光线",
        "english": "anxious atmosphere, unstable lighting",
        "visual": "anxious atmosphere, flickering light, uneven shadows, restless mood, chaotic composition"
    },
    "忧郁": {
        "chinese": "忧郁氛围，冷色调",
        "english": "melancholic atmosphere, cool tones",
        "visual": "melancholic atmosphere, cool color tones, soft shadows, contemplative mood, muted palette"
    },
    "希望": {
        "chinese": "希望氛围，明亮前景",
        "english": "hopeful atmosphere, bright foreground",
        "visual": "hopeful atmosphere, bright foreground, soft background, optimistic mood, warm highlights"
    },
    "绝望": {
        "chinese": "绝望氛围，压抑阴影",
        "english": "desperate atmosphere, oppressive shadows",
        "visual": "desperate atmosphere, heavy shadows, low contrast, bleak mood, desaturated colors"
    },
    "胜利": {
        "chinese": "胜利氛围，辉煌光线",
        "english": "triumphant atmosphere, glorious light",
        "visual": "triumphant atmosphere, bright lighting, high contrast, heroic mood, epic scale"
    },
    "孤独": {
        "chinese": "孤独氛围，空旷冷清",
        "english": "lonely atmosphere, empty and desolate",
        "visual": "lonely atmosphere, sparse composition, cool tones, isolated mood, minimal elements"
    },
    "温暖": {
        "chinese": "温暖氛围，柔和暖光",
        "english": "warm atmosphere, soft warm light",
        "visual": "warm atmosphere, golden hour lighting, warm color palette, cozy mood, soft shadows"
    },
    "冷酷": {
        "chinese": "冷酷氛围，冷色调高对比",
        "english": "cold atmosphere, cool tones high contrast",
        "visual": "cold atmosphere, cool color tones, high contrast, harsh lighting, clinical mood"
    },
    "中性": {
        "chinese": "中性氛围，平衡自然",
        "english": "neutral atmosphere, balanced and natural",
        "visual": "neutral atmosphere, natural lighting, balanced tones, objective mood, realistic colors"
    }
}

# 时间映射
TIME_MAPPING = {
    "白天": {
        "chinese": "白天，自然光",
        "english": "daytime, natural light",
        "visual": "daytime, natural sunlight, bright ambient light, clear visibility"
    },
    "夜晚": {
        "chinese": "夜晚，人工光源",
        "english": "night, artificial light",
        "visual": "nighttime, artificial lighting, street lights, neon signs, low light, dark atmosphere"
    },
    "黄昏": {
        "chinese": "黄昏，金色光线",
        "english": "dusk, golden light",
        "visual": "golden hour, warm sunset light, orange and pink sky, dramatic clouds, cinematic"
    },
    "黎明": {
        "chinese": "黎明，柔和光线",
        "english": "dawn, soft light",
        "visual": "dawn, soft morning light, blue hour, cool tones, peaceful atmosphere"
    },
    "中午": {
        "chinese": "中午，强烈阳光",
        "english": "noon, strong sunlight",
        "visual": "noon, strong overhead sunlight, harsh shadows, high contrast, bright"
    },
    "下午": {
        "chinese": "下午，斜射光线",
        "english": "afternoon, angled light",
        "visual": "afternoon, angled sunlight, long shadows, warm tones, natural lighting"
    }
}

# 通用负面提示词
DEFAULT_NEGATIVE_PROMPT = {
    "chinese": "低质量, 模糊, 失真, 变形, 多余的手指, 多余的手臂, 文字, 水印, 签名, 丑陋, 畸变, 错误, 低分辨率, 像素化, 噪点, 伪影, 不自然, 不协调",
    "english": "low quality, blurry, distorted, deformed, extra fingers, extra arms, text, watermark, signature, ugly, distorted, error, low resolution, pixelated, noise, artifacts, unnatural, inconsistent",
    "visual": "low quality, blurry, distorted, deformed, extra fingers, extra arms, text, watermark, signature, ugly, distorted, error, low resolution, pixelated, noise, artifacts, unnatural, inconsistent, bad anatomy, bad proportions"
}

# 质量标签
QUALITY_TAGS = {
    "chinese": "高质量, 8K, 细节丰富, 专业摄影, 电影级",
    "english": "high quality, 8K, detailed, professional photography, cinematic",
    "visual": "high quality, 8K resolution, extremely detailed, professional cinematography, cinematic lighting, film grain, sharp focus"
}
