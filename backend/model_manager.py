# AI-Powered SDLC System - Model Manager Module

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from api_connector import AIModelFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("model_manager.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("model_manager")

class ModelManager:
    """Manager class for handling multiple AI models."""
    
    def __init__(self):
        """Initialize the model manager."""
        self.api_keys = {}
        self.connectors = {}
        self.active_model = None
        logger.info("Initialized Model Manager")
    
    def set_api_key(self, model_name: str, api_key: str) -> bool:
        """Set the API key for a model.
        
        Args:
            model_name: Name of the AI model
            api_key: API key for the model
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.api_keys[model_name] = api_key
            
            # Create a connector for the model
            if api_key:
                self.connectors[model_name] = AIModelFactory.create_connector(model_name, api_key)
                logger.info(f"Set API key for {model_name}")
                
                # Set as active model if no active model is set
                if self.active_model is None:
                    self.active_model = model_name
                    logger.info(f"Set {model_name} as active model")
                
                return True
            else:
                # Remove the connector if the API key is empty
                if model_name in self.connectors:
                    del self.connectors[model_name]
                    logger.info(f"Removed connector for {model_name} due to empty API key")
                
                # Update active model if necessary
                if self.active_model == model_name:
                    self.active_model = next(iter(self.connectors)) if self.connectors else None
                    logger.info(f"Updated active model to {self.active_model}")
                
                return True
        
        except Exception as e:
            logger.error(f"Error setting API key for {model_name}: {str(e)}")
            return False
    
    def set_active_model(self, model_name: str) -> bool:
        """Set the active model.
        
        Args:
            model_name: Name of the AI model
            
        Returns:
            True if successful, False otherwise
        """
        if model_name in self.connectors:
            self.active_model = model_name
            logger.info(f"Set {model_name} as active model")
            return True
        else:
            logger.error(f"Cannot set {model_name} as active model: No connector available")
            return False
    
    def get_active_model(self) -> Optional[str]:
        """Get the active model.
        
        Returns:
            Name of the active model, or None if no active model is set
        """
        return self.active_model
    
    def get_available_models(self) -> List[str]:
        """Get the list of available models.
        
        Returns:
            List of available model names
        """
        return list(self.connectors.keys())
    
    def generate_code(self, prompt: str, model_name: Optional[str] = None, temperature: float = 0.3) -> Dict[str, Any]:
        """Generate code using the specified model or the active model.
        
        Args:
            prompt: The prompt for code generation
            model_name: Name of the AI model to use (optional)
            temperature: Temperature for generation
            
        Returns:
            Generated code and explanation
        """
        # Use the specified model or the active model
        model_to_use = model_name if model_name else self.active_model
        
        if not model_to_use:
            logger.error("No active model set")
            return {"error": "No active model set"}
        
        if model_to_use not in self.connectors:
            logger.error(f"Model {model_to_use} not available")
            return {"error": f"Model {model_to_use} not available"}
        
        try:
            # Generate code using the model
            connector = self.connectors[model_to_use]
            result = connector.generate_code(prompt, temperature=temperature)
            
            # Add model information to the result
            result["model"] = model_to_use
            
            # Ensure code and explanation are in the result
            if "code" not in result:
                result["code"] = "// No code generated"
            if "explanation" not in result:
                result["explanation"] = "No explanation provided"
                
            return result
        
        except Exception as e:
            logger.error(f"Error generating code with {model_to_use}: {str(e)}")
            return {"error": f"Failed to generate code: {str(e)}"}
    
    def generate_documentation(self, code: str, model_name: Optional[str] = None, temperature: float = 0.3) -> Dict[str, Any]:
        """Generate documentation for the given code.
        
        Args:
            code: The code to document
            model_name: Name of the AI model to use (optional)
            temperature: Temperature for generation
            
        Returns:
            Generated documentation
        """
        prompt = f"Generate comprehensive documentation for the following code:\n\n```\n{code}\n```\n\nPlease include:\n1. Overview of what the code does\n2. Function/class descriptions\n3. Parameter explanations\n4. Return value descriptions\n5. Usage examples"
        
        return self.generate_code(prompt, model_name, temperature)
    
    def generate_tests(self, code: str, model_name: Optional[str] = None, temperature: float = 0.3) -> Dict[str, Any]:
        """Generate test cases for the given code.
        
        Args:
            code: The code to test
            model_name: Name of the AI model to use (optional)
            temperature: Temperature for generation
            
        Returns:
            Generated test cases
        """
        prompt = f"Generate comprehensive test cases for the following code:\n\n```\n{code}\n```\n\nPlease include:\n1. Unit tests for all functions/methods\n2. Edge case tests\n3. Integration tests if applicable\n4. Test setup and teardown code"
        
        return self.generate_code(prompt, model_name, temperature)
    
    def fix_bugs(self, code: str, error_message: str, model_name: Optional[str] = None, temperature: float = 0.3) -> Dict[str, Any]:
        """Fix bugs in the given code.
        
        Args:
            code: The code with bugs
            error_message: The error message
            model_name: Name of the AI model to use (optional)
            temperature: Temperature for generation
            
        Returns:
            Fixed code and explanation
        """
        prompt = f"Fix the bugs in the following code that is producing this error:\n\nError: {error_message}\n\nCode:\n```\n{code}\n```\n\nPlease provide:\n1. The fixed code\n2. An explanation of what was wrong\n3. How the fix resolves the issue"
        
        return self.generate_code(prompt, model_name, temperature)
    
    def optimize_code(self, code: str, optimization_goal: str, model_name: Optional[str] = None, temperature: float = 0.3) -> Dict[str, Any]:
        """Optimize the given code.
        
        Args:
            code: The code to optimize
            optimization_goal: The optimization goal (e.g., "performance", "memory", "readability")
            model_name: Name of the AI model to use (optional)
            temperature: Temperature for generation
            
        Returns:
            Optimized code and explanation
        """
        prompt = f"Optimize the following code for {optimization_goal}:\n\n```\n{code}\n```\n\nPlease provide:\n1. The optimized code\n2. An explanation of the optimizations made\n3. The expected improvements"
        
        return self.generate_code(prompt, model_name, temperature)
    
    def save_api_keys(self, file_path: str) -> bool:
        """Save API keys to a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save API keys to file
            with open(file_path, 'w') as f:
                json.dump(self.api_keys, f)
            
            logger.info(f"Saved API keys to {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving API keys: {str(e)}")
            return False
    
    def load_api_keys(self, file_path: str) -> bool:
        """Load API keys from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                logger.warning(f"API keys file {file_path} does not exist")
                return False
            
            # Load API keys from file
            with open(file_path, 'r') as f:
                api_keys = json.load(f)
            
            # Set API keys
            for model_name, api_key in api_keys.items():
                self.set_api_key(model_name, api_key)
            
            logger.info(f"Loaded API keys from {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error loading API keys: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    # Create a model manager
    manager = ModelManager()
    
    # Set API keys
    manager.set_api_key("deepseek", "your_deepseek_api_key")
    manager.set_api_key("gemini", "your_gemini_api_key")
    manager.set_api_key("chatgpt", "your_openai_api_key")
    manager.set_api_key("grok", "your_grok_api_key")
    manager.set_api_key("claude", "your_anthropic_api_key")
    
    # Set active model
    manager.set_active_model("deepseek")
    
    # Generate code
    result = manager.generate_code(
        prompt="Create a simple web server in Node.js that serves static files",
        temperature=0.3
    )
    
    print("Generated Code:")
    print(result["code"])
    print("\nExplanation:")
    print(result["explanation"])