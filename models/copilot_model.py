from typing import Dict, Any, List
import requests
from .base_model import SQLAnalyzerModel
import os

class CopilotModel(SQLAnalyzerModel):
    """使用GitHub Copilot进行SQL分析的模型实现"""
    
    def __init__(self):
        self.api_url = os.getenv('COPILOT_API_URL', 'http://localhost:8080')
        self.language = 'sql'
    
    def _query_copilot(self, prompt: str) -> str:
        """向本地Copilot代理服务发送请求"""
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(
                self.api_url,
                headers=headers,
                json={
                    'prompt': prompt,
                    'language': self.language
                }
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise Exception(f"Copilot API调用失败: {str(e)}")
    
    def analyze(self, sql_query: str) -> Dict[str, Any]:
        """分析SQL查询并返回分析结果"""
        safety_issues = self.get_safety_issues(sql_query)
        performance_suggestions = self.get_performance_suggestions(sql_query)
        risk_score = self.calculate_risk_score(sql_query)
        
        return {
            "safety_issues": safety_issues,
            "performance_suggestions": performance_suggestions,
            "risk_score": risk_score,
            "risk_level": self.get_risk_level(risk_score),
            "details": "由GitHub Copilot模型分析生成"
        }
    
    def get_safety_issues(self, sql_query: str) -> List[Dict[str, Any]]:
        prompt = f"分析以下SQL查询的安全问题，返回JSON格式的问题列表，每个问题包含issue、severity和recommendation字段：\n{sql_query}"
        response = self._query_copilot(prompt)
        try:
            import json
            issues = json.loads(response)
            return issues if isinstance(issues, list) else []
        except:
            return [{
                "issue": "无法解析Copilot返回的安全问题分析结果",
                "severity": "high",
                "recommendation": "请检查Copilot API配置是否正确"
            }]
    
    def get_performance_suggestions(self, sql_query: str) -> List[Dict[str, Any]]:
        prompt = f"分析以下SQL查询的性能问题，返回JSON格式的优化建议列表，每个建议包含suggestion、impact和recommendation字段：\n{sql_query}"
        response = self._query_copilot(prompt)
        try:
            import json
            suggestions = json.loads(response)
            return suggestions if isinstance(suggestions, list) else []
        except:
            return [{
                "suggestion": "无法解析Copilot返回的性能建议",
                "impact": "medium",
                "recommendation": "请检查Copilot API配置是否正确"
            }]
    
    def calculate_risk_score(self, sql_query: str) -> int:
        prompt = f"评估以下SQL查询的风险等级，返回0-100之间的整数：\n{sql_query}"
        response = self._query_copilot(prompt)
        try:
            score = int(response.strip())
            return max(0, min(100, score))  # 确保分数在0-100之间
        except:
            return 50  # 默认中等风险