from flask import Flask
import random as rd

random_number = rd.randint(0, 10)

app = Flask(__name__)

@app.route('/')
def home():
    return """
        <h1>Welcome to the Higher Lower Game!</h1><br>
        <img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" alt="Higher Lower Game">
    """

@app.route('/<int:guess>')
def guess_number(guess):
    if guess < random_number:
        return "<h1>Too low! Try again.</h1><br><img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif' alt='Too Low'></img>"
    elif guess > random_number:
        return "<h1>Too high! Try again.</h1><br><img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif' alt='Too High'></img>"
    else:
        return "<h1>Congratulations! You guessed the number.</h1><br><img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif' alt='Congratulations'></img>"


if __name__ == '__main__':
    app.run(debug=True)