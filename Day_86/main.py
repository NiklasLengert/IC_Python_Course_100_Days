import tkinter as tk
from tkinter import messagebox
import time
import random

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(False, False)
        
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet and is commonly used for typing practice.",
            "Programming is the art of telling another human being what one wants the computer to do. It requires patience, logic, and creativity.",
            "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole filled with the ends of worms and an oozy smell.",
            "To be or not to be, that is the question. Whether tis nobler in the mind to suffer the slings and arrows of outrageous fortune.",
            "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness and hope.",
            "Science is not only compatible with spirituality but is a profound source of spirituality and wonder about our universe.",
            "The only way to do great work is to love what you do. If you haven't found it yet, keep looking and don't settle for less.",
            "Life is what happens to you while you're busy making other plans. Every moment is precious and should be lived fully."
        ]
        
        self.current_text = ""
        self.start_time = None
        self.test_active = False
        self.test_completed = False
        
        self.setup_gui()
        self.reset_test()
    
    def setup_gui(self):
        # Title
        title_label = tk.Label(self.root, text="⌨️ Typing Speed Test", 
                              font=('Arial', 24, 'bold'), bg='#f0f8ff', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="Click 'Start Test' and type the text below as quickly and accurately as possible.",
                               font=('Arial', 12), bg='#f0f8ff', fg='#34495e')
        instructions.pack(pady=(0, 20))
        
        # Sample text display
        text_frame = tk.Frame(self.root, bg='white', relief=tk.SUNKEN, bd=2)
        text_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        self.sample_label = tk.Text(text_frame, height=6, font=('Courier New', 14), 
                                   wrap=tk.WORD, bg='#f8f9fa', fg='#2c3e50',
                                   state=tk.DISABLED, relief=tk.FLAT, padx=20, pady=15)
        self.sample_label.pack(fill=tk.BOTH, expand=True)
        
        # Typing area
        typing_frame = tk.Frame(self.root, bg='#f0f8ff')
        typing_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        tk.Label(typing_frame, text="Type here:", font=('Arial', 12, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').pack(anchor=tk.W)
        
        self.typing_area = tk.Text(typing_frame, height=6, font=('Courier New', 14), 
                                  wrap=tk.WORD, bg='white', relief=tk.SUNKEN, bd=2,
                                  padx=20, pady=15)
        self.typing_area.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.typing_area.bind('<KeyPress>', self.on_key_press)
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg='#f0f8ff')
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(button_frame, text="Start Test", 
                                  command=self.start_test, font=('Arial', 12, 'bold'),
                                  bg='#27ae60', fg='white', padx=30, pady=10, height=2)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.reset_btn = tk.Button(button_frame, text="Reset", 
                                  command=self.reset_test, font=('Arial', 12, 'bold'),
                                  bg='#e74c3c', fg='white', padx=30, pady=10, height=2)
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
        self.new_text_btn = tk.Button(button_frame, text="New Text", 
                                     command=self.load_new_text, font=('Arial', 12, 'bold'),
                                     bg='#3498db', fg='white', padx=30, pady=10, height=2)
        self.new_text_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Stats display
        stats_frame = tk.Frame(self.root, bg='#ecf0f1', relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        tk.Label(stats_frame, text="📊 Statistics", font=('Arial', 14, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').pack(pady=(10, 5))
        
        stats_grid = tk.Frame(stats_frame, bg='#ecf0f1')
        stats_grid.pack(pady=(0, 10))
        
        # WPM
        tk.Label(stats_grid, text="Words per Minute:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=0, column=0, padx=20, sticky=tk.W)
        self.wpm_label = tk.Label(stats_grid, text="0", font=('Arial', 11), 
                                 bg='#ecf0f1', fg='#27ae60')
        self.wpm_label.grid(row=0, column=1, padx=20, sticky=tk.W)
        
        # Accuracy
        tk.Label(stats_grid, text="Accuracy:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=0, column=2, padx=20, sticky=tk.W)
        self.accuracy_label = tk.Label(stats_grid, text="100%", font=('Arial', 11), 
                                      bg='#ecf0f1', fg='#27ae60')
        self.accuracy_label.grid(row=0, column=3, padx=20, sticky=tk.W)
        
        # Time
        tk.Label(stats_grid, text="Time:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=1, column=0, padx=20, sticky=tk.W)
        self.time_label = tk.Label(stats_grid, text="0s", font=('Arial', 11), 
                                  bg='#ecf0f1', fg='#3498db')
        self.time_label.grid(row=1, column=1, padx=20, sticky=tk.W)
        
        # Characters
        tk.Label(stats_grid, text="Characters:", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=1, column=2, padx=20, sticky=tk.W)
        self.chars_label = tk.Label(stats_grid, text="0", font=('Arial', 11), 
                                   bg='#ecf0f1', fg='#3498db')
        self.chars_label.grid(row=1, column=3, padx=20, sticky=tk.W)
    
    def load_new_text(self):
        self.current_text = random.choice(self.sample_texts)
        self.sample_label.config(state=tk.NORMAL)
        self.sample_label.delete(1.0, tk.END)
        self.sample_label.insert(1.0, self.current_text)
        self.sample_label.config(state=tk.DISABLED)
        self.reset_test()
    
    def start_test(self):
        if not self.test_active and not self.test_completed:
            self.test_active = True
            self.start_time = time.time()
            self.start_btn.config(state=tk.DISABLED)
            self.typing_area.focus_set()
            self.typing_area.config(bg='#fff3cd')
            messagebox.showinfo("Test Started", "Start typing! The timer has begun.")
    
    def reset_test(self):
        self.test_active = False
        self.test_completed = False
        self.start_time = None
        self.start_btn.config(state=tk.NORMAL)
        self.typing_area.config(bg='white')
        self.typing_area.delete(1.0, tk.END)
        self.update_stats(0, 100, 0, 0)
        
        if not self.current_text:
            self.load_new_text()
    
    def on_key_press(self, event):
        if not self.test_active:
            return "break"
        
        self.root.after(10, self.update_progress)
    
    def update_progress(self):
        if not self.test_active:
            return
        
        typed_text = self.typing_area.get(1.0, tk.END).rstrip('\n')
        
        # Calculate stats
        elapsed_time = time.time() - self.start_time
        char_count = len(typed_text)
        word_count = len(typed_text.split()) if typed_text.strip() else 0
        wpm = (word_count / elapsed_time) * 60 if elapsed_time > 0 else 0
        
        # Calculate accuracy
        accuracy = self.calculate_accuracy(typed_text, self.current_text)
        
        self.update_stats(wpm, accuracy, elapsed_time, char_count)
        
        # Check if test is complete
        if typed_text == self.current_text:
            self.complete_test()
        elif len(typed_text) > len(self.current_text):
            self.typing_area.config(bg='#f8d7da')
        else:
            # Color coding for accuracy
            if accuracy >= 95:
                self.typing_area.config(bg='#d4edda')
            elif accuracy >= 80:
                self.typing_area.config(bg='#fff3cd')
            else:
                self.typing_area.config(bg='#f8d7da')
    
    def calculate_accuracy(self, typed, original):
        if not typed:
            return 100
        
        correct_chars = 0
        for i, char in enumerate(typed):
            if i < len(original) and char == original[i]:
                correct_chars += 1
        
        return (correct_chars / len(typed)) * 100 if typed else 100
    
    def update_stats(self, wpm, accuracy, time_elapsed, char_count):
        self.wpm_label.config(text=f"{wpm:.1f}")
        self.accuracy_label.config(text=f"{accuracy:.1f}%")
        self.time_label.config(text=f"{time_elapsed:.1f}s")
        self.chars_label.config(text=str(char_count))
        
        # Color coding for stats
        if wpm >= 60:
            self.wpm_label.config(fg='#27ae60')
        elif wpm >= 40:
            self.wpm_label.config(fg='#f39c12')
        else:
            self.wpm_label.config(fg='#e74c3c')
        
        if accuracy >= 95:
            self.accuracy_label.config(fg='#27ae60')
        elif accuracy >= 80:
            self.accuracy_label.config(fg='#f39c12')
        else:
            self.accuracy_label.config(fg='#e74c3c')
    
    def complete_test(self):
        self.test_active = False
        self.test_completed = True
        self.typing_area.config(bg='#d4edda')
        
        elapsed_time = time.time() - self.start_time
        typed_text = self.typing_area.get(1.0, tk.END).rstrip('\n')
        word_count = len(typed_text.split())
        wpm = (word_count / elapsed_time) * 60
        accuracy = self.calculate_accuracy(typed_text, self.current_text)
        
        # Final message
        if wpm >= 60 and accuracy >= 95:
            level = "Excellent! 🌟"
        elif wpm >= 40 and accuracy >= 90:
            level = "Good job! 👍"
        elif wpm >= 25:
            level = "Keep practicing! 📈"
        else:
            level = "Practice makes perfect! 💪"
        
        messagebox.showinfo("Test Complete!", 
                           f"🎉 Test completed!\n\n"
                           f"Words per minute: {wpm:.1f}\n"
                           f"Accuracy: {accuracy:.1f}%\n"
                           f"Time: {elapsed_time:.1f}s\n\n"
                           f"{level}")

def main():
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
