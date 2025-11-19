"""
Configuration loader for forecasting models
"""
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Load and manage configuration from YAML file"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config.yml file
        """
        if config_path is None:
            # Default path relative to src/models/
            config_path = Path(__file__).parent / 'config.yml'
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    @property
    def forecasting(self) -> Dict[str, Any]:
        """Get forecasting configuration"""
        return self.config.get('forecasting', {})
    
    @property
    def arima(self) -> Dict[str, Any]:
        """Get ARIMA configuration"""
        return self.forecasting.get('statsmodels', {})
    
    @property
    def prophet(self) -> Dict[str, Any]:
        """Get Prophet configuration"""
        return self.forecasting.get('prophet', {})
    
    @property
    def quadrant(self) -> Dict[str, Any]:
        """Get quadrant analysis configuration"""
        return self.config.get('quadrant', {})
    
    @property
    def outputs(self) -> Dict[str, Any]:
        """Get output configuration"""
        return self.config.get('outputs', {})
    
    def __repr__(self):
        return f"Config(config_path='{self.config_path}')"
