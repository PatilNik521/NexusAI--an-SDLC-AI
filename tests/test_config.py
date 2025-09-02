# AI-Powered SDLC System - Test Configuration

import os
import json
import tempfile

# Test configuration class
class TestConfig:
    """Configuration for test environment."""
    
    def __init__(self):
        """Initialize test configuration."""
        # Base paths
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Temporary directory for test artifacts
        self.temp_dir = tempfile.mkdtemp(prefix="ai_sdlc_test_")
        
        # Mock API keys for testing
        self.mock_api_keys = {
            "model1": "test-model1-key",
            "model2": "test-model2-key",
            "model3": "test-model3-key",
            "model4": "test-model4-key",
            "model5": "test-model5-key"
        }
        
        # Test data paths
        self.test_data_dir = os.path.join(self.test_dir, "test_data")
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Create test data if it doesn't exist
        self._create_test_data()
    
    def _create_test_data(self):
        """Create test data files if they don't exist."""
        # Sample code snippets for testing
        code_samples = {
            "factorial.js": "function factorial(n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
            
            "buggy_divide.js": "function divide(a, b) {\n    return a / b;\n}",
            
            "unoptimized_factorial.js": "function factorial(n) {\n    let result = 1;\n    for (let i = 1; i <= n; i++) {\n        result = result * i;\n    }\n    return result;\n}",
            
            "sample_class.py": "class Calculator:\n    def __init__(self):\n        self.result = 0\n    \n    def add(self, a, b):\n        self.result = a + b\n        return self.result\n    \n    def subtract(self, a, b):\n        self.result = a - b\n        return self.result\n    \n    def multiply(self, a, b):\n        self.result = a * b\n        return self.result\n    \n    def divide(self, a, b):\n        if b == 0:\n            raise ValueError('Cannot divide by zero')\n        self.result = a / b\n        return self.result"
        }
        
        # Write code samples to test data directory
        for filename, content in code_samples.items():
            file_path = os.path.join(self.test_data_dir, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(content)
        
        # Create mock API responses
        mock_responses = {
            "code_generation": {
                "prompt": "Create a function to calculate the factorial of a number",
                "response": {
                    "code": "function factorial(n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
                    "explanation": "This is a recursive implementation of the factorial function. It handles the base case (n <= 1) by returning 1, and for larger values, it multiplies n by the factorial of (n-1)."
                }
            },
            "documentation_generation": {
                "code": "function factorial(n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
                "response": "/**\n * Calculates the factorial of a number.\n * \n * @param {number} n - The number to calculate factorial for.\n * @returns {number} The factorial of n.\n * \n * @example\n * // returns 120\n * factorial(5);\n */"
            },
            "test_generation": {
                "code": "function factorial(n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
                "response": "describe('factorial', () => {\n    test('should return 1 for 0', () => {\n        expect(factorial(0)).toBe(1);\n    });\n    \n    test('should return 1 for 1', () => {\n        expect(factorial(1)).toBe(1);\n    });\n    \n    test('should return 2 for 2', () => {\n        expect(factorial(2)).toBe(2);\n    });\n    \n    test('should return 6 for 3', () => {\n        expect(factorial(3)).toBe(6);\n    });\n    \n    test('should return 120 for 5', () => {\n        expect(factorial(5)).toBe(120);\n    });\n    \n    test('should handle negative numbers', () => {\n        // This depends on the expected behavior for negative inputs\n        // Assuming we want to throw an error for negative inputs\n        expect(() => factorial(-1)).toThrow();\n    });\n});"
            },
            "bug_fixing": {
                "code": "function divide(a, b) {\n    return a / b;\n}",
                "error": "Error: Division by zero",
                "response": {
                    "fixed_code": "function divide(a, b) {\n    if (b === 0) {\n        throw new Error('Division by zero');\n    }\n    return a / b;\n}",
                    "explanation": "The bug was that the function didn't check for division by zero, which is undefined in mathematics and causes errors in JavaScript. I added a check to throw an error when b is zero."
                }
            },
            "code_optimization": {
                "code": "function factorial(n) {\n    let result = 1;\n    for (let i = 1; i <= n; i++) {\n        result = result * i;\n    }\n    return result;\n}",
                "response": {
                    "optimized_code": "function factorial(n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
                    "explanation": "I've optimized the function by using a recursive approach, which is more concise and often considered more elegant for factorial calculations. However, for very large values of n, the iterative approach might be more efficient to avoid stack overflow."
                }
            }
        }
        
        # Write mock responses to test data directory
        mock_responses_path = os.path.join(self.test_data_dir, "mock_responses.json")
        if not os.path.exists(mock_responses_path):
            with open(mock_responses_path, 'w') as f:
                json.dump(mock_responses, f, indent=2)
    
    def get_mock_response(self, response_type):
        """Get a mock API response for testing.
        
        Args:
            response_type (str): Type of response to get ('code_generation', 
                                'documentation_generation', etc.)
        
        Returns:
            dict: The mock response data
        """
        mock_responses_path = os.path.join(self.test_data_dir, "mock_responses.json")
        with open(mock_responses_path, 'r') as f:
            mock_responses = json.load(f)
        
        return mock_responses.get(response_type, {})
    
    def get_test_file_path(self, filename):
        """Get the path to a test data file.
        
        Args:
            filename (str): Name of the test file
        
        Returns:
            str: Full path to the test file
        """
        return os.path.join(self.test_data_dir, filename)
    
    def get_test_file_content(self, filename):
        """Get the content of a test data file.
        
        Args:
            filename (str): Name of the test file
        
        Returns:
            str: Content of the test file
        """
        file_path = self.get_test_file_path(filename)
        with open(file_path, 'r') as f:
            return f.read()
    
    def cleanup(self):
        """Clean up temporary test files."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Warning: Failed to clean up temporary directory: {e}")

# Create a singleton instance
config = TestConfig()