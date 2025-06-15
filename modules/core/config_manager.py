import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration and settings"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.decoder.JSONDecodeError, OSError) as e:
                print(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration settings"""
        return {
            "ui": {
                "theme": "default",
                "window_size": [1024, 768],
                "window_position": [100, 100],
                "remember_window_state": True
            },
            "prompt": {
                "default_mode": "SFW",
                "separator": ", ",
                "auto_generate": True,
                "max_prompt_length": 1000
            },
            "templates": {
                "auto_save_drafts": True,
                "max_recent_templates": 10,
                "default_export_format": "json"
            },
            "categories": {
                "show_descriptions": True,
                "enable_custom_options": True,
                "default_weights": True
            }
        }
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except (OSError, json.decoder.JSONDecodeError) as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'ui.theme')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
                
        return value
    
    def set(self, key_path: str, value: Any) -> bool:
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config_ref = self.config
        
        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        config_ref[keys[-1]] = value
        return self.save_config()
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values"""
        self.config = self.get_default_config()
        return self.save_config()
    
    def get_window_geometry(self) -> Dict[str, Any]:
        """Get window geometry settings"""
        return {
            "size": self.get("ui.window_size", [1024, 768]),
            "position": self.get("ui.window_position", [100, 100])
        }
    
    def set_window_geometry(self, width: int, height: int, x: int, y: int):
        """Save window geometry settings"""
        self.set("ui.window_size", [width, height])
        self.set("ui.window_position", [x, y])
