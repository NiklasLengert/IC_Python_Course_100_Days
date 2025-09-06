from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

todos = [
    {
        'id': 1,
        'task': 'Complete Python course project',
        'description': 'Finish the Day 89 todo list website with Flask',
        'priority': 'high',
        'completed': False,
        'created_at': datetime(2024, 12, 1, 10, 30),
        'due_date': datetime(2024, 12, 15),
        'category': 'Education'
    },
    {
        'id': 2,
        'task': 'Buy groceries',
        'description': 'Milk, eggs, bread, and fruits for the week',
        'priority': 'medium',
        'completed': False,
        'created_at': datetime(2024, 12, 2, 14, 20),
        'due_date': datetime(2024, 12, 5),
        'category': 'Personal'
    },
    {
        'id': 3,
        'task': 'Schedule dentist appointment',
        'description': 'Annual checkup and cleaning',
        'priority': 'low',
        'completed': True,
        'created_at': datetime(2024, 11, 28, 9, 15),
        'due_date': datetime(2024, 12, 10),
        'category': 'Health'
    },
    {
        'id': 4,
        'task': 'Prepare presentation',
        'description': 'Create slides for Monday meeting with the team',
        'priority': 'high',
        'completed': False,
        'created_at': datetime(2024, 12, 3, 16, 45),
        'due_date': datetime(2024, 12, 8),
        'category': 'Work'
    }
]

@app.route('/')
def home():
    filter_status = request.args.get('filter', 'all')
    category = request.args.get('category', 'all')
    
    filtered_todos = todos.copy()
    
    if filter_status == 'completed':
        filtered_todos = [todo for todo in filtered_todos if todo['completed']]
    elif filter_status == 'pending':
        filtered_todos = [todo for todo in filtered_todos if not todo['completed']]
    
    if category != 'all':
        filtered_todos = [todo for todo in filtered_todos if todo['category'] == category]
    
    categories = list(set(todo['category'] for todo in todos))
    stats = {
        'total': len(todos),
        'completed': len([todo for todo in todos if todo['completed']]),
        'pending': len([todo for todo in todos if not todo['completed']]),
        'high_priority': len([todo for todo in todos if todo['priority'] == 'high' and not todo['completed']])
    }
    
    return render_template('index.html', todos=filtered_todos, categories=categories, stats=stats, current_filter=filter_status, current_category=category, now=datetime.now())

@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        new_todo = {
            'id': max([todo['id'] for todo in todos]) + 1 if todos else 1,
            'task': request.form['task'],
            'description': request.form['description'],
            'priority': request.form['priority'],
            'completed': False,
            'created_at': datetime.now(),
            'due_date': datetime.strptime(request.form['due_date'], '%Y-%m-%d') if request.form['due_date'] else None,
            'category': request.form['category']
        }
        todos.append(new_todo)
        flash('Task added successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_todo.html', now=datetime.now())

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if not todo:
        flash('Task not found!', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        todo['task'] = request.form['task']
        todo['description'] = request.form['description']
        todo['priority'] = request.form['priority']
        todo['due_date'] = datetime.strptime(request.form['due_date'], '%Y-%m-%d') if request.form['due_date'] else None
        todo['category'] = request.form['category']
        flash('Task updated successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('edit_todo.html', todo=todo)

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        todo['completed'] = not todo['completed']
        status = 'completed' if todo['completed'] else 'pending'
        flash(f'Task marked as {status}!', 'success')
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/api/stats')
def api_stats():
    stats = {
        'total': len(todos),
        'completed': len([todo for todo in todos if todo['completed']]),
        'pending': len([todo for todo in todos if not todo['completed']]),
        'high_priority': len([todo for todo in todos if todo['priority'] == 'high' and not todo['completed']]),
        'categories': {}
    }
    
    for todo in todos:
        category = todo['category']
        if category not in stats['categories']:
            stats['categories'][category] = {'total': 0, 'completed': 0}
        stats['categories'][category]['total'] += 1
        if todo['completed']:
            stats['categories'][category]['completed'] += 1
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
