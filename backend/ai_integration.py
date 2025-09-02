# AI-Powered SDLC System - AI Integration Module

import os
import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_integration.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ai_integration")

# AI Model Configuration
AI_MODELS = {
    "model1": {
        "name": "Model 1",
        "api_key": None,
        "endpoint": "https://api.deepseek.com/v1",
        "models": {
            "code": "deepseek-coder",
            "chat": "deepseek-chat",
            "vision": "deepseek-vision"
        }
    },
    "model2": {
        "name": "Model 2",
        "api_key": None,
        "endpoint": "https://generativelanguage.googleapis.com/v1",
        "models": {
            "code": "gemini-pro-code",
            "chat": "gemini-pro",
            "vision": "gemini-pro-vision"
        }
    },
    "model3": {
        "name": "Model 3",
        "api_key": None,
        "endpoint": "https://api.openai.com/v1",
        "models": {
            "code": "gpt-5",
            "chat": "gpt-5",
            "vision": "gpt-5-vision"
        }
    },
    "model4": {
        "name": "Model 4",
        "api_key": None,
        "endpoint": "https://api.grok.com/v1",
        "models": {
            "code": "grok-2",
            "chat": "grok-2",
            "vision": "grok-2-vision"
        }
    },
    "model5": {
        "name": "Model 5",
        "api_key": None,
        "endpoint": "https://api.anthropic.com/v1",
        "models": {
            "code": "claude-3-opus",
            "chat": "claude-3-opus",
            "vision": "claude-3-opus"
        }
    }
}

class AIIntegration:
    """Main class for AI model integration in the SDLC system."""
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """Initialize the AI integration module.
        
        Args:
            api_keys: Dictionary mapping model names to API keys
        """
        self.models = AI_MODELS.copy()
        
        # Set API keys if provided
        if api_keys:
            for model_name, api_key in api_keys.items():
                if model_name in self.models:
                    self.models[model_name]["api_key"] = api_key
        
        logger.info("AI Integration module initialized")
    
    def set_api_key(self, model_name: str, api_key: str) -> bool:
        """Set the API key for a specific model.
        
        Args:
            model_name: Name of the AI model
            api_key: API key for the model
            
        Returns:
            bool: True if successful, False otherwise
        """
        if model_name not in self.models:
            logger.error(f"Unknown model: {model_name}")
            return False
        
        self.models[model_name]["api_key"] = api_key
        logger.info(f"API key set for {model_name}")
        return True
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get a list of available AI models with API keys.
        
        Returns:
            List of dictionaries containing model information
        """
        available_models = []
        
        for model_id, model_info in self.models.items():
            if model_info["api_key"]:
                available_models.append({
                    "id": model_id,
                    "name": model_info["name"],
                    "capabilities": list(model_info["models"].keys())
                })
        
        return available_models
    
    def generate_code(self, 
                     model_name: str, 
                     requirements: str, 
                     language: str, 
                     framework: Optional[str] = None,
                     include_tests: bool = False,
                     include_docs: bool = False,
                     optimize: bool = False) -> Dict[str, Any]:
        """Generate code using the specified AI model.
        
        Args:
            model_name: Name of the AI model to use
            requirements: Description of the code requirements
            language: Programming language to use
            framework: Framework to use (optional)
            include_tests: Whether to include tests
            include_docs: Whether to include documentation
            optimize: Whether to optimize the code
            
        Returns:
            Dictionary containing the generated code and explanation
        """
        if model_name not in self.models:
            return {"error": f"Unknown model: {model_name}"}
        
        model_info = self.models[model_name]
        
        if not model_info["api_key"]:
            return {"error": f"No API key provided for {model_info['name']}"}
        
        # Construct the prompt
        framework_text = f" using the {framework} framework" if framework and framework != "none" else ""
        test_text = "\nInclude comprehensive tests for the code." if include_tests else ""
        doc_text = "\nInclude detailed documentation and comments." if include_docs else ""
        optimize_text = "\nOptimize the code for performance and efficiency." if optimize else ""
        
        prompt = f"Generate {language} code{framework_text} that meets these requirements:\n{requirements}{test_text}{doc_text}{optimize_text}"
        
        try:
            # Call the appropriate API based on the model
            if model_name == "model1":
                return self._call_model1_api(prompt, "code")
            elif model_name == "model2":
                return self._call_model2_api(prompt, "code")
            elif model_name == "model3":
                return self._call_model3_api(prompt, "code")
            elif model_name == "model4":
                return self._call_model4_api(prompt, "code")
            elif model_name == "model5":
                return self._call_model5_api(prompt, "code")
            else:
                return {"error": f"API integration not implemented for {model_name}"}
        
        except Exception as e:
            logger.error(f"Error generating code with {model_name}: {str(e)}")
            return {"error": f"Failed to generate code: {str(e)}"}
    
    def generate_documentation(self, 
                             model_name: str, 
                             code: str,
                             language: str,
                             doc_format: str = "markdown") -> Dict[str, Any]:
        """Generate documentation for the provided code.
        
        Args:
            model_name: Name of the AI model to use
            code: Code to document
            language: Programming language of the code
            doc_format: Format of the documentation (markdown, html, etc.)
            
        Returns:
            Dictionary containing the generated documentation
        """
        if model_name not in self.models:
            return {"error": f"Unknown model: {model_name}"}
        
        model_info = self.models[model_name]
        
        if not model_info["api_key"]:
            return {"error": f"No API key provided for {model_info['name']}"}
        
        # Construct the prompt
        prompt = f"Generate comprehensive documentation in {doc_format} format for the following {language} code:\n```{language}\n{code}\n```\n\nInclude:\n1. Overview of what the code does\n2. Explanation of key functions and classes\n3. Usage examples\n4. Parameters and return values\n5. Any dependencies or requirements"
        
        try:
            # Call the appropriate API based on the model
            if model_name == "model1":
                return self._call_model1_api(prompt, "chat")
            elif model_name == "model2":
                return self._call_model2_api(prompt, "chat")
            elif model_name == "model3":
                return self._call_model3_api(prompt, "chat")
            elif model_name == "model4":
                return self._call_model4_api(prompt, "chat")
            elif model_name == "model5":
                return self._call_model5_api(prompt, "chat")
            else:
                return {"error": f"API integration not implemented for {model_name}"}
        
        except Exception as e:
            logger.error(f"Error generating documentation with {model_name}: {str(e)}")
            return {"error": f"Failed to generate documentation: {str(e)}"}
    
    def generate_tests(self, 
                      model_name: str, 
                      code: str,
                      language: str,
                      test_framework: Optional[str] = None) -> Dict[str, Any]:
        """Generate test cases for the provided code.
        
        Args:
            model_name: Name of the AI model to use
            code: Code to test
            language: Programming language of the code
            test_framework: Testing framework to use (optional)
            
        Returns:
            Dictionary containing the generated tests
        """
        if model_name not in self.models:
            return {"error": f"Unknown model: {model_name}"}
        
        model_info = self.models[model_name]
        
        if not model_info["api_key"]:
            return {"error": f"No API key provided for {model_info['name']}"}
        
        # Construct the prompt
        framework_text = f" using the {test_framework} testing framework" if test_framework and test_framework != "none" else ""
        prompt = f"Generate comprehensive test cases{framework_text} for the following {language} code:\n```{language}\n{code}\n```\n\nInclude:\n1. Unit tests for all functions and methods\n2. Edge case testing\n3. Integration tests if applicable\n4. Test setup and teardown code"
        
        try:
            # Call the appropriate API based on the model
            if model_name == "model1":
                return self._call_model1_api(prompt, "code")
            elif model_name == "model2":
                return self._call_model2_api(prompt, "code")
            elif model_name == "model3":
                return self._call_model3_api(prompt, "code")
            elif model_name == "model4":
                return self._call_model4_api(prompt, "code")
            elif model_name == "model5":
                return self._call_model5_api(prompt, "code")
            else:
                return {"error": f"API integration not implemented for {model_name}"}
        
        except Exception as e:
            logger.error(f"Error generating tests with {model_name}: {str(e)}")
            return {"error": f"Failed to generate tests: {str(e)}"}
    
    def fix_bugs(self, 
                model_name: str, 
                code: str,
                error_message: str,
                language: str) -> Dict[str, Any]:
        """Fix bugs in the provided code based on error messages.
        
        Args:
            model_name: Name of the AI model to use
            code: Code with bugs
            error_message: Error message or description of the bug
            language: Programming language of the code
            
        Returns:
            Dictionary containing the fixed code and explanation
        """
        if model_name not in self.models:
            return {"error": f"Unknown model: {model_name}"}
        
        model_info = self.models[model_name]
        
        if not model_info["api_key"]:
            return {"error": f"No API key provided for {model_info['name']}"}
        
        # Construct the prompt
        prompt = f"Fix the bugs in the following {language} code based on the error message:\n\nError: {error_message}\n\nCode:\n```{language}\n{code}\n```\n\nProvide:\n1. The fixed code\n2. An explanation of what was wrong\n3. How the fix resolves the issue"
        
        try:
            # Call the appropriate API based on the model
            if model_name == "model1":
                return self._call_model1_api(prompt, "code")
            elif model_name == "model2":
                return self._call_model2_api(prompt, "code")
            elif model_name == "model3":
                return self._call_model3_api(prompt, "code")
            elif model_name == "model4":
                return self._call_model4_api(prompt, "code")
            elif model_name == "model5":
                return self._call_model5_api(prompt, "code")
            else:
                return {"error": f"API integration not implemented for {model_name}"}
        
        except Exception as e:
            logger.error(f"Error fixing bugs with {model_name}: {str(e)}")
            return {"error": f"Failed to fix bugs: {str(e)}"}
    
    def optimize_code(self, 
                     model_name: str, 
                     code: str,
                     language: str,
                     optimization_target: str = "performance") -> Dict[str, Any]:
        """Optimize the provided code for performance, readability, or memory usage.
        
        Args:
            model_name: Name of the AI model to use
            code: Code to optimize
            language: Programming language of the code
            optimization_target: Target of optimization (performance, readability, memory)
            
        Returns:
            Dictionary containing the optimized code and explanation
        """
        if model_name not in self.models:
            return {"error": f"Unknown model: {model_name}"}
        
        model_info = self.models[model_name]
        
        if not model_info["api_key"]:
            return {"error": f"No API key provided for {model_info['name']}"}
        
        # Construct the prompt
        prompt = f"Optimize the following {language} code for {optimization_target}:\n```{language}\n{code}\n```\n\nProvide:\n1. The optimized code\n2. An explanation of the optimizations made\n3. The expected improvements in {optimization_target}"
        
        try:
            # Call the appropriate API based on the model
            if model_name == "deepseek":
                return self._call_deepseek_api(prompt, "code")
            elif model_name == "gemini":
                return self._call_gemini_api(prompt, "code")
            elif model_name == "chatgpt":
                return self._call_openai_api(prompt, "code")
            elif model_name == "grok":
                return self._call_grok_api(prompt, "code")
            elif model_name == "claude":
                return self._call_anthropic_api(prompt, "code")
            else:
                return {"error": f"API integration not implemented for {model_name}"}
        
        except Exception as e:
            logger.error(f"Error optimizing code with {model_name}: {str(e)}")
            return {"error": f"Failed to optimize code: {str(e)}"}
    
    # === API Integration Methods ===
    
    def _call_model1_api(self, prompt: str, mode: str) -> Dict[str, Any]:
        """
Call the Model 1 API.
        
        Args:
            prompt: The prompt to send to the API
            mode: The mode of operation (code, chat, vision)
            
        Returns:
            Dictionary containing the API response
        """
        model_info = self.models["model1"]
        model = model_info["models"][mode]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {model_info['api_key']}"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3 if mode == "code" else 0.7
        }
        
        # In a real implementation, this would make an actual API call
        # For this demo, we'll simulate a response
        
        # Simulate API call delay
        time.sleep(1)
        
        # Sample response
        if mode == "code":
            return {
                "code": f"// Generated code using DeepSeek\n\nfunction example() {{\n  console.log('Hello, world!');\n  // Implementation based on requirements\n}}\n\nexample();",
                "explanation": "This code implements a basic solution based on your requirements."
            }
        else:
            return {
                "content": "This is a sample response from the DeepSeek API."
            }
    
    def _call_model2_api(self, prompt: str, mode: str) -> Dict[str, Any]:
        """
Call the Model 2 API.
        
        Args:
            prompt: The prompt to send to the API
            mode: The mode of operation (code, chat, vision)
            
        Returns:
            Dictionary containing the API response
        """
        model_info = self.models["model2"]
        model = model_info["models"][mode]
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": model_info["api_key"]
        }
        
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.3 if mode == "code" else 0.7
            }
        }
        
        # In a real implementation, this would make an actual API call
        # For this demo, we'll simulate a response
        
        # Simulate API call delay
        time.sleep(1)
        
        # Sample response
        if mode == "code":
            return {
                "code": f"// Generated code using Gemini\n\nfunction example() {{\n  console.log('Hello, world!');\n  // Implementation based on requirements\n}}\n\nexample();",
                "explanation": "This code implements a basic solution based on your requirements."
            }
        else:
            return {
                "content": "This is a sample response from the Gemini API."
            }
    
    def _call_model3_api(self, prompt: str, mode: str) -> Dict[str, Any]:
        """
Call the Model 3 API.
        
        Args:
            prompt: The prompt to send to the API
            mode: The mode of operation (code, chat, vision)
            
        Returns:
            Dictionary containing the API response
        """
        model_info = self.models["model3"]
        model = model_info["models"][mode]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {model_info['api_key']}"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3 if mode == "code" else 0.7
        }
        
        # In a real implementation, this would make an actual API call
        # For this demo, we'll simulate a response
        
        # Simulate API call delay
        time.sleep(1)
        
        # Sample response
        if mode == "code":
            return {
                "code": f"// Generated code using ChatGPT-5\n\nfunction example() {{\n  console.log('Hello, world!');\n  // Implementation based on requirements\n}}\n\nexample();",
                "explanation": "This code implements a basic solution based on your requirements."
            }
        else:
            return {
                "content": "This is a sample response from the OpenAI API."
            }
    
    def _call_model4_api(self, prompt: str, mode: str) -> Dict[str, Any]:
        """
Call the Model 4 API.
        
        Args:
            prompt: The prompt to send to the API
            mode: The mode of operation (code, chat, vision)
            
        Returns:
            Dictionary containing the API response
        """
        model_info = self.models["model4"]
        model = model_info["models"][mode]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {model_info['api_key']}"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3 if mode == "code" else 0.7
        }
        
        # In a real implementation, this would make an actual API call
        # For this demo, we'll simulate a response
        
        # Simulate API call delay
        time.sleep(1)
        
        # Sample response
        if mode == "code":
            return {
                "code": f"// Generated code using Grok\n\nfunction example() {{\n  console.log('Hello, world!');\n  // Implementation based on requirements\n}}\n\nexample();",
                "explanation": "This code implements a basic solution based on your requirements."
            }
        else:
            return {
                "content": "This is a sample response from the Grok API."
            }
    
    def _call_model5_api(self, prompt: str, mode: str) -> Dict[str, Any]:
        """
Call the Model 5 API.
        
        Args:
            prompt: The prompt to send to the API
            mode: The mode of operation (code, chat, vision)
            
        Returns:
            Dictionary containing the API response
        """
        model_info = self.models["model5"]
        model = model_info["models"][mode]
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": model_info["api_key"],
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3 if mode == "code" else 0.7
        }
        
        # In a real implementation, this would make an actual API call
        # For this demo, we'll simulate a response
        
        # Simulate API call delay
        time.sleep(1)
        
        # Sample response
        if mode == "code":
            return {
                "code": f"// Generated code using Claude\n\nfunction example() {{\n  console.log('Hello, world!');\n  // Implementation based on requirements\n}}\n\nexample();",
                "explanation": "This code implements a basic solution based on your requirements."
            }
        else:
            return {
                "content": "This is a sample response from the Anthropic API."
            }

# Example usage
if __name__ == "__main__":
    # Initialize the AI integration module
    ai = AIIntegration()
    
    # Set API keys (in a real application, these would be loaded from environment variables or a secure storage)
    ai.set_api_key("model1", "your_model1_api_key")
    ai.set_api_key("model2", "your_model2_api_key")
    ai.set_api_key("model3", "your_model3_api_key")
    ai.set_api_key("model4", "your_model4_api_key")
    ai.set_api_key("model5", "your_model5_api_key")
    
    # Generate code
    result = ai.generate_code(
        model_name="model1",
        requirements="Create a simple web server that serves static files",
        language="javascript",
        framework="express",
        include_tests=True
    )
    
    print("Generated Code:")
    print(result["code"])
    print("\nExplanation:")
    print(result["explanation"])