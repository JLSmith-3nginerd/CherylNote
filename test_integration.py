#!/usr/bin/env python3
"""
Integration test to verify all AI models can be loaded and used.
"""

import sys
import os

# Add src directory to path for imports  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_model_integration():
    """Test that all components can load their required models"""
    
    print("Testing AI model integration...")
    
    # Test audio processor
    try:
        from audio_processor import AudioProcessor
        ap = AudioProcessor()
        print("✓ AudioProcessor loaded successfully")
    except Exception as e:
        print(f"✗ AudioProcessor failed: {e}")
        return False
    
    # Test diarization manager (this will try to load the model)
    try:
        from diarization_manager import DiarizationManager
        dm = DiarizationManager()
        print("✓ DiarizationManager loaded successfully")
    except Exception as e:
        print(f"✗ DiarizationManager failed: {e}")
        return False
    
    # Test transcription manager (this will try to load the model)
    try:
        from transcription_manager import TranscriptionManager
        tm = TranscriptionManager()
        print("✓ TranscriptionManager loaded successfully")
    except Exception as e:
        print(f"✗ TranscriptionManager failed: {e}")
        return False
    
    # Test note generator (this will try to load the model)
    try:
        from note_generator import NoteGenerator
        ng = NoteGenerator()
        print("✓ NoteGenerator loaded successfully")
    except Exception as e:
        print(f"✗ NoteGenerator failed: {e}")
        return False
    
    # Test content classifier
    try:
        from content_classifier import ContentClassifierSimple
        cc = ContentClassifierSimple()
        print("✓ ContentClassifierSimple loaded successfully")
    except Exception as e:
        print(f"✗ ContentClassifierSimple failed: {e}")
        return False
    
    # Test that we can at least import the required libraries
    try:
        import whisper
        print("✓ Whisper library imported successfully")
        
        from pyannote.audio import Pipeline
        print("✓ Pyannote audio library imported successfully")
        
        from transformers import pipeline
        print("✓ Transformers library imported successfully")
        
    except Exception as e:
        print(f"✗ Required libraries failed to import: {e}")
        return False
    
    # Test basic functionality
    try:
        # Test content classification with mock data  
        cc = ContentClassifierSimple()
        mock_transcription = [
            {"start": 0.0, "end": 5.0, "text": "This is a test meeting with agenda items and action items."}
        ]
        
        content_type = cc.classify_content(mock_transcription)
        print(f"✓ Content classification works: {content_type}")
        
        # Test note generation
        ng = NoteGenerator()
        notes = ng.generate_notes(mock_transcription, "meeting")
        print("✓ Note generation works")
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False
    
    print("\n🎉 All components successfully integrated with AI models!")
    print("The application is ready for real model processing.")
    
    return True

if __name__ == "__main__":
    success = test_model_integration()
    if not success:
        print("\n❌ Some components failed integration")
        sys.exit(1)
    else:
        print("\n✅ All model integrations successful!")