# PyScript application for AI-SDLC
import json
import sys
from js import document, console, localStorage

# Import backend modules
from model_manager import ModelManager
from api_connector import AIModelFactory

# Create model manager instance
model_manager = ModelManager()

# Initialize API keys from localStorage
def init_api_keys():
    try:
        # Model 1 API key
        model1_key = localStorage.getItem("model1_api_key")
        if model1_key:
            model_manager.set_api_key("model1", model1_key)
            console.log("Model 1 API key loaded")
        
        # Model 2 API key
        model2_key = localStorage.getItem("model2_api_key")
        if model2_key:
            model_manager.set_api_key("model2", model2_key)
            console.log("Model 2 API key loaded")
        
        # Model 3 API key
        model3_key = localStorage.getItem("model3_api_key")
        if model3_key:
            model_manager.set_api_key("model3", model3_key)
            console.log("Model 3 API key loaded")
        
        # Model 4 API key
        model4_key = localStorage.getItem("model4_api_key")
        if model4_key:
            model_manager.set_api_key("model4", model4_key)
            console.log("Model 4 API key loaded")
        
        # Model 5 API key
        model5_key = localStorage.getItem("model5_api_key")
        if model5_key:
            model_manager.set_api_key("model5", model5_key)
            console.log("Model 5 API key loaded")
    except Exception as e:
        console.error(f"Error initializing API keys: {e}")

# Save API keys to localStorage
def save_api_keys():
    try:
        # Get values from input fields
        model1_key = document.getElementById("model1-api-key").value
        model2_key = document.getElementById("model2-api-key").value
        model3_key = document.getElementById("model3-api-key").value
        model4_key = document.getElementById("model4-api-key").value
        model5_key = document.getElementById("model5-api-key").value
        
        # Save to localStorage
        if model1_key:
            localStorage.setItem("model1_api_key", model1_key)
            model_manager.set_api_key("model1", model1_key)
        
        if model2_key:
            localStorage.setItem("model2_api_key", model2_key)
            model_manager.set_api_key("model2", model2_key)
        
        if model3_key:
            localStorage.setItem("model3_api_key", model3_key)
            model_manager.set_api_key("model3", model3_key)
        
        if model4_key:
            localStorage.setItem("model4_api_key", model4_key)
            model_manager.set_api_key("model4", model4_key)
        
        if model5_key:
            localStorage.setItem("model5_api_key", model5_key)
            model_manager.set_api_key("model5", model5_key)
        
        # Close modal
        document.getElementById("settings-modal").classList.add("hidden")
        console.log("API keys saved")
    except Exception as e:
        console.error(f"Error saving API keys: {e}")

# Get selected AI model
def get_selected_model():
    try:
        model_selector = document.getElementById("ai-model-selector")
        model_text = model_selector.querySelector("span").textContent
        model_name = model_text.replace("AI Model: ", "").lower()
        return model_name
    except Exception as e:
        console.error(f"Error getting selected model: {e}")
        return "model1"  # Default model

# Handle generate code button click
def handle_generate_code(event):
    try:
        console.log("Generate code button clicked")
        # Show loading state
        generate_btn = document.getElementById("generate-code-btn")
        generate_btn.classList.add("loading")
        generate_btn.disabled = True
        
        # Get input values
        requirements = document.getElementById("code-requirements").value
        language = document.getElementById("programming-language").value
        framework = document.getElementById("framework").value
        
        if not requirements:
            console.error("Requirements cannot be empty")
            # Show error message
            error_msg = document.getElementById("error-message")
            error_msg.textContent = "Please enter your requirements"
            error_msg.classList.remove("hidden")
            # Reset button state
            generate_btn.classList.remove("loading")
            generate_btn.disabled = False
            return
        
        # Hide error message if it was shown
        error_msg = document.getElementById("error-message")
        error_msg.classList.add("hidden")
        
        # Get selected model
        model_name = get_selected_model()
        
        # Create AI model instance
        ai_model = AIModelFactory.create_connector(model_name)
        
        # Generate code
        prompt = f"Generate {language} code using {framework} framework for the following requirements:\n{requirements}"
        response = ai_model.generate_code(prompt)
        
        # Process response
        if response and "code" in response:
            # Update code editor
            code_editor = document.getElementById("code-editor")
            code_editor.textContent = response["code"]
            
            # Update explanation
            explanation = document.getElementById("code-explanation")
            if "explanation" in response:
                explanation.textContent = response["explanation"]
            
            # Show success message
            success_msg = document.getElementById("success-message")
            success_msg.textContent = "Code generated successfully!"
            success_msg.classList.remove("hidden")
            
            # Enable copy and download buttons
            document.getElementById("copy-code-btn").disabled = False
            document.getElementById("download-code-btn").disabled = False
        else:
            # Show error message
            error_msg = document.getElementById("error-message")
            error_msg.textContent = "Failed to generate code. Please try again."
            error_msg.classList.remove("hidden")
        
        # Reset button state
        generate_btn.classList.remove("loading")
        generate_btn.disabled = False
    except Exception as e:
        console.error(f"Error generating code: {e}")
        # Show error message
        error_msg = document.getElementById("error-message")
        error_msg.textContent = f"Error: {str(e)}"
        error_msg.classList.remove("hidden")
        # Reset button state
        generate_btn = document.getElementById("generate-code-btn")
        generate_btn.classList.remove("loading")
        generate_btn.disabled = False

# Handle generate documentation button click
def handle_generate_docs(event):
    try:
        console.log("Generate documentation button clicked")
        # Show loading state
        generate_btn = document.getElementById("generate-docs-btn")
        generate_btn.classList.add("loading")
        generate_btn.disabled = True
        
        # Get input values
        code = document.getElementById("code-for-docs").value
        doc_type = document.getElementById("doc-type-selector").value
        
        if not code:
            console.error("Code cannot be empty")
            # Show error message
            error_msg = document.getElementById("docs-error-message")
            error_msg.textContent = "Please enter your code"
            error_msg.classList.remove("hidden")
            # Reset button state
            generate_btn.classList.remove("loading")
            generate_btn.disabled = False
            return
        
        # Hide error message if it was shown
        error_msg = document.getElementById("docs-error-message")
        error_msg.classList.add("hidden")
        
        # Get selected model
        model_name = get_selected_model()
        
        # Create AI model instance
        ai_model = AIModelFactory.create_model(model_name, model_manager.get_api_key(model_name))
        
        # Generate documentation
        prompt = f"Generate {doc_type} documentation for the following code:\n{code}"
        response = ai_model.generate_documentation(prompt)
        
        # Process response
        if response and "documentation" in response:
            # Update documentation editor
            docs_editor = document.getElementById("docs-editor")
            docs_editor.textContent = response["documentation"]
            
            # Show success message
            success_msg = document.getElementById("docs-success-message")
            success_msg.textContent = "Documentation generated successfully!"
            success_msg.classList.remove("hidden")
            
            # Enable copy and download buttons
            document.getElementById("copy-docs-btn").disabled = False
            document.getElementById("download-docs-btn").disabled = False
        else:
            # Show error message
            error_msg = document.getElementById("docs-error-message")
            error_msg.textContent = "Failed to generate documentation. Please try again."
            error_msg.classList.remove("hidden")
        
        # Reset button state
        generate_btn.classList.remove("loading")
        generate_btn.disabled = False
    except Exception as e:
        console.error(f"Error generating documentation: {e}")
        # Show error message
        error_msg = document.getElementById("docs-error-message")
        error_msg.textContent = f"Error: {str(e)}"
        error_msg.classList.remove("hidden")
        # Reset button state
        generate_btn = document.getElementById("generate-docs-btn")
        generate_btn.classList.remove("loading")
        generate_btn.disabled = False

# Handle generate tests button click
def handle_generate_tests(event):
    try:
        console.log("Generate tests button clicked")
        # Show loading state
        generate_btn = document.getElementById("generate-tests-btn")
        generate_btn.classList.add("loading")
        generate_btn.disabled = True
        
        # Get input values
        code = document.getElementById("code-for-tests").value
        test_framework = document.getElementById("test-framework-selector").value
        
        if not code:
            console.error("Code cannot be empty")
            # Show error message
            error_msg = document.getElementById("tests-error-message")
            error_msg.textContent = "Please enter your code"
            error_msg.classList.remove("hidden")
            # Reset button state
            generate_btn.classList.remove("loading")
            generate_btn.disabled = False
            return
        
        # Hide error message if it was shown
        error_msg = document.getElementById("tests-error-message")
        error_msg.classList.add("hidden")
        
        # Get selected model
        model_name = get_selected_model()
        
        # Create AI model instance
        ai_model = AIModelFactory.create_model(model_name, model_manager.get_api_key(model_name))
        
        # Generate tests
        prompt = f"Generate tests using {test_framework} for the following code:\n{code}"
        response = ai_model.generate_tests(prompt)
        
        # Process response
        if response and "tests" in response:
            # Update tests editor
            tests_editor = document.getElementById("tests-editor")
            tests_editor.textContent = response["tests"]
            
            # Show success message
            success_msg = document.getElementById("tests-success-message")
            success_msg.textContent = "Tests generated successfully!"
            success_msg.classList.remove("hidden")
            
            # Enable copy and download buttons
            document.getElementById("copy-tests-btn").disabled = False
            document.getElementById("download-tests-btn").disabled = False
        else:
            # Show error message
            error_msg = document.getElementById("tests-error-message")
            error_msg.textContent = "Failed to generate tests. Please try again."
            error_msg.classList.remove("hidden")
        
        # Reset button state
        generate_btn.classList.remove("loading")
        generate_btn.disabled = False
    except Exception as e:
        console.error(f"Error generating tests: {e}")
        # Show error message
        error_msg = document.getElementById("tests-error-message")
        error_msg.textContent = f"Error: {str(e)}"
        error_msg.classList.remove("hidden")
        # Reset button state
        generate_btn = document.getElementById("generate-tests-btn")
        generate_btn.classList.remove("loading")
        generate_btn.disabled = False

# Handle fix bugs button click
def handle_fix_bugs(event):
    try:
        console.log("Fix bugs button clicked")
        # Show loading state
        fix_btn = document.getElementById("fix-bugs-btn")
        fix_btn.classList.add("loading")
        fix_btn.disabled = True
        
        # Get input values
        code = document.getElementById("buggy-code").value
        error_msg = document.getElementById("error-description").value
        
        if not code:
            console.error("Code cannot be empty")
            # Show error message
            error_display = document.getElementById("bugs-error-message")
            error_display.textContent = "Please enter your code"
            error_display.classList.remove("hidden")
            # Reset button state
            fix_btn.classList.remove("loading")
            fix_btn.disabled = False
            return
        
        # Hide error message if it was shown
        error_display = document.getElementById("bugs-error-message")
        error_display.classList.add("hidden")
        
        # Get selected model
        model_name = get_selected_model()
        
        # Create AI model instance
        ai_model = AIModelFactory.create_model(model_name, model_manager.get_api_key(model_name))
        
        # Fix bugs
        prompt = f"Fix bugs in the following code:\n{code}\n\nError description:\n{error_msg}"
        response = ai_model.fix_bugs(prompt)
        
        # Process response
        if response and "fixed_code" in response:
            # Update fixed code editor
            fixed_code_editor = document.getElementById("fixed-code-editor")
            fixed_code_editor.textContent = response["fixed_code"]
            
            # Update explanation
            explanation = document.getElementById("bug-fix-explanation")
            if "explanation" in response:
                explanation.textContent = response["explanation"]
            
            # Show success message
            success_msg = document.getElementById("bugs-success-message")
            success_msg.textContent = "Bugs fixed successfully!"
            success_msg.classList.remove("hidden")
            
            # Enable copy and download buttons
            document.getElementById("copy-fixed-code-btn").disabled = False
            document.getElementById("download-fixed-code-btn").disabled = False
        else:
            # Show error message
            error_display = document.getElementById("bugs-error-message")
            error_display.textContent = "Failed to fix bugs. Please try again."
            error_display.classList.remove("hidden")
        
        # Reset button state
        fix_btn.classList.remove("loading")
        fix_btn.disabled = False
    except Exception as e:
        console.error(f"Error fixing bugs: {e}")
        # Show error message
        error_display = document.getElementById("bugs-error-message")
        error_display.textContent = f"Error: {str(e)}"
        error_display.classList.remove("hidden")
        # Reset button state
        fix_btn = document.getElementById("fix-bugs-btn")
        fix_btn.classList.remove("loading")
        fix_btn.disabled = False

# Handle optimize code button click
def handle_optimize_code(event):
    try:
        console.log("Optimize code button clicked")
        # Show loading state
        optimize_btn = document.getElementById("optimize-code-btn")
        optimize_btn.classList.add("loading")
        optimize_btn.disabled = True
        
        # Get input values
        code = document.getElementById("code-to-optimize").value
        optimization_goal = document.getElementById("optimization-goal-selector").value
        
        if not code:
            console.error("Code cannot be empty")
            # Show error message
            error_msg = document.getElementById("optimize-error-message")
            error_msg.textContent = "Please enter your code"
            error_msg.classList.remove("hidden")
            # Reset button state
            optimize_btn.classList.remove("loading")
            optimize_btn.disabled = False
            return
        
        # Hide error message if it was shown
        error_msg = document.getElementById("optimize-error-message")
        error_msg.classList.add("hidden")
        
        # Get selected model
        model_name = get_selected_model()
        
        # Create AI model instance
        ai_model = AIModelFactory.create_model(model_name, model_manager.get_api_key(model_name))
        
        # Optimize code
        prompt = f"Optimize the following code for {optimization_goal}:\n{code}"
        response = ai_model.optimize_code(prompt)
        
        # Process response
        if response and "optimized_code" in response:
            # Update optimized code editor
            optimized_code_editor = document.getElementById("optimized-code-editor")
            optimized_code_editor.textContent = response["optimized_code"]
            
            # Update explanation
            explanation = document.getElementById("optimization-explanation")
            if "explanation" in response:
                explanation.textContent = response["explanation"]
            
            # Show success message
            success_msg = document.getElementById("optimize-success-message")
            success_msg.textContent = "Code optimized successfully!"
            success_msg.classList.remove("hidden")
            
            # Enable copy and download buttons
            document.getElementById("copy-optimized-code-btn").disabled = False
            document.getElementById("download-optimized-code-btn").disabled = False
        else:
            # Show error message
            error_msg = document.getElementById("optimize-error-message")
            error_msg.textContent = "Failed to optimize code. Please try again."
            error_msg.classList.remove("hidden")
        
        # Reset button state
        optimize_btn.classList.remove("loading")
        optimize_btn.disabled = False
    except Exception as e:
        console.error(f"Error optimizing code: {e}")
        # Show error message
        error_msg = document.getElementById("optimize-error-message")
        error_msg.textContent = f"Error: {str(e)}"
        error_msg.classList.remove("hidden")
        # Reset button state
        optimize_btn = document.getElementById("optimize-code-btn")
        optimize_btn.classList.remove("loading")
        optimize_btn.disabled = False

# Initialize the application
def init_app():
    try:
        console.log("Initializing application...")
        
        # Initialize API keys
        init_api_keys()
        
        # Add event listeners for buttons
        generate_code_btn = document.getElementById("generate-code-btn")
        generate_code_btn.addEventListener("click", handle_generate_code)
        
        generate_docs_btn = document.getElementById("generate-docs-btn")
        generate_docs_btn.addEventListener("click", handle_generate_docs)
        
        generate_tests_btn = document.getElementById("generate-tests-btn")
        generate_tests_btn.addEventListener("click", handle_generate_tests)
        
        fix_bugs_btn = document.getElementById("fix-bugs-btn")
        fix_bugs_btn.addEventListener("click", handle_fix_bugs)
        
        optimize_code_btn = document.getElementById("optimize-code-btn")
        optimize_code_btn.addEventListener("click", handle_optimize_code)
        
        save_settings_btn = document.getElementById("save-settings")
        save_settings_btn.addEventListener("click", save_api_keys)
        
        console.log("Application initialized successfully")
    except Exception as e:
        console.error(f"Error initializing application: {e}")

# Call init_app when the page loads
init_app()
console.log("app.py loaded and init_app() called")