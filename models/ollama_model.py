from typing import Dict, Any, List
import requests
import json
from .base_model import SQLAnalyzerModel

class OllamaModel(SQLAnalyzerModel):
    """使用Ollama进行SQL分析的模型实现"""
    
    def __init__(self, model_name: str = "deepseek-coder:6.7b", api_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.api_url = api_url
        
    def _query_ollama(self, prompt: str) -> str:
        """向Ollama API发送请求"""
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt
                },
                stream=True
            )
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line)
                        full_response += json_response.get('response', '')
                    except json.JSONDecodeError:
                        continue
            return full_response
        except Exception as e:
            raise Exception(f"Ollama API调用失败: {str(e)}")
    
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
            "details": "由Ollama模型分析生成"
        }
    
    def get_safety_issues(self, sql_query: str) -> List[Dict[str, Any]]:
        prompt = f"分析以下SQL查询的安全问题，以JSON格式返回问题列表：\n{sql_query}"
        response = self._query_ollama(prompt)
        try:
            # 这里假设Ollama返回的是格式化的JSON字符串
            import json
            issues = json.loads(response)
            return issues if isinstance(issues, list) else []
        except:
            return [{
                "issue": "无法解析Ollama返回的安全问题分析结果",
                "severity": "high",
                "recommendation": "请检查Ollama服务是否正常运行"
            }]
    
    def get_performance_suggestions(self, sql_query: str) -> List[Dict[str, Any]]:
        prompt = f"分析以下SQL查询的性能问题，提供优化建议，以JSON格式返回：\n{sql_query}"
        response = self._query_ollama(prompt)
        try:
            import json
            suggestions = json.loads(response)
            return suggestions if isinstance(suggestions, list) else []
        except:
            return [{
                "suggestion": "无法解析Ollama返回的性能建议",
                "impact": "medium",
                "recommendation": "请检查Ollama服务是否正常运行"
            }]
    
    def calculate_risk_score(self, sql_query: str) -> int:
        prompt = f"评估以下SQL查询的风险等级（0-100），只返回数字：\n{sql_query}"
        response = self._query_ollama(prompt)
        try:
            score = int(response.strip())
            return max(0, min(100, score))  # 确保分数在0-100之间
        except:
            return 50  # 默认中等风险