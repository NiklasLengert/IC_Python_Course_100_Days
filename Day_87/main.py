import turtle
import random

class BreakoutGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("🧱 Breakout Game")
        self.screen.bgcolor("black")
        self.screen.setup(width=800, height=600)
        
        # Game variables
        self.score = 0
        self.lives = 3
        self.ball_speed = 8
        self.game_running = True
        
        self.setup_game()
        self.create_bricks()
        self.setup_controls()
        
        self.screen.update()
        self.screen.ontimer(self.game_step, 20)
    
    def setup_game(self):
        self.paddle = turtle.Turtle()
        self.paddle.speed(0)
        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.penup()
        self.paddle.goto(0, -250)
        self.paddle.shapesize(stretch_wid=1, stretch_len=6)
        
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape("circle")
        self.ball.color("yellow")
        self.ball.penup()
        self.ball.goto(0, -200)
        self.ball.shapesize(2, 2)
        self.ball.showturtle()
        self.ball.dx = random.choice([-self.ball_speed, self.ball_speed])
        self.ball.dy = self.ball_speed
        
        self.score_display = turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-380, 260)
        self.update_score()
        
        self.lives_display = turtle.Turtle()
        self.lives_display.speed(0)
        self.lives_display.color("white")
        self.lives_display.penup()
        self.lives_display.hideturtle()
        self.lives_display.goto(280, 260)
        self.update_lives()
    
    def create_bricks(self):
        self.bricks = []
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        
        for row in range(6):
            for col in range(12):
                brick = turtle.Turtle()
                brick.speed(0)
                brick.shape("square")
                brick.color(colors[row])
                brick.penup()
                x_pos = -350 + col * 60
                y_pos = 150 - row * 25
                brick.goto(x_pos, y_pos)
                brick.shapesize(stretch_wid=1.5, stretch_len=2.5)
                brick.showturtle()
                self.bricks.append(brick)
    
    def setup_controls(self):
        self.screen.listen()
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")
        self.screen.onkey(self.move_left, "a")
        self.screen.onkey(self.move_right, "d")
    
    def move_left(self):
        x = self.paddle.xcor()
        if x > -340:
            self.paddle.setx(x - 20)
    
    def move_right(self):
        x = self.paddle.xcor()
        if x < 340:
            self.paddle.setx(x + 20)
    
    def update_score(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}", align="left", 
                                font=("Arial", 16, "bold"))
    
    def update_lives(self):
        self.lives_display.clear()
        self.lives_display.write(f"Lives: {self.lives}", align="left", 
                                font=("Arial", 16, "bold"))
    
    def reset_ball(self):
        self.ball.goto(0, -200)
        self.ball.dx = random.choice([-self.ball_speed, self.ball_speed])
        self.ball.dy = self.ball_speed
    
    def check_collision(self, obj1, obj2):
        distance = ((obj1.xcor() - obj2.xcor())**2 + (obj1.ycor() - obj2.ycor())**2)**0.5
        return distance < 30
    
    def game_step(self):
        if not self.game_running:
            return
        
        # Move ball
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)
        
        # Ball collision with walls
        if self.ball.xcor() > 390 or self.ball.xcor() < -390:
            self.ball.dx *= -1
        
        if self.ball.ycor() > 290:
            self.ball.dy *= -1
        
        # Ball falls below paddle
        if self.ball.ycor() < -290:
            self.lives -= 1
            self.update_lives()
            
            if self.lives <= 0:
                self.game_over()
                return
            else:
                self.reset_ball()
        
        if (self.ball.ycor() > -260 and self.ball.ycor() < -240 and
            self.ball.xcor() > self.paddle.xcor() - 60 and
            self.ball.xcor() < self.paddle.xcor() + 60):
            
            hit_pos = (self.ball.xcor() - self.paddle.xcor()) / 60
            self.ball.dx = hit_pos * 4
            self.ball.dy *= -1
            
            if abs(self.ball.dx) < 8:
                self.ball.dx *= 1.05
            if abs(self.ball.dy) < 8:
                self.ball.dy *= 1.05
        
        for brick in self.bricks[:]:
            if self.check_collision(self.ball, brick):
                brick.goto(1000, 1000)
                self.bricks.remove(brick)
                self.ball.dy *= -1
                
                if brick.color()[0] == "red":
                    self.score += 100
                elif brick.color()[0] == "orange":
                    self.score += 90
                elif brick.color()[0] == "yellow":
                    self.score += 80
                elif brick.color()[0] == "green":
                    self.score += 70
                elif brick.color()[0] == "blue":
                    self.score += 60
                else:
                    self.score += 50
                
                self.update_score()
                break
        
        if not self.bricks:
            self.win_game()
            return
        
        self.screen.ontimer(self.game_step, 20)
    
    def game_over(self):
        self.game_running = False
        
        # Display game over message
        game_over_text = turtle.Turtle()
        game_over_text.speed(0)
        game_over_text.color("red")
        game_over_text.penup()
        game_over_text.hideturtle()
        game_over_text.goto(0, 0)
        game_over_text.write("GAME OVER!", align="center", 
                           font=("Arial", 36, "bold"))
        
        final_score = turtle.Turtle()
        final_score.speed(0)
        final_score.color("white")
        final_score.penup()
        final_score.hideturtle()
        final_score.goto(0, -50)
        final_score.write(f"Final Score: {self.score}", align="center", 
                         font=("Arial", 18, "normal"))
        
        restart_text = turtle.Turtle()
        restart_text.speed(0)
        restart_text.color("yellow")
        restart_text.penup()
        restart_text.hideturtle()
        restart_text.goto(0, -100)
        restart_text.write("Press SPACE to play again or ESC to quit", align="center", 
                          font=("Arial", 14, "normal"))
        
        self.screen.onkey(self.restart_game, "space")
        self.screen.onkey(self.quit_game, "Escape")
    
    def win_game(self):
        self.game_running = False
        
        # Display win message
        win_text = turtle.Turtle()
        win_text.speed(0)
        win_text.color("gold")
        win_text.penup()
        win_text.hideturtle()
        win_text.goto(0, 50)
        win_text.write("🎉 YOU WIN! 🎉", align="center", 
                      font=("Arial", 36, "bold"))
        
        final_score = turtle.Turtle()
        final_score.speed(0)
        final_score.color("white")
        final_score.penup()
        final_score.hideturtle()
        final_score.goto(0, 0)
        final_score.write(f"Final Score: {self.score}", align="center", 
                         font=("Arial", 18, "normal"))
        
        bonus_text = turtle.Turtle()
        bonus_text.speed(0)
        bonus_text.color("green")
        bonus_text.penup()
        bonus_text.hideturtle()
        bonus_text.goto(0, -30)
        bonus_text.write("Congratulations! You cleared all bricks!", align="center", 
                        font=("Arial", 14, "normal"))
        
        restart_text = turtle.Turtle()
        restart_text.speed(0)
        restart_text.color("yellow")
        restart_text.penup()
        restart_text.hideturtle()
        restart_text.goto(0, -80)
        restart_text.write("Press SPACE to play again or ESC to quit", align="center", 
                          font=("Arial", 14, "normal"))
        
        self.screen.onkey(self.restart_game, "space")
        self.screen.onkey(self.quit_game, "Escape")
    
    def restart_game(self):
        try:
            self.screen.clear()
            self.__init__()
        except turtle.Terminator:
            pass
    
    def quit_game(self):
        try:
            self.game_running = False
            self.screen.bye()
        except:
            pass

def main():
    try:
        game = BreakoutGame()
        game.screen.mainloop()
    except turtle.Terminator:
        pass

if __name__ == "__main__":
    main()
