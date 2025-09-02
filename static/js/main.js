/**
 * AI-Powered SDLC System - Main JavaScript
 * Handles UI interactions and 3D environment
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the application
    initApp();
    
    // Initialize the 3D environment
    init3DEnvironment();
});

/**
 * Initialize the application UI and event listeners
 */
function initApp() {
    // Initialize UI components
    initUIComponents();
    
    // Initialize event listeners
    initEventListeners();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize the AI model selector
    initAIModelSelector();
    
    console.log('Application initialized');
}

/**
 * Initialize UI components
 */
function initUIComponents() {
    // Show the loading screen
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.classList.remove('hidden');
    }
    
    // Initialize the sidebar navigation
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    sidebarItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove active class from all items
            sidebarItems.forEach(i => i.classList.remove('active'));
            
            // Add active class to clicked item
            item.classList.add('active');
            
            // Get the target section
            const targetId = item.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);
            
            // Hide all sections
            const sections = document.querySelectorAll('.main-section');
            sections.forEach(section => section.classList.add('hidden'));
            
            // Show the target section
            if (targetSection) {
                targetSection.classList.remove('hidden');
            }
        });
    });
    
    // Initialize code editor tabs
    const editorTabs = document.querySelectorAll('.editor-tab');
    editorTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs
            editorTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Get the target editor
            const targetId = tab.getAttribute('data-target');
            const targetEditor = document.getElementById(targetId);
            
            // Hide all editors
            const editors = document.querySelectorAll('.code-editor-content');
            editors.forEach(editor => editor.classList.add('hidden'));
            
            // Show the target editor
            if (targetEditor) {
                targetEditor.classList.remove('hidden');
            }
        });
    });
}

/**
 * Initialize event listeners for UI interactions
 */
function initEventListeners() {
    // Settings button
    const settingsBtn = document.getElementById('settings-button');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.getElementById('close-settings');
    
    if (settingsBtn && settingsModal) {
        settingsBtn.addEventListener('click', () => {
            settingsModal.classList.remove('hidden');
        });
    }
    
    if (closeSettingsBtn && settingsModal) {
        closeSettingsBtn.addEventListener('click', () => {
            settingsModal.classList.add('hidden');
        });
    }
    
    // Click outside to close modals
    window.addEventListener('click', (e) => {
        if (settingsModal && e.target === settingsModal) {
            settingsModal.classList.add('hidden');
        }
    });
    
    // Framework selector
    const languageSelect = document.getElementById('programming-language');
    const frameworkSelect = document.getElementById('framework');
    
    if (languageSelect && frameworkSelect) {
        languageSelect.addEventListener('change', () => {
            updateFrameworkOptions(languageSelect.value);
        });
    }
    
    // Dark mode toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', () => {
            document.documentElement.classList.toggle('light-mode', !darkModeToggle.checked);
            localStorage.setItem('darkMode', darkModeToggle.checked ? 'enabled' : 'disabled');
        });
        
        // Initialize dark mode from localStorage
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'disabled') {
            darkModeToggle.checked = false;
            document.documentElement.classList.add('light-mode');
        }
    }
    
    // 3D toggle
    const enable3DToggle = document.getElementById('enable-3d-toggle');
    if (enable3DToggle) {
        enable3DToggle.addEventListener('change', () => {
            const container = document.getElementById('three-container');
            if (container) {
                container.style.display = enable3DToggle.checked ? 'block' : 'none';
            }
            localStorage.setItem('enable3D', enable3DToggle.checked ? 'enabled' : 'disabled');
        });
        
        // Initialize 3D from localStorage
        const saved3D = localStorage.getItem('enable3D');
        if (saved3D === 'disabled') {
            enable3DToggle.checked = false;
            const container = document.getElementById('three-container');
            if (container) {
                container.style.display = 'none';
            }
        }
    }
    
    // 3D quality selector
    const qualitySelect = document.getElementById('3d-quality');
    if (qualitySelect) {
        qualitySelect.addEventListener('change', () => {
            update3DQuality(qualitySelect.value);
            localStorage.setItem('3dQuality', qualitySelect.value);
        });
        
        // Initialize quality from localStorage
        const savedQuality = localStorage.getItem('3dQuality');
        if (savedQuality) {
            qualitySelect.value = savedQuality;
            update3DQuality(savedQuality);
        }
    }
    
    // Reset settings button
    const resetSettingsBtn = document.getElementById('reset-settings');
    if (resetSettingsBtn) {
        resetSettingsBtn.addEventListener('click', resetSettings);
    }
}

/**
 * Initialize tooltips for UI elements
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');
        
        element.addEventListener('mouseenter', () => {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            
            document.body.appendChild(tooltip);
            
            const rect = element.getBoundingClientRect();
            tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
            
            element.setAttribute('data-tooltip-active', 'true');
        });
        
        element.addEventListener('mouseleave', () => {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                document.body.removeChild(tooltip);
            }
            element.removeAttribute('data-tooltip-active');
        });
    });
}

/**
 * Initialize the AI model selector
 */
function initAIModelSelector() {
    const modelSelector = document.getElementById('ai-model-selector');
    const modelDropdown = document.getElementById('ai-model-dropdown');
    const modelOptions = document.querySelectorAll('#ai-model-dropdown a');
    
    if (modelSelector && modelDropdown && modelOptions.length > 0) {
        console.log('Initializing AI model selector');
        
        // Set default model
        const defaultModel = localStorage.getItem('selectedAIModel') || 'model1';
        modelSelector.setAttribute('data-model', defaultModel);
        
        // Update the selector text
        const selectedOption = document.querySelector(`#ai-model-dropdown a[data-model="${defaultModel}"]`);
        if (selectedOption) {
            const selectedModelName = selectedOption.textContent;
            const selectorText = modelSelector.querySelector('span');
            if (selectorText) {
                selectorText.textContent = `AI Model: ${selectedModelName}`;
            }
        }
        
        // Add click event to model options
        modelOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const model = option.getAttribute('data-model');
                modelSelector.setAttribute('data-model', model);
                
                const selectorText = modelSelector.querySelector('span');
                if (selectorText) {
                    selectorText.textContent = `AI Model: ${option.textContent}`;
                }
                
                // Save selection to localStorage
                localStorage.setItem('selectedAIModel', model);
                
                // Close the dropdown
                modelDropdown.classList.add('hidden');
                console.log('Model selected:', model);
            });
        });
        
        // Toggle dropdown
        modelSelector.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('Model selector clicked, toggling dropdown');
            modelDropdown.classList.toggle('hidden');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (modelSelector && !modelSelector.contains(e.target)) {
                modelDropdown.classList.add('hidden');
            }
        });
    }
}

/**
 * Update framework options based on selected programming language
 */
function updateFrameworkOptions(language) {
    const frameworkSelect = document.getElementById('framework');
    if (!frameworkSelect) return;
    
    // Clear existing options
    frameworkSelect.innerHTML = '<option value="none">None</option>';
    
    // Add language-specific frameworks
    const frameworks = {
        'javascript': ['React', 'Angular', 'Vue', 'Next.js', 'Express'],
        'python': ['Django', 'Flask', 'FastAPI', 'Pyramid', 'Tornado'],
        'java': ['Spring', 'Hibernate', 'Struts', 'JavaFX', 'Micronaut'],
        'csharp': ['.NET Core', 'ASP.NET', 'Xamarin', 'Unity', 'WPF'],
        'go': ['Gin', 'Echo', 'Fiber', 'Buffalo', 'Beego'],
        'ruby': ['Rails', 'Sinatra', 'Hanami', 'Padrino', 'Grape'],
        'php': ['Laravel', 'Symfony', 'CodeIgniter', 'Yii', 'CakePHP'],
        'typescript': ['Angular', 'React', 'Next.js', 'NestJS', 'Express'],
        'swift': ['SwiftUI', 'UIKit', 'Vapor', 'Kitura', 'Perfect'],
        'kotlin': ['Spring Boot', 'Ktor', 'Android SDK', 'Compose', 'Exposed']
    };
    
    if (frameworks[language]) {
        frameworks[language].forEach(framework => {
            const option = document.createElement('option');
            option.value = framework.toLowerCase().replace(/\s+/g, '');
            option.textContent = framework;
            frameworkSelect.appendChild(option);
        });
    }
}

/**
 * Reset settings to default values
 */
function resetSettings() {
    // Reset API keys (just clear the input fields, not the stored keys)
    const apiKeyInputs = document.querySelectorAll('input[id$="-key"]');
    apiKeyInputs.forEach(input => {
        input.value = '';
    });
    
    // Reset dark mode
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.checked = true;
        document.documentElement.classList.remove('light-mode');
        localStorage.setItem('darkMode', 'enabled');
    }
    
    // Reset 3D settings
    const enable3DToggle = document.getElementById('enable-3d-toggle');
    if (enable3DToggle) {
        enable3DToggle.checked = true;
        const container = document.getElementById('three-container');
        if (container) {
            container.style.display = 'block';
        }
        localStorage.setItem('enable3D', 'enabled');
    }
    
    // Reset 3D quality
    const qualitySelect = document.getElementById('3d-quality');
    if (qualitySelect) {
        qualitySelect.value = 'medium';
        update3DQuality('medium');
        localStorage.setItem('3dQuality', 'medium');
    }
    
    // Show confirmation message
    const settingsModal = document.getElementById('settings-modal');
    if (settingsModal) {
        const message = document.createElement('div');
        message.className = 'bg-green-500 text-white px-4 py-2 rounded-lg mb-4 flex items-center justify-between';
        message.innerHTML = `
            <span>Settings reset to default values</span>
            <button class="text-white hover:text-gray-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
            </button>
        `;
        
        const container = settingsModal.querySelector('.p-6');
        container.insertBefore(message, container.firstChild);
        
        // Remove the message after 3 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 3000);
        
        // Add click event to close button
        message.querySelector('button').addEventListener('click', () => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        });
    }
}

// ===== 3D Environment =====

let scene, camera, renderer, controls;
let particles, particleSystem;
let raycaster, mouse;
let clock;

/**
 * Initialize the 3D environment
 */
function init3DEnvironment() {
    // Create container for Three.js scene
    const container = document.createElement('div');
    container.id = 'three-container';
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.zIndex = '-1';
    container.style.pointerEvents = 'none';
    document.body.appendChild(container);
    
    // Check if 3D is enabled in settings
    const enable3D = localStorage.getItem('enable3D');
    if (enable3D === 'disabled') {
        container.style.display = 'none';
        return;
    }
    
    // Initialize Three.js scene
    scene = new THREE.Scene();
    
    // Initialize camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 30;
    
    // Initialize renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);
    
    // Initialize controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = false;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.5;
    
    // Initialize raycaster for interaction
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    
    // Initialize clock for animations
    clock = new THREE.Clock();
    
    // Create particle system
    createParticleSystem();
    
    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
    
    // Start animation loop
    animate();
    
    // Set quality based on settings
    const quality = localStorage.getItem('3dQuality') || 'medium';
    update3DQuality(quality);
}

/**
 * Create particle system for background effect
 */
function createParticleSystem() {
    const particleCount = 1000;
    const particleGeometry = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleSizes = new Float32Array(particleCount);
    const particleColors = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
        // Position
        const i3 = i * 3;
        particlePositions[i3] = (Math.random() - 0.5) * 100;
        particlePositions[i3 + 1] = (Math.random() - 0.5) * 100;
        particlePositions[i3 + 2] = (Math.random() - 0.5) * 100;
        
        // Size
        particleSizes[i] = Math.random() * 2 + 0.5;
        
        // Color
        const color = new THREE.Color();
        color.setHSL(Math.random() * 0.2 + 0.5, 0.7, 0.5); // Blue-ish colors
        particleColors[i3] = color.r;
        particleColors[i3 + 1] = color.g;
        particleColors[i3 + 2] = color.b;
    }
    
    particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeometry.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
    
    // Particle material
    const particleMaterial = new THREE.ShaderMaterial({
        uniforms: {
            time: { value: 0.0 },
            pointTexture: { value: new THREE.TextureLoader().load('static/images/particle.svg') }
        },
        vertexShader: `
            attribute float size;
            attribute vec3 color;
            varying vec3 vColor;
            uniform float time;
            
            void main() {
                vColor = color;
                vec3 pos = position;
                pos.y += sin(time * 0.2 + position.x * 0.05) * 0.5;
                pos.x += cos(time * 0.2 + position.y * 0.05) * 0.5;
                
                vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
                gl_PointSize = size * (300.0 / -mvPosition.z);
                gl_Position = projectionMatrix * mvPosition;
            }
        `,
        fragmentShader: `
            uniform sampler2D pointTexture;
            varying vec3 vColor;
            
            void main() {
                gl_FragColor = vec4(vColor, 1.0) * texture2D(pointTexture, gl_PointCoord);
            }
        `,
        blending: THREE.AdditiveBlending,
        depthTest: false,
        transparent: true
    });
    
    // Create particle system
    particleSystem = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particleSystem);
    
    // Store particles for animation
    particles = {
        positions: particlePositions,
        sizes: particleSizes,
        colors: particleColors,
        geometry: particleGeometry,
        material: particleMaterial
    };
}

/**
 * Handle window resize
 */
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

/**
 * Animation loop
 */
function animate() {
    requestAnimationFrame(animate);
    
    // Update controls
    controls.update();
    
    // Update particle system
    if (particleSystem) {
        const time = clock.getElapsedTime();
        particleSystem.material.uniforms.time.value = time;
        
        // Slowly rotate the particle system
        particleSystem.rotation.y = time * 0.05;
    }
    
    // Render scene
    renderer.render(scene, camera);
}

/**
 * Update 3D quality settings
 */
function update3DQuality(quality) {
    if (!renderer) return;
    
    switch (quality) {
        case 'high':
            renderer.setPixelRatio(window.devicePixelRatio);
            if (particleSystem) {
                // Increase particle count for high quality
                scene.remove(particleSystem);
                createParticleSystem(2000);
            }
            break;
        case 'medium':
            renderer.setPixelRatio(window.devicePixelRatio);
            // Default particle count
            break;
        case 'low':
            renderer.setPixelRatio(1);
            if (particleSystem) {
                // Decrease particle count for low quality
                scene.remove(particleSystem);
                createParticleSystem(500);
            }
            break;
    }
}