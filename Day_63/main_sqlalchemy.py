from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os

'''
SQLAlchemy version - This shows how you would typically use SQLAlchemy with Flask.
Note: May have compatibility issues with Python 3.13
'''

# Create the Flask application
app = Flask(__name__)

# Configure the SQLite database
database_path = os.path.join(os.path.dirname(__file__), 'new-books-collection.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    __tablename__ = 'books'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=float(request.form["rating"])
        )
        
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


with app.app_context():
    db.create_all()
    print("Database tables created!")

    existing_book = db.session.execute(db.select(Book)).first()
    if not existing_book:
        sample_book = Book(
            title="Harry Potter",
            author="J. K. Rowling",
            rating=9.3
        )
        
        db.session.add(sample_book)
        db.session.commit()
        print("Sample book added to database!")


if __name__ == "__main__":
    app.run(debug=True)
