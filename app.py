from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from models import SimpleModel, CopilotModel, AdvancedModel, OllamaModel
import json
import os

app = FastAPI(
    title="SQL Safety Checker API",
    description="API for analyzing SQL queries for safety and performance",
    version="1.0.0"
)

class SQLAnalysisRequest(BaseModel):
    sql: str
    model: str = "simple"  # Default to simple model

class AnalysisIssue(BaseModel):
    type: str
    severity: str
    description: str
    suggestion: str

class SQLAnalysisResponse(BaseModel):
    safety_score: float
    performance_score: float
    issues: List[AnalysisIssue]
    summary: str

# Model mapping dictionary
MODEL_MAP = {
    "simple": SimpleModel,
    "copilot": CopilotModel,
    "advanced": AdvancedModel,
    "ollama": OllamaModel
}

def validate_analysis_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate analysis result against the prompt template requirements"""
    try:
        # Validate scores
        if not (0 <= result.get('safety_score', 0) <= 100):
            raise ValueError("Safety score must be between 0 and 100")
        if not (0 <= result.get('performance_score', 0) <= 100):
            raise ValueError("Performance score must be between 0 and 100")
        
        # Validate issues
        for issue in result.get('issues', []):
            if issue['type'] not in ['safety', 'performance']:
                raise ValueError(f"Invalid issue type: {issue['type']}")
            if issue['severity'] not in ['high', 'medium', 'low']:
                raise ValueError(f"Invalid severity: {issue['severity']}")
            if not issue.get('description') or not issue.get('suggestion'):
                raise ValueError("Issue must have description and suggestion")
        
        # Validate summary
        if not result.get('summary'):
            raise ValueError("Analysis must include a summary")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid analysis result format: {str(e)}")

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
        
        # Validate and return the result
        validated_result = validate_analysis_result(result)
        return SQLAnalysisResponse(**validated_result)
    
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