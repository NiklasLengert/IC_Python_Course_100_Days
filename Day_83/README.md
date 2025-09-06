# Day 83 - Personal Portfolio Website

A Flask-based personal portfolio website to showcase projects and skills.

## Features

- **Home Page**: Hero section with introduction and featured projects
- **About Page**: Personal information, education, and skills with progress bars
- **Projects Page**: Showcase of all projects with detailed descriptions
- **Project Details**: Individual pages for each project with features and technologies
- **Contact Form**: Working contact form with email functionality
- **Responsive Design**: Mobile-friendly layout using Bootstrap

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5, Font Awesome icons, Custom CSS
- **Email**: SMTP integration for contact form

## Project Structure

```
Day_83/
├── main.py              # Flask application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── about.html      # About page
│   ├── projects.html   # Projects listing
│   ├── project_detail.html  # Individual project pages
│   └── contact.html    # Contact form
└── static/            # Static files
    ├── style.css      # Custom styles
    └── script.js      # JavaScript functionality
```

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure email (optional)**:
   - Update `MY_EMAIL` and `MY_PASSWORD` in `main.py`
   - Use Gmail App Password for authentication

3. **Customize content**:
   - Update personal information in templates
   - Modify project data in `main.py`
   - Update skills and their levels
   - Add your own project images

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Visit**: http://localhost:5000

## Customization

### Adding New Projects
Edit the `projects_data` list in `main.py`:
```python
{
    'id': 5,
    'title': 'Your New Project',
    'description': 'Project description here',
    'technologies': ['Python', 'Flask'],
    'github_link': 'https://github.com/yourusername/project',
    'demo_link': 'https://your-demo-link.com',
    'image': 'project-image.jpg'
}
```

### Updating Skills
Modify the `skills_data` list in `main.py`:
```python
{'name': 'New Skill', 'level': 75}
```

### Styling
- Edit `static/style.css` for visual customizations
- Modify Bootstrap classes in templates
- Update color scheme in CSS variables

## Features Implemented

- **Responsive Navigation**: Mobile-friendly navigation bar
- **Hero Section**: Eye-catching landing area with call-to-action
- **Project Showcase**: Grid layout for projects with filtering
- **Skills Visualization**: Animated progress bars for skills
- **Contact Integration**: Functional email contact form
- **Smooth Animations**: CSS and JavaScript animations
- **SEO Friendly**: Proper HTML structure and meta tags

## Learning Objectives

This project demonstrates:
- Flask web application structure
- Template inheritance with Jinja2
- Static file serving
- Form handling and validation
- Email integration
- Responsive web design
- JavaScript DOM manipulation
- CSS animations and transitions

## Future Enhancements

- Add a blog section
- Implement project filtering by technology
- Add a portfolio admin panel
- Integrate with GitHub API for live project data
- Add dark/light mode toggle
- Implement visitor analytics

## Author

Built as part of the 100 Days of Code Python course - Day 83 project.
