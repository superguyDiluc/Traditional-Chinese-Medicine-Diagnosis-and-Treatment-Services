# 中药调理方案（Prescription）模块生成指南

## 概述

本文档介绍如何使用 AI 模型生成中药调理方案模块的结构化 JSON 数据。该模块用于展示具体的中药方剂、食疗方案和相关的使用指导。

## JSON 数据结构

### 完整格式

```json
{
  "sectionTitle": {
    "icon": "Font Awesome 图标类名",
    "text": "章节标题"
  },
  "prescriptions": [
    {
      "name": "方剂名称",
      "icon": "Font Awesome 图标类名", 
      "sections": [
        {
          "title": "小节标题",
          "icon": "Font Awesome 图标类名",
          "type": "内容类型",
          "content": "内容数据"
        }
      ]
    }
  ]
}
```

### 字段说明

- **sectionTitle**: 整个模块的标题
  - `icon`: 章节图标
  - `text`: 章节标题文本

- **prescriptions**: 方剂/方案数组
  - `name`: 方剂名称
  - `icon`: 方剂图标
  - `sections`: 详细信息部分数组

- **sections**: 方剂详细信息
  - `title`: 小节标题
  - `icon`: 小节图标
  - `type`: 内容类型（"list", "steps", "text"）
  - `content`: 具体内容

### 内容类型说明

1. **"list"**: 无序列表，`content` 为字符串数组
2. **"steps"**: 有序步骤，`content` 为字符串数组
3. **"text"**: 段落文本，`content` 为字符串

## Prompt 模板

### 基础 Prompt

```
你是一位专业的中医师，请根据以下信息生成中药调理方案的结构化数据。

请严格按照以下 JSON 格式输出，不要添加任何额外的文字解释：

{
  "sectionTitle": {
    "icon": "fas fa-prescription-bottle-alt",
    "text": "中药调理方案"
  },
  "prescriptions": [
    {
      "name": "[方剂名称]",
      "icon": "[图标类名]",
      "sections": [
        {
          "title": "组成与剂量",
          "icon": "fas fa-list-ul",
          "type": "list",
          "content": ["[药材清单]"]
        },
        {
          "title": "功能主治", 
          "icon": "fas fa-stethoscope",
          "type": "text",
          "content": "[功效描述]"
        },
        {
          "title": "服用建议",
          "icon": "fas fa-calendar-day", 
          "type": "text",
          "content": "[用法用量]"
        },
        {
          "title": "调整方向",
          "icon": "fas fa-lightbulb",
          "type": "text", 
          "content": "[加减化裁]"
        },
        {
          "title": "注意事项",
          "icon": "fas fa-exclamation-triangle",
          "type": "text",
          "content": "[禁忌注意]"
        }
      ]
    }
  ]
}

病情信息：
- 中医诊断：[诊断名称]
- 主要症状：[症状列表]
- 治疗原则：[治法]

请生成 2-3 个调理方案（包括中药方剂和食疗）。
```

### 具体示例 1 - 肝郁气滞

```
你是一位专业的中医师，请根据以下信息生成中药调理方案的结构化数据。

病情信息：
- 中医诊断：肝郁气滞证
- 主要症状：胸胁胀痛，情绪抑郁，易怒烦躁，口苦咽干
- 治疗原则：疏肝解郁，理气和中

请生成包含以下方案的 JSON 数据：
1. 逍遥散加减（中药方剂）
2. 疏肝理气茶（食疗方案）

按照标准 JSON 格式输出，包含组成、功效、用法、注意事项等完整信息。
```

### 具体示例 2 - 脾胃虚弱

```
你是一位专业的中医师，请根据以下信息生成中药调理方案的结构化数据。

病情信息：
- 中医诊断：脾胃虚弱证
- 主要症状：食欲不振，腹胀腹泻，疲倦乏力，面色萎黄
- 治疗原则：健脾益气，和胃助运

请生成包含以下方案的 JSON 数据：
1. 四君子汤加味（中药方剂）
2. 健脾养胃粥（食疗方案）

按照标准 JSON 格式输出，包含完整的制作方法和使用指导。
```

## 常用图标参考

### 方剂类型图标
- `fas fa-seedling` - 中药方剂
- `fas fa-bowl-food` - 食疗方案
- `fas fa-yin-yang` - 特殊配方
- `fas fa-mortar-pestle` - 丸散剂
- `fas fa-vial` - 汤剂

### 信息类型图标
- `fas fa-list-ul` - 组成、食材
- `fas fa-stethoscope` - 功能主治
- `fas fa-calendar-day` - 服用建议
- `fas fa-utensils` - 制作方法
- `fas fa-lightbulb` - 调整方向
- `fas fa-exclamation-triangle` - 注意事项
- `fas fa-eye` - 观察重点
- `fas fa-brain` - 治疗思路
- `fas fa-clipboard-check` - 用法
- `fas fa-circle-info` - 温馨提示

## 使用指南

### 1. 数据验证要点
- JSON 格式必须严格正确
- 每个方剂至少包含 3-5 个 sections
- content 数组中每个元素应简洁明确
- 图标类名必须是有效的 Font Awesome 类名

### 2. 内容编写建议
- **组成与剂量**: 药物名称 + 用量，用 "·" 分隔
- **功能主治**: 简明扼要地描述功效和适应症
- **服用建议**: 明确用法用量和服用时间
- **注意事项**: 重点提及禁忌和注意事项

### 3. 方案搭配原则
- 中药方剂 + 食疗方案
- 经典方剂 + 现代应用
- 内服 + 外用（如适用）

## 示例输出

```json
{
  "sectionTitle": {
    "icon": "fas fa-prescription-bottle-alt",
    "text": "中药调理方案"
  },
  "prescriptions": [
    {
      "name": "逍遥散加减",
      "icon": "fas fa-seedling",
      "sections": [
        {
          "title": "组成与剂量",
          "icon": "fas fa-list-ul",
          "type": "list",
          "content": [
            "柴胡 10克 · 当归 12克 · 白芍 12克",
            "白术 10克 · 茯苓 15克 · 炙甘草 6克"
          ]
        },
        {
          "title": "功能主治",
          "icon": "fas fa-stethoscope", 
          "type": "text",
          "content": "疏肝解郁，健脾和胃。主治肝郁脾虚证。"
        }
      ]
    }
  ]
}
```

## 注意事项

1. **安全性**: 生成的方剂必须是经典有效的中医方剂
2. **准确性**: 药物剂量应符合临床常用标准
3. **完整性**: 每个方案都应包含完整的使用指导
4. **专业性**: 术语使用应准确，符合中医理论

通过使用这些 Prompt 模板，AI 模型可以生成标准化的中药调理方案数据，直接应用到网页系统中。