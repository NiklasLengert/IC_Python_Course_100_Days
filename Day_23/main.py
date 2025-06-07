import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()
screen.listen()
screen.onkey(player.move_up, "Up")
screen.onkey(player.move_down, "Down")


game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car_manager.create_car()
    car_manager.move_cars()

    # Check for collision with cars
    for car in car_manager.cars:
        if player.distance(car) < 20:  # Adjust the distance threshold as needed
            game_is_on = False
            scoreboard.game_over()

    # Check if player has reached the finish line
    if player.ycor() > 280:
        player.reset_position()
        car_manager.increase_speed()
        scoreboard.increase_level()

screen.exitonclick()

