import os
import json
import shutil
import zipfile
from datetime import datetime

class Deployment:
    """
    Handles deployment operations for the AI-powered SDLC system.
    Supports local deployment, packaging, and configuration management.
    """
    
    def __init__(self, base_dir="."):
        self.base_dir = os.path.abspath(base_dir)
        self.static_dir = os.path.join(self.base_dir, "static")
        self.backend_dir = os.path.join(self.base_dir, "backend")
        self.config_file = os.path.join(self.base_dir, "config.json")
        self.default_config = {
            "version": "1.0.0",
            "environment": "development",
            "api_timeout": 30,
            "max_tokens": 4096,
            "models": {
                "deepseek": {"enabled": True, "priority": 1},
                "gemini": {"enabled": True, "priority": 2},
                "chatgpt": {"enabled": True, "priority": 3},
                "grok": {"enabled": True, "priority": 4},
                "claude": {"enabled": True, "priority": 5}
            }
        }
        
        # Ensure config file exists
        if not os.path.exists(self.config_file):
            self._create_default_config()
    
    def _create_default_config(self):
        """
        Creates a default configuration file if none exists.
        """
        with open(self.config_file, 'w') as f:
            json.dump(self.default_config, f, indent=4)
        print(f"Created default configuration at {self.config_file}")
    
    def load_config(self):
        """
        Loads the current configuration.
        """
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            return self.default_config
    
    def save_config(self, config):
        """
        Saves the provided configuration.
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
            return False
    
    def update_config(self, key, value):
        """
        Updates a specific configuration value.
        """
        config = self.load_config()
        
        # Handle nested keys (e.g., "models.deepseek.enabled")
        if '.' in key:
            parts = key.split('.')
            current = config
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    current[part] = value
                else:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
        else:
            config[key] = value
        
        return self.save_config(config)
    
    def create_backup(self):
        """
        Creates a backup of the entire application.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.base_dir, "backups")
        backup_file = os.path.join(backup_dir, f"ai_sdlc_backup_{timestamp}.zip")
        
        # Create backups directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        try:
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add index.html
                index_path = os.path.join(self.base_dir, "index.html")
                if os.path.exists(index_path):
                    zipf.write(index_path, os.path.relpath(index_path, self.base_dir))
                
                # Add config.json
                if os.path.exists(self.config_file):
                    zipf.write(self.config_file, os.path.relpath(self.config_file, self.base_dir))
                
                # Add static files
                for root, _, files in os.walk(self.static_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, self.base_dir))
                
                # Add backend files
                for root, _, files in os.walk(self.backend_dir):
                    for file in files:
                        if file.endswith(".py"):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, self.base_dir))
            
            print(f"Backup created at {backup_file}")
            return backup_file
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return None
    
    def restore_from_backup(self, backup_file):
        """
        Restores the application from a backup file.
        """
        if not os.path.exists(backup_file):
            print(f"Backup file not found: {backup_file}")
            return False
        
        try:
            # Create a temporary directory for extraction
            temp_dir = os.path.join(self.base_dir, "temp_restore")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # Extract backup to temporary directory
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Copy files to their respective locations
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, temp_dir)
                    dest_path = os.path.join(self.base_dir, rel_path)
                    
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(src_path, dest_path)
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            
            print(f"Application restored from {backup_file}")
            return True
        except Exception as e:
            print(f"Error restoring from backup: {str(e)}")
            return False
    
    def prepare_deployment_package(self, target_env="production"):
        """
        Prepares a deployment package for the specified environment.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_dir = os.path.join(self.base_dir, "packages")
        package_file = os.path.join(package_dir, f"ai_sdlc_{target_env}_{timestamp}.zip")
        
        # Create packages directory if it doesn't exist
        if not os.path.exists(package_dir):
            os.makedirs(package_dir)
        
        try:
            # Create a modified config for the target environment
            config = self.load_config()
            config["environment"] = target_env
            
            # Adjust settings based on environment
            if target_env == "production":
                config["debug"] = False
                config["api_timeout"] = 60  # Longer timeout for production
            elif target_env == "staging":
                config["debug"] = True
                config["api_timeout"] = 45  # Medium timeout for staging
            
            # Create the deployment package
            with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add index.html
                index_path = os.path.join(self.base_dir, "index.html")
                if os.path.exists(index_path):
                    zipf.write(index_path, os.path.relpath(index_path, self.base_dir))
                
                # Add modified config.json
                temp_config = os.path.join(self.base_dir, "temp_config.json")
                with open(temp_config, 'w') as f:
                    json.dump(config, f, indent=4)
                zipf.write(temp_config, "config.json")
                os.remove(temp_config)  # Clean up temporary config
                
                # Add static files
                for root, _, files in os.walk(self.static_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, self.base_dir))
                
                # Add backend files
                for root, _, files in os.walk(self.backend_dir):
                    for file in files:
                        if file.endswith(".py"):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, self.base_dir))
                
                # Add README.md if it exists
                readme_path = os.path.join(self.base_dir, "README.md")
                if os.path.exists(readme_path):
                    zipf.write(readme_path, os.path.relpath(readme_path, self.base_dir))
                
                # Add deployment instructions
                deploy_instructions = f"""# Deployment Instructions for {target_env.capitalize()} Environment

1. Extract this package to your server directory
2. Ensure Python 3.8+ is installed
3. Install required packages: `pip install -r requirements.txt`
4. Configure your API keys in the settings panel
5. For production, consider setting up a proper web server like Nginx or Apache

Deployment package created on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
                zipf.writestr("DEPLOY.md", deploy_instructions)
                
                # Add requirements.txt
                requirements = """pyscript>=0.1.5
numpy>=1.20.0
requests>=2.25.1
pydantic>=1.8.2
"""
                zipf.writestr("requirements.txt", requirements)
            
            print(f"Deployment package created at {package_file}")
            return package_file
        except Exception as e:
            print(f"Error creating deployment package: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    deployer = Deployment()
    
    # Create a backup
    backup_file = deployer.create_backup()
    
    # Prepare a deployment package for production
    package_file = deployer.prepare_deployment_package("production")
    
    # Update configuration
    deployer.update_config("models.deepseek.priority", 2)
    deployer.update_config("models.gemini.priority", 1)