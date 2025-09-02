# AI-Powered SDLC System - Core Functionality Tests

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import backend modules
from backend.model_manager import ModelManager
from backend.api_connector import APIConnector, DeepSeekConnector, GeminiConnector, OpenAIConnector, GrokConnector, ClaudeConnector

class TestModelManager(unittest.TestCase):
    """Test cases for the ModelManager class"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.model_manager = ModelManager()
        # Mock API keys for testing
        self.test_api_keys = {
            "deepseek": "test_deepseek_key",
            "gemini": "test_gemini_key",
            "chatgpt": "test_chatgpt_key",
            "grok": "test_grok_key",
            "claude": "test_claude_key"
        }
    
    def test_set_api_key(self):
        """Test setting API keys"""
        for model, key in self.test_api_keys.items():
            self.model_manager.set_api_key(model, key)
            self.assertEqual(self.model_manager.get_api_key(model), key)
    
    def test_activate_model(self):
        """Test activating models"""
        # Set API keys first
        for model, key in self.test_api_keys.items():
            self.model_manager.set_api_key(model, key)
        
        # Activate models
        for model in self.test_api_keys.keys():
            result = self.model_manager.activate_model(model)
            self.assertTrue(result)
            self.assertIn(model, self.model_manager.get_active_models())
    
    def test_deactivate_model(self):
        """Test deactivating models"""
        # Set API keys and activate models first
        for model, key in self.test_api_keys.items():
            self.model_manager.set_api_key(model, key)
            self.model_manager.activate_model(model)
        
        # Deactivate models
        for model in self.test_api_keys.keys():
            result = self.model_manager.deactivate_model(model)
            self.assertTrue(result)
            self.assertNotIn(model, self.model_manager.get_active_models())
    
    @patch('backend.model_manager.ModelManager.save_api_keys')
    def test_save_api_keys(self, mock_save):
        """Test saving API keys"""
        mock_save.return_value = True
        
        # Set API keys
        for model, key in self.test_api_keys.items():
            self.model_manager.set_api_key(model, key)
        
        # Save API keys
        result = self.model_manager.save_api_keys()
        self.assertTrue(result)
        mock_save.assert_called_once()
    
    @patch('backend.model_manager.ModelManager.load_api_keys')
    def test_load_api_keys(self, mock_load):
        """Test loading API keys"""
        mock_load.return_value = True
        
        # Load API keys
        result = self.model_manager.load_api_keys()
        self.assertTrue(result)
        mock_load.assert_called_once()


class TestAPIConnector(unittest.TestCase):
    """Test cases for the APIConnector class and its subclasses"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.api_key = "test_api_key"
        self.base_connector = APIConnector(self.api_key)
        self.deepseek_connector = DeepSeekConnector(self.api_key)
        self.gemini_connector = GeminiConnector(self.api_key)
        self.openai_connector = OpenAIConnector(self.api_key)
        self.grok_connector = GrokConnector(self.api_key)
        self.claude_connector = ClaudeConnector(self.api_key)
    
    def test_set_api_key(self):
        """Test setting API key"""
        new_key = "new_test_key"
        self.base_connector.set_api_key(new_key)
        self.assertEqual(self.base_connector.api_key, new_key)
    
    def test_connector_initialization(self):
        """Test connector initialization"""
        self.assertEqual(self.deepseek_connector.api_key, self.api_key)
        self.assertEqual(self.gemini_connector.api_key, self.api_key)
        self.assertEqual(self.openai_connector.api_key, self.api_key)
        self.assertEqual(self.grok_connector.api_key, self.api_key)
        self.assertEqual(self.claude_connector.api_key, self.api_key)
    
    def test_base_url_configuration(self):
        """Test base URL configuration"""
        self.assertIsNotNone(self.deepseek_connector.base_url)
        self.assertIsNotNone(self.gemini_connector.base_url)
        self.assertIsNotNone(self.openai_connector.base_url)
        self.assertIsNotNone(self.grok_connector.base_url)
        self.assertIsNotNone(self.claude_connector.base_url)
    
    def test_is_available(self):
        """Test is_available method"""
        # Base connector should not be available (abstract class)
        with self.assertRaises(NotImplementedError):
            self.base_connector.generate_code("test", "python")
        
        # Concrete connectors should have implemented methods
        with patch.object(DeepSeekConnector, 'generate_code', return_value=("code", "explanation")):
            code, explanation = self.deepseek_connector.generate_code("test", "python")
            self.assertEqual(code, "code")
            self.assertEqual(explanation, "explanation")


class TestAIIntegration(unittest.TestCase):
    """Test cases for AI integration functionality"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.model_manager = ModelManager()
        # Mock API keys for testing
        self.test_api_keys = {
            "deepseek": "test_deepseek_key",
            "gemini": "test_gemini_key",
            "chatgpt": "test_chatgpt_key",
            "grok": "test_grok_key",
            "claude": "test_claude_key"
        }
        
        # Set API keys and activate models
        for model, key in self.test_api_keys.items():
            self.model_manager.set_api_key(model, key)
            self.model_manager.activate_model(model)
    
    @patch('backend.api_connector.DeepSeekConnector.generate_code')
    def test_generate_code(self, mock_generate):
        """Test code generation"""
        mock_generate.return_value = ("def hello_world():\n    print('Hello, World!')", "A simple hello world function")
        
        # Test code generation
        code, explanation = self.model_manager.generate_code("Create a hello world function", "python")
        self.assertIn("def hello_world", code)
        self.assertIn("Hello, World", code)
        self.assertIn("hello world", explanation.lower())
    
    @patch('backend.api_connector.GeminiConnector.generate_documentation')
    def test_generate_documentation(self, mock_generate):
        """Test documentation generation"""
        mock_generate.return_value = "# Hello World Function\n\nA simple function that prints 'Hello, World!'\n"
        
        # Test documentation generation
        code = "def hello_world():\n    print('Hello, World!')"
        docs = self.model_manager.generate_documentation(code, "python")
        self.assertIn("Hello World Function", docs)
        self.assertIn("simple function", docs)
    
    @patch('backend.api_connector.OpenAIConnector.generate_tests')
    def test_generate_tests(self, mock_generate):
        """Test test case generation"""
        mock_generate.return_value = "def test_hello_world(capsys):\n    hello_world()\n    captured = capsys.readouterr()\n    assert 'Hello, World!' in captured.out"
        
        # Test test case generation
        code = "def hello_world():\n    print('Hello, World!')"
        tests = self.model_manager.generate_tests(code, "python")
        self.assertIn("test_hello_world", tests)
        self.assertIn("assert", tests)
    
    @patch('backend.api_connector.GrokConnector.fix_bugs')
    def test_fix_bugs(self, mock_fix):
        """Test bug fixing"""
        mock_fix.return_value = ("def divide(a, b):\n    if b == 0:\n        return 'Cannot divide by zero'\n    return a / b", "Added check for division by zero")
        
        # Test bug fixing
        buggy_code = "def divide(a, b):\n    return a / b"
        error_message = "ZeroDivisionError: division by zero"
        fixed_code, explanation = self.model_manager.fix_bugs(buggy_code, error_message, "python")
        self.assertIn("if b == 0", fixed_code)
        self.assertIn("Cannot divide by zero", fixed_code)
        self.assertIn("division by zero", explanation.lower())
    
    @patch('backend.api_connector.ClaudeConnector.optimize_code')
    def test_optimize_code(self, mock_optimize):
        """Test code optimization"""
        mock_optimize.return_value = ("def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)", "Simplified the factorial function using recursion")
        
        # Test code optimization
        code = "def factorial(n):\n    result = 1\n    for i in range(1, n+1):\n        result *= i\n    return result"
        optimized_code, explanation = self.model_manager.optimize_code(code, "python")
        self.assertIn("if n <= 1", optimized_code)
        self.assertIn("return n * factorial", optimized_code)
        self.assertIn("recursion", explanation.lower())


if __name__ == '__main__':
    unittest.main()