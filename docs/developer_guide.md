# AI-Powered SDLC System Developer Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Project Structure](#project-structure)
4. [Technology Stack](#technology-stack)
5. [Setup and Installation](#setup-and-installation)
6. [Core Components](#core-components)
   - [Frontend](#frontend)
   - [Backend](#backend)
   - [AI Integration](#ai-integration)
7. [Development Workflow](#development-workflow)
8. [API Documentation](#api-documentation)
9. [Extending the System](#extending-the-system)
10. [Testing](#testing)
11. [Deployment](#deployment)
12. [Contributing Guidelines](#contributing-guidelines)

## Introduction

This developer guide provides comprehensive information for developers who want to understand, modify, or extend the AI-Powered SDLC System. The system integrates multiple AI models to assist with various aspects of the software development lifecycle, including code generation, documentation, testing, bug fixing, and optimization.

## Architecture Overview

The AI-Powered SDLC System follows a client-side architecture with PyScript for backend processing:

```
+---------------------+
|     User Interface  |
|  (HTML, CSS, JS)    |
+----------+----------+
           |
           v
+----------+----------+
|  PyScript Runtime   |
| (Python in Browser) |
+----------+----------+
           |
           v
+----------+----------+
|   AI Model Manager  |
|                     |
+----------+----------+
           |
           v
+---------------------------+
| External AI Model APIs    |
| (Model 1, Model 2, etc.)  |
+---------------------------+
```

The system uses:
- HTML/CSS/JS for the frontend UI
- Three.js for 3D visualization
- PyScript for running Python in the browser
- Multiple AI model APIs for intelligent assistance

## Project Structure

```
d:\AI\
├── index.html              # Main application entry point
├── README.md               # Project overview and documentation
├── static\                 # Static assets
│   ├── css\               # Stylesheets
│   │   └── styles.css     # Custom CSS styles
│   ├── js\                # JavaScript files
│   │   └── main.js        # Main JavaScript functionality
│   ├── images\            # Image assets
│   │   └── particle.svg   # Particle image for 3D environment
│   └── models\            # 3D models (if any)
├── backend\               # Python backend code
│   ├── ai_integration.py  # AI integration logic
│   ├── api_connector.py   # API connector classes
│   ├── model_manager.py   # Model management
│   └── deployment.py      # Deployment utilities
└── docs\                  # Documentation
    ├── user_guide.md      # User documentation
    └── developer_guide.md # Developer documentation
```

## Technology Stack

### Frontend
- **HTML5**: Structure and content
- **CSS3/Tailwind CSS**: Styling and responsive design
- **JavaScript**: Client-side interactivity
- **Three.js**: 3D visualization and effects

### Backend (Browser-based)
- **PyScript**: Python runtime in the browser
- **Python 3.x**: Backend logic and AI integration

### AI Integration
- **Model 1 API**: Code generation and optimization
- **Model 2 API**: Documentation and explanations
- **Model 3 API**: General-purpose AI assistance
- **Model 4 API**: Bug fixing and code analysis
- **Model 5 API**: Advanced reasoning and problem-solving


## Setup and Installation

### Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-sdlc-system.git
   cd ai-sdlc-system
   ```

2. No build process is required as this is a client-side application. Simply open `index.html` in a web browser.

3. For development, we recommend using a local web server:
   ```bash
   # Using Python
   python -m http.server
   
   # Or using Node.js
   npx serve
   ```

4. Access the application at `http://localhost:8000` or the port specified by your web server.

### API Key Configuration

To develop with AI functionality, you'll need to obtain API keys from the following services:

- DeepSeek: [https://deepseek.ai](https://deepseek.ai)
- Gemini: [https://ai.google.dev](https://ai.google.dev)
- OpenAI (ChatGPT): [https://platform.openai.com](https://platform.openai.com)
- Grok: [https://grok.x.ai](https://grok.x.ai)
- Anthropic (Claude): [https://anthropic.com](https://anthropic.com)

Store these keys in your browser's local storage through the application's Settings panel for development purposes.

## Core Components

### Frontend

#### HTML Structure

The main application structure is defined in `index.html`, which includes:

- Navigation sidebar
- Content sections for each SDLC phase
- Settings panel
- 3D background container
- PyScript integration

#### CSS Styling

The application uses a combination of Tailwind CSS and custom styles defined in `static/css/styles.css`. Key styling components include:

- Dark/light mode theming
- Responsive layout
- Card and form styling
- Animation effects
- 3D environment styling

#### JavaScript Functionality

The `static/js/main.js` file handles:

- UI interactions and animations
- 3D background initialization and rendering
- Settings management
- Event listeners for user actions
- Theme switching

### Backend

#### PyScript Integration

PyScript allows running Python code directly in the browser. The main Python code is embedded in the `<py-script>` tag in `index.html` and handles:

- Initialization of the application
- Event handling for Python-based features
- Integration with the Model Manager

#### AI Integration

The AI integration is managed through several Python modules:

- `backend/ai_integration.py`: Core AI functionality
- `backend/api_connector.py`: API connector classes for each AI model
- `backend/model_manager.py`: Management of multiple AI models

### AI Model Factory

The system uses a factory pattern to create and manage AI model connectors:

```python
class AIModelFactory:
    @staticmethod
    def create_connector(model_name, api_key):
        if model_name == "deepseek":
            return DeepSeekConnector(api_key)
        elif model_name == "gemini":
            return GeminiConnector(api_key)
        elif model_name == "chatgpt":
            return OpenAIConnector(api_key)
        elif model_name == "grok":
            return GrokConnector(api_key)
        elif model_name == "claude":
            return ClaudeConnector(api_key)
        else:
            raise ValueError(f"Unknown model: {model_name}")
```

## Development Workflow

### Adding a New Feature

1. **Frontend Changes**:
   - Update HTML structure in `index.html`
   - Add necessary CSS styles in `static/css/styles.css`
   - Implement JavaScript functionality in `static/js/main.js`

2. **Backend Changes**:
   - Add or modify Python functions in the appropriate backend files
   - Update the PyScript section in `index.html` to expose new functionality

3. **AI Integration**:
   - Extend the appropriate connector classes in `backend/api_connector.py`
   - Update the Model Manager in `backend/model_manager.py`

### Example: Adding a New AI Model

1. Create a new connector class in `backend/api_connector.py`:

```python
class NewModelConnector(APIConnector):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.base_url = "https://api.newmodel.ai/v1"
        
    def generate_code(self, prompt, language):
        # Implementation for the new model
        pass
        
    # Implement other required methods
```

2. Update the `AIModelFactory` to include the new model:

```python
@staticmethod
def create_connector(model_name, api_key):
    # Existing code...
    elif model_name == "newmodel":
        return NewModelConnector(api_key)
    # Existing code...
```

3. Add the new model to the settings UI in `index.html`.

## API Documentation

### Model Manager API

The `ModelManager` class provides the following key methods:

#### Setting API Keys

```python
def set_api_key(self, model_name, api_key):
    """Set the API key for a specific model."""
```

#### Generating Code

```python
def generate_code(self, prompt, language):
    """Generate code based on the prompt and language."""
```

#### Generating Documentation

```python
def generate_documentation(self, code, language):
    """Generate documentation for the given code."""
```

#### Generating Tests

```python
def generate_tests(self, code, language):
    """Generate test cases for the given code."""
```

#### Fixing Bugs

```python
def fix_bugs(self, code, error_message, language):
    """Fix bugs in the given code based on the error message."""
```

#### Optimizing Code

```python
def optimize_code(self, code, optimization_target, language):
    """Optimize the given code for the specified target."""
```

### API Connector Interface

All API connectors implement the following interface:

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

## Extending the System

### Adding a New SDLC Phase

To add a new phase to the SDLC system:

1. **Update the HTML**:
   - Add a new section to `index.html`
   - Create the necessary UI elements
   - Add a navigation item in the sidebar

2. **Add CSS Styles**:
   - Add styles for the new section in `static/css/styles.css`

3. **Implement JavaScript Functionality**:
   - Add event listeners and UI logic in `static/js/main.js`

4. **Add Python Backend**:
   - Implement the necessary functions in the PyScript section
   - Add corresponding methods to the Model Manager and API connectors

### Customizing the 3D Environment

The 3D background is implemented using Three.js in `static/js/main.js`. To customize it:

1. Modify the `initThreeJS()` function to change the scene setup
2. Update the particle system in `createParticles()` to change the visual effects
3. Adjust the animation in `animateThreeJS()` to change the movement patterns

## Testing

### Manual Testing

For manual testing, focus on the following areas:

1. **UI Functionality**:
   - Test all interactive elements
   - Verify responsive design on different screen sizes
   - Check dark/light mode switching

2. **AI Integration**:
   - Test each AI model with various inputs
   - Verify error handling for API failures
   - Check performance with large inputs

3. **3D Environment**:
   - Test performance at different quality settings
   - Verify toggling the 3D background works correctly

### Automated Testing

To implement automated testing:

1. Use a framework like Jest for JavaScript testing
2. Create unit tests for the Python code using PyTest
3. Implement end-to-end tests using a tool like Playwright or Cypress

## Deployment

The system can be deployed in several ways:

### Static Web Server

As a client-side application, it can be deployed to any static web server:

1. Copy all files to the web server's document root
2. Ensure the server is configured to serve HTML, CSS, JS, and SVG files with the correct MIME types

### Local Deployment

For local deployment, simply open `index.html` in a web browser.

### Custom Deployment

For custom deployment scenarios, use the `backend/deployment.py` script, which provides utilities for:

- Creating deployment packages
- Configuring environment-specific settings
- Backing up and restoring application state

## Contributing Guidelines

### Code Style

- **HTML/CSS**: Follow BEM (Block Element Modifier) methodology
- **JavaScript**: Use ES6+ features and maintain clean, documented code
- **Python**: Follow PEP 8 style guidelines

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with a clear description of the changes

### Documentation

When contributing, please update the relevant documentation:

- Update this developer guide for architectural changes
- Update the user guide for user-facing changes
- Add inline comments for complex code sections

---

This developer guide is a living document and will be updated as the system evolves. For questions or clarifications, please contact the project maintainers.