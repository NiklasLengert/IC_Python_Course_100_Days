from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import webcolors
from werkzeug.utils import secure_filename
import colorsys
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

class ColorAnalyzer:
    def __init__(self, image_path=None, image_data=None):
        if image_path:
            self.image = Image.open(image_path).convert('RGB')
        elif image_data:
            self.image = Image.open(BytesIO(image_data)).convert('RGB')
        else:
            raise ValueError("Must provide either image_path or image_data")
        
        self.original_size = self.image.size
        self.resize_for_analysis()
        
    def resize_for_analysis(self):
        max_size = 300
        if max(self.image.size) > max_size:
            ratio = max_size / max(self.image.size)
            new_size = tuple(int(dim * ratio) for dim in self.image.size)
            self.image = self.image.resize(new_size, Image.Resampling.LANCZOS)
    
    def get_dominant_colors(self, num_colors=8):
        image_array = np.array(self.image)
        image_array = image_array.reshape((-1, 3))
        
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(image_array)
        
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        color_counts = Counter(labels)
        total_pixels = len(labels)
        
        color_info = []
        for i in range(num_colors):
            rgb = tuple(int(c) for c in colors[i])
            percentage = (color_counts[i] / total_pixels) * 100
            
            hex_code = '#{:02x}{:02x}{:02x}'.format(*rgb)
            color_name = self.get_color_name(rgb)
            hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
            
            color_info.append({
                'rgb': rgb,
                'hex': hex_code,
                'name': color_name,
                'percentage': round(percentage, 2),
                'hsv': {
                    'h': round(hsv[0] * 360),
                    's': round(hsv[1] * 100),
                    'v': round(hsv[2] * 100)
                },
                'luminance': self.get_luminance(rgb)
            })
        
        return sorted(color_info, key=lambda x: x['percentage'], reverse=True)
    
    def get_color_name(self, rgb):
        try:
            return webcolors.rgb_to_name(rgb)
        except ValueError:
            min_distance = float('inf')
            closest_name = 'Unknown'
            
            for name, hex_code in webcolors.CSS3_HEX_TO_NAMES.items():
                r, g, b = webcolors.hex_to_rgb(hex_code)
                distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, (r, g, b)))
                
                if distance < min_distance:
                    min_distance = distance
                    closest_name = name
            
            return closest_name.replace('_', ' ').title()
    
    def get_luminance(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def get_color_harmony(self, base_color):
        r, g, b = base_color['rgb']
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        harmonies = {
            'complementary': [(h + 0.5) % 1],
            'triadic': [(h + 1/3) % 1, (h + 2/3) % 1],
            'analogous': [(h - 1/12) % 1, (h + 1/12) % 1],
            'split_complementary': [(h + 5/12) % 1, (h + 7/12) % 1]
        }
        
        harmony_colors = {}
        for name, hues in harmonies.items():
            colors = []
            for hue in hues:
                rgb = colorsys.hsv_to_rgb(hue, s, v)
                rgb_int = tuple(int(c * 255) for c in rgb)
                hex_code = '#{:02x}{:02x}{:02x}'.format(*rgb_int)
                colors.append({
                    'rgb': rgb_int,
                    'hex': hex_code,
                    'name': self.get_color_name(rgb_int)
                })
            harmony_colors[name] = colors
        
        return harmony_colors

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_colors():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            num_colors = int(request.form.get('num_colors', 8))
            num_colors = max(3, min(15, num_colors))
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            analyzer = ColorAnalyzer(image_path=filepath)
            dominant_colors = analyzer.get_dominant_colors(num_colors)
            
            harmony_colors = analyzer.get_color_harmony(dominant_colors[0])
            
            buffered = BytesIO()
            display_image = Image.open(filepath)
            if max(display_image.size) > 800:
                ratio = 800 / max(display_image.size)
                new_size = tuple(int(dim * ratio) for dim in display_image.size)
                display_image = display_image.resize(new_size, Image.Resampling.LANCZOS)
            
            display_image.save(buffered, format="JPEG", quality=90)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            total_percentage = sum(color['percentage'] for color in dominant_colors)
            avg_luminance = sum(color['luminance'] for color in dominant_colors) / len(dominant_colors)
            
            color_temperature = "Warm" if dominant_colors[0]['hsv']['h'] < 60 or dominant_colors[0]['hsv']['h'] > 300 else "Cool"
            
            os.remove(filepath)
            
            return render_template('results.html', 
                                 colors=dominant_colors,
                                 harmony_colors=harmony_colors,
                                 image_data=img_str,
                                 filename=filename,
                                 original_size=analyzer.original_size,
                                 total_percentage=round(total_percentage, 2),
                                 avg_luminance=round(avg_luminance, 3),
                                 color_temperature=color_temperature,
                                 num_colors=num_colors)
        
        except Exception as e:
            flash(f'Error processing image: {str(e)}', 'error')
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('home'))
    
    else:
        flash('Invalid file type. Please upload an image file.', 'error')
        return redirect(url_for('home'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        num_colors = int(request.form.get('num_colors', 8))
        num_colors = max(3, min(15, num_colors))
        
        image_data = file.read()
        analyzer = ColorAnalyzer(image_data=image_data)
        dominant_colors = analyzer.get_dominant_colors(num_colors)
        
        return jsonify({
            'success': True,
            'colors': dominant_colors,
            'image_size': analyzer.original_size,
            'analysis_settings': {
                'num_colors': num_colors,
                'total_pixels': analyzer.image.size[0] * analyzer.image.size[1]
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gallery')
def gallery():
    sample_images = [
        {
            'name': 'Sunset',
            'colors': ['#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#118AB2'],
            'description': 'Warm sunset colors with orange and yellow tones'
        },
        {
            'name': 'Ocean',
            'colors': ['#03045E', '#0077B6', '#00B4D8', '#90E0EF', '#CAF0F8'],
            'description': 'Cool ocean blues from deep navy to light cyan'
        },
        {
            'name': 'Forest',
            'colors': ['#2D5016', '#3D6116', '#4E7A1B', '#8FBC8F', '#98FB98'],
            'description': 'Natural forest greens in various shades'
        },
        {
            'name': 'Autumn',
            'colors': ['#8B0000', '#FF4500', '#FF6347', '#FFD700', '#DEB887'],
            'description': 'Autumn leaf colors with reds, oranges, and golds'
        }
    ]
    
    return render_template('gallery.html', samples=sample_images)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5003)
