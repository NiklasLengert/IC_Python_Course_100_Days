from flask import Flask
app = Flask(__name__)

def make_bold(function):
    def wrapper():
        return f"<b>{function()}</b>"
    return wrapper

def make_underline(function):
    def wrapper():
        return f"<u>{function()}</u>"
    return wrapper

def make_italic(function):
    def wrapper():
        return f"<i>{function()}</i>"
    return wrapper

@app.route('/')
def hello_world():
    return '<h1 style="text-align: center;">Hello, Flask!</h1>\n<p>Welcome to the Flask app!</p>'

@app.route('/bye')
def say_bye():
    return "Bye!"

@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)
