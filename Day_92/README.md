# Color Palette Extractor

A sophisticated Flask web application that extracts dominant colors from images using machine learning algorithms and provides detailed color analysis.

## Features

### Core Functionality
- **Image Upload**: Drag-and-drop or click to upload images (JPEG, PNG, GIF, WebP)
- **Color Extraction**: Uses K-means clustering to identify dominant colors
- **Color Analysis**: Provides color names, RGB/HEX values, and coverage percentages
- **Color Harmonies**: Generates complementary, triadic, and analogous color schemes
- **Visual Analytics**: Color temperature analysis and luminance calculations

### Advanced Features
- **Responsive Design**: Modern Bootstrap 5 interface with custom styling
- **Interactive Elements**: Click colors to copy to clipboard
- **Download Results**: Export color palettes as JSON files
- **Gallery**: Curated collection of sample color palettes
- **Accessibility**: WCAG compliant with proper contrast and keyboard navigation

## Technical Implementation

### Machine Learning
- **K-means Clustering**: Scikit-learn implementation for color grouping
- **Color Space Conversion**: HSV transformations for color harmony generation
- **Statistical Analysis**: Color distribution and luminance calculations

### Libraries Used
- **Flask**: Web framework and routing
- **PIL (Pillow)**: Image processing and manipulation
- **NumPy**: Numerical operations on image data
- **Scikit-learn**: Machine learning algorithms
- **webcolors**: Color name identification
- **Bootstrap 5**: Frontend UI framework

### Architecture
- **MVC Pattern**: Separation of concerns with templates and logic
- **RESTful Design**: Clean URL structure and API endpoints
- **Security**: File validation, size limits, and secure filename handling
- **Performance**: Image resizing and optimized processing

## Installation

1. Install required packages:
```bash
pip install flask pillow numpy scikit-learn webcolors
```

2. Run the application:
```bash
python main.py
```

3. Open your browser to `http://localhost:5003`

## Usage

### Basic Color Extraction
1. Upload an image using the drag-and-drop interface
2. Select the number of colors to extract (3-10)
3. Click "Analyze Colors" to process the image
4. View the extracted palette with detailed color information

### Color Analysis Features
- **Color Information**: View hex codes, RGB values, and color names
- **Coverage Analysis**: See what percentage each color represents
- **Harmony Generation**: Explore complementary and related color schemes
- **Temperature Analysis**: Understand warm vs cool color tendencies
- **Luminance Data**: Check brightness levels for accessibility

### Export Options
- Download individual color palettes as JSON
- Copy color values to clipboard
- Export complete analysis results

## API Endpoints

- `GET /`: Home page with upload interface
- `POST /`: Process uploaded image and return analysis
- `GET /gallery`: View sample color palettes
- `GET /about`: Application information and features
- `POST /api/analyze`: JSON API for color analysis

## File Structure
```
Day_92/
├── main.py              # Flask application and ColorAnalyzer class
├── templates/
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Home page with upload interface  
│   ├── results.html     # Color analysis results display
│   ├── gallery.html     # Sample palette gallery
│   └── about.html       # Application information
├── static/
│   ├── css/
│   │   └── style.css    # Custom styles and animations
│   └── js/
│       └── app.js       # JavaScript functionality
└── uploads/             # Temporary image storage
```

## Color Analysis Process

1. **Image Processing**: Resize and normalize uploaded image
2. **Pixel Sampling**: Extract RGB values from all pixels
3. **K-means Clustering**: Group similar colors together
4. **Color Identification**: Map RGB values to human-readable names
5. **Harmony Generation**: Calculate complementary and analogous colors
6. **Statistical Analysis**: Compute coverage percentages and luminance
7. **Results Display**: Present analysis with interactive visualizations

## Educational Value

This project demonstrates:
- Machine learning application in web development
- Color theory and digital image processing
- Modern web development with Flask and Bootstrap
- Responsive design and user experience principles
- Data visualization and interactive interfaces
- RESTful API design and JSON data handling

Perfect for portfolio projects showcasing the intersection of computer science, design theory, and web development skills.

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Modern browser features required for optimal experience including CSS Grid, Flexbox, and ES6 JavaScript.
