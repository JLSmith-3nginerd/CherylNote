# Audio Notes Processor

A Python application that processes audio files to identify speakers, transcribe audio into text, and generate structured notes based on content type.

## Features

- **Speaker Diarization**: Identify different speakers in audio recordings
- **Audio Transcription**: Convert speech to text using Whisper
- **Content Classification**: Automatically detect content type (meeting, lecture, etc.)
- **Custom Notes Generation**: Generate structured notes based on content type
- **Speaker Naming**: Assign custom names to speakers
- **Multiple Output Formats**: Support for text, markdown, and PDF output

## Project Structure

```
audio-notes-processor/
├── src/
│   ├── __init__.py
│   ├── audio_processor.py        # Audio file handling and preprocessing
│   ├── diarization_manager.py    # Speaker diarization functionality  
│   ├── transcription_manager.py  # Audio transcription with Whisper
│   ├── note_generator.py         # Generate structured notes
│   ├── content_classifier.py     # Classify content type
│   └── gui_app.py                # Main GUI application
├── models/
│   └── diarization_model.pth     # Speaker diarization model
├── assets/
│   └── icon.ico                  # Application icon
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup script
└── main.py                       # Entry point for the GUI application
```

## Requirements

- Python 3.7+
- PyTorch
- librosa
- soundfile
- pyannote.audio
- openai-whisper
- tkinter (usually included with Python)

## Installation

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

1. Select an audio file (MP3, WAV, AAC, M4A, MP4, MOV)
2. Optionally assign names to speakers
3. Select output format (text/markdown/PDF)
4. Click "Process Audio" to start
5. View results in the tabs

## Development Status

**Phase 2: Core Features**
- [x] GUI framework with file selection
- [x] Audio processing and conversion  
- [x] Speaker diarization integration (mock implementation)
- [x] Whisper transcription functionality
- [x] Content classifier for note customization
- [x] Speaker naming feature
- [x] Multiple output format support

## Architecture Notes

The application follows a modular design with clear separation of concerns:

- **AudioProcessor**: Handles audio file preparation and conversion
- **DiarizationManager**: Manages speaker identification 
- **TranscriptionManager**: Handles audio transcription
- **NoteGenerator**: Creates structured notes from transcriptions
- **ContentClassifier**: Determines content type for note formatting
- **GUI Application**: User interface and workflow coordination

## Cross-Platform Compatibility

The application is designed to run on:
- Windows, macOS, Linux desktops
- Raspberry Pi 5 (with appropriate performance considerations)
- iOS devices (via Swift reimplementation)

## Future Enhancements

1. **Model Optimization**: Implement quantization for better Raspberry Pi performance
2. **Advanced Speaker Recognition**: Add voice sample analysis and automatic speaker matching
3. **Cloud Integration**: Optional cloud processing for heavy workloads  
4. **Mobile App**: Native iOS app with Swift backend
5. **Multi-language Support**: Extend to support multiple languages

## License

MIT License