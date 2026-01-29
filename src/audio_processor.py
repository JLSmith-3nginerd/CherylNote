# src/audio_processor.py - Audio file handling with ffmpeg support

import os
import tempfile
from pathlib import Path
import sys

# Add src to path for imports  
sys.path.insert(0, os.path.dirname(__file__))

from model_utils import is_running_from_executable

class AudioProcessor:
    def __init__(self):
        self.supported_formats = ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.mov', '.mp4']
        
        # Check if we're running from executable and handle ffmpeg appropriately
        if is_running_from_executable():
            # For PyInstaller, we'll need to ensure ffmpeg is available
            self._setup_ffmpeg_for_executable()
    
    def _setup_ffmpeg_for_executable(self):
        """Setup ffmpeg for executable environment"""
        try:
            # When running from PyInstaller, we need to make sure ffmpeg is accessible
            import subprocess
            
            # Try to find or extract ffmpeg
            try:
                # Check if ffmpeg is available in PATH
                subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # If not available, we'll need to handle this appropriately
                print("ffmpeg not found in PATH - transcription may have issues")
                
        except Exception as e:
            print(f"Warning: Could not setup ffmpeg for executable: {e}")
    
    def prepare_file(self, file_path):
        """Prepare audio file for processing (handle video files)"""
        path = Path(file_path)
        
        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {file_path} does not exist")
            
        # Check file extension
        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {path.suffix}")
            
        return str(path)
    
    def convert_to_wav(self, input_file):
        """Convert any audio file to WAV format for processing"""
        # In a real implementation, you would use librosa or ffmpeg
        try:
            # For now, just return the original file path (mock implementation)
            print(f"Converting {input_file} to WAV format...")
            return input_file
        except Exception as e:
            print(f"Error converting file to WAV: {e}")
            return input_file
    
    def get_audio_info(self, file_path):
        """Get basic info about audio file"""
        try:
            # In a real implementation, this would use librosa
            # For now, we'll return mock data 
            print(f"Getting audio info for {file_path}...")
            
            # Mock return values
            return {
                'duration': 300.0,  # 5 minutes mock duration
                'sample_rate': 44100,
                'channels': 2
            }
        except Exception as e:
            raise RuntimeError(f"Error reading audio file: {str(e)}")