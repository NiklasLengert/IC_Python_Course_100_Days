import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import pyttsx3
import threading
import os
from pathlib import Path

class PDFToSpeechConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF to Speech Converter")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.is_paused = False
        self.current_text = ""
        self.current_sentence_index = 0
        self.sentences = []
        self.speech_thread = None
        
        self.setup_ui()
        self.setup_speech_engine()
        
    def setup_speech_engine(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        if voices:
            self.engine.setProperty('voice', voices[0].id)
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="PDF to Speech Converter", 
                              font=('Arial', 24, 'bold'), 
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        file_frame = tk.Frame(main_frame, bg='#2c3e50')
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file_label = tk.Label(file_frame, text="No PDF file selected", 
                                  font=('Arial', 12), 
                                  fg='#bdc3c7', bg='#2c3e50')
        self.file_label.pack(side=tk.LEFT, padx=(0, 20))
        
        select_btn = tk.Button(file_frame, text="Select PDF", 
                              command=self.select_pdf,
                              font=('Arial', 12, 'bold'),
                              bg='#3498db', fg='white',
                              relief=tk.FLAT, padx=20, pady=10)
        select_btn.pack(side=tk.RIGHT)
        
        settings_frame = tk.LabelFrame(main_frame, text="Speech Settings", 
                                     font=('Arial', 14, 'bold'),
                                     fg='#ecf0f1', bg='#2c3e50')
        settings_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        speed_frame = tk.Frame(settings_frame, bg='#2c3e50')
        speed_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(speed_frame, text="Speed:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#2c3e50').pack(side=tk.LEFT)
        
        self.speed_var = tk.IntVar(value=150)
        self.speed_scale = tk.Scale(speed_frame, from_=50, to=300, 
                                   orient=tk.HORIZONTAL, variable=self.speed_var,
                                   command=self.update_speed,
                                   bg='#34495e', fg='#ecf0f1', 
                                   highlightbackground='#2c3e50')
        self.speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        volume_frame = tk.Frame(settings_frame, bg='#2c3e50')
        volume_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(volume_frame, text="Volume:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#2c3e50').pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=0.9)
        self.volume_scale = tk.Scale(volume_frame, from_=0.1, to=1.0, 
                                    orient=tk.HORIZONTAL, variable=self.volume_var,
                                    resolution=0.1, command=self.update_volume,
                                    bg='#34495e', fg='#ecf0f1', 
                                    highlightbackground='#2c3e50')
        self.volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        voice_frame = tk.Frame(settings_frame, bg='#2c3e50')
        voice_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(voice_frame, text="Voice:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#2c3e50').pack(side=tk.LEFT)
        
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(voice_frame, textvariable=self.voice_var,
                                       state="readonly")
        self.voice_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.voice_combo.bind('<<ComboboxSelected>>', self.update_voice)
        
        self.populate_voices()
        
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.play_btn = tk.Button(control_frame, text="▶ Play", 
                                 command=self.toggle_speech,
                                 font=('Arial', 14, 'bold'),
                                 bg='#27ae60', fg='white',
                                 relief=tk.FLAT, padx=30, pady=15,
                                 state=tk.DISABLED)
        self.play_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(control_frame, text="⏹ Stop", 
                                 command=self.stop_speech,
                                 font=('Arial', 14, 'bold'),
                                 bg='#e74c3c', fg='white',
                                 relief=tk.FLAT, padx=30, pady=15,
                                 state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = tk.Button(control_frame, text="💾 Save Audio", 
                                 command=self.save_audio,
                                 font=('Arial', 14, 'bold'),
                                 bg='#9b59b6', fg='white',
                                 relief=tk.FLAT, padx=30, pady=15,
                                 state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT)
        
        progress_frame = tk.Frame(main_frame, bg='#2c3e50')
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(progress_frame, text="Progress:", font=('Arial', 12), 
                fg='#ecf0f1', bg='#2c3e50').pack(anchor=tk.W)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          maximum=100, length=400)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Ready to convert PDF to speech", 
                                    font=('Arial', 10), 
                                    fg='#95a5a6', bg='#2c3e50')
        self.status_label.pack(anchor=tk.W)
        
        text_frame = tk.LabelFrame(main_frame, text="Extracted Text Preview", 
                                  font=('Arial', 14, 'bold'),
                                  fg='#ecf0f1', bg='#2c3e50')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        text_scroll_frame = tk.Frame(text_frame, bg='#2c3e50')
        text_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_area = tk.Text(text_scroll_frame, wrap=tk.WORD, 
                               font=('Arial', 11),
                               bg='#34495e', fg='#ecf0f1',
                               insertbackground='white',
                               selectbackground='#3498db')
        
        text_scrollbar = tk.Scrollbar(text_scroll_frame, orient=tk.VERTICAL, 
                                    command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=text_scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def populate_voices(self):
        voices = self.engine.getProperty('voices')
        voice_names = []
        
        for voice in voices:
            name = voice.name if hasattr(voice, 'name') else voice.id
            voice_names.append(name)
        
        self.voice_combo['values'] = voice_names
        if voice_names:
            self.voice_combo.current(0)
    
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.extract_text_from_pdf(file_path)
    
    def extract_text_from_pdf(self, file_path):
        try:
            self.status_label.config(text="Extracting text from PDF...")
            self.progress_var.set(0)
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                extracted_text = ""
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n\n"
                    
                    progress = (page_num + 1) / total_pages * 100
                    self.progress_var.set(progress)
                    self.root.update_idletasks()
                
                if extracted_text.strip():
                    self.current_text = extracted_text.strip()
                    self.current_sentence_index = 0  # Reset position for new text
                    self.sentences = []  # Clear previous sentences
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, self.current_text)
                    
                    self.play_btn.config(state=tk.NORMAL)
                    self.save_btn.config(state=tk.NORMAL)
                    self.status_label.config(text=f"Successfully extracted text from {total_pages} pages")
                else:
                    messagebox.showwarning("Warning", "No text could be extracted from the PDF file.")
                    self.status_label.config(text="No text found in PDF")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF file:\n{str(e)}")
            self.status_label.config(text="Error reading PDF file")
    
    def update_speed(self, value):
        self.engine.setProperty('rate', int(value))
    
    def update_volume(self, value):
        self.engine.setProperty('volume', float(value))
    
    def update_voice(self, event):
        voices = self.engine.getProperty('voices')
        selected_index = self.voice_combo.current()
        if 0 <= selected_index < len(voices):
            self.engine.setProperty('voice', voices[selected_index].id)
    
    def toggle_speech(self):
        if not self.is_speaking:
            self.start_speech()
        else:
            if self.is_paused:
                self.resume_speech()
            else:
                self.pause_speech()
    
    def start_speech(self):
        if not self.current_text:
            messagebox.showwarning("Warning", "No text to convert to speech.")
            return
        
        self.is_speaking = True
        self.is_paused = False
        
        # Prepare sentences if starting fresh
        if self.current_sentence_index == 0:
            self.sentences = [s.strip() for s in self.current_text.split('.') if s.strip()]
        
        self.play_btn.config(text="⏸ Pause", bg='#f39c12')
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Converting text to speech...")
        
        self.speech_thread = threading.Thread(target=self.speak_text)
        self.speech_thread.daemon = True
        self.speech_thread.start()
    
    def pause_speech(self):
        self.is_paused = True
        self.engine.stop()  # Stop current sentence
        self.play_btn.config(text="▶ Resume", bg='#27ae60')
        self.status_label.config(text="Speech paused")
    
    def resume_speech(self):
        if self.current_sentence_index >= len(self.sentences):
            # If we've reached the end, restart from beginning
            self.current_sentence_index = 0
        
        self.is_paused = False
        self.play_btn.config(text="⏸ Pause", bg='#f39c12')
        self.status_label.config(text="Resuming speech...")
        
        self.speech_thread = threading.Thread(target=self.speak_text)
        self.speech_thread.daemon = True
        self.speech_thread.start()
    
    def stop_speech(self):
        self.engine.stop()
        self.is_speaking = False
        self.is_paused = False
        self.current_sentence_index = 0
        self.play_btn.config(text="▶ Play", bg='#27ae60', state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_label.config(text="Speech stopped")
    
    def speak_text(self):
        try:
            total_sentences = len(self.sentences)
            
            # Continue from where we left off
            for i in range(self.current_sentence_index, total_sentences):
                # Check if we should stop or pause
                if not self.is_speaking or self.is_paused:
                    self.current_sentence_index = i  # Save position for resume
                    return
                
                sentence = self.sentences[i]
                if sentence.strip():
                    # Update current position
                    self.current_sentence_index = i
                    
                    # Speak the sentence
                    self.engine.say(sentence.strip() + '.')
                    self.engine.runAndWait()
                    
                    # Update progress
                    progress = (i + 1) / total_sentences * 100
                    self.progress_var.set(progress)
                    
                    # Update status with current sentence preview
                    preview = sentence[:50] + "..." if len(sentence) > 50 else sentence
                    self.status_label.config(text=f"Speaking: {preview}")
            
            # If we completed all sentences
            if self.is_speaking and not self.is_paused:
                self.current_sentence_index = 0  # Reset for next time
                self.is_speaking = False
                self.play_btn.config(text="▶ Play", bg='#27ae60')
                self.stop_btn.config(state=tk.DISABLED)
                self.progress_var.set(100)
                self.status_label.config(text="Speech completed successfully")
                messagebox.showinfo("Complete", "Text-to-speech conversion completed!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Speech synthesis error:\n{str(e)}")
            self.stop_speech()
    
    def save_audio(self):
        if not self.current_text:
            messagebox.showwarning("Warning", "No text to save as audio.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Audio File",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.status_label.config(text="Saving audio file...")
                self.engine.save_to_file(self.current_text, file_path)
                self.engine.runAndWait()
                self.status_label.config(text=f"Audio saved to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Audio file saved successfully!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio file:\n{str(e)}")
                self.status_label.config(text="Error saving audio file")
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        if self.is_speaking:
            self.is_speaking = False
            self.is_paused = False
            self.engine.stop()
        self.root.destroy()

if __name__ == "__main__":
    app = PDFToSpeechConverter()
    app.run()
