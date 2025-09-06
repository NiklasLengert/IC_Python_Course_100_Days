from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

writing_sessions = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/write')
def write():
    difficulty = request.args.get('difficulty', 'normal')
    timeout_settings = {
        'easy': 10000,
        'normal': 5000,
        'hard': 3000,
        'extreme': 1500
    }
    timeout = timeout_settings.get(difficulty, 5000)
    return render_template('write.html', timeout=timeout, difficulty=difficulty)

@app.route('/save_session', methods=['POST'])
def save_session():
    data = request.json
    session = {
        'id': len(writing_sessions) + 1,
        'content': data.get('content', ''),
        'word_count': data.get('word_count', 0),
        'char_count': data.get('char_count', 0),
        'writing_time': data.get('writing_time', 0),
        'difficulty': data.get('difficulty', 'normal'),
        'timestamp': datetime.now(),
        'completed': data.get('completed', False)
    }
    writing_sessions.append(session)
    return jsonify({'success': True, 'session_id': session['id']})

@app.route('/sessions')
def sessions():
    sorted_sessions = sorted(writing_sessions, key=lambda x: x['timestamp'], reverse=True)
    return render_template('sessions.html', sessions=sorted_sessions)

@app.route('/session/<int:session_id>')
def view_session(session_id):
    session = next((s for s in writing_sessions if s['id'] == session_id), None)
    if not session:
        flash('Session not found!', 'error')
        return redirect(url_for('sessions'))
    return render_template('view_session.html', session=session)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
