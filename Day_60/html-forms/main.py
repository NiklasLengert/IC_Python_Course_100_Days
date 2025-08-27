from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
    return f"Your username is {username} and your email is {email}"

if __name__ == "__main__":
    app.run(debug=True)
