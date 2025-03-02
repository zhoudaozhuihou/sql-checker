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

## 部署方式

### 环境要求

- Python 3.8+
- pip包管理工具

### 安装步骤

1. 克隆项目代码
```bash
git clone https://github.com/yourusername/sql-check.git
cd sql-check
```

2. 安装依赖包
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
# 复制环境变量示例文件
copy .env.example .env

# 编辑.env文件，配置必要的环境变量
# 如果使用Copilot模型，需要配置GitHub Copilot API密钥
GITHUB_COPILOT_TOKEN=your_token_here
```

## 启动方式

### 启动API服务

```bash
python app.py
```

服务默认在 http://localhost:5000 启动，可以通过环境变量配置端口号：
```bash
# Windows
set PORT=8000
python app.py

# Linux/Mac
export PORT=8000
python app.py
```

## 配置新模型

### 创建新的分析模型

1. 在`models`目录下创建新的模型文件，例如`custom_model.py`

2. 继承基础模型类并实现必要的方法：

```python
from typing import Dict, Any, List
from .base_model import SQLAnalyzerModel

class CustomModel(SQLAnalyzerModel):
    """自定义SQL分析模型"""
    
    def analyze(self, sql_query: str) -> Dict[str, Any]:
        """实现SQL分析逻辑"""
        safety_issues = self.get_safety_issues(sql_query)
        performance_suggestions = self.get_performance_suggestions(sql_query)
        risk_score = self.calculate_risk_score(sql_query)
        
        return {
            "safety_issues": safety_issues,
            "performance_suggestions": performance_suggestions,
            "risk_score": risk_score,
            "risk_level": self.get_risk_level(risk_score),
            "details": "由自定义模型分析生成"
        }
    
    def get_safety_issues(self, sql_query: str) -> List[Dict[str, Any]]:
        """实现安全性检查逻辑"""
        # 自定义实现
        pass
    
    def get_performance_suggestions(self, sql_query: str) -> List[Dict[str, Any]]:
        """实现性能建议逻辑"""
        # 自定义实现
        pass
    
    def calculate_risk_score(self, sql_query: str) -> int:
        """实现风险评分逻辑"""
        # 自定义实现
        pass
```

3. 在`models/__init__.py`中注册新模型：

```python
from .custom_model import CustomModel

# 将新模型添加到可用模型字典中
MODEL_MAPPING = {
    "simple": SimpleModel,
    "advanced": AdvancedModel,
    "copilot": CopilotModel,
    "ollama": OllamaModel,
    "custom": CustomModel  # 添加新模型
}
```

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
| 低风险 | 0-30 |
| 中风险 | 31-70 |
| 高风险 | 71-100 |
