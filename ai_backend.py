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
  "patientName": "患者姓名（如无则填：患者）",
  "syndrome": "中医证型名称",
  "icon": "fas fa-yin-yang",
  "description": "症状描述（50-80字）",
  "symptoms": [
    "主要症状1",
    "主要症状2",
    "主要症状3"
  ],
  "pulse": "脉象描述",
  "tongue": "舌象描述"
}}

用户描述的症状：{user_input}

请直接返回标准的 JSON 格式，不要包含任何其他文字说明。
"""

# Prescription 模块的 Prompt 模板
PRESCRIPTION_PROMPT = PRESCRIPTION_PROMPT = """
请根据用户描述的中医证型或症状，生成一个中药调理方案的 JSON 数据。JSON 格式如下：

{{
  "sectionTitle": "调理方案标题",
  "prescriptions": [
    {{
      "title": "方剂名称",
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
    }},
    {{
      "title": "饮食调理",
      "icon": "fas fa-utensils",
      "sections": [
        {{
          "type": "list",
          "title": "推荐食物",
          "items": [
            "适宜食物1",
            "适宜食物2",
            "适宜食物3"
          ]
        }},
        {{
          "type": "list",
          "title": "忌食",
          "items": [
            "禁忌食物1",
            "禁忌食物2"
          ]
        }}
      ]
    }},
    {{
      "title": "生活调理",
      "icon": "fas fa-spa",
      "sections": [
        {{
          "type": "steps",
          "title": "日常护理",
          "items": [
            "作息调理建议",
            "运动调理建议",
            "情志调理建议"
          ]
        }}
      ]
    }}
  ]
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

@app.route('/test', methods=['GET'])
def test():
    """测试接口"""
    return jsonify({'message': '后端服务运行正常'})

if __name__ == '__main__':
    print("启动中医 AI 后端服务...")
    print("访问 http://localhost:5000/test 测试服务状态")
    app.run(host='0.0.0.0', port=5000, debug=True)