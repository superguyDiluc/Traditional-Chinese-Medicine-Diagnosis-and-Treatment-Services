import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from http import HTTPStatus
from dashscope import Application

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# DashScope API 配置
API_KEY = "sk-90426267f6844b9d815527ec5c210644"
APP_ID = "09927ed45026488e961c35d96fb4b5c4"

# TCM Hero 模块的 Prompt 模板
TCM_HERO_PROMPT = """
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
"""

# Prescription 模块的 Prompt 模板
PRESCRIPTION_PROMPT = """
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
"""

# Suggestion 模块的 Prompt 模板
SUGGESTION_PROMPT = """
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
"""

# Followup 模块的 Prompt 模板
FOLLOWUP_PROMPT = """
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

def call_dashscope_api(prompt):
    """调用 DashScope API"""
    try:
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt,
        )
        
        if response.status_code == HTTPStatus.OK:
            return response.output.text
        else:
            return None
    except Exception as e:
        print(f"API 调用错误: {e}")
        return None

def extract_json_from_response(response_text):
    """从响应文本中提取 JSON"""
    import traceback
    try:
      # 如果响应直接是 JSON
      return json.loads(response_text)
    except Exception as e:
      print("JSON解析失败:", e)
      print("原始AI响应内容:", response_text)
      traceback.print_exc()
      try:
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
          return json.loads(json_match.group(1))
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
          return json.loads(json_match.group(0))
        return None
      except Exception as e2:
        print("二次解析也失败:", e2)
        traceback.print_exc()
        return None

@app.route('/generate-hero', methods=['POST'])
def generate_hero():
    """生成 TCM Hero JSON 数据"""
    try:
        print('DEBUG: start generate_hero')
        data = request.get_json()
        user_input = data.get('prompt', '')
        
        if not user_input:
            return jsonify({'error': '请提供症状描述'}), 400
        

        print('DEBUG: start build prompt')
        # 构建完整的 prompt
        full_prompt = TCM_HERO_PROMPT.format(user_input=user_input)
        
        print('DEBUG: call API')
        # 调用 API
        response_text = call_dashscope_api(full_prompt)
        print(f'DEBUG: response text {response_text}')

        if not response_text:
            return jsonify({'error': 'API 调用失败'}), 500
        
        # 提取 JSON
        json_data = extract_json_from_response(response_text)
        
        if not json_data:
            return jsonify({'error': 'JSON 解析失败', 'raw_response': response_text}), 500

        return jsonify({
            'success': True,
            'data': json_data,
            'raw_response': response_text
        })
        
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/generate-prescription', methods=['POST'])
def generate_prescription():
    """生成 Prescription JSON 数据"""
    try:
        data = request.get_json()
        user_input = data.get('prompt', '')
        
        if not user_input:
            return jsonify({'error': '请提供证型或症状描述'}), 400
        
        # 构建完整的 prompt
        full_prompt = PRESCRIPTION_PROMPT.format(user_input=user_input)
        print('DEBUG: generate_prescription - build prompt success')

        # 调用 API
        response_text = call_dashscope_api(full_prompt)
        print('DEBUG: generate_prescription - call api success')

        if not response_text:
            return jsonify({'error': 'API 调用失败'}), 500
        
        # 提取 JSON
        json_data = extract_json_from_response(response_text)
        print('DEBUG: generate_prescription - extract json success')

        if not json_data:
            return jsonify({'error': 'JSON 解析失败', 'raw_response': response_text}), 500
        
        return jsonify({
            'success': True,
            'data': json_data,
            'raw_response': response_text
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/generate-suggestion', methods=['POST'])
def generate_suggestion():
    """生成 Suggestion JSON 数据"""
    try:
        data = request.get_json()
        user_input = data.get('prompt', '')
        
        if not user_input:
            return jsonify({'error': '请提供证型或症状描述'}), 400
        
        # 构建完整的 prompt
        full_prompt = SUGGESTION_PROMPT.format(user_input=user_input)
        print('DEBUG: generate_suggestion - build prompt success')

        # 调用 API
        response_text = call_dashscope_api(full_prompt)
        print('DEBUG: generate_suggestion - call api success')

        if not response_text:
            return jsonify({'error': 'API 调用失败'}), 500
        
        # 提取 JSON
        json_data = extract_json_from_response(response_text)
        print('DEBUG: generate_suggestion - extract json success')

        if not json_data:
            return jsonify({'error': 'JSON 解析失败', 'raw_response': response_text}), 500
        
        return jsonify({
            'success': True,
            'data': json_data,
            'raw_response': response_text
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/generate-followup', methods=['POST'])
def generate_followup():
    """生成复诊与安全提示 JSON 数据"""
    try:
        data = request.get_json()
        user_input = data.get('prompt', '')

        if not user_input:
            return jsonify({'error': '请提供证型或症状描述'}), 400

        full_prompt = FOLLOWUP_PROMPT.format(user_input=user_input)
        print('DEBUG: generate_followup - build prompt success')

        response_text = call_dashscope_api(full_prompt)
        print('DEBUG: generate_followup - call api success')

        if not response_text:
            return jsonify({'error': 'API 调用失败'}), 500

        json_data = extract_json_from_response(response_text)
        print('DEBUG: generate_followup - extract json success')

        if not json_data:
            return jsonify({'error': 'JSON 解析失败', 'raw_response': response_text}), 500

        return jsonify({
            'success': True,
            'data': json_data,
            'raw_response': response_text
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/generate-unified', methods=['POST'])
def generate_unified():
    """生成统一的中医调理方案（包含大体状况、中药调理、日常调养、复诊安全）"""
    try:
        data = request.get_json()
        user_input = data.get('prompt', '')

        if not user_input:
            return jsonify({'error': '请提供患者症状描述'}), 400

        import concurrent.futures
        import requests

        def call_api(endpoint, prompt):
            try:
                response = requests.post(
                    f'http://localhost:5000/{endpoint}',
                    json={'prompt': prompt},
                    timeout=50
                )
                return response.json()
            except Exception as e:
                return {'success': False, 'error': str(e)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                'hero': executor.submit(call_api, 'generate-hero', user_input),
                'prescription': executor.submit(call_api, 'generate-prescription', user_input),
                'suggestion': executor.submit(call_api, 'generate-suggestion', user_input),
                'followup': executor.submit(call_api, 'generate-followup', user_input)
            }

            results = {key: future.result() for key, future in futures.items()}

        all_success = all(result.get('success', False) for result in results.values())

        if all_success:
            return jsonify({
                'success': True,
                'data': {
                    'hero': results['hero']['data'],
                    'prescription': results['prescription']['data'],
                    'suggestion': results['suggestion']['data'],
                    'followup': results['followup']['data']
                }
            })
        else:
            errors = []
            for key, result in results.items():
                if not result.get('success', False):
                    errors.append(f'{key}: {result.get("error", "未知错误")}')
            return jsonify({'error': '部分生成失败: ' + '; '.join(errors)}), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/test', methods=['GET'])
def test():
    """测试接口"""
    return jsonify({'message': '后端服务运行正常'})

if __name__ == '__main__':
    print("启动中医 AI 后端服务...")
    print("访问 http://localhost:5000/test 测试服务状态")
    app.run(host='0.0.0.0', port=5000, debug=True)