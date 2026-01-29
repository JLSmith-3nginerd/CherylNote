#!/bin/bash

# Final packaging script for audio notes processor with embedded models
echo "=== FINAL PACKAGING SCRIPT ==="

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.spec __pycache__/ .pytest_cache/
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Create the executable with embedded models and proper structure
echo "Creating executable with all models embedded..."

# Make sure we have the correct directory structure for packaging
mkdir -p dist_temp/src

# Copy all source files and models to temp directory  
echo "Copying project files..."
cp -r src/* dist_temp/src/
cp main.py dist_temp/
cp requirements.txt dist_temp/

# Create a proper run script that handles imports correctly
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

# Create the final executable with proper data inclusion
echo "Building executable with PyInstaller..."

pyinstaller \
    --onefile \
    --windowed \
    --name="AudioNotesProcessor" \
    --add-data="models:models" \
    --add-data="assets:assets" \
    --clean \
    dist_temp/run_app.py

echo ""
echo "=== PACKAGING COMPLETE ==="
echo "Your executable is now ready in dist/AudioNotesProcessor"
echo ""
echo "To test the executable:"
echo "1. Navigate to dist/"
echo "2. Run ./AudioNotesProcessor (on macOS)"
echo ""
echo "Features of your executable:"
echo "- All models embedded in the executable"
echo "- No internet required for operation"  
echo "- Self-contained application"