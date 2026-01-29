import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Setup model paths if running from executable
try:
    from src.model_utils import setup_model_paths
    setup_model_paths()
except Exception as e:
    print(f"Warning: Could not set up model paths: {e}")

from gui_app import AudioNotesGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioNotesGUI(root)
    root.mainloop()