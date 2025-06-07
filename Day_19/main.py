from turtle import Turtle, Screen, pencolor
import random as r

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput("Make your bet.", "Which turtle will win? Enter a color:")
colors = ["blue", "red", "purple", "green", "yellow"]
is_race_on = False
all_turtles = []

if user_bet:
    is_race_on = True

for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index % len(colors)])
    new_turtle.penup()
    new_turtle.goto(-240, 150 - (turtle_index * 50))
    all_turtles.append(new_turtle)

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            print(f"The {turtle.pencolor()} turtle wins!")
            if turtle.pencolor() == user_bet:
                print("Congratulations! You win!")
            else:
                print("Sorry, you lose.")
        
        random_distance = r.randint(0, 10)
        turtle.forward(random_distance)

            
        



screen.exitonclick()

# def move_forward():
#     tim.setheading(0)
#     tim.forward(10)

# def move_backward():
#     tim.setheading(180)
#     tim.forward(10)

# def move_up():
#     tim.setheading(90)
#     tim.forward(10)

# def move_down():
#     tim.setheading(270)
#     tim.forward(10)

# def clear_screen():
#     tim.clear()
#     tim.penup()
#     tim.home()
#     tim.pendown()

# screen.listen()
# screen.onkey(key="w", fun=move_up)
# screen.onkey(key="s", fun=move_down)
# screen.onkey(key="a", fun=move_backward)
# screen.onkey(key="d", fun=move_forward)
# screen.onkey(key="c", fun=clear_screen)
# screen.title("Turtle Movement Control")
# screen.bgcolor("lightblue")

# screen.exitonclick()