import unittest
from models.simple_model import SimpleModel
from models.advanced_model import AdvancedModel
from models.ollama_model import OllamaModel
from models.copilot_model import CopilotModel
from utils.logger import logger
import os

class TestSQLAnalyzerModels(unittest.TestCase):
    def setUp(self):
        logger.info("开始设置测试环境")
        self.simple_model = SimpleModel()
        self.advanced_model = AdvancedModel()
        
        # Ollama和Copilot模型需要特定环境配置才能测试
        self.test_ollama = os.getenv('TEST_OLLAMA', 'false').lower() == 'true'
        self.test_copilot = os.getenv('TEST_COPILOT', 'false').lower() == 'true'
        
        if self.test_ollama:
            logger.info("初始化Ollama模型")
            self.ollama_model = OllamaModel()
        if self.test_copilot:
            logger.info("初始化Copilot模型")
            self.copilot_model = CopilotModel()
        logger.info("测试环境设置完成")
    
    def test_safe_query(self):
        """测试安全的SQL查询"""
        logger.info("=== 开始测试安全SQL查询 ===")
        sql = "SELECT id, name FROM users WHERE age >= 18"
        logger.info(f"测试SQL: {sql}")
        
        # 测试简单模型
        logger.info("测试简单模型...")
        result = self.simple_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertEqual(len(result['safety_issues']), 0)
        self.assertTrue(result['risk_score'] < 30)
        self.assertEqual(result['risk_level'], 'low')
        logger.info("简单模型测试通过！")
        
        # 测试高级模型
        logger.info("测试高级模型...")
        result = self.advanced_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertEqual(len(result['safety_issues']), 0)
        self.assertTrue(result['risk_score'] < 30)
        self.assertEqual(result['risk_level'], 'low')
        logger.info("高级模型测试通过！")
        logger.info("=== 安全SQL查询测试完成 ===\n")
    
    def test_dangerous_query(self):
        """测试危险的SQL查询"""
        logger.info("=== 开始测试危险SQL查询 ===")
        sql = "DROP TABLE users"
        logger.info(f"测试SQL: {sql}")
        
        # 测试简单模型
        logger.info("测试简单模型...")
        result = self.simple_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(len(result['safety_issues']) > 0)
        self.assertTrue(result['risk_score'] >= 70)
        self.assertEqual(result['risk_level'], 'high')
        logger.info("简单模型测试通过！")
        
        # 测试高级模型
        logger.info("测试高级模型...")
        result = self.advanced_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(len(result['safety_issues']) > 0)
        self.assertTrue(result['risk_score'] >= 70)
        self.assertEqual(result['risk_level'], 'high')
        logger.info("高级模型测试通过！")
        logger.info("=== 危险SQL查询测试完成 ===\n")
    
    def test_sql_injection(self):
        """测试SQL注入风险"""
        logger.info("=== 开始测试SQL注入风险 ===")
        sql = "SELECT * FROM users WHERE username = 'admin' OR '1'='1'"
        logger.info(f"测试SQL: {sql}")
        
        # 测试简单模型
        logger.info("测试简单模型...")
        result = self.simple_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(any(issue['issue'].find('SQL注入') != -1 for issue in result['safety_issues']))
        logger.info("简单模型测试通过！")
        
        # 测试高级模型
        logger.info("测试高级模型...")
        result = self.advanced_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(any(issue['issue'].find('SQL注入') != -1 for issue in result['safety_issues']))
        logger.info("高级模型测试通过！")
        logger.info("=== SQL注入风险测试完成 ===\n")
    
    def test_performance_issues(self):
        """测试性能问题检测"""
        logger.info("=== 开始测试性能问题检测 ===")
        sql = "SELECT * FROM users"
        logger.info(f"测试SQL: {sql}")
        
        # 测试简单模型
        logger.info("测试简单模型...")
        result = self.simple_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(any(sugg['suggestion'].find('SELECT *') != -1 
                          for sugg in result['performance_suggestions']))
        logger.info("简单模型测试通过！")
        
        # 测试高级模型
        logger.info("测试高级模型...")
        result = self.advanced_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(any(sugg['suggestion'].find('SELECT *') != -1 
                          for sugg in result['performance_suggestions']))
        logger.info("高级模型测试通过！")
        logger.info("=== 性能问题检测测试完成 ===\n")
    
    def test_missing_where_clause(self):
        """测试缺少WHERE子句的情况"""
        logger.info("=== 开始测试缺少WHERE子句 ===")
        sql = "DELETE FROM users"
        logger.info(f"测试SQL: {sql}")
        
        # 测试简单模型
        logger.info("测试简单模型...")
        result = self.simple_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(any(sugg['suggestion'].find('WHERE') != -1 
                          for sugg in result['performance_suggestions']))
        logger.info("简单模型测试通过！")
        
        # 测试高级模型
        logger.info("测试高级模型...")
        result = self.advanced_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        self.assertTrue(any(sugg['suggestion'].find('WHERE') != -1 
                          for sugg in result['performance_suggestions']))
        logger.info("高级模型测试通过！")
        logger.info("=== 缺少WHERE子句测试完成 ===\n")
    
    def test_ollama_model(self):
        """测试Ollama模型（如果启用）"""
        if not self.test_ollama:
            logger.info("=== 跳过Ollama模型测试（未启用）===\n")
            self.skipTest('Ollama测试未启用')
        
        logger.info("=== 开始测试Ollama模型 ===")
        sql = "SELECT * FROM users WHERE username = 'admin'"
        logger.info(f"测试SQL: {sql}")
        result = self.ollama_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        
        self.assertIsInstance(result['safety_issues'], list)
        self.assertIsInstance(result['performance_suggestions'], list)
        self.assertIsInstance(result['risk_score'], int)
        self.assertIn(result['risk_level'], ['low', 'medium', 'high'])
        logger.info("Ollama模型测试通过！")
        logger.info("=== Ollama模型测试完成 ===\n")
    
    def test_copilot_model(self):
        """测试Copilot模型（如果启用）"""
        if not self.test_copilot:
            logger.info("=== 跳过Copilot模型测试（未启用）===\n")
            self.skipTest('Copilot测试未启用')
        
        logger.info("=== 开始测试Copilot模型 ===")
        sql = "SELECT * FROM users WHERE username = 'admin'"
        logger.info(f"测试SQL: {sql}")
        result = self.copilot_model.analyze(sql)
        logger.info(f"安全问题: {result['safety_issues']}")
        logger.info(f"性能建议: {result['performance_suggestions']}")
        logger.info(f"风险评分: {result['risk_score']}")
        logger.info(f"风险等级: {result['risk_level']}")
        
        self.assertIsInstance(result['safety_issues'], list)
        self.assertIsInstance(result['performance_suggestions'], list)
        self.assertIsInstance(result['risk_score'], int)
        self.assertIn(result['risk_level'], ['low', 'medium', 'high'])
        logger.info("Copilot模型测试通过！")
        logger.info("=== Copilot模型测试完成 ===\n")
    
    def test_copilot_connection(self):
        """测试Copilot模型的连接功能"""
        if not self.test_copilot:
            self.skipTest('Copilot测试未启用')
        
        # 测试模型初始化
        model = CopilotModel()
        self.assertEqual(model.language, 'sql')
        self.assertTrue(model.api_url.startswith('http'))
        
        # 测试API调用
        sql = "SELECT * FROM users LIMIT 1"
        try:
            result = model._query_copilot(f"分析以下SQL查询：{sql}")
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)
        except Exception as e:
            self.fail(f"Copilot API调用失败: {str(e)}")

if __name__ == '__main__':
    unittest.main()