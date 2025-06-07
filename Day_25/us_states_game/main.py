import turtle
import os
import pandas as pd


image = os.path.join(os.path.dirname(__file__), "blank_states_img.gif")
data_path = os.path.join(os.path.dirname(__file__), "50_states.csv")

screen = turtle.Screen()
screen.title("U.S. States Game")
screen.addshape(image)
screen.setup(width=725, height=491)
background = turtle.Turtle()
background.shape(image)


answered_state = screen.textinput(title="Guess the State", prompt="What's another state's name?").title()
data = pd.read_csv(data_path)
data_as_list = data["state"].tolist()
data_as_dict = data.to_dict(orient="records")
guessed_states = []

while answered_state != "Exit":
    if answered_state == "Quit":
        missing_states = [state for state in data_as_list if state not in guessed_states]
        missing_states_df = pd.DataFrame(missing_states)
        missing_states_df.to_csv("states_to_learn.csv", index=False)
        turtle.goto(0, 0)
        turtle.write("Thanks for playing! States to learn saved to 'states_to_learn.csv'.", align="center", font=("Arial", 16, "bold"))
        break
    if answered_state != "Quit" and answered_state != "Exit":
        for state in data_as_dict:
            if answered_state == state["state"]:
                guessed_states.append(state["state"])
                x = state["x"]
                y = state["y"]
                turtle.penup()
                turtle.hideturtle()
                turtle.goto(x, y)
                turtle.write(state["state"], align="center", font=("Arial", 8, "normal"))
                answered_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct",
                                                prompt="What's another state's name?").title()
        if len(guessed_states) == 50:
            turtle.goto(0, 0)
            turtle.write("Congratulations! You've guessed all the states!", align="center", font=("Arial", 16, "bold"))
            break
    else:
        turtle.clear()
        turtle.penup()
        turtle.goto(0, 0)
        if answered_state in guessed_states:
            turtle.write("You already guessed that state!", align="center", font=("Arial", 16, "bold"))
        else:
            turtle.write("State not found. Try again!", align="center", font=("Arial", 16, "bold"))
    
    answered_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct", prompt="What's another state's name?").title()
