# AI-Powered SDLC System - API Connector Module

import os
import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_connector.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("api_connector")

class APIConnector:
    """Base class for API connections to AI models."""
    
    def __init__(self, api_key: str, base_url: str):
        """Initialize the API connector.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        logger.info(f"Initialized API connector for {base_url}")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                     headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request data
            headers: Request headers
            params: Query parameters
            
        Returns:
            API response as a dictionary
        """
        url = urljoin(self.base_url, endpoint)
        
        if headers is None:
            headers = {}
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            return {"error": str(e)}


class DeepSeekConnector(APIConnector):
    """Connector for DeepSeek API."""
    
    def __init__(self, api_key: str):
        """Initialize the DeepSeek API connector.
        
        Args:
            api_key: DeepSeek API key
        """
        super().__init__(api_key, "https://api.deepseek.com/v1")
    
    def generate_code(self, prompt: str, model: str = "deepseek-coder", temperature: float = 0.3) -> Dict[str, Any]:
        """Generate code using DeepSeek API.
        
        Args:
            prompt: The prompt for code generation
            model: The model to use
            temperature: Temperature for generation
            
        Returns:
            Generated code and explanation
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        
        response = self._make_request("POST", "chat/completions", data=data, headers=headers)
        
        if "error" in response:
            return response
        
        try:
            # Process the response to extract code and explanation
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract code blocks from the content
            import re
            
            # Default values in case extraction fails
            code = "// No code found in the response"
            explanation = "No explanation found in the response"
            code_blocks = re.findall(r'```(?:\w+)?\n(.+?)\n```', content, re.DOTALL)
            
            if code_blocks:
                code = code_blocks[0]
            else:
                code = content
            
            # Remove code blocks from content to get explanation
            explanation = re.sub(r'```(?:\w+)?\n.+?\n```', '', content, flags=re.DOTALL).strip()
            
            return {
                "code": code,
                "explanation": explanation
            }
        
        except Exception as e:
            logger.error(f"Error processing DeepSeek response: {str(e)}")
            return {"error": f"Failed to process response: {str(e)}"}


class GeminiConnector(APIConnector):
    """Connector for Google's Gemini API."""
    
    def __init__(self, api_key: str):
        """Initialize the Gemini API connector.
        
        Args:
            api_key: Gemini API key
        """
        super().__init__(api_key, "https://generativelanguage.googleapis.com/v1")
    
    def generate_code(self, prompt: str, model: str = "gemini-pro-code", temperature: float = 0.3) -> Dict[str, Any]:
        """Generate code using Gemini API.
        
        Args:
            prompt: The prompt for code generation
            model: The model to use
            temperature: Temperature for generation
            
        Returns:
            Dictionary containing generated code and explanation
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": temperature
            }
        }
        
        params = {
            "key": self.api_key
        }
        
        endpoint = f"models/{model}:generateContent"
        response = self._make_request("POST", endpoint, data=data, headers=headers, params=params)
        
        if "error" in response:
            return response
        
        try:
            # Process the response to extract code and explanation
            content = response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # Extract code blocks from the content
            import re
            
            # Default values in case extraction fails
            code = "// No code found in the response"
            explanation = "No explanation found in the response"
            
            code_blocks = re.findall(r'```(?:\w+)?\n(.+?)\n```', content, re.DOTALL)
            
            if code_blocks:
                code = code_blocks[0]
            else:
                code = content
            
            # Remove code blocks from content to get explanation
            explanation = re.sub(r'```(?:\w+)?\n.+?\n```', '', content, flags=re.DOTALL).strip()
            
            return {
                "code": code,
                "explanation": explanation
            }
        
        except Exception as e:
            logger.error(f"Error processing Gemini response: {str(e)}")
            return {"error": f"Failed to process response: {str(e)}"}


class OpenAIConnector(APIConnector):
    """Connector for OpenAI's API (ChatGPT)."""
    
    def __init__(self, api_key: str):
        """Initialize the OpenAI API connector.
        
        Args:
            api_key: OpenAI API key
        """
        super().__init__(api_key, "https://api.openai.com/v1")
    
    def generate_code(self, prompt: str, model: str = "gpt-5", temperature: float = 0.3) -> Dict[str, Any]:
        """Generate code using OpenAI API.
        
        Args:
            prompt: The prompt for code generation
            model: The model to use
            temperature: Temperature for generation
            
        Returns:
            Generated code and explanation
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        
        response = self._make_request("POST", "chat/completions", data=data, headers=headers)
        
        if "error" in response:
            return response
        
        try:
            # Process the response to extract code and explanation
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract code blocks from the content
            import re
            
            # Default values in case extraction fails
            code = "// No code found in the response"
            explanation = "No explanation found in the response"
            
            code_blocks = re.findall(r'```(?:\w+)?\n(.+?)\n```', content, re.DOTALL)
            
            if code_blocks:
                code = code_blocks[0]
            else:
                code = content
            
            # Remove code blocks from content to get explanation
            explanation = re.sub(r'```(?:\w+)?\n.+?\n```', '', content, flags=re.DOTALL).strip()
            
            return {
                "code": code,
                "explanation": explanation
            }
        
        except Exception as e:
            logger.error(f"Error processing OpenAI response: {str(e)}")
            return {"error": f"Failed to process response: {str(e)}"}


class GrokConnector(APIConnector):
    """Connector for Grok API."""
    
    def __init__(self, api_key: str):
        """Initialize the Grok API connector.
        
        Args:
            api_key: Grok API key
        """
        super().__init__(api_key, "https://api.grok.com/v1")
    
    def generate_code(self, prompt: str, model: str = "grok-2", temperature: float = 0.3) -> Dict[str, Any]:
        """Generate code using Grok API.
        
        Args:
            prompt: The prompt for code generation
            model: The model to use
            temperature: Temperature for generation
            
        Returns:
            Generated code and explanation
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        
        response = self._make_request("POST", "chat/completions", data=data, headers=headers)
        
        if "error" in response:
            return response
        
        try:
            # Process the response to extract code and explanation
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract code blocks from the content
            import re
            
            # Default values in case extraction fails
            code = "// No code found in the response"
            explanation = "No explanation found in the response"
            
            code_blocks = re.findall(r'```(?:\w+)?\n(.+?)\n```', content, re.DOTALL)
            
            if code_blocks:
                code = code_blocks[0]
            else:
                code = content
            
            # Remove code blocks from content to get explanation
            explanation = re.sub(r'```(?:\w+)?\n.+?\n```', '', content, flags=re.DOTALL).strip()
            
            return {
                "code": code,
                "explanation": explanation
            }
        
        except Exception as e:
            logger.error(f"Error processing Grok response: {str(e)}")
            return {"error": f"Failed to process response: {str(e)}"}


class ClaudeConnector(APIConnector):
    """Connector for Anthropic's Claude API."""
    
    def __init__(self, api_key: str):
        """Initialize the Claude API connector.
        
        Args:
            api_key: Claude API key
        """
        super().__init__(api_key, "https://api.anthropic.com/v1")
    
    def generate_code(self, prompt: str, model: str = "claude-3-opus", temperature: float = 0.3) -> Dict[str, Any]:
        """Generate code using Claude API.
        
        Args:
            prompt: The prompt for code generation
            model: The model to use
            temperature: Temperature for generation
            
        Returns:
            Generated code and explanation
        """
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        
        response = self._make_request("POST", "messages", data=data, headers=headers)
        
        if "error" in response:
            return response
        
        try:
            # Process the response to extract code and explanation
            content = response.get("content", [{}])[0].get("text", "")
            
            # Extract code blocks from the content
            import re
            
            # Default values in case extraction fails
            code = "// No code found in the response"
            explanation = "No explanation found in the response"
            
            code_blocks = re.findall(r'```(?:\w+)?\n(.+?)\n```', content, re.DOTALL)
            
            if code_blocks:
                code = code_blocks[0]
            else:
                code = content
            
            # Remove code blocks from content to get explanation
            explanation = re.sub(r'```(?:\w+)?\n.+?\n```', '', content, flags=re.DOTALL).strip()
            
            return {
                "code": code,
                "explanation": explanation
            }
        
        except Exception as e:
            logger.error(f"Error processing Claude response: {str(e)}")
            return {"error": f"Failed to process response: {str(e)}"}


class AIModelFactory:
    """Factory class for creating AI model connectors."""
    
    @staticmethod
    def create_connector(model_name: str, api_key: str) -> APIConnector:
        """Create an API connector for the specified model.
        
        Args:
            model_name: Name of the AI model
            api_key: API key for the model
            
        Returns:
            An API connector instance
        """
        if model_name == "model1":
            return DeepSeekConnector(api_key)
        elif model_name == "model2":
            return GeminiConnector(api_key)
        elif model_name == "model3":
            return OpenAIConnector(api_key)
        elif model_name == "model4":
            return GrokConnector(api_key)
        elif model_name == "model5":
            return ClaudeConnector(api_key)
        else:
            raise ValueError(f"Unknown model: {model_name}")


# Example usage
if __name__ == "__main__":
    # Example API keys (these would be loaded from environment variables or a secure storage in a real application)
    api_keys = {
        "model1": "your_model1_api_key",
        "model2": "your_model2_api_key",
        "model3": "your_model3_api_key",
        "model4": "your_model4_api_key",
        "model5": "your_model5_api_key"
    }
    
    # Create a connector for Model 1
    connector = AIModelFactory.create_connector("model1", api_keys["model1"])
    
    # Generate code
    result = connector.generate_code(
        prompt="Create a simple web server in Node.js that serves static files",
        temperature=0.3
    )
    
    print("Generated Code:")
    print(result["code"])
    print("\nExplanation:")
    print(result["explanation"])