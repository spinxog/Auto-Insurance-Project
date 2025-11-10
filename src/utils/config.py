"""Configuration management."""

import os
import yaml
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration based on CONFIG_ENV."""
    env = os.getenv('CONFIG_ENV', 'local')
    config_file = f'config/{env}.yml'

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # Override with environment variables
    for key in config:
        env_var = key.upper()
        if env_var in os.environ:
            config[key] = os.environ[env_var]

    return config

def get_config() -> Dict[str, Any]:
    """Get the global configuration."""
    return CONFIG

# Global config
CONFIG = load_config()
