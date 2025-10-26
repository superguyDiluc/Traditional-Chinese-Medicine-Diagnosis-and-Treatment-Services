# 项目介绍
基于“百炼大模型”平台训练的模型，为用户提供高质量的中医建议。

**主要模块**

- 大体状况（TCM Hero）：展示证型标题、症状标签、调理目标/体质/节奏与温馨提示。
- 中药调理方案（Prescription）：方剂卡片组合，支持折叠、列表/步骤/文本等多段落结构。
- 日常生活调养（Suggestion）：饮食、睡眠、情志、运动四类卡片。
- 复诊与安全提示（Followup）：复诊安排、监测要点、安全用药、警示信号与总括提醒。

## 后端

**环境变量设置**

- 由于基于百炼大模型提供的模型应用接口，需要先设置模型的API_KEY与APP_ID。
- 在根目录下创建.env文件，并填入下列信息

```
DASHSCOPE_API_KEY = "你的API_KEY"
DASHSCOPE_APP_ID = "你的APP_ID"
```

**本地启动**

本项目使用uv来管理

在项目根目录下创建虚拟环境并激活
```powershell
uv venv
.venv/Scripts/activate.ps1
```

安装相关依赖
```powershell
uv sync
```

启动后端
```poweshell
uv run backend.py
```

**backend/prompts.py**

- 由于需要定制化内容生成，所以通过json来结构化模型输出。该文件有四个模块的内嵌模板。后续如果若要为模板添加新的内容，或者新增模板。统一在这里添加

**backend/backend.py**

- 后端采用的是flask服务，有一个统一函数`generate_unified()`通过线程池来异步调用四个模块，最后将模型生成的结果收集起来，并JSON化交给发送给前端。

- 每个模块的流程是这样的，将PROMPTS中的模板先格式化，然后作为输入丢给模型，再将模型返回的内容JSON化并返回

## 前端

**入口文件**

- frontend/index.html 为纯静态页面，无打包与框架依赖，直接在浏览器中打开即可预览 UI。

**交互与渲染**

- 控制面板支持一键“AI 生成完整方案”，输入症状后请求后端统一接口，自动渲染四大模块。
- 卡片折叠组件支持点击与键盘 Enter/Space 切换，提升可访问性。
- 示例数据集（tcmExamples、prescriptionExamples、suggestionExamples）可离线预览样式。

**后端接口**

- API_BASE_URL 默认为 http://localhost:5000
- 后端返回的四块数据分别通过适配器转换后渲染。

**数据适配器（容错与规范化）**

- adaptHeroData(aiData)：将后端/AI 字段映射为前端所需的标题、症状、摘要与提示。
- adaptPrescriptionData(aiData)：兼容多种字段命名（name/title、sections/items/content），统一为卡片+段落结构。
- adaptSuggestionData(aiData)：将 suggestions/tips 标准化为图标+标题+内容的卡片列表。
- adaptFollowupData(aiData)：统一 followupItems/monitoring/safetyNotes/warningSignals，支持列表或纯文本。

对应渲染函数：
- updateTcmHero、updatePrescription、updateSuggestion、updateFollowup 负责将规范化数据注入 DOM。

**本地启动**

- frontend 目录运行：
  - Python: uv run python -m http.server 8080

**依赖与资源**

- 使用 Font Awesome CDN 提供图标，无其它前端依赖与构建步骤。