from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from models import SimpleModel, CopilotModel, AdvancedModel, OllamaModel

app = FastAPI(
    title="SQL Safety Checker API",
    description="API for analyzing SQL queries for safety and performance",
    version="1.0.0"
)

class SQLAnalysisRequest(BaseModel):
    sql: str
    model: str = "simple"  # 默认使用simple模型

# 模型映射字典
MODEL_MAP = {
    "simple": SimpleModel,
    "copilot": CopilotModel,
    "advanced": AdvancedModel,
    "ollama": OllamaModel
}

@app.post("/api/analyze")
async def analyze_sql(request: SQLAnalysisRequest):
    """分析SQL查询的安全性和性能"""
    try:
        # 获取请求的模型类
        model_class = MODEL_MAP.get(request.model.lower())
        if not model_class:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的模型类型: {request.model}. 可用选项: simple, copilot, advanced"
            )
        
        # 实例化模型并分析SQL
        model = model_class()
        result = model.analyze(request.sql)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API根路径，返回基本信息"""
    return {
        "name": "SQL Safety Checker API",
        "version": "1.0.0",
        "description": "API for analyzing SQL queries for safety and performance"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)