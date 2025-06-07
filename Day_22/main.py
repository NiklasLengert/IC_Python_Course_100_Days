from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=800, height=600)
screen.title("Pong Game")
screen.bgcolor("black")
screen.tracer(0)

paddle = Paddle((350, 0))
paddle2 = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()



screen.listen()
screen.onkey(paddle.go_up, "Up")
screen.onkey(paddle.go_down, "Down")
screen.onkey(paddle2.go_up, "w")
screen.onkey(paddle2.go_down, "s")

game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    if(ball.ycor() > 280 or ball.ycor() < -280):
        ball.bounce_y()

    if(ball.xcor() > 320 and ball.distance(paddle) < 50) or (ball.xcor() < -320 and ball.distance(paddle2) < 50):
        ball.bounce_x()

    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.increase_l_score()


    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.increase_r_score()

    if scoreboard.l_score == 5 or scoreboard.r_score == 5:
        game_is_on = False
        if scoreboard.l_score == 5:
            print("Left Player Wins!")
        else:
            print("Right Player Wins!")


















screen.exitonclick()