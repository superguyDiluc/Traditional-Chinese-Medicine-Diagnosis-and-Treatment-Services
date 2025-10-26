import os
from dotenv import load_dotenv

# 加载.env文件并读取环境变量
load_dotenv()
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
APP_ID = os.environ.get("DASHSCOPE_APP_ID", "")

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from http import HTTPStatus
from dashscope import Application
# 导入提示词模板
from prompts import (
    TCM_HERO_PROMPT,
    PRESCRIPTION_PROMPT,
    SUGGESTION_PROMPT,
    FOLLOWUP_PROMPT
)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

def call_dashscope_api(prompt):
    """调用 DashScope API"""
    try:
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt,
        )
        
        if response.status_code == HTTPStatus.OK: # type: ignore
            return response.output.text # type: ignore
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

# Hero模块
@app.route('/generate-hero', methods=['POST'])
def generate_hero():
    """
    生成 TCM Hero JSON 数据
    """
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

# Prescription模块
@app.route('/generate-prescription', methods=['POST'])
def generate_prescription():
    """
    生成 Prescription JSON 数据
    """
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

# Suggestion模块
@app.route('/generate-suggestion', methods=['POST'])
def generate_suggestion():
    """
    生成 Suggestion JSON 数据
    """
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

# followup模块
@app.route('/generate-followup', methods=['POST'])
def generate_followup():
    """
    生成复诊与安全提示 JSON 数据
    """
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

# 统一大模块
@app.route('/generate-unified', methods=['POST'])
def generate_unified():
    """
    生成统一的中医调理方案（包含大体状况、中药调理、日常调养、复诊安全
    """
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

# Test模块
@app.route('/test', methods=['GET'])
def test():
    """测试接口"""
    return jsonify({'message': '后端服务运行正常'})

if __name__ == '__main__':
    print("启动中医 AI 后端服务...")
    print("访问 http://localhost:5000/test 测试服务状态")
    app.run(host='0.0.0.0', port=5000, debug=True)