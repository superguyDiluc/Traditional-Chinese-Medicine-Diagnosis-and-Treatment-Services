import pathlib

BASE_DIR = pathlib.Path(__file__).parent
# 可选项：把单独的 .txt 放到这个目录
PROMPTS_DIR = BASE_DIR / "prompt_templates"

def _read_file(name: str) -> str | None:
    p = PROMPTS_DIR / f"{name}.txt"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return None

# 备用内嵌模板
EMBEDDED = {
    "tcm_hero": """
请根据用户描述的症状，生成一个中医诊断的 JSON 数据。JSON 格式如下：

{{
  "syndrome": "中医证型名称",
  "icon": "fas fa-yin-yang",
  "description": "病人的调理目标，该调理成什么水平、什么情况（50-80字）",
  "symptoms": [
    "主要症状1",
    "主要症状2",
    "主要症状3"
  ],
  "constitution": "分析得到的病人的体质",
  "recommendation": "推荐病人需要以怎样的节奏生活与疗养",
  "hint": "结合气候等条件，来温馨提示用户要注意什么"
}}

用户描述的症状：{user_input}

请直接返回标准的 JSON 格式，不要包含任何其他文字说明。
""",
    "prescription": """
请根据用户描述的中医证型或症状，生成一个中药调理方案的 JSON 数据。JSON 格式如下：

{{
  "sectionTitle": "调理方案标题",
  "prescriptions": [
    {{
      "title": "方剂名称1",
      "sections": [
        {{
          "type": "list",
          "title": "药物组成",
          "items": [
            "药物1 用量",
            "药物2 用量",
            "药物3 用量"
          ]
        }},
        {{
          "type": "text",
          "title": "功效",
          "content": "方剂功效描述"
        }},
        {{
          "type": "steps",
          "title": "服用方法",
          "items": [
            "煎煮方法步骤1",
            "服用时间和剂量",
            "注意事项"
          ]
        }}
      ]
    }},
    {{
      "title": "方剂名称2",
      "icon": "fas fa-leaf",
      "sections": [
        {{
          "type": "list",
          "title": "药物组成",
          "items": [
            "药物1 用量",
            "药物2 用量",
            "药物3 用量"
          ]
        }},
        {{
          "type": "text",
          "title": "功效",
          "content": "方剂功效描述"
        }},
        {{
          "type": "steps",
          "title": "服用方法",
          "items": [
            "煎煮方法步骤1",
            "服用时间和剂量",
            "注意事项"
          ]
        }}
      ]
    }}
  ]
}}

用户描述的证型/症状：{user_input}

请根据中医理论，为该证型提供2-3个不同的中药方剂，每个方剂要有明确的药物组成、功效和服用方法。最后再提供饮食调理和生活调理建议。请直接返回标准的 JSON 格式，不要包含任何其他文字说明。
""",
    "suggestion": """
请根据用户描述的中医证型或症状，生成一个日常生活调养建议的 JSON 数据。JSON 格式如下：

{{
  "sectionTitle": {{
    "icon": "fas fa-seedling",
    "text": "日常生活调养"
  }},
  "suggestions": [
    {{
      "icon": "fas fa-utensils",
      "title": "饮食调理",
      "content": "饮食方面的具体建议和注意事项"
    }},
    {{
      "icon": "fas fa-bed",
      "title": "睡眠调理",
      "content": "睡眠方面的具体建议和注意事项"
    }},
    {{
      "icon": "fas fa-face-smile",
      "title": "情志调理",
      "content": "情绪和心理方面的调理建议"
    }},
    {{
      "icon": "fas fa-person-running",
      "title": "运动调理",
      "content": "运动和生活习惯方面的建议"
    }}
  ]
}}

用户描述的证型/症状：{user_input}

请根据中医理论，为该证型提供4个方面的日常生活调养建议，每个建议包含具体的、可操作的内容。请直接返回标准的 JSON 格式，不要包含任何其他文字说明。
""",
    "followup": """
请根据用户描述的中医证型或症状，生成一个复诊与安全提示的 JSON 数据。JSON 格式如下：

{{
  "sectionTitle": {{
    "icon": "fas fa-notes-medical",
    "text": "复诊与安全提示"
  }},
  "followupItems": [
    {{
      "icon": "fas fa-calendar-check",
      "title": "复诊时间安排",
      "items": [
        "首次复诊时间与评估重点",
        "持续随访的频率建议",
        "伴随慢性病的联合随访提醒"
      ]
    }},
    {{
      "icon": "fas fa-stethoscope",
      "title": "就诊沟通要点",
      "items": [
        "复诊时需要反馈的症状变化",
        "药物或调理过程中出现的不适",
        "需要医生关注的体征或化验指标"
      ]
    }}
  ],
  "monitoring": [
    {{
      "icon": "fas fa-chart-line",
      "title": "家庭自我监测",
      "items": [
        "需要记录的睡眠、情绪或饮食情况",
        "关键体征的监测频率",
        "适合使用的健康记录工具"
      ]
    }}
  ],
  "safetyNotes": [
    {{
      "icon": "fas fa-shield-heart",
      "title": "安全用药提示",
      "items": [
        "服药时的饮食禁忌或药物相互作用提醒",
        "特殊人群（如孕妇、慢病患者）的加注说明",
        "出现不良反应时的处理建议"
      ]
    }}
  ],
  "warningSignals": [
    {{
      "icon": "fas fa-triangle-exclamation",
      "title": "需立即就医的信号",
      "items": [
        "突发或加重的危险症状",
        "需紧急处理的体征变化",
        "伴随的心理或神经系统异常"
      ]
    }}
  ],
  "overallReminder": "一句总括提醒，说明出现异常时的处理建议与专业医生沟通的重要性"
}}

用户描述的证型/症状：{user_input}

请直接返回标准的 JSON 格式，不要包含任何其他文字说明。
"""
}

def load_prompt(name: str) -> str:
    # 优先读取 prompt_templates/{name}.txt（便于编辑）
    txt = _read_file(name)
    if txt:
        return txt
    return EMBEDDED.get(name, "")
    
# 导出常量，方便直接使用
TCM_HERO_PROMPT = load_prompt("tcm_hero")
PRESCRIPTION_PROMPT = load_prompt("prescription")
SUGGESTION_PROMPT = load_prompt("suggestion")
FOLLOWUP_PROMPT = load_prompt("followup")