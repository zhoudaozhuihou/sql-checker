from abc import ABC, abstractmethod
from typing import Dict, Any, List


class SQLAnalyzerModel(ABC):
    """
    Abstract base class for SQL analyzer models.
    All SQL analyzer models should inherit from this class and implement the analyze method.
    """
    
    @abstractmethod
    def analyze(self, sql_query: str) -> Dict[str, Any]:
        """
        Analyze a SQL query and return the analysis result.
        
        Args:
            sql_query: The SQL query to analyze
            
        Returns:
            A dictionary containing the analysis result with the following keys:
            - safety_issues: List of safety issues found in the query
            - performance_suggestions: List of performance optimization suggestions
            - risk_score: A score indicating the risk level of the query (0-100)
            - risk_level: A string indicating the risk level (low, medium, high)
            - details: Additional details about the analysis
        """
        pass
    
    @abstractmethod
    def get_safety_issues(self, sql_query: str) -> List[Dict[str, Any]]:
        """
        Get a list of safety issues found in the SQL query.
        
        Args:
            sql_query: The SQL query to analyze
            
        Returns:
            A list of dictionaries containing safety issues with the following keys:
            - issue: The safety issue description
            - severity: The severity of the issue (low, medium, high)
            - recommendation: A recommendation to fix the issue
        """
        pass
    
    @abstractmethod
    def get_performance_suggestions(self, sql_query: str) -> List[Dict[str, Any]]:
        """
        Get a list of performance optimization suggestions for the SQL query.
        
        Args:
            sql_query: The SQL query to analyze
            
        Returns:
            A list of dictionaries containing performance suggestions with the following keys:
            - suggestion: The performance suggestion description
            - impact: The impact of the suggestion (low, medium, high)
            - recommendation: A recommendation to implement the suggestion
        """
        pass
    
    @abstractmethod
    def calculate_risk_score(self, sql_query: str) -> int:
        """
        Calculate a risk score for the SQL query.
        
        Args:
            sql_query: The SQL query to analyze
            
        Returns:
            An integer between 0 and 100 indicating the risk level of the query
        """
        pass
    
    @staticmethod
    def get_risk_level(risk_score: int) -> str:
        """
        Get a risk level string based on the risk score.
        
        Args:
            risk_score: The risk score (0-100)
            
        Returns:
            A string indicating the risk level (low, medium, high)
        """
        if risk_score < 30:
            return "low"
        elif risk_score < 70:
            return "medium"
        else:
            return "high"