import PyPDF2
import pyttsx3
import argparse
import sys
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"Processing {len(pdf_reader.pages)} pages...")
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                print(f"Processed page {page_num + 1}/{len(pdf_reader.pages)}")
            
            return text.strip()
    
    except FileNotFoundError:
        print(f"Error: File '{pdf_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def text_to_speech(text, rate=150, volume=0.9, save_path=None):
    """Convert text to speech."""
    try:
        engine = pyttsx3.init()
        
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        voices = engine.getProperty('voices')
        if voices:
            print(f"Using voice: {voices[0].name if hasattr(voices[0], 'name') else voices[0].id}")
        
        if save_path:
            print(f"Saving audio to: {save_path}")
            engine.save_to_file(text, save_path)
            engine.runAndWait()
            print("Audio file saved successfully!")
        else:
            print("Starting text-to-speech conversion...")
            print("Press Ctrl+C to stop")
            
            sentences = text.split('.')
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    print(f"Speaking sentence {i+1}/{len(sentences)}: {sentence[:50]}...")
                    engine.say(sentence.strip() + '.')
                    engine.runAndWait()
            
            print("Speech conversion completed!")
    
    except KeyboardInterrupt:
        print("\nSpeech stopped by user.")
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Speech")
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("--rate", type=int, default=150, help="Speech rate (50-300, default: 150)")
    parser.add_argument("--volume", type=float, default=0.9, help="Volume (0.1-1.0, default: 0.9)")
    parser.add_argument("--save", help="Save audio to file instead of playing")
    parser.add_argument("--preview", action="store_true", help="Show extracted text preview")
    
    args = parser.parse_args()
    
    if not Path(args.pdf_file).exists():
        print(f"Error: File '{args.pdf_file}' does not exist.")
        sys.exit(1)
    
    print(f"Extracting text from: {args.pdf_file}")
    text = extract_text_from_pdf(args.pdf_file)
    
    if not text:
        print("No text could be extracted from the PDF.")
        sys.exit(1)
    
    print(f"Extracted {len(text)} characters from PDF")
    word_count = len(text.split())
    print(f"Word count: {word_count}")
    estimated_time = word_count / (args.rate / 60)
    print(f"Estimated speech time: {estimated_time:.1f} minutes")
    
    if args.preview:
        print("\n" + "="*50)
        print("TEXT PREVIEW:")
        print("="*50)
        print(text[:500] + "..." if len(text) > 500 else text)
        print("="*50)
        
        response = input("\nProceed with text-to-speech? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled by user.")
            sys.exit(0)
    
    text_to_speech(text, args.rate, args.volume, args.save)

if __name__ == "__main__":
    main()
