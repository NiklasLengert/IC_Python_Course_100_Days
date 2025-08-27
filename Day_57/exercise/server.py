from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Try to type 'guess/<your_name>' in the url bar."

@app.route("/guess/<name>")
def guess(name):
    response_age = requests.get(f"https://api.agify.io?name={name}")
    age = response_age.json().get("age", 0)
    response_gender = requests.get(f"https://api.genderize.io?name={name}")
    gender = response_gender.json().get("gender", "Unknown")
    return render_template("index.html", name=name, age=age, gender=gender)

@app.route("/blog")
def get_blog():
    blog_url = " https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    blog_posts = response.json()
    return render_template("blog.html", posts=blog_posts)

if __name__ == "__main__":
    app.run(debug=True)