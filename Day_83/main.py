from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-for-portfolio'

MY_EMAIL = "niklas.lengert@example.com"
MY_PASSWORD = "your-app-password"

projects_data = [
    {
        'id': 1,
        'title': 'Morse Code Converter',
        'description': 'A Python program that converts text to Morse code and vice versa. Features include interactive menu and complete character support.',
        'technologies': ['Python', 'String Processing', 'Dictionaries'],
        'github_link': 'https://github.com/NiklasLengert/IC_Python_Course_100_Days/tree/main/Day_82',
        'demo_link': None,
        'image': 'morse-code.jpg'
    },
    {
        'id': 2,
        'title': 'Blog Website',
        'description': 'A full-featured blog with user authentication, admin panel, and commenting system built with Flask.',
        'technologies': ['Python', 'Flask', 'SQLAlchemy', 'HTML/CSS', 'Bootstrap'],
        'github_link': 'https://github.com/NiklasLengert/IC_Python_Course_100_Days/tree/main/Day_69',
        'demo_link': None,
        'image': 'blog-website.jpg'
    },
    {
        'id': 3,
        'title': 'Snake Game',
        'description': 'Classic Snake game implemented in Python using Turtle graphics. Features score tracking and collision detection.',
        'technologies': ['Python', 'Turtle Graphics', 'OOP'],
        'github_link': 'https://github.com/NiklasLengert/IC_Python_Course_100_Days/tree/main/Day_20_21',
        'demo_link': None,
        'image': 'snake-game.jpg'
    },
    {
        'id': 4,
        'title': 'Weather App',
        'description': 'Weather application that fetches real-time weather data using API integration and displays forecasts.',
        'technologies': ['Python', 'APIs', 'JSON', 'Requests'],
        'github_link': 'https://github.com/NiklasLengert/IC_Python_Course_100_Days/tree/main/Day_35',
        'demo_link': None,
        'image': 'weather-app.jpg'
    }
]

skills_data = [
    {'name': 'Python', 'level': 85},
    {'name': 'HTML/CSS', 'level': 75},
    {'name': 'JavaScript', 'level': 60},
    {'name': 'Flask', 'level': 70},
    {'name': 'SQLAlchemy', 'level': 65},
    {'name': 'Git/GitHub', 'level': 80},
    {'name': 'Bootstrap', 'level': 70},
    {'name': 'API Integration', 'level': 75}
]

@app.route('/')
def home():
    return render_template('index.html', projects=projects_data[:3])

@app.route('/about')
def about():
    return render_template('about.html', skills=skills_data)

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = None
    for p in projects_data:
        if p['id'] == project_id:
            project = p
            break
    
    if project is None:
        return "Project not found", 404
    
    return render_template('project_detail.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if name and email and subject and message:
            success = send_email(name, email, subject, message)
            if success:
                flash('Thank you for your message! I will get back to you soon.', 'success')
            else:
                flash('Sorry, there was an error sending your message. Please try again.', 'error')
        else:
            flash('Please fill in all fields.', 'error')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

def send_email(name, sender_email, subject, message):
    try:
        email_message = f"""Subject: Portfolio Contact: {subject}

New message from your portfolio website:

Name: {name}
Email: {sender_email}
Subject: {subject}

Message:
{message}
        """
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(MY_EMAIL, MY_PASSWORD)
            server.sendmail(MY_EMAIL, MY_EMAIL, email_message)
        
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True, port=5000)
