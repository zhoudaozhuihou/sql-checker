from typing import Dict, Any, List
from .base_model import SQLAnalyzerModel
import re

class AdvancedModel(SQLAnalyzerModel):
    """提供高级SQL分析功能的模型"""
    
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
            "details": "由高级分析模型生成"
        }
    
    def get_safety_issues(self, sql_query: str) -> List[Dict[str, Any]]:
        issues = []
        
        # 检查SQL注入风险
        if "'" in sql_query or "\"" in sql_query:
            issues.append({
                "issue": "可能存在SQL注入风险",
                "severity": "high",
                "recommendation": "使用参数化查询替代字符串拼接，并对输入进行严格验证"
            })
        
        # 检查危险操作
        dangerous_keywords = {
            "DROP": "删除数据库对象",
            "TRUNCATE": "清空表数据",
            "DELETE": "删除数据",
            "UPDATE": "更新数据",
            "GRANT": "授予权限",
            "REVOKE": "撤销权限",
            "EXECUTE": "执行动态SQL"
        }
        
        for keyword, description in dangerous_keywords.items():
            if re.search(rf"\b{keyword}\b", sql_query.upper()):
                issues.append({
                    "issue": f"包含危险操作: {keyword} ({description})",
                    "severity": "high",
                    "recommendation": "确保有适当的权限控制、数据备份和审计日志"
                })
        
        # 检查注释
        if "--" in sql_query or "/*" in sql_query:
            issues.append({
                "issue": "包含SQL注释",
                "severity": "medium",
                "recommendation": "移除不必要的注释，防止SQL注入"
            })
        
        return issues
    
    def get_performance_suggestions(self, sql_query: str) -> List[Dict[str, Any]]:
        suggestions = []
        
        # 检查SELECT *
        if re.search(r"SELECT\s+\*", sql_query.upper()):
            suggestions.append({
                "suggestion": "避免使用SELECT *",
                "impact": "medium",
                "recommendation": "明确指定需要的列名，减少不必要的数据传输"
            })
        
        # 检查是否缺少WHERE子句
        if not re.search(r"\bWHERE\b", sql_query.upper()) and (
            re.search(r"\bUPDATE\b", sql_query.upper()) or 
            re.search(r"\bDELETE\b", sql_query.upper())):
            suggestions.append({
                "suggestion": "缺少WHERE子句",
                "impact": "high",
                "recommendation": "添加WHERE子句以限制影响范围，防止全表更新或删除"
            })
        
        # 检查LIKE通配符
        if re.search(r"LIKE\s+'%.*'", sql_query.upper()):
            suggestions.append({
                "suggestion": "LIKE子句以通配符开头",
                "impact": "high",
                "recommendation": "避免在LIKE子句中使用前缀通配符，可能导致全表扫描"
            })
        
        # 检查JOIN
        if re.search(r"\bJOIN\b", sql_query.upper()) and not re.search(r"\bON\b", sql_query.upper()):
            suggestions.append({
                "suggestion": "JOIN缺少ON子句",
                "impact": "high",
                "recommendation": "添加明确的JOIN条件，避免笛卡尔积"
            })
        
        return suggestions
    
    def calculate_risk_score(self, sql_query: str) -> int:
        score = 0
        
        # 基于关键字评估风险
        high_risk_keywords = ["DROP", "TRUNCATE", "DELETE", "UPDATE", "GRANT", "REVOKE"]
        medium_risk_keywords = ["ALTER", "CREATE", "INSERT", "EXECUTE"]
        
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
            score += 20
        
        # 注释风险
        if "--" in sql_query or "/*" in sql_query:
            score += 10
        
        # 性能风险
        if re.search(r"SELECT\s+\*", sql_query.upper()):
            score += 5
        
        if re.search(r"LIKE\s+'%.*'", sql_query.upper()):
            score += 10
        
        # 确保分数在0-100之间
        return max(0, min(100, score))