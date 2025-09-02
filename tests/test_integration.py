# AI-Powered SDLC System - Integration Tests

import unittest
import os
import sys
import json

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import backend modules for testing
from backend.model_manager import ModelManager
from backend.api_connector import AIModelFactory, DeepSeekConnector, GeminiConnector, OpenAIConnector, GrokConnector, ClaudeConnector
from tests.test_config import config

class IntegrationTests(unittest.TestCase):
    """Integration tests for the AI-Powered SDLC System."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment before any tests run."""
        # Initialize the ModelManager with test keys
        cls.model_manager = ModelManager()
        for model, key in config.mock_api_keys.items():
            cls.model_manager.set_api_key(model, key)
        
        # Activate all models for testing
        for model in config.mock_api_keys.keys():
            cls.model_manager.activate_model(model)
    
    def test_model_factory_creates_correct_connectors(self):
        """Test that the AIModelFactory creates the correct connector types."""
        # Test each connector type
        model1 = AIModelFactory.create_connector("model1", "test-key")
        model2 = AIModelFactory.create_connector("model2", "test-key")
        model3 = AIModelFactory.create_connector("model3", "test-key")
        model4 = AIModelFactory.create_connector("model4", "test-key")
        model5 = AIModelFactory.create_connector("model5", "test-key")
        
        # Verify the correct types
        self.assertIsInstance(model1, DeepSeekConnector)
        self.assertIsInstance(model2, GeminiConnector)
        self.assertIsInstance(model3, OpenAIConnector)
        self.assertIsInstance(model4, GrokConnector)
        self.assertIsInstance(model5, ClaudeConnector)
    
    def test_model_manager_integration_with_connectors(self):
        """Test that the ModelManager correctly integrates with connectors."""
        # Set up a test model manager
        manager = ModelManager()
        
        # Add connectors
        for model, key in config.mock_api_keys.items():
            manager.set_api_key(model, key)
        
        # Verify connectors were added
        for model in config.mock_api_keys.keys():
            self.assertIn(model, manager.connectors)
        
        # Test activation
        for model in config.mock_api_keys.keys():
            result = manager.activate_model(model)
            self.assertTrue(result)
            self.assertEqual(manager.active_model, model)
    
    def test_code_generation_workflow(self):
        """Test the complete code generation workflow."""
        # Mock the API response
        mock_response = config.get_mock_response("code_generation")
        
        # Patch the connector's generate_code method to return the mock response
        original_generate_code = DeepSeekConnector.generate_code
        DeepSeekConnector.generate_code = lambda self, prompt, language: mock_response["response"]
        
        try:
            # Activate Model 1
            self.model_manager.activate_model("model1")
            
            # Generate code
            result = self.model_manager.generate_code(
                mock_response["prompt"], 
                "javascript"
            )
            
            # Verify the result
            self.assertEqual(result["code"], mock_response["response"]["code"])
            self.assertEqual(result["explanation"], mock_response["response"]["explanation"])
        finally:
            # Restore the original method
            DeepSeekConnector.generate_code = original_generate_code
    
    def test_documentation_generation_workflow(self):
        """Test the complete documentation generation workflow."""
        # Mock the API response
        mock_response = config.get_mock_response("documentation_generation")
        
        # Patch the connector's generate_documentation method to return the mock response
        original_generate_docs = GeminiConnector.generate_documentation
        GeminiConnector.generate_documentation = lambda self, code, language: mock_response["response"]
        
        try:
            # Activate Gemini model
            self.model_manager.activate_model("gemini")
            
            # Generate documentation
            result = self.model_manager.generate_documentation(
                mock_response["code"], 
                "javascript"
            )
            
            # Verify the result
            self.assertEqual(result, mock_response["response"])
        finally:
            # Restore the original method
            GeminiConnector.generate_documentation = original_generate_docs
    
    def test_test_generation_workflow(self):
        """Test the complete test generation workflow."""
        # Mock the API response
        mock_response = config.get_mock_response("test_generation")
        
        # Patch the connector's generate_tests method to return the mock response
        original_generate_tests = OpenAIConnector.generate_tests
        OpenAIConnector.generate_tests = lambda self, code, language: mock_response["response"]
        
        try:
            # Activate OpenAI model
            self.model_manager.activate_model("chatgpt")
            
            # Generate tests
            result = self.model_manager.generate_tests(
                mock_response["code"], 
                "javascript"
            )
            
            # Verify the result
            self.assertEqual(result, mock_response["response"])
        finally:
            # Restore the original method
            OpenAIConnector.generate_tests = original_generate_tests
    
    def test_bug_fixing_workflow(self):
        """Test the complete bug fixing workflow."""
        # Mock the API response
        mock_response = config.get_mock_response("bug_fixing")
        
        # Patch the connector's fix_bugs method to return the mock response
        original_fix_bugs = GrokConnector.fix_bugs
        GrokConnector.fix_bugs = lambda self, code, error_message, language: mock_response["response"]
        
        try:
            # Activate Grok model
            self.model_manager.activate_model("grok")
            
            # Fix bugs
            result = self.model_manager.fix_bugs(
                mock_response["code"],
                mock_response["error"],
                "javascript"
            )
            
            # Verify the result
            self.assertEqual(result["fixed_code"], mock_response["response"]["fixed_code"])
            self.assertEqual(result["explanation"], mock_response["response"]["explanation"])
        finally:
            # Restore the original method
            GrokConnector.fix_bugs = original_fix_bugs
    
    def test_code_optimization_workflow(self):
        """Test the complete code optimization workflow."""
        # Mock the API response
        mock_response = config.get_mock_response("code_optimization")
        
        # Patch the connector's optimize_code method to return the mock response
        original_optimize_code = ClaudeConnector.optimize_code
        ClaudeConnector.optimize_code = lambda self, code, optimization_target, language: mock_response["response"]
        
        try:
            # Activate Claude model
            self.model_manager.activate_model("claude")
            
            # Optimize code
            result = self.model_manager.optimize_code(
                mock_response["code"],
                "performance",
                "javascript"
            )
            
            # Verify the result
            self.assertEqual(result["optimized_code"], mock_response["response"]["optimized_code"])
            self.assertEqual(result["explanation"], mock_response["response"]["explanation"])
        finally:
            # Restore the original method
            ClaudeConnector.optimize_code = original_optimize_code
    
    def test_model_switching(self):
        """Test switching between different AI models."""
        # Test switching between models
        models = list(config.mock_api_keys.keys())
        
        for model in models:
            # Activate the model
            result = self.model_manager.activate_model(model)
            
            # Verify activation was successful
            self.assertTrue(result)
            self.assertEqual(self.model_manager.active_model, model)
    
    def test_api_key_persistence(self):
        """Test saving and loading API keys."""
        # Create a temporary file for testing
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        
        try:
            # Create a new model manager
            manager = ModelManager()
            
            # Set API keys
            for model, key in config.mock_api_keys.items():
                manager.set_api_key(model, key)
            
            # Save API keys to the temp file
            manager.save_api_keys(temp_file.name)
            
            # Create a new manager and load the keys
            new_manager = ModelManager()
            new_manager.load_api_keys(temp_file.name)
            
            # Verify the keys were loaded correctly
            for model, key in config.mock_api_keys.items():
                self.assertIn(model, new_manager.connectors)
        finally:
            # Clean up
            os.unlink(temp_file.name)

if __name__ == "__main__":
    unittest.main()