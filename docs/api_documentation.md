# AI-Powered SDLC System API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [API Overview](#api-overview)
3. [Authentication](#authentication)
4. [AI Model Connectors](#ai-model-connectors)
   - [Model 1 Connector](#model1-connector)
   - [Model 2 Connector](#model2-connector)
   - [Model 3 Connector](#model3-connector)
   - [Model 4 Connector](#model4-connector)
   - [Model 5 Connector](#model5-connector)
5. [Model Manager API](#model-manager-api)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Best Practices](#best-practices)

## Introduction

This document provides detailed information about the APIs used in the AI-Powered SDLC System. The system integrates with multiple AI model providers to deliver comprehensive assistance throughout the software development lifecycle.

## API Overview

The AI-Powered SDLC System uses a modular architecture for AI integration:

1. **API Connectors**: Individual classes that handle communication with specific AI model providers
2. **Model Manager**: A central manager that coordinates between the application and the appropriate AI model
3. **PyScript Integration**: Browser-based Python runtime that executes the API calls

## Authentication

All API connectors require authentication via API keys. These keys are stored in the browser's local storage and are only sent to the respective AI service providers.

### API Key Management

```python
def set_api_key(model_name, api_key):
    """Set the API key for a specific model in local storage."""
    localStorage.setItem(f"{model_name}_api_key", api_key)

def get_api_key(model_name):
    """Get the API key for a specific model from local storage."""
    return localStorage.getItem(f"{model_name}_api_key")
```

## AI Model Connectors

All model connectors implement a common interface defined in the `APIConnector` base class:

```python
class APIConnector:
    def __init__(self, api_key):
        self.api_key = api_key
        
    def generate_code(self, prompt, language):
        """Generate code based on the prompt and language."""
        raise NotImplementedError
        
    def generate_documentation(self, code, language):
        """Generate documentation for the given code."""
        raise NotImplementedError
        
    def generate_tests(self, code, language):
        """Generate test cases for the given code."""
        raise NotImplementedError
        
    def fix_bugs(self, code, error_message, language):
        """Fix bugs in the given code based on the error message."""
        raise NotImplementedError
        
    def optimize_code(self, code, optimization_target, language):
        """Optimize the given code for the specified target."""
        raise NotImplementedError
```

### Model 1 Connector

The Model 1 connector interfaces with the Model 1 AI API for code-related tasks.

#### Initialization

```python
class DeepSeekConnector(APIConnector):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
```

#### Generate Code

```python
def generate_code(self, prompt, language):
    """Generate code using Model 1 AI.
    
    Args:
        prompt (str): The description of the code to generate
        language (str): The programming language
        
    Returns:
        dict: The generated code and explanation
    """
    payload = {
        "model": "deepseek-coder",
        "messages": [
            {"role": "system", "content": f"You are an expert {language} programmer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    # API call implementation
    # ...
    
    return {
        "code": generated_code,
        "explanation": explanation
    }
```

### Gemini Connector

The Gemini connector interfaces with Google's Gemini AI API.

#### Initialization

```python
class GeminiConnector(APIConnector):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1"
        self.headers = {
            "Content-Type": "application/json"
        }
```

#### Generate Documentation

```python
def generate_documentation(self, code, language):
    """Generate documentation using Gemini AI.
    
    Args:
        code (str): The code to document
        language (str): The programming language
        
    Returns:
        str: The generated documentation
    """
    prompt = f"Generate comprehensive documentation for the following {language} code:\n\n{code}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }
    
    url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
    
    # API call implementation
    # ...
    
    return documentation
```

### OpenAI (ChatGPT) Connector

The OpenAI connector interfaces with OpenAI's API for ChatGPT models.

#### Initialization

```python
class OpenAIConnector(APIConnector):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model = "gpt-4o"
```

#### Generate Tests

```python
def generate_tests(self, code, language):
    """Generate test cases using OpenAI.
    
    Args:
        code (str): The code to test
        language (str): The programming language
        
    Returns:
        str: The generated test cases
    """
    prompt = f"Generate comprehensive test cases for the following {language} code:\n\n{code}\n\nInclude unit tests, edge cases, and any necessary setup."
    
    payload = {
        "model": self.model,
        "messages": [
            {"role": "system", "content": f"You are an expert in {language} testing."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    # API call implementation
    # ...
    
    return test_cases
```

### Grok Connector

The Grok connector interfaces with Grok's AI API for code analysis and bug fixing.

#### Initialization

```python
class GrokConnector(APIConnector):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://api.grok.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
```

#### Fix Bugs

```python
def fix_bugs(self, code, error_message, language):
    """Fix bugs using Grok AI.
    
    Args:
        code (str): The code with bugs
        error_message (str): The error message or description
        language (str): The programming language
        
    Returns:
        dict: The fixed code and explanation
    """
    prompt = f"Fix the following {language} code that has this error: {error_message}\n\n{code}"
    
    payload = {
        "messages": [
            {"role": "system", "content": f"You are an expert {language} debugger."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }
    
    # API call implementation
    # ...
    
    return {
        "fixed_code": fixed_code,
        "explanation": explanation
    }
```

### Claude Connector

The Claude connector interfaces with Anthropic's Claude AI API.

#### Initialization

```python
class ClaudeConnector(APIConnector):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        self.model = "claude-3-opus-20240229"
```

#### Optimize Code

```python
def optimize_code(self, code, optimization_target, language):
    """Optimize code using Claude AI.
    
    Args:
        code (str): The code to optimize
        optimization_target (str): The optimization target (e.g., "performance", "readability")
        language (str): The programming language
        
    Returns:
        dict: The optimized code and explanation
    """
    prompt = f"Optimize the following {language} code for {optimization_target}:\n\n{code}\n\nProvide the optimized code and explain your changes."
    
    payload = {
        "model": self.model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.2
    }
    
    # API call implementation
    # ...
    
    return {
        "optimized_code": optimized_code,
        "explanation": explanation
    }
```

## Model Manager API

The Model Manager coordinates between the application and the appropriate AI model connectors.

### Initialization

```python
class ModelManager:
    def __init__(self):
        self.connectors = {}
        self.active_model = None
        
    def set_api_key(self, model_name, api_key):
        """Set the API key for a specific model.
        
        Args:
            model_name (str): The name of the model (e.g., "deepseek", "gemini")
            api_key (str): The API key for the model
        """
        if api_key and api_key.strip():
            self.connectors[model_name] = AIModelFactory.create_connector(model_name, api_key)
            localStorage.setItem(f"{model_name}_api_key", api_key)
            
    def activate_model(self, model_name):
        """Activate a specific model for use.
        
        Args:
            model_name (str): The name of the model to activate
            
        Returns:
            bool: True if successful, False otherwise
        """
        if model_name in self.connectors:
            self.active_model = model_name
            return True
        return False
```

### Core Functionality

```python
def generate_code(self, prompt, language):
    """Generate code using the active model.
    
    Args:
        prompt (str): The description of the code to generate
        language (str): The programming language
        
    Returns:
        dict: The generated code and explanation
    """
    if not self.active_model or self.active_model not in self.connectors:
        raise ValueError("No active model available")
        
    return self.connectors[self.active_model].generate_code(prompt, language)
    
def generate_documentation(self, code, language):
    """Generate documentation using the active model.
    
    Args:
        code (str): The code to document
        language (str): The programming language
        
    Returns:
        str: The generated documentation
    """
    if not self.active_model or self.active_model not in self.connectors:
        raise ValueError("No active model available")
        
    return self.connectors[self.active_model].generate_documentation(code, language)
```

## Error Handling

The system implements standardized error handling for API calls:

```python
def handle_api_error(response):
    """Handle API error responses.
    
    Args:
        response: The API response object
        
    Returns:
        dict: Error information
    """
    if response.status_code == 401:
        return {"error": "Authentication error. Please check your API key."}
    elif response.status_code == 429:
        return {"error": "Rate limit exceeded. Please try again later."}
    elif response.status_code >= 500:
        return {"error": "Server error. Please try again later."}
    else:
        try:
            error_data = response.json()
            return {"error": error_data.get("error", {}).get("message", "Unknown error")}
        except:
            return {"error": f"Error: {response.status_code} - {response.text}"}
```

## Rate Limiting

The system implements basic rate limiting to prevent excessive API calls:

```python
class RateLimiter:
    def __init__(self, max_calls=10, time_window=60):
        """Initialize the rate limiter.
        
        Args:
            max_calls (int): Maximum number of calls allowed in the time window
            time_window (int): Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
        
    def can_make_call(self):
        """Check if a call can be made within the rate limits.
        
        Returns:
            bool: True if a call can be made, False otherwise
        """
        current_time = time.time()
        # Remove calls outside the time window
        self.calls = [call_time for call_time in self.calls if current_time - call_time <= self.time_window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(current_time)
            return True
        return False
```

## Best Practices

### API Key Security

- Never expose API keys in client-side code (except in local storage)
- Use environment variables for API keys in production environments
- Implement proper access controls for API key management

### Optimizing API Calls

- Batch requests when possible
- Implement caching for frequently used responses
- Use appropriate model parameters (temperature, max tokens) for each task

### Error Handling

- Always handle API errors gracefully
- Provide clear error messages to users
- Implement retry logic for transient errors

### Rate Limiting

- Respect the rate limits of each AI provider
- Implement client-side rate limiting to prevent excessive calls
- Consider using a queue for high-volume scenarios

---

This API documentation is subject to change as the AI models and their APIs evolve. Always refer to the official documentation of each AI provider for the most up-to-date information.