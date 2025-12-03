"""Configuration loading utilities"""
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Handles loading and merging configuration files"""
    
    @staticmethod
    def load_config(config_path: str = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path (str): Path to config YAML file. If None, loads default config.
            
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        if config_path is None:
            # Load default config
            config_path = Path(__file__).parent.parent.parent / 'config' / 'default_config.yaml'
        
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config if config is not None else {}
