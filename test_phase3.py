#!/usr/bin/env python3
"""
Test script to verify the audio notes processor components work correctly.
This script tests that all modules can be imported and instantiated properly.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_components():
    """Test that all components can be imported and instantiated"""
    
    print("Testing component imports...")
    
    # Test audio processor
    try:
        from audio_processor import AudioProcessor
        ap = AudioProcessor()
        print("✓ AudioProcessor imported and instantiated successfully")
    except Exception as e:
        print(f"✗ AudioProcessor failed: {e}")
        return False
    
    # Test diarization manager
    try:
        from diarization_manager import DiarizationManager
        dm = DiarizationManager()
        print("✓ DiarizationManager imported and instantiated successfully")
    except Exception as e:
        print(f"✗ DiarizationManager failed: {e}")
        return False
    
    # Test transcription manager
    try:
        from transcription_manager import TranscriptionManager
        tm = TranscriptionManager()
        print("✓ TranscriptionManager imported and instantiated successfully")
    except Exception as e:
        print(f"✗ TranscriptionManager failed: {e}")
        return False
    
    # Test note generator
    try:
        from note_generator import NoteGenerator
        ng = NoteGenerator()
        print("✓ NoteGenerator imported and instantiated successfully")
    except Exception as e:
        print(f"✗ NoteGenerator failed: {e}")
        return False
    
    # Test content classifier
    try:
        from content_classifier import ContentClassifierSimple
        cc = ContentClassifierSimple()
        print("✓ ContentClassifierSimple imported and instantiated successfully")
    except Exception as e:
        print(f"✗ ContentClassifierSimple failed: {e}")
        return False
    
    # Test GUI (basic import)
    try:
        from gui_app import AudioNotesGUI
        print("✓ GUI imported successfully")
    except Exception as e:
        print(f"✗ GUI failed: {e}")
        return False
    
    print("\nAll components imported and instantiated successfully!")
    return True

def test_functionality():
    """Test basic functionality of components"""
    
    print("\nTesting component functionality...")
    
    try:
        from audio_processor import AudioProcessor
        ap = AudioProcessor()
        
        # Test supported formats
        print("✓ Supported formats:", ap.supported_formats)
        
        from note_generator import NoteGenerator
        ng = NoteGenerator()
        
        # Test basic note generation (mock data)
        mock_transcription = [
            {"start": 0.0, "end": 5.0, "text": "This is a test transcription."}
        ]
        
        notes = ng.generate_notes(mock_transcription, "meeting")
        print("✓ Note generation works")
        
        from content_classifier import ContentClassifierSimple
        cc = ContentClassifierSimple()
        content_type = cc.classify_content(mock_transcription)
        print("✓ Content classification works:", content_type)
        
        print("\nAll functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    success1 = test_components()
    success2 = test_functionality()
    
    if not (success1 and success2):
        sys.exit(1)
        
    print("\n🎉 All tests passed! The implementation is ready for Phase 3.")