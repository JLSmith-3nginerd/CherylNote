#!/bin/bash

# Packaging script for audio notes processor
# This creates an executable with embedded models

echo "Creating executable with embedded models..."

# Create a temporary directory for packaging
mkdir -p dist_temp

# Copy all necessary files to temp directory
cp -r src/ dist_temp/
cp main.py dist_temp/
cp requirements.txt dist_temp/
cp -r models/ dist_temp/
cp -r assets/ dist_temp/

# Create a simple script to test the packaging
cat > dist_temp/run_app.py << 'EOF'
import sys
import os

# Add src to path for imports  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the GUI
from gui_app import AudioNotesGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioNotesGUI(root)
    root.mainloop()
EOF

# Create the executable with embedded models using PyInstaller
echo "Building executable with PyInstaller..."

pyinstaller \
    --onefile \
    --windowed \
    --name="AudioNotesProcessor" \
    --add-data="models:models" \
    --add-data="assets:assets" \
    --icon=assets/icon.ico \
    dist_temp/run_app.py

echo "Executable created in dist/AudioNotesProcessor"
echo ""
echo "To test:"
echo "1. Navigate to dist/"
echo "2. Run ./AudioNotesProcessor"
echo ""
echo "Note: The executable will include all models and dependencies."