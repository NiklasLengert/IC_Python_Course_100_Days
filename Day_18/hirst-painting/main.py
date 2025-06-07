import colorgram as cg
import turtle as t
from turtle import Screen
from random import choice

def extract_colors(image_path, num_colors):
    colors = cg.extract(image_path, num_colors)
    return [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]

def draw_dots(turtle, colors, num_dots, dot_size, spacing):
    turtle.penup()
    turtle.hideturtle()
    turtle.speed("fastest")

    turtle.setheading(0)
    turtle.goto(-250, -200)  # Starting position
    
    for dot_count in range(num_dots):
        turtle.dot(dot_size, choice(colors))
        turtle.forward(spacing)
        
        if (dot_count + 1) % 10 == 0:
            turtle.setheading(90)
            turtle.forward(spacing)
            turtle.setheading(180)
            turtle.forward(spacing * 10)
            turtle.setheading(0)

def main():
    screen = Screen()
    screen.colormode(255)
    
    colors = extract_colors("Day_18/hirst-painting/image.jpg", 30)
    
    hirst_turtle = t.Turtle()
    hirst_turtle.hideturtle()
    draw_dots(hirst_turtle, colors, 100, 20, 50)
    
    screen.exitonclick()

if __name__ == "__main__":
    main()