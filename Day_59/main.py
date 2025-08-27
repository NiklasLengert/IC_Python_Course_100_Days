from flask import Flask, render_template, request
import requests

app = Flask(__name__)

posts = requests.get("https://api.npoint.io/82eda33aefdd057fc373").json()


@app.route("/")
def home():
    return render_template("index.html", posts=posts['posts'])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Message: {message}")
        
        return "<h1>Successfully sent your message</h1>"
    else:
        return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
