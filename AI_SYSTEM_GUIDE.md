# 中医 AI 系统使用说明

## 系统概述
该系统集成了大模型 AI 功能，可以根据用户输入的症状描述自动生成中医诊断和调理方案的 JSON 数据，并实时显示在网页上。

## 功能特点
- **AI 智能生成**: 基于 DashScope API 的大模型，智能生成中医诊断内容
- **双模块支持**: 支持"大体状况"和"中药调理方案"两个模块的生成
- **实时预览**: 生成的内容立即应用到页面显示
- **JSON 编辑**: 支持手动编辑和格式化 JSON 数据
- **多种示例**: 内置多种证型示例，快速体验

## 快速启动

### 方法一：一键启动（推荐）
1. 双击运行 `start_system.bat`
2. 系统会自动安装依赖并启动前后端服务
3. 访问 http://localhost:8000 使用系统

### 方法二：手动启动
1. 安装 Python 依赖：
   ```bash
   pip install flask flask-cors dashscope
   ```

2. 启动后端服务：
   ```bash
   python ai_backend.py
   ```

3. 启动前端服务：
   ```bash
   python -m http.server 8000
   ```

4. 在浏览器访问：http://localhost:8000

## 使用方法

### 1. AI 生成大体状况
1. 在控制面板中选择"大体状况模块"标签
2. 在"AI 生成大体状况"区域输入患者症状描述
   - 例如：患者失眠多梦，心悸不安，手足心热，口干咽燥，腰膝酸软，舌红少苔，脉细数
3. 点击"AI 生成 JSON"按钮
4. 等待生成完成，系统会自动应用到页面显示

### 2. AI 生成中药调理方案
1. 在控制面板中选择"中药调理模块"标签
2. 在"AI 生成中药调理方案"区域输入证型或症状描述
   - 例如：肝郁气滞型失眠，需要疏肝解郁，养心安神的调理方案
3. 点击"AI 生成 JSON"按钮
4. 等待生成完成，系统会自动应用到页面显示

### 3. 手动编辑 JSON
- 在 JSON 输入框中可以手动编辑生成的数据
- 点击"格式化"按钮美化 JSON 格式
- 点击"应用到xxx"按钮将修改应用到页面

### 4. 使用预设示例
- 点击"肝郁气滞"、"脾胃虚弱"等按钮快速加载示例数据
- 点击"原始示例"恢复默认数据

## 技术架构

### 后端 (ai_backend.py)
- **框架**: Flask + Flask-CORS
- **AI 模型**: 阿里云 DashScope API
- **端口**: 5000
- **API 接口**:
  - `/generate-hero` - 生成大体状况 JSON
  - `/generate-prescription` - 生成中药调理方案 JSON
  - `/test` - 服务状态检测

### 前端 (index.html)
- **技术**: HTML5 + CSS3 + JavaScript
- **UI 组件**: Font Awesome 图标
- **端口**: 8000
- **主要功能**:
  - 响应式设计的中医诊断界面
  - 双模块控制面板
  - AI 生成功能集成
  - JSON 数据实时应用

## 配置说明

### API 密钥配置
在 `ai_backend.py` 中修改以下配置：
```python
API_KEY = "sk-90426267f6844b9d815527ec5c210644"
APP_ID = "09927ed45026488e961c35d96fb4b5c4"
```

### Prompt 模板自定义
可以在 `ai_backend.py` 中修改 `TCM_HERO_PROMPT` 和 `PRESCRIPTION_PROMPT` 变量来自定义 AI 生成的提示词模板。

## 常见问题

### Q: AI 生成失败怎么办？
A: 检查以下几点：
1. 确保后端服务正在运行 (http://localhost:5000/test)
2. 检查 API 密钥是否有效
3. 确保网络连接正常
4. 查看浏览器控制台的错误信息

### Q: 生成的 JSON 格式不正确？
A: 系统会自动从 AI 响应中提取 JSON，如果提取失败，可以：
1. 检查原始响应内容
2. 手动修正 JSON 格式
3. 优化输入的症状描述

### Q: 如何修改 UI 样式？
A: 在 `index.html` 的 `<style>` 部分修改 CSS 样式变量：
```css
:root {
    --tcm-brand-green: #2e7d32;
    --tcm-accent-green: #66bb6a;
    --tcm-soft-bg: #f5f8f4;
    /* 其他样式变量 */
}
```

## 目录结构
```
new_project/
├── index.html              # 前端主页面
├── ai_backend.py           # 后端 API 服务
├── test.py                 # 原始 API 测试脚本
├── start_system.bat        # 一键启动脚本
├── requirements.txt        # Python 依赖包
├── prescription-example.json    # 处方示例数据
├── prescription-examples.json   # 多种处方示例
├── PRESCRIPTION_PROMPT_GUIDE.md # 处方生成指南
├── PROJECT_SUMMARY.md      # 项目总结
└── AI_SYSTEM_GUIDE.md      # 本说明文件
```

## 更新日志
- v1.0 - 基础中医诊断展示系统
- v1.1 - 集成 AI 生成功能
- v1.2 - 优化用户界面和交互体验

## 技术支持
如有问题，请检查：
1. Python 环境是否正确安装
2. 依赖包是否安装完整
3. API 密钥是否有效
4. 网络连接是否正常