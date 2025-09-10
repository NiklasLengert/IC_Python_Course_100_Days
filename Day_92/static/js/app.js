class ColorExtractor {
    constructor() {
        this.initializeEventListeners();
        this.initializeTooltips();
    }

    initializeEventListeners() {
        this.setupImagePreview();
        this.setupColorCopying();
        this.setupFormValidation();
        this.setupKeyboardNavigation();
    }

    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                delay: { show: 500, hide: 100 }
            });
        });
    }

    setupImagePreview() {
        const uploadZone = document.getElementById('uploadZone');
        const imageInput = document.getElementById('imageInput');
        
        if (!uploadZone || !imageInput) return;

        uploadZone.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadZone.addEventListener('drop', this.handleDrop.bind(this));
        
        imageInput.addEventListener('change', this.handleFileSelect.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.currentTarget.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        const uploadZone = e.currentTarget;
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && this.validateImageFile(files[0])) {
            document.getElementById('imageInput').files = files;
            this.previewImage(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file && this.validateImageFile(file)) {
            this.previewImage(file);
        }
    }

    validateImageFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        const maxSize = 10 * 1024 * 1024;
        
        if (!validTypes.includes(file.type)) {
            this.showToast('Please select a valid image file (JPEG, PNG, GIF, WebP)', 'error');
            return false;
        }
        
        if (file.size > maxSize) {
            this.showToast('File size must be less than 10MB', 'error');
            return false;
        }
        
        return true;
    }

    previewImage(file) {
        const reader = new FileReader();
        const previewSection = document.getElementById('previewSection');
        const imagePreview = document.getElementById('imagePreview');
        const imageDetails = document.getElementById('imageDetails');
        
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.onload = () => {
                const sizeKB = (file.size / 1024).toFixed(2);
                const dimensions = `${imagePreview.naturalWidth}x${imagePreview.naturalHeight}`;
                imageDetails.textContent = `${file.name} (${sizeKB} KB) - ${dimensions}`;
                
                previewSection.classList.remove('d-none');
                previewSection.classList.add('fade-in');
            };
        };
        reader.readAsDataURL(file);
    }

    setupColorCopying() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('color-swatch') || 
                e.target.classList.contains('color-swatch-small') ||
                e.target.classList.contains('harmony-preview')) {
                this.copyColorToClipboard(e.target);
            }
        });
    }

    async copyColorToClipboard(element) {
        const backgroundColor = window.getComputedStyle(element).backgroundColor;
        const colorHex = this.rgbToHex(backgroundColor);
        
        try {
            await navigator.clipboard.writeText(colorHex);
            this.showToast(`Color ${colorHex} copied to clipboard!`, 'success');
            
            element.style.transform = 'scale(1.2)';
            element.style.transition = 'transform 0.2s ease';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 200);
        } catch (err) {
            this.showToast('Failed to copy color', 'error');
        }
    }

    rgbToHex(rgb) {
        const rgbArray = rgb.match(/\d+/g);
        if (!rgbArray) return rgb;
        
        const r = parseInt(rgbArray[0]);
        const g = parseInt(rgbArray[1]);
        const b = parseInt(rgbArray[2]);
        
        return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase()}`;
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.showToast('Please fill in all required fields', 'error');
                }
                form.classList.add('was-validated');
            });
        });
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const dropdowns = document.querySelectorAll('.dropdown-menu.show');
                dropdowns.forEach(dropdown => {
                    const toggle = dropdown.previousElementSibling;
                    if (toggle) {
                        bootstrap.Dropdown.getInstance(toggle)?.hide();
                    }
                });
            }
            
            if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
                e.preventDefault();
                const uploadBtn = document.getElementById('imageInput');
                if (uploadBtn) uploadBtn.click();
            }
        });
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.textContent = message;
        
        const bgColor = type === 'error' ? '#dc3545' : 
                        type === 'success' ? '#28a745' : '#17a2b8';
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${bgColor};
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-size: 14px;
            max-width: 300px;
            word-wrap: break-word;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
        
        toast.addEventListener('click', () => {
            toast.remove();
        });
    }

    static downloadJSON(data, filename) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { 
            type: 'application/json' 
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    static formatColorData(colors) {
        return colors.map(color => ({
            name: color.name,
            hex: color.hex,
            rgb: color.rgb,
            hsl: this.rgbToHsl(color.rgb),
            percentage: color.percentage
        }));
    }

    static rgbToHsl(rgb) {
        const [r, g, b] = rgb.map(x => x / 255);
        const max = Math.max(r, g, b);
        const min = Math.min(r, g, b);
        let h, s, l = (max + min) / 2;

        if (max === min) {
            h = s = 0;
        } else {
            const d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
            switch (max) {
                case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                case g: h = (b - r) / d + 2; break;
                case b: h = (r - g) / d + 4; break;
            }
            h /= 6;
        }

        return [
            Math.round(h * 360),
            Math.round(s * 100),
            Math.round(l * 100)
        ];
    }
}

class Analytics {
    static trackColorExtraction(colorCount, imageSize) {
        console.log('Color extraction:', { colorCount, imageSize });
    }
    
    static trackDownload(type, data) {
        console.log('Download:', { type, data });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.colorExtractor = new ColorExtractor();
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Processing...';
                submitBtn.disabled = true;
                
                setTimeout(() => {
                    if (!this.checkValidity()) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }
                }, 100);
            }
        });
    });
});

function downloadPalette(name, colors) {
    const palette = {
        name: name,
        colors: colors,
        timestamp: new Date().toISOString(),
        format: 'Color Extractor Palette v1.0'
    };
    
    ColorExtractor.downloadJSON(palette, `${name.replace(/\s+/g, '_')}_palette.json`);
    window.colorExtractor.showToast(`Palette "${name}" downloaded successfully!`, 'success');
    Analytics.trackDownload('palette', { name, colorCount: colors.length });
}

function downloadResults() {
    const data = window.colorResults || {};
    ColorExtractor.downloadJSON(data, 'color_analysis_results.json');
    window.colorExtractor.showToast('Results downloaded successfully!', 'success');
    Analytics.trackDownload('results', data);
}
