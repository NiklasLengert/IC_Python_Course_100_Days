import turtle as t 
from turtle import Screen
from random import choice

t.colormode(255)

def random_color():
    r = choice(range(256))
    g = choice(range(256))
    b = choice(range(256))
    return (r, g, b)


tim = t.Turtle()
tim.shape("turtle")
tim.color("coral")

# for _ in range(4):
#     tim.forward(100)
#     tim.right(90)

# colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", 
#           "coral", "cyan", "magenta", "lime", "teal", "navy", "maroon", "olive", "gray", "gold", "silver"]
# for x in range(3, 10):
#     choosen_color = choice(colors)
#     tim.color(choosen_color)
#     for y in range(x):
#         tim.forward(100)
#         tim.right(360 / x)

# tim.speed("fastest")
# tim.pensize(15)
# for _ in range(800):
#     tim.forward(30)
#     tim.setheading(choice([0, 90, 180, 270]))
#     tim.color(choice(["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", 
#                       "black", "coral", "cyan", "magenta", "lime", "teal", "navy", 
#                       "maroon", "olive", "gray", "gold", "silver"]))

tim.speed("fastest")
def draw_spirograph(size_of_gap):
    for angle in range(0, 360, size_of_gap):
        tim.color(random_color())
        tim.circle(100)
        tim.setheading(angle)
draw_spirograph(12)

screen = Screen()
screen.exitonclick()