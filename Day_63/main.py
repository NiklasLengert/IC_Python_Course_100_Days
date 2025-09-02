from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

# Create the Flask application
app = Flask(__name__)

# Database configuration
DATABASE = os.path.join(os.path.dirname(__file__), 'new-books-collection.db')

def init_db():
    """Initialize the database and create the books table"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Create the books table with the required fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                title VARCHAR(250) UNIQUE NOT NULL,
                author VARCHAR(250) NOT NULL,
                rating FLOAT NOT NULL
            )
        ''')

        cursor.execute('SELECT COUNT(*) FROM books')
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute('''
                INSERT INTO books (title, author, rating) 
                VALUES (?, ?, ?)
            ''', ('Harry Potter', 'J. K. Rowling', 9.3))
            
            print("Sample book added to database!")
        
        conn.commit()

def get_all_books():
    """Get all books from the database"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author, rating FROM books ORDER BY title')
        books = cursor.fetchall()
        
        # Convert to list of dictionaries for template
        book_list = []
        for book in books:
            book_list.append({
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'rating': book[3]
            })
        
        return book_list

def add_book(title, author, rating):
    """Add a new book to the database"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, rating) 
            VALUES (?, ?, ?)
        ''', (title, author, float(rating)))
        conn.commit()


@app.route('/')
def home():
    # Get all books from database
    all_books = get_all_books()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get form data and add to database
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        
        add_book(title, author, rating)
        
        # Redirect to home page to show updated book list
        return redirect(url_for('home'))
    
    # If GET request, show the add book form
    return render_template("add.html")


# Initialize the database with Flask app context
with app.app_context():
    init_db()
    print("Database initialized successfully!")


if __name__ == "__main__":
    app.run(debug=True)

