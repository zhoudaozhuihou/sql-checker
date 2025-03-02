from typing import Dict, Any, List
from .base_model import SQLAnalyzerModel
import re

class SimpleModel(SQLAnalyzerModel):
    """基于规则的简单SQL分析模型"""
    
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
            "details": "由简单规则模型分析生成"
        }
    
    def get_safety_issues(self, sql_query: str) -> List[Dict[str, Any]]:
        issues = []
        
        # 检查SQL注入风险
        if "'" in sql_query or "\"" in sql_query:
            issues.append({
                "issue": "可能存在SQL注入风险",
                "severity": "high",
                "recommendation": "使用参数化查询替代字符串拼接"
            })
        
        # 检查危险操作
        dangerous_keywords = ["DROP", "TRUNCATE", "DELETE", "UPDATE"]
        for keyword in dangerous_keywords:
            if re.search(rf"\b{keyword}\b", sql_query.upper()):
                issues.append({
                    "issue": f"包含危险操作: {keyword}",
                    "severity": "high",
                    "recommendation": "确保有适当的权限控制和数据备份"
                })
        
        return issues
    
    def get_performance_suggestions(self, sql_query: str) -> List[Dict[str, Any]]:
        suggestions = []
        
        # 检查SELECT *
        if re.search(r"SELECT\s+\*", sql_query.upper()):
            suggestions.append({
                "suggestion": "避免使用SELECT *",
                "impact": "medium",
                "recommendation": "明确指定需要的列名"
            })
        
        # 检查是否缺少WHERE子句
        if not re.search(r"\bWHERE\b", sql_query.upper()) and (
            re.search(r"\bUPDATE\b", sql_query.upper()) or 
            re.search(r"\bDELETE\b", sql_query.upper())):
            suggestions.append({
                "suggestion": "缺少WHERE子句",
                "impact": "high",
                "recommendation": "添加WHERE子句以限制影响范围"
            })
        
        return suggestions
    
    def calculate_risk_score(self, sql_query: str) -> int:
        score = 0
        
        # 基于关键字评估风险
        high_risk_keywords = ["DROP", "TRUNCATE", "DELETE", "UPDATE"]
        medium_risk_keywords = ["ALTER", "CREATE", "INSERT"]
        
        # 高风险操作
        for keyword in high_risk_keywords:
            if re.search(rf"\b{keyword}\b", sql_query.upper()):
                score = 70  # 设置基础分数为70
                break  # 一旦发现高风险操作，立即设置基础分数
        
        # 中等风险操作
        for keyword in medium_risk_keywords:
            if re.search(rf"\b{keyword}\b", sql_query.upper()):
                score += 15
        
        # SQL注入风险
        if "'" in sql_query or "\"" in sql_query:
            score += 25
        
        # 确保分数在0-100之间
        return max(0, min(100, score))