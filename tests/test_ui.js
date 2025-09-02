// AI-Powered SDLC System - UI Tests

/**
 * This file contains tests for the UI components of the AI-Powered SDLC System.
 * It uses Jest and Testing Library for testing the frontend functionality.
 */

// Mock dependencies
jest.mock('three', () => ({
  Scene: jest.fn().mockImplementation(() => ({
    add: jest.fn(),
    background: null
  })),
  PerspectiveCamera: jest.fn(),
  WebGLRenderer: jest.fn().mockImplementation(() => ({
    setSize: jest.fn(),
    setClearColor: jest.fn(),
    domElement: document.createElement('canvas'),
    render: jest.fn()
  })),
  Color: jest.fn(),
  BufferGeometry: jest.fn(),
  BufferAttribute: jest.fn(),
  Points: jest.fn(),
  ShaderMaterial: jest.fn(),
  TextureLoader: jest.fn().mockImplementation(() => ({
    load: jest.fn().mockReturnValue({})
  }))
}));

// Import dependencies
import { fireEvent, getByText, getByTestId, waitFor } from '@testing-library/dom';
import '@testing-library/jest-dom';
import { initThreeJS, createParticles, animateThreeJS } from '../static/js/main.js';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: jest.fn(key => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    removeItem: jest.fn(key => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    })
  };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock document functions
document.getElementById = jest.fn(id => {
  const element = document.createElement('div');
  element.id = id;
  if (id === 'threeContainer') {
    element.style.width = '800px';
    element.style.height = '600px';
  }
  return element;
});

document.querySelector = jest.fn(selector => {
  const element = document.createElement('div');
  if (selector === '.dark-mode-toggle') {
    element.classList.add('dark-mode-toggle');
    element.checked = false;
  }
  return element;
});

document.querySelectorAll = jest.fn(selector => {
  const elements = [];
  if (selector === '.nav-item') {
    for (let i = 0; i < 5; i++) {
      const element = document.createElement('div');
      element.classList.add('nav-item');
      element.dataset.section = `section-${i}`;
      elements.push(element);
    }
  }
  return elements;
});

// Setup and teardown
beforeEach(() => {
  // Setup DOM for testing
  document.body.innerHTML = `
    <div id="app" class="light-mode">
      <div id="loading-screen">
        <div class="spinner"></div>
        <p>Loading AI-Powered SDLC System...</p>
      </div>
      <div class="sidebar">
        <div class="nav-item active" data-section="code-section">Code Generation</div>
        <div class="nav-item" data-section="docs-section">Documentation</div>
        <div class="nav-item" data-section="testing-section">Testing</div>
        <div class="nav-item" data-section="bugs-section">Bug Fixing</div>
        <div class="nav-item" data-section="optimization-section">Optimization</div>
      </div>
      <div class="main-content">
        <div id="code-section" class="content-section active">
          <textarea id="code-input" placeholder="Enter your requirements here..."></textarea>
          <button id="generate-code-btn">Generate Code</button>
          <div id="code-output"></div>
        </div>
        <div id="docs-section" class="content-section">
          <textarea id="docs-input" placeholder="Enter your code here..."></textarea>
          <button id="generate-docs-btn">Generate Documentation</button>
          <div id="docs-output"></div>
        </div>
        <div id="testing-section" class="content-section">
          <textarea id="test-input" placeholder="Enter your code here..."></textarea>
          <button id="generate-tests-btn">Generate Tests</button>
          <div id="test-output"></div>
        </div>
        <div id="bugs-section" class="content-section">
          <textarea id="bug-input" placeholder="Enter your code here..."></textarea>
          <textarea id="error-input" placeholder="Enter error message or description..."></textarea>
          <button id="fix-bugs-btn">Fix Bugs</button>
          <div id="bug-output"></div>
        </div>
        <div id="optimization-section" class="content-section">
          <textarea id="optimization-input" placeholder="Enter your code here..."></textarea>
          <button id="optimize-code-btn">Optimize Code</button>
          <div id="optimization-output"></div>
        </div>
      </div>
      <div id="settings-panel" class="hidden">
        <h2>Settings</h2>
        <div class="settings-group">
          <h3>API Keys</h3>
          <div class="form-group">
            <label for="deepseek-key">DeepSeek API Key</label>
            <input type="password" id="deepseek-key" />
          </div>
          <div class="form-group">
            <label for="gemini-key">Gemini API Key</label>
            <input type="password" id="gemini-key" />
          </div>
          <div class="form-group">
            <label for="chatgpt-key">ChatGPT API Key</label>
            <input type="password" id="chatgpt-key" />
          </div>
          <div class="form-group">
            <label for="grok-key">Grok API Key</label>
            <input type="password" id="grok-key" />
          </div>
          <div class="form-group">
            <label for="claude-key">Claude API Key</label>
            <input type="password" id="claude-key" />
          </div>
        </div>
        <div class="settings-group">
          <h3>Appearance</h3>
          <div class="form-group">
            <label for="dark-mode-toggle">Dark Mode</label>
            <input type="checkbox" id="dark-mode-toggle" class="dark-mode-toggle" />
          </div>
          <div class="form-group">
            <label for="3d-toggle">Enable 3D Background</label>
            <input type="checkbox" id="3d-toggle" checked />
          </div>
          <div class="form-group">
            <label for="3d-quality">3D Quality</label>
            <select id="3d-quality">
              <option value="low">Low</option>
              <option value="medium" selected>Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>
        <div class="settings-actions">
          <button id="save-settings-btn">Save Settings</button>
          <button id="cancel-settings-btn">Cancel</button>
        </div>
      </div>
      <div id="threeContainer"></div>
    </div>
  `;
  
  // Reset mocks
  jest.clearAllMocks();
});

afterEach(() => {
  // Clean up
  document.body.innerHTML = '';
});

// Test cases
describe('UI Navigation', () => {
  test('should switch active section when nav item is clicked', () => {
    // Get all nav items
    const navItems = document.querySelectorAll('.nav-item');
    
    // Click on the Documentation nav item
    fireEvent.click(navItems[1]);
    
    // Check that the active class is updated
    expect(navItems[0].classList.contains('active')).toBe(false);
    expect(navItems[1].classList.contains('active')).toBe(true);
    
    // Check that the content section is updated
    const codeSection = document.getElementById('code-section');
    const docsSection = document.getElementById('docs-section');
    expect(codeSection.classList.contains('active')).toBe(false);
    expect(docsSection.classList.contains('active')).toBe(true);
  });
});

describe('Dark Mode Toggle', () => {
  test('should toggle dark mode when switch is clicked', () => {
    // Get the dark mode toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const app = document.getElementById('app');
    
    // Initially in light mode
    expect(app.classList.contains('dark-mode')).toBe(false);
    
    // Click the toggle
    fireEvent.click(darkModeToggle);
    
    // Should switch to dark mode
    expect(app.classList.contains('dark-mode')).toBe(true);
    
    // Click again
    fireEvent.click(darkModeToggle);
    
    // Should switch back to light mode
    expect(app.classList.contains('dark-mode')).toBe(false);
  });
});

describe('Settings Panel', () => {
  test('should show settings panel when settings button is clicked', () => {
    // Create settings button
    const settingsBtn = document.createElement('button');
    settingsBtn.id = 'settings-btn';
    document.body.appendChild(settingsBtn);
    
    // Get the settings panel
    const settingsPanel = document.getElementById('settings-panel');
    
    // Initially hidden
    expect(settingsPanel.classList.contains('hidden')).toBe(true);
    
    // Click the settings button
    fireEvent.click(settingsBtn);
    
    // Should be visible
    expect(settingsPanel.classList.contains('hidden')).toBe(false);
    
    // Click cancel button
    const cancelBtn = document.getElementById('cancel-settings-btn');
    fireEvent.click(cancelBtn);
    
    // Should be hidden again
    expect(settingsPanel.classList.contains('hidden')).toBe(true);
  });
  
  test('should save API keys when save button is clicked', () => {
    // Set values for API key inputs
    const deepseekKey = document.getElementById('deepseek-key');
    const geminiKey = document.getElementById('gemini-key');
    const chatgptKey = document.getElementById('chatgpt-key');
    const grokKey = document.getElementById('grok-key');
    const claudeKey = document.getElementById('claude-key');
    
    fireEvent.change(deepseekKey, { target: { value: 'test-deepseek-key' } });
    fireEvent.change(geminiKey, { target: { value: 'test-gemini-key' } });
    fireEvent.change(chatgptKey, { target: { value: 'test-chatgpt-key' } });
    fireEvent.change(grokKey, { target: { value: 'test-grok-key' } });
    fireEvent.change(claudeKey, { target: { value: 'test-claude-key' } });
    
    // Click save button
    const saveBtn = document.getElementById('save-settings-btn');
    fireEvent.click(saveBtn);
    
    // Check localStorage was called with the correct values
    expect(localStorage.setItem).toHaveBeenCalledWith('deepseek_api_key', 'test-deepseek-key');
    expect(localStorage.setItem).toHaveBeenCalledWith('gemini_api_key', 'test-gemini-key');
    expect(localStorage.setItem).toHaveBeenCalledWith('chatgpt_api_key', 'test-chatgpt-key');
    expect(localStorage.setItem).toHaveBeenCalledWith('grok_api_key', 'test-grok-key');
    expect(localStorage.setItem).toHaveBeenCalledWith('claude_api_key', 'test-claude-key');
  });
});

describe('3D Environment', () => {
  test('should toggle 3D background when switch is clicked', () => {
    // Mock the 3D container
    const threeContainer = document.getElementById('threeContainer');
    
    // Get the 3D toggle
    const threeDToggle = document.getElementById('3d-toggle');
    
    // Initially enabled (checked)
    expect(threeDToggle.checked).toBe(true);
    
    // Click the toggle to disable
    fireEvent.click(threeDToggle);
    
    // Should be disabled
    expect(threeDToggle.checked).toBe(false);
    expect(threeContainer.style.display).toBe('none');
    
    // Click again to enable
    fireEvent.click(threeDToggle);
    
    // Should be enabled
    expect(threeDToggle.checked).toBe(true);
    expect(threeContainer.style.display).toBe('block');
  });
  
  test('should change 3D quality when dropdown is changed', () => {
    // Get the 3D quality dropdown
    const qualityDropdown = document.getElementById('3d-quality');
    
    // Initially set to medium
    expect(qualityDropdown.value).toBe('medium');
    
    // Change to high quality
    fireEvent.change(qualityDropdown, { target: { value: 'high' } });
    
    // Should update the value
    expect(qualityDropdown.value).toBe('high');
    
    // Change to low quality
    fireEvent.change(qualityDropdown, { target: { value: 'low' } });
    
    // Should update the value
    expect(qualityDropdown.value).toBe('low');
  });
});

describe('Code Generation', () => {
  test('should display loading state when generate button is clicked', () => {
    // Get the code input and button
    const codeInput = document.getElementById('code-input');
    const generateBtn = document.getElementById('generate-code-btn');
    
    // Enter some text
    fireEvent.change(codeInput, { target: { value: 'Create a function to calculate factorial' } });
    
    // Click the generate button
    fireEvent.click(generateBtn);
    
    // Button should show loading state
    expect(generateBtn.textContent).toBe('Generating...');
    expect(generateBtn.disabled).toBe(true);
  });
});

describe('Documentation Generation', () => {
  test('should display loading state when generate button is clicked', () => {
    // Get the docs input and button
    const docsInput = document.getElementById('docs-input');
    const generateBtn = document.getElementById('generate-docs-btn');
    
    // Enter some code
    fireEvent.change(docsInput, { target: { value: 'function factorial(n) { return n <= 1 ? 1 : n * factorial(n-1); }' } });
    
    // Click the generate button
    fireEvent.click(generateBtn);
    
    // Button should show loading state
    expect(generateBtn.textContent).toBe('Generating...');
    expect(generateBtn.disabled).toBe(true);
  });
});

describe('Test Generation', () => {
  test('should display loading state when generate button is clicked', () => {
    // Get the test input and button
    const testInput = document.getElementById('test-input');
    const generateBtn = document.getElementById('generate-tests-btn');
    
    // Enter some code
    fireEvent.change(testInput, { target: { value: 'function factorial(n) { return n <= 1 ? 1 : n * factorial(n-1); }' } });
    
    // Click the generate button
    fireEvent.click(generateBtn);
    
    // Button should show loading state
    expect(generateBtn.textContent).toBe('Generating...');
    expect(generateBtn.disabled).toBe(true);
  });
});

describe('Bug Fixing', () => {
  test('should display loading state when fix button is clicked', () => {
    // Get the bug input, error input, and button
    const bugInput = document.getElementById('bug-input');
    const errorInput = document.getElementById('error-input');
    const fixBtn = document.getElementById('fix-bugs-btn');
    
    // Enter some code and error
    fireEvent.change(bugInput, { target: { value: 'function divide(a, b) { return a / b; }' } });
    fireEvent.change(errorInput, { target: { value: 'Error: Division by zero' } });
    
    // Click the fix button
    fireEvent.click(fixBtn);
    
    // Button should show loading state
    expect(fixBtn.textContent).toBe('Fixing...');
    expect(fixBtn.disabled).toBe(true);
  });
});

describe('Code Optimization', () => {
  test('should display loading state when optimize button is clicked', () => {
    // Get the optimization input and button
    const optimizationInput = document.getElementById('optimization-input');
    const optimizeBtn = document.getElementById('optimize-code-btn');
    
    // Enter some code
    fireEvent.change(optimizationInput, { target: { value: 'function factorial(n) { let result = 1; for(let i = 1; i <= n; i++) { result *= i; } return result; }' } });
    
    // Click the optimize button
    fireEvent.click(optimizeBtn);
    
    // Button should show loading state
    expect(optimizeBtn.textContent).toBe('Optimizing...');
    expect(optimizeBtn.disabled).toBe(true);
  });
});