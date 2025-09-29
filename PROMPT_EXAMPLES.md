# 中医调理方案生成 - Prompt 示例

## 用于生成 JSON 数据的 Prompt 模板

### 基础 Prompt

```
你是一位专业的中医师，请根据以下信息生成一个中医调理方案的结构化数据。

请严格按照以下 JSON 格式输出，不要添加任何额外的文字解释：

{
  "title": {
    "icon": "fas fa-leaf",
    "text": "大体状况（[中医诊断名称]）"
  },
  "symptoms": [
    {
      "icon": "[Font Awesome图标类名]",
      "text": "[症状描述]"
    }
  ],
  "summary": {
    "treatmentGoal": "[调理目标，使用·分隔多个要点]",
    "constitution": "[体质特点描述]",
    "recommendation": "[推荐的调理方式]"
  },
  "note": "[专业的温馨提示，建议在50字以内]"
}

患者信息：
- 主要症状：[在这里填入症状]
- 体质特征：[在这里填入体质信息]
- 中医诊断：[在这里填入诊断结果]

请生成对应的 JSON 数据。
```

### 具体示例 1

```
你是一位专业的中医师，请根据以下信息生成一个中医调理方案的结构化数据。

患者信息：
- 主要症状：经常头晕目眩，疲倦乏力，食欲不振，面色苍白，月经量少色淡
- 体质特征：气血不足，脉象细弱，舌质淡
- 中医诊断：气血两虚

请按照指定的 JSON 格式输出调理方案数据。
```

### 具体示例 2  

```
你是一位专业的中医师，请根据以下信息生成一个中医调理方案的结构化数据。

患者信息：
- 主要症状：口干口苦，大便干结，易怒烦躁，胸胁胀痛，睡眠不安
- 体质特征：肝火旺盛，舌红苔黄，脉弦数
- 中医诊断：肝火上炎

请按照指定的 JSON 格式输出调理方案数据。
```

## 常用 Font Awesome 图标参考

### 症状相关图标
- `fas fa-moon` - 失眠、睡眠问题
- `fas fa-heart` - 心悸、胸闷
- `fas fa-fire` - 发热、上火症状
- `fas fa-snowflake` - 怕冷、寒证
- `fas fa-stomach` - 消化系统症状
- `fas fa-tired` - 疲劳、乏力
- `fas fa-dizzy` - 头晕、眩晕
- `fas fa-headache` - 头痛
- `fas fa-angry` - 易怒、情绪问题
- `fas fa-sad-tear` - 抑郁、情绪低落
- `fas fa-tint` - 汗出、分泌物异常
- `fas fa-bolt` - 疼痛、刺痛
- `fas fa-cloud-moon` - 多梦、睡眠质量差
- `fas fa-face-frown` - 面色不佳
- `fas fa-back` - 腰背疼痛
- `fas fa-hand-dots` - 皮肤问题
- `fas fa-circle` - 舌象异常

### 调理方式图标
- `fas fa-leaf` - 中药治疗
- `fas fa-seedling` - 调理养护
- `fas fa-mortar-pestle` - 中药制剂
- `fas fa-yin-yang` - 阴阳调和
- `fas fa-bowl-food` - 食疗
- `fas fa-dumbbell` - 运动调理

## 使用说明

1. 将上述 Prompt 复制到支持中医知识的 AI 模型中
2. 替换患者信息部分的内容
3. 获得 JSON 格式的输出
4. 将 JSON 数据复制到网页的编辑框中
5. 点击"应用数据"按钮查看效果

## 注意事项

1. 确保 AI 模型具备中医知识背景
2. 症状描述要准确简洁
3. 图标选择要与症状相关
4. JSON 格式必须严格正确
5. 温馨提示应该包含专业建议