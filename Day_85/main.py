import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermark Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        self.root.minsize(800, 600)
        
        self.original_image = None
        self.watermarked_image = None
        self.preview_image = None
        
        self.setup_gui()
    
    def setup_gui(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Image Watermark Tool", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(0, 20))
        
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.upload_btn = tk.Button(button_frame, text="Upload Image", 
                                   command=self.upload_image, font=('Arial', 12, 'bold'),
                                   bg='#4CAF50', fg='white', padx=20, pady=10, height=2)
        self.upload_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = tk.Button(button_frame, text="Save Watermarked Image", 
                                 command=self.save_image, font=('Arial', 12, 'bold'),
                                 bg='#2196F3', fg='white', padx=20, pady=10,
                                 state=tk.DISABLED, height=2)
        self.save_btn.pack(side=tk.RIGHT)
        
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = tk.Frame(content_frame, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(content_frame, bg='#f0f0f0', width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        self.setup_image_display(left_frame)
        self.setup_watermark_controls(right_frame)
    
    def setup_image_display(self, parent):
        image_label = tk.Label(parent, text="Image Preview", font=('Arial', 14, 'bold'), bg='#f0f0f0')
        image_label.pack(pady=(0, 10))
        
        self.image_canvas = tk.Canvas(parent, bg='white', relief=tk.SUNKEN, borderwidth=2)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.image_canvas.create_text(250, 200, text="No image loaded\nClick 'Upload Image' to start", 
                                     font=('Arial', 14), fill='gray')
    
    def setup_watermark_controls(self, parent):
        controls_label = tk.Label(parent, text="Watermark Settings", 
                                 font=('Arial', 14, 'bold'), bg='#f0f0f0')
        controls_label.pack(pady=(0, 15))
        
        # Put preview button at the top for visibility
        self.preview_btn = tk.Button(parent, text="Preview Watermark", 
                                    command=self.preview_watermark, font=('Arial', 12, 'bold'),
                                    bg='#FF9800', fg='white', padx=20, pady=15,
                                    state=tk.DISABLED, height=2)
        self.preview_btn.pack(pady=(0, 20), fill=tk.X)
        
        text_frame = tk.LabelFrame(parent, text="Text Watermark", font=('Arial', 11, 'bold'), 
                                  bg='#f0f0f0', padx=10, pady=10)
        text_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(text_frame, text="Watermark Text:", bg='#f0f0f0').pack(anchor=tk.W)
        self.text_entry = tk.Entry(text_frame, font=('Arial', 11))
        self.text_entry.pack(fill=tk.X, pady=(5, 10))
        self.text_entry.insert(0, "© Your Watermark")
        
        tk.Label(text_frame, text="Font Size:", bg='#f0f0f0').pack(anchor=tk.W)
        self.font_size_var = tk.IntVar(value=36)
        font_size_scale = tk.Scale(text_frame, from_=12, to=100, orient=tk.HORIZONTAL, 
                                  variable=self.font_size_var, bg='#f0f0f0')
        font_size_scale.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(text_frame, text="Transparency:", bg='#f0f0f0').pack(anchor=tk.W)
        self.opacity_var = tk.IntVar(value=128)
        opacity_scale = tk.Scale(text_frame, from_=50, to=255, orient=tk.HORIZONTAL, 
                                variable=self.opacity_var, bg='#f0f0f0')
        opacity_scale.pack(fill=tk.X, pady=(5, 10))
        
        position_frame = tk.LabelFrame(parent, text="Position", font=('Arial', 11, 'bold'), 
                                      bg='#f0f0f0', padx=10, pady=10)
        position_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.position_var = tk.StringVar(value="bottom-right")
        positions = [
            ("Top Left", "top-left"),
            ("Top Right", "top-right"),
            ("Bottom Left", "bottom-left"),
            ("Bottom Right", "bottom-right"),
            ("Center", "center")
        ]
        
        for text, value in positions:
            tk.Radiobutton(position_frame, text=text, variable=self.position_var, 
                          value=value, bg='#f0f0f0').pack(anchor=tk.W)
    
    def upload_image(self):
        file_types = [
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Select an image",
            filetypes=file_types
        )
        
        if filename:
            try:
                self.original_image = Image.open(filename)
                self.display_image(self.original_image)
                self.preview_btn.config(state=tk.NORMAL)
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image):
        self.image_canvas.delete("all")
        
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, lambda: self.display_image(image))
            return
        
        img_width, img_height = image.size
        scale = min(canvas_width / img_width, canvas_height / img_height, 1.0)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(resized_image)
        
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=self.preview_image)
    
    def get_watermark_position(self, image_size, text_size):
        img_width, img_height = image_size
        text_width, text_height = text_size
        margin = 50
        
        position = self.position_var.get()
        
        if position == "top-left":
            return (margin, margin)
        elif position == "top-right":
            return (img_width - text_width - margin, margin)
        elif position == "bottom-left":
            return (margin, img_height - text_height - margin)
        elif position == "bottom-right":
            return (img_width - text_width - margin, img_height - text_height - margin)
        else:
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
    
    def create_watermark(self, image):
        watermark_text = self.text_entry.get().strip()
        if not watermark_text:
            messagebox.showwarning("Warning", "Please enter watermark text!")
            return None
        
        watermarked = image.copy()
        
        try:
            font_size = self.font_size_var.get()
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        overlay = Image.new('RGBA', watermarked.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = self.get_watermark_position(watermarked.size, (text_width, text_height))
        opacity = self.opacity_var.get()
        
        # Use black shadow behind white text for better visibility
        shadow_color = (0, 0, 0, min(255, opacity + 50))
        text_color = (255, 255, 255, opacity)
        
        # Draw shadow and main text
        shadow_pos = (position[0] + 2, position[1] + 2)
        draw.text(shadow_pos, watermark_text, font=font, fill=shadow_color)
        draw.text(position, watermark_text, font=font, fill=text_color)
        
        if watermarked.mode != 'RGBA':
            watermarked = watermarked.convert('RGBA')
        
        return Image.alpha_composite(watermarked, overlay).convert('RGB')
    
    def preview_watermark(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return
        
        try:
            self.watermarked_image = self.create_watermark(self.original_image)
            if self.watermarked_image:
                self.display_image(self.watermarked_image)
                self.save_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create watermark: {str(e)}")
    
    def save_image(self):
        if self.watermarked_image is None:
            messagebox.showwarning("Warning", "Please preview the watermark first!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save watermarked image",
            defaultextension=".png",
            filetypes=[('PNG files', '*.png'), ('JPEG files', '*.jpg')]
        )
        
        if filename:
            try:
                self.watermarked_image.save(filename)
                messagebox.showinfo("Success", f"Watermarked image saved as:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
