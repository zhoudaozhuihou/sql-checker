from typing import Dict, Any, List
import re
from .base_model import SQLAnalyzerModel

class AdvancedModel(SQLAnalyzerModel):
    """Advanced model implementation for SQL analysis using rule-based approach"""
    
    def analyze(self, sql_query: str) -> Dict[str, Any]:
        """Analyze SQL query and return analysis results"""
        safety_issues = self.get_safety_issues(sql_query)
        performance_suggestions = self.get_performance_suggestions(sql_query)
        risk_score = self.calculate_risk_score(sql_query)
        
        return {
            "safety_issues": safety_issues,
            "performance_suggestions": performance_suggestions,
            "risk_score": risk_score,
            "risk_level": self.get_risk_level(risk_score),
            "details": "Generated by rule-based analysis"
        }
    
    def get_safety_issues(self, sql_query: str) -> List[Dict[str, Any]]:
        """Analyze SQL query for safety issues"""
        issues = []
        
        # Normalize SQL query for analysis
        sql_normalized = sql_query.lower()
        
        # Check for SQL injection risks
        if "'" in sql_query or '"' in sql_query:
            issues.append({
                "issue": "Potential SQL injection risk",
                "severity": "high",
                "recommendation": "Use parameterized queries instead of string concatenation",
                "explanation": "The query contains quote characters which may indicate string concatenation. This could lead to SQL injection if user input is not properly sanitized."
            })
        
        # Check for dangerous operations
        dangerous_operations = {
            "drop": "high",
            "truncate": "high",
            "delete": "medium",
            "update": "medium",
            "grant": "high",
            "revoke": "high",
            "alter": "medium"
        }
        
        for operation, severity in dangerous_operations.items():
            pattern = r'\b' + operation + r'\b'
            if re.search(pattern, sql_normalized):
                issues.append({
                    "issue": f"Dangerous operation: {operation.upper()}",
                    "severity": severity,
                    "recommendation": f"Ensure {operation.upper()} operation is necessary and properly authorized",
                    "explanation": f"The {operation.upper()} operation can potentially cause data loss or security issues if not properly controlled."
                })
        
        # Check for SELECT * usage
        if re.search(r'select\s+\*', sql_normalized):
            issues.append({
                "issue": "Use of SELECT *",
                "severity": "low",
                "recommendation": "Specify only the columns you need instead of using SELECT *",
                "explanation": "Using SELECT * can expose sensitive data and may impact performance by retrieving unnecessary columns."
            })
        
        # Check for comments that might be used for SQL injection
        if "--" in sql_query or "/*" in sql_query:
            issues.append({
                "issue": "SQL comments detected",
                "severity": "medium",
                "recommendation": "Review comments for potential SQL injection vectors",
                "explanation": "SQL comments can sometimes be used to modify query behavior in SQL injection attacks."
            })
        
        return issues
    
    def get_performance_suggestions(self, sql_query: str) -> List[Dict[str, Any]]:
        """Analyze SQL query for performance suggestions"""
        suggestions = []
        
        # Normalize SQL query for analysis
        sql_normalized = sql_query.lower()
        
        # Check for SELECT * usage
        if re.search(r'select\s+\*', sql_normalized):
            suggestions.append({
                "suggestion": "Avoid using SELECT *",
                "impact": "medium",
                "recommendation": "Specify only the columns you need",
                "explanation": "Using SELECT * retrieves all columns, which can increase I/O, memory usage, and network traffic, especially for tables with many columns or large data types."
            })
        
        # Check for missing WHERE clause in SELECT queries
        if re.search(r'select', sql_normalized) and not re.search(r'where', sql_normalized):
            if not (re.search(r'count\(\*\)', sql_normalized) and not re.search(r'group\s+by', sql_normalized)):
                suggestions.append({
                    "suggestion": "Missing WHERE clause",
                    "impact": "high",
                    "recommendation": "Add a WHERE clause to filter the results",
                    "explanation": "Queries without a WHERE clause can result in full table scans and return large result sets, causing performance issues."
                })
        
        # Check for potential Cartesian products (missing JOIN conditions)
        if re.search(r'join', sql_normalized) and not re.search(r'on', sql_normalized) and not re.search(r'using', sql_normalized):
            suggestions.append({
                "suggestion": "Potential Cartesian product",
                "impact": "high",
                "recommendation": "Add proper JOIN conditions using ON or USING clauses",
                "explanation": "Joins without conditions can result in Cartesian products, which multiply the number of rows and cause severe performance issues."
            })
        
        # Check for ORDER BY with large result sets
        if re.search(r'order\s+by', sql_normalized) and not re.search(r'limit', sql_normalized) and not re.search(r'top', sql_normalized):
            suggestions.append({
                "suggestion": "ORDER BY without LIMIT",
                "impact": "medium",
                "recommendation": "Add a LIMIT clause when using ORDER BY",
                "explanation": "Sorting large result sets without limiting the number of rows can consume significant memory and processing resources."
            })
        
        # Check for potential full table scans
        if re.search(r'where', sql_normalized):
            # Check for functions on indexed columns
            function_patterns = [r'(\w+)\s*\(', r'lower\s*\(', r'upper\s*\(', r'concat\s*\(']
            for pattern in function_patterns:
                if re.search(pattern, sql_normalized):
                    suggestions.append({
                        "suggestion": "Function applied to column in WHERE clause",
                        "impact": "medium",
                        "recommendation": "Avoid using functions on columns in WHERE clauses",
                        "explanation": "Applying functions to columns in WHERE clauses can prevent the use of indexes, resulting in full table scans."
                    })
                    break
        
        return suggestions
    
    def calculate_risk_score(self, sql_query: str) -> int:
        """Calculate risk score for SQL query"""
        score = 0
        
        # Normalize SQL query for analysis
        sql_normalized = sql_query.lower()
        
        # Data modification risk (0-30 points)
        if re.search(r'\bdrop\b', sql_normalized):
            score += 30
        elif re.search(r'\btruncate\b', sql_normalized):
            score += 25
        elif re.search(r'\bdelete\b', sql_normalized):
            score += 20
        elif re.search(r'\bupdate\b', sql_normalized):
            score += 15
        elif re.search(r'\binsert\b', sql_normalized):
            score += 10
        
        # Permission risk (0-20 points)
        if re.search(r'\bgrant\b', sql_normalized) or re.search(r'\brevoke\b', sql_normalized):
            score += 20
        
        # Injection risk (0-20 points)
        if "'" in sql_query or '"' in sql_query:
            score += 15
        if "--" in sql_query or "/*" in sql_query:
            score += 10
        
        # Performance risk (0-15 points)
        if re.search(r'select\s+\*', sql_normalized):
            score += 5
        if re.search(r'join', sql_normalized) and not re.search(r'on', sql_normalized) and not re.search(r'using', sql_normalized):
            score += 15
        if re.search(r'where', sql_normalized):
            function_patterns = [r'(\w+)\s*\(', r'lower\s*\(', r'upper\s*\(', r'concat\s*\(']
            for pattern in function_patterns:
                if re.search(pattern, sql_normalized):
                    score += 10
                    break
        
        # Data leakage risk (0-15 points)
        if re.search(r'select', sql_normalized) and not re.search(r'where', sql_normalized):
            score += 15
        
        # Ensure score is between 0-100
        return max(0, min(100, score))