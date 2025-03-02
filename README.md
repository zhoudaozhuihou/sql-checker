# SQL Safety Checker

一个全面的SQL分析工具，用于检查SQL查询的安全性问题、性能优化建议，并提供改进建议。

## 功能特点

- 多种分析模型：
  - **SimpleModel**: 基于规则的基础SQL分析
  - **CopilotModel**: 使用GitHub Copilot API的AI驱动SQL分析
  - **AdvancedModel**: 具有详细安全检查的综合SQL分析
  - **OllamaModel**: 基于Ollama的本地AI模型分析
- 安全性检查
- 性能优化建议
- SQL注入漏洞检测
- 风险评分和分级
- API接口集成
- 分析结果存储

## 项目结构

```
sql-check/
├── models/              # SQL分析模型
├── api/                 # API接口
├── database/           # 数据库集成
├── config/             # 配置管理
├── utils/              # 工具函数
└── main.py            # 应用入口
```

## 使用方法

### Python代码调用

```python
# 示例代码
from models import SimpleModel, CopilotModel, AdvancedModel

# 选择分析模型
model = AdvancedModel()

# 分析SQL查询
result = model.analyze("SELECT * FROM users WHERE id = 1")
print(result)
```

### API接口调用

#### 分析SQL查询

```http
POST /api/analyze
Content-Type: application/json

{
    "sql": "SELECT * FROM users WHERE id = 1",
    "model": "advanced"  # 可选值: simple, copilot, advanced, ollama
}
```

响应格式：

```json
{
    "safety_issues": [
        {
            "issue": "问题描述",
            "severity": "high/medium/low",
            "recommendation": "改进建议"
        }
    ],
    "performance_suggestions": [
        {
            "suggestion": "建议描述",
            "impact": "high/medium/low",
            "recommendation": "优化建议"
        }
    ],
    "risk_score": 25,
    "risk_level": "low/medium/high",
    "details": "分析详情"
}
```

## 评估标准

### 风险评分标准

| 操作类型 | 风险等级 | 基础分值 |
|---------|---------|--------|
| DROP, TRUNCATE, DELETE, UPDATE, GRANT, REVOKE | 高风险 | 70 |
| ALTER, CREATE, INSERT, EXECUTE | 中风险 | +15 |
| SQL注入风险（包含引号） | 中风险 | +20 |
| 包含SQL注释 | 低风险 | +10 |
| SELECT * | 低风险 | +5 |
| LIKE前缀通配符 | 低风险 | +10 |

### 风险等级划分

| 风险等级 | 分数范围 |
|---------|----------|
| 高风险 (High) | 70-100 |
| 中风险 (Medium) | 30-69 |
| 低风险 (Low) | 0-29 |

### 分析模型特点

#### SimpleModel
- 基础的规则匹配
- 快速的风险评估
- 适合简单SQL查询检查

#### AdvancedModel
- 详细的安全性分析
- 全面的性能建议
- 精确的风险评分
- 支持复杂SQL语句

#### CopilotModel
- AI驱动的智能分析
- 需要GitHub Copilot API支持
- 可提供更自然的建议

#### OllamaModel
- 本地AI模型分析
- 无需外部API
- 支持自定义模型

## 环境配置

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
# .env文件
TEST_OLLAMA=true  # 启用Ollama模型测试
TEST_COPILOT=true # 启用Copilot模型测试
```

## 注意事项

1. 高风险操作建议：
   - 确保有适当的权限控制
   - 进行数据备份
   - 启用审计日志

2. 性能优化建议：
   - 避免使用SELECT *
   - 添加适当的WHERE条件
   - 注意索引使用

3. 安全性建议：
   - 使用参数化查询
   - 避免SQL注入风险
   - 限制查询范围