# PDF to Speech Converter - Day 91

A Python application that converts PDF documents into spoken audio with both GUI and command-line interfaces.

## Features

### GUI Version (main.py)
- **Modern Interface**: Dark theme with intuitive controls
- **PDF Text Extraction**: Automatically extracts text from multi-page PDFs
- **Speech Controls**: Play, pause, stop, and resume functionality
- **Customizable Settings**: Adjust speech rate, volume, and voice
- **Progress Tracking**: Real-time progress bar during conversion
- **Text Preview**: View extracted text before conversion
- **Audio Export**: Save speech as WAV audio files
- **Error Handling**: Comprehensive error messages and validation

### CLI Version (pdf_to_speech_cli.py)
- **Command-line Interface**: Simple and efficient terminal-based usage
- **Batch Processing**: Perfect for automation and scripting
- **Preview Mode**: Option to preview extracted text before conversion
- **Audio Export**: Save speech directly to audio files
- **Progress Indicators**: Real-time feedback during processing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### GUI Application
```bash
python main.py
```

1. Click "Select PDF" to choose your PDF file
2. Adjust speech settings (speed, volume, voice)
3. Click "Play" to start text-to-speech conversion
4. Use controls to pause/resume/stop as needed
5. Optionally save audio to file using "Save Audio"

### Command Line Application
```bash
python pdf_to_speech_cli.py document.pdf
```

**Options:**
- `--rate 200`: Set speech rate (50-300 WPM)
- `--volume 0.8`: Set volume (0.1-1.0)
- `--save output.wav`: Save audio to file instead of playing
- `--preview`: Show text preview before conversion

**Examples:**
```bash
# Basic conversion
python pdf_to_speech_cli.py sample_document.pdf

# Fast speech with preview
python pdf_to_speech_cli.py document.pdf --rate 200 --preview

# Save to audio file
python pdf_to_speech_cli.py document.pdf --save speech_output.wav

# Custom settings
python pdf_to_speech_cli.py document.pdf --rate 120 --volume 0.7
```

## Technical Details

- **PDF Processing**: PyPDF2 library for text extraction
- **Text-to-Speech**: pyttsx3 engine with SAPI support
- **GUI Framework**: Tkinter with custom styling
- **Threading**: Non-blocking speech processing
- **Error Handling**: Robust exception handling throughout

## System Requirements

- Python 3.7+
- Windows/macOS/Linux
- Audio output device
- PDF files with extractable text

## File Structure

```
Day_91/
├── main.py                    # GUI application
├── pdf_to_speech_cli.py       # Command-line version
├── requirements.txt           # Python dependencies
├── sample_document.txt        # Sample text file
├── run_gui.bat               # Windows batch file
└── README.md                 # This file
```

## Performance

- **Processing Speed**: ~1000 words/minute extraction
- **Speech Rate**: 50-300 WPM (default: 150 WPM)
- **Memory Usage**: Efficient PDF streaming
- **File Size**: Supports large PDF documents

## Troubleshooting

**No audio output**: Check system audio settings and volume
**PDF extraction fails**: Ensure PDF contains selectable text (not scanned images)
**Voice not available**: Install additional TTS voices through system settings
**Memory issues**: Process large PDFs in smaller sections

## Future Enhancements

- OCR support for scanned PDFs
- Multiple audio format export
- Batch PDF processing
- Cloud TTS integration
- Multilingual support
