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
    model: str = "simple"  # Default to simple model

# Model mapping dictionary
MODEL_MAP = {
    "simple": SimpleModel,
    "copilot": CopilotModel,
    "advanced": AdvancedModel,
    "ollama": OllamaModel
}

@app.post("/api/analyze")
async def analyze_sql(request: SQLAnalysisRequest):
    """Analyze SQL query for safety and performance"""
    try:
        # Get the requested model class
        model_class = MODEL_MAP.get(request.model.lower())
        if not model_class:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported model type: {request.model}. Available options: simple, copilot, advanced, ollama"
            )
        
        # Instantiate model and analyze SQL
        model = model_class()
        result = model.analyze(request.sql)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API root path, returns basic information"""
    return {
        "name": "SQL Safety Checker API",
        "version": "1.0.0",
        "description": "API for analyzing SQL queries for safety and performance"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)