# src/model_utils.py - Utility functions for handling embedded models

import os
import sys
from pathlib import Path


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    This helps find models when running from embedded executable
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def is_running_from_executable():
    """
    Check if the application is running from a PyInstaller executable
    """
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def get_model_path(model_name):
    """
    Get the path to a model file, checking both embedded and local locations
    """
    # First check if we're running from executable
    if is_running_from_executable():
        # Look for model in embedded resources
        embedded_path = get_resource_path(os.path.join("models", model_name))
        if os.path.exists(embedded_path):
            return embedded_path
    
    # Fall back to local path
    local_path = os.path.join("models", model_name)
    if os.path.exists(local_path):
        return local_path
        
    # If not found anywhere, return None
    return None


def setup_model_paths():
    """
    Configure paths for models when running from executable
    """
    if is_running_from_executable():
        # In PyInstaller, we need to handle model paths properly
        print("Running from executable - using embedded models")
        
        # Add the models directory to Python path for imports
        models_path = get_resource_path("models")
        if os.path.exists(models_path):
            sys.path.insert(0, models_path)
            
    else:
        print("Running from source - using local models")