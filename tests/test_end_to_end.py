# AI-Powered SDLC System - End-to-End Tests

import unittest
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import backend modules for testing
from backend.model_manager import ModelManager
from backend.api_connector import AIModelFactory

class EndToEndTests(unittest.TestCase):
    """End-to-End tests for the AI-Powered SDLC System."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment before any tests run."""
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the WebDriver
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Set window size
        cls.driver.set_window_size(1920, 1080)
        
        # Set up test API keys (these would be mock keys for testing)
        cls.test_api_keys = {
            "deepseek": "test-deepseek-key",
            "gemini": "test-gemini-key",
            "chatgpt": "test-chatgpt-key",
            "grok": "test-grok-key",
            "claude": "test-claude-key"
        }
        
        # Initialize the ModelManager with test keys
        cls.model_manager = ModelManager()
        for model, key in cls.test_api_keys.items():
            cls.model_manager.set_api_key(model, key)
            cls.model_manager.activate_model(model)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests have run."""
        cls.driver.quit()
    
    def setUp(self):
        """Set up before each test."""
        # Navigate to the application
        self.driver.get("file://" + os.path.abspath(os.path.join(os.path.dirname(__file__), "../index.html")))
        
        # Wait for the application to load
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "loading-screen"))
        )
        
        # Set up API keys in localStorage for the browser
        for model, key in self.test_api_keys.items():
            self.driver.execute_script(f"localStorage.setItem('{model}_api_key', '{key}')")
        
        # Refresh to apply localStorage changes
        self.driver.refresh()
        
        # Wait for the application to load again
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "loading-screen"))
        )
    
    def test_01_ui_loads_correctly(self):
        """Test that the UI loads correctly with all expected elements."""
        # Check that the main UI elements are present
        self.assertTrue(self.driver.find_element(By.ID, "app").is_displayed())
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "sidebar").is_displayed())
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "main-content").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "threeContainer").is_displayed())
        
        # Check that all sections are present
        sections = ["code-section", "docs-section", "testing-section", "bugs-section", "optimization-section"]
        for section in sections:
            self.assertTrue(self.driver.find_element(By.ID, section).is_displayed())
        
        # Check that the code section is active by default
        active_section = self.driver.find_element(By.CSS_SELECTOR, ".content-section.active")
        self.assertEqual(active_section.get_attribute("id"), "code-section")
    
    def test_02_navigation_works(self):
        """Test that navigation between sections works correctly."""
        # Get all navigation items
        nav_items = self.driver.find_elements(By.CLASS_NAME, "nav-item")
        
        # Click on each nav item and verify the corresponding section becomes active
        for i, nav_item in enumerate(nav_items):
            section_id = nav_item.get_attribute("data-section")
            nav_item.click()
            
            # Wait for the section to become active
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, section_id))
            )
            
            # Verify the section is active
            active_section = self.driver.find_element(By.CSS_SELECTOR, ".content-section.active")
            self.assertEqual(active_section.get_attribute("id"), section_id)
            
            # Verify the nav item is active
            self.assertTrue("active" in nav_item.get_attribute("class"))
    
    def test_03_dark_mode_toggle(self):
        """Test that dark mode toggle works correctly."""
        # Open settings panel
        settings_btn = self.driver.find_element(By.ID, "settings-btn")
        settings_btn.click()
        
        # Wait for settings panel to be visible
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Get the app element and dark mode toggle
        app = self.driver.find_element(By.ID, "app")
        dark_mode_toggle = self.driver.find_element(By.ID, "dark-mode-toggle")
        
        # Check initial state (should be light mode)
        self.assertFalse("dark-mode" in app.get_attribute("class"))
        
        # Toggle dark mode
        dark_mode_toggle.click()
        
        # Save settings
        save_btn = self.driver.find_element(By.ID, "save-settings-btn")
        save_btn.click()
        
        # Wait for settings panel to close
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Verify dark mode is enabled
        self.assertTrue("dark-mode" in app.get_attribute("class"))
        
        # Open settings again
        settings_btn.click()
        
        # Wait for settings panel to be visible
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Toggle back to light mode
        dark_mode_toggle = self.driver.find_element(By.ID, "dark-mode-toggle")
        dark_mode_toggle.click()
        
        # Save settings
        save_btn = self.driver.find_element(By.ID, "save-settings-btn")
        save_btn.click()
        
        # Wait for settings panel to close
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Verify light mode is enabled
        self.assertFalse("dark-mode" in app.get_attribute("class"))
    
    def test_04_code_generation(self):
        """Test the code generation functionality."""
        # Navigate to code section
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item[data-section='code-section']").click()
        
        # Enter requirements in the input field
        code_input = self.driver.find_element(By.ID, "code-input")
        test_requirement = "Create a function to calculate the factorial of a number"
        code_input.send_keys(test_requirement)
        
        # Click the generate button
        generate_btn = self.driver.find_element(By.ID, "generate-code-btn")
        generate_btn.click()
        
        # Wait for the generation to complete (button text changes back from "Generating...")
        WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.ID, "generate-code-btn").text != "Generating..."
        )
        
        # Check that output contains code
        code_output = self.driver.find_element(By.ID, "code-output")
        output_text = code_output.text
        
        # Verify that the output contains expected factorial function elements
        self.assertIn("function", output_text.lower())
        self.assertIn("factorial", output_text.lower())
        self.assertTrue("return" in output_text.lower())
    
    def test_05_documentation_generation(self):
        """Test the documentation generation functionality."""
        # Navigate to documentation section
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item[data-section='docs-section']").click()
        
        # Enter code in the input field
        docs_input = self.driver.find_element(By.ID, "docs-input")
        test_code = """function factorial(n) {
            if (n <= 1) return 1;
            return n * factorial(n - 1);
        }"""
        docs_input.send_keys(test_code)
        
        # Click the generate button
        generate_btn = self.driver.find_element(By.ID, "generate-docs-btn")
        generate_btn.click()
        
        # Wait for the generation to complete
        WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.ID, "generate-docs-btn").text != "Generating..."
        )
        
        # Check that output contains documentation
        docs_output = self.driver.find_element(By.ID, "docs-output")
        output_text = docs_output.text
        
        # Verify that the output contains expected documentation elements
        self.assertIn("factorial", output_text.lower())
        self.assertTrue(any(term in output_text.lower() for term in ["calculates", "computes", "returns"]))
        self.assertIn("parameter", output_text.lower())
    
    def test_06_test_generation(self):
        """Test the test case generation functionality."""
        # Navigate to testing section
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item[data-section='testing-section']").click()
        
        # Enter code in the input field
        test_input = self.driver.find_element(By.ID, "test-input")
        test_code = """function factorial(n) {
            if (n <= 1) return 1;
            return n * factorial(n - 1);
        }"""
        test_input.send_keys(test_code)
        
        # Click the generate button
        generate_btn = self.driver.find_element(By.ID, "generate-tests-btn")
        generate_btn.click()
        
        # Wait for the generation to complete
        WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.ID, "generate-tests-btn").text != "Generating..."
        )
        
        # Check that output contains test cases
        test_output = self.driver.find_element(By.ID, "test-output")
        output_text = test_output.text
        
        # Verify that the output contains expected test elements
        self.assertTrue(any(term in output_text.lower() for term in ["test", "assert", "expect"]))
        self.assertIn("factorial", output_text.lower())
    
    def test_07_bug_fixing(self):
        """Test the bug fixing functionality."""
        # Navigate to bug fixing section
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item[data-section='bugs-section']").click()
        
        # Enter buggy code in the input field
        bug_input = self.driver.find_element(By.ID, "bug-input")
        buggy_code = """function divide(a, b) {
            return a / b;
        }"""
        bug_input.send_keys(buggy_code)
        
        # Enter error description
        error_input = self.driver.find_element(By.ID, "error-input")
        error_description = "Error: Division by zero when b is 0"
        error_input.send_keys(error_description)
        
        # Click the fix button
        fix_btn = self.driver.find_element(By.ID, "fix-bugs-btn")
        fix_btn.click()
        
        # Wait for the fixing to complete
        WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.ID, "fix-bugs-btn").text != "Fixing..."
        )
        
        # Check that output contains fixed code
        bug_output = self.driver.find_element(By.ID, "bug-output")
        output_text = bug_output.text
        
        # Verify that the output contains division by zero check
        self.assertIn("if", output_text.lower())
        self.assertTrue(any(term in output_text.lower() for term in ["b === 0", "b == 0", "b !== 0", "b != 0", "b > 0"]))
    
    def test_08_code_optimization(self):
        """Test the code optimization functionality."""
        # Navigate to optimization section
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item[data-section='optimization-section']").click()
        
        # Enter code to optimize in the input field
        optimization_input = self.driver.find_element(By.ID, "optimization-input")
        unoptimized_code = """function factorial(n) {
            let result = 1;
            for (let i = 1; i <= n; i++) {
                result = result * i;
            }
            return result;
        }"""
        optimization_input.send_keys(unoptimized_code)
        
        # Click the optimize button
        optimize_btn = self.driver.find_element(By.ID, "optimize-code-btn")
        optimize_btn.click()
        
        # Wait for the optimization to complete
        WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element(By.ID, "optimize-code-btn").text != "Optimizing..."
        )
        
        # Check that output contains optimized code
        optimization_output = self.driver.find_element(By.ID, "optimization-output")
        output_text = optimization_output.text
        
        # Verify that the output contains optimized code
        # This could be various optimizations, so we check for common ones
        self.assertIn("factorial", output_text.lower())
        
    def test_09_api_key_management(self):
        """Test the API key management functionality."""
        # Open settings panel
        settings_btn = self.driver.find_element(By.ID, "settings-btn")
        settings_btn.click()
        
        # Wait for settings panel to be visible
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Check that API key fields are populated with masked values
        for model in ["deepseek", "gemini", "chatgpt", "grok", "claude"]:
            key_input = self.driver.find_element(By.ID, f"{model}-key")
            # The value should be populated (not empty) due to our localStorage setup
            self.assertTrue(key_input.get_attribute("value") != "")
        
        # Change an API key
        new_key = "new-test-key-123"
        deepseek_key_input = self.driver.find_element(By.ID, "deepseek-key")
        deepseek_key_input.clear()
        deepseek_key_input.send_keys(new_key)
        
        # Save settings
        save_btn = self.driver.find_element(By.ID, "save-settings-btn")
        save_btn.click()
        
        # Wait for settings panel to close
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Verify the key was saved in localStorage
        saved_key = self.driver.execute_script("return localStorage.getItem('deepseek_api_key')")
        self.assertEqual(saved_key, new_key)
        
        # Open settings again to verify the UI shows the updated key
        settings_btn.click()
        
        # Wait for settings panel to be visible
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Verify the key input shows the updated value
        deepseek_key_input = self.driver.find_element(By.ID, "deepseek-key")
        self.assertEqual(deepseek_key_input.get_attribute("value"), new_key)
    
    def test_10_3d_environment_controls(self):
        """Test the 3D environment control functionality."""
        # Open settings panel
        settings_btn = self.driver.find_element(By.ID, "settings-btn")
        settings_btn.click()
        
        # Wait for settings panel to be visible
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Get the 3D toggle and the three container
        toggle_3d = self.driver.find_element(By.ID, "3d-toggle")
        three_container = self.driver.find_element(By.ID, "threeContainer")
        
        # Check initial state (should be enabled)
        self.assertTrue(toggle_3d.is_selected())
        self.assertTrue(three_container.is_displayed())
        
        # Disable 3D
        toggle_3d.click()
        
        # Save settings
        save_btn = self.driver.find_element(By.ID, "save-settings-btn")
        save_btn.click()
        
        # Wait for settings panel to close
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Verify 3D is disabled
        self.assertFalse(three_container.is_displayed())
        
        # Open settings again
        settings_btn.click()
        
        # Wait for settings panel to be visible
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Enable 3D again
        toggle_3d = self.driver.find_element(By.ID, "3d-toggle")
        toggle_3d.click()
        
        # Change 3D quality
        quality_select = self.driver.find_element(By.ID, "3d-quality")
        quality_select.click()
        
        # Select high quality option
        high_option = self.driver.find_element(By.CSS_SELECTOR, "#3d-quality option[value='high']")
        high_option.click()
        
        # Save settings
        save_btn = self.driver.find_element(By.ID, "save-settings-btn")
        save_btn.click()
        
        # Wait for settings panel to close
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((By.ID, "settings-panel"))
        )
        
        # Verify 3D is enabled again
        self.assertTrue(three_container.is_displayed())


if __name__ == "__main__":
    unittest.main()