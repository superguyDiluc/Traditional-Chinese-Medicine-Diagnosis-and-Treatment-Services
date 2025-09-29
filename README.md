# 中医调理方案生成系统使用说明

## 概述

本系统通过结构化的 JSON 数据来生成中医调理方案的展示页面。主要用于动态生成 `tcm-hero` 模块的内容，该模块展示患者的大体状况、症状标签和调理总结。

## JSON 数据结构

### 基本格式

```json
{
  "title": {
    "icon": "Font Awesome 图标类名",
    "text": "标题文本"
  },
  "symptoms": [
    {
      "icon": "Font Awesome 图标类名",
      "text": "症状描述"
    }
  ],
  "summary": {
    "treatmentGoal": "调理目标",
    "constitution": "体质特点",
    "recommendation": "推荐节奏"
  },
  "note": "温馨提示内容"
}
```

### 字段说明

- **title**: 模块标题
  - `icon`: Font Awesome 图标类名（如 "fas fa-leaf"）
  - `text`: 显示的标题文本

- **symptoms**: 症状标签数组
  - `icon`: 每个症状对应的图标
  - `text`: 症状描述文本

- **summary**: 调理总结信息
  - `treatmentGoal`: 调理目标
  - `constitution`: 体质特点
  - `recommendation`: 推荐的调理节奏

- **note**: 页面底部的温馨提示文本

## 使用方法

### 1. 使用预设示例

页面顶部提供了几个预设的病症示例：
- 肝郁气滞
- 脾胃虚弱  
- 肾阳虚
- 血瘀体质
- 原始示例（心肾不交 · 阴虚火旺）

点击对应按钮即可快速切换不同的病症展示。

### 2. 自定义数据

1. 在 JSON 编辑框中修改或输入新的 JSON 数据
2. 点击"格式化 JSON"按钮可以美化 JSON 格式
3. 点击"应用数据"按钮将自定义数据应用到页面

### 3. API 集成

在实际应用中，可以通过以下方式集成：

```javascript
// 从后端 API 获取数据
fetch('/api/tcm-diagnosis', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        symptoms: ['失眠', '心悸', '盗汗'],
        patient_info: { /* 患者信息 */ }
    })
})
.then(response => response.json())
.then(data => {
    updateTcmHero(data);
});
```

## JavaScript API

### 核心函数

#### `generateTcmHero(data)`
根据 JSON 数据生成 HTML 模板字符串。

参数：
- `data`: 符合规格的 JSON 对象

返回：
- HTML 字符串

#### `updateTcmHero(data)`
更新页面中的 tcm-hero 模块内容。

参数：
- `data`: 符合规格的 JSON 对象

#### `loadExample(exampleName)`
加载预设示例数据。

参数：
- `exampleName`: 示例名称（如 "肝郁气滞"）

#### `applyCustomData()`
应用 JSON 编辑框中的自定义数据。

#### `formatJSON()`
格式化 JSON 编辑框中的内容。

## 扩展说明

### 添加新的病症示例

在 `tcmExamples` 对象中添加新的示例：

```javascript
const tcmExamples = {
    // 现有示例...
    "新病症": {
        "title": {
            "icon": "fas fa-leaf",
            "text": "大体状况（新病症描述）"
        },
        "symptoms": [
            // 症状列表
        ],
        "summary": {
            // 总结信息
        },
        "note": "温馨提示"
    }
};
```

### 自定义图标

可以使用任何 Font Awesome 图标，常用的中医相关图标：
- `fas fa-leaf` - 叶子（通用）
- `fas fa-heart` - 心脏
- `fas fa-stomach` - 胃部
- `fas fa-moon` - 月亮（失眠）
- `fas fa-fire` - 火焰（热证）
- `fas fa-snowflake` - 雪花（寒证）
- `fas fa-tired` - 疲劳
- `fas fa-dizzy` - 眩晕

## Prompt 示例

如果要让 AI 模型生成相应的 JSON 数据，可以使用类似以下的 prompt：

```
请根据以下症状和诊断信息，生成一个符合中医调理方案格式的 JSON 数据：

患者症状：[列出症状]
中医诊断：[诊断结果]
调理方向：[调理思路]

请按照以下 JSON 格式输出：
{
  "title": {
    "icon": "fas fa-leaf",
    "text": "大体状况（诊断名称）"
  },
  "symptoms": [
    {"icon": "相关图标", "text": "症状描述"}
  ],
  "summary": {
    "treatmentGoal": "调理目标",
    "constitution": "体质特点",
    "recommendation": "推荐节奏"
  },
  "note": "专业提示"
}
```

## 注意事项

1. JSON 格式必须严格符合规范，缺少字段会导致显示错误
2. 图标类名必须是有效的 Font Awesome 类名
3. 建议在应用自定义数据前先使用格式化功能检查语法
4. 系统仅用于展示目的，不能替代专业医疗诊断