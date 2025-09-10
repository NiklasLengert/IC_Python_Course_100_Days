import pygame
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = 5
        self.bullets = []
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            
    def shoot(self):
        bullet = Bullet(self.x + self.width // 2, self.y)
        self.bullets.append(bullet)
        
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
                
    def draw(self, screen):
        # Draw player ship
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # Add ship detail
        pygame.draw.polygon(screen, (0, 200, 0), [
            (self.x + self.width//2, self.y),
            (self.x + 10, self.y + self.height),
            (self.x + self.width - 10, self.y + self.height)
        ])
        for bullet in self.bullets:
            bullet.draw(screen)

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 0.8  # Faster movement
        
    def move(self, direction):
        self.x += direction * self.speed
        
    def drop_down(self):
        self.y += 15  # Smaller drop
        
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Add simple alien design
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x + self.width//2), int(self.y + 10)), 5)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 7
        
    def move(self):
        self.y -= self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.aliens = []
        self.alien_direction = 1
        self.alien_move_timer = 0
        self.alien_move_delay = 20 
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.create_alien_fleet()
        
    def create_alien_fleet(self):
        rows = 5
        cols = 10
        for row in range(rows):
            for col in range(cols):
                alien_x = 75 + col * 60
                alien_y = 50 + row * 50
                alien = Alien(alien_x, alien_y)
                self.aliens.append(alien)
                
    def check_collisions(self):
        for bullet in self.player.bullets[:]:
            for alien in self.aliens[:]:
                if (bullet.x < alien.x + alien.width and
                    bullet.x + bullet.width > alien.x and
                    bullet.y < alien.y + alien.height and
                    bullet.y + bullet.height > alien.y):
                    self.player.bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.score += 10
                    break
                    
    def move_aliens(self):
        edge_hit = False
        
        for alien in self.aliens:
            if alien.x <= 0 or alien.x >= SCREEN_WIDTH - alien.width:
                edge_hit = True
                break
                
        if edge_hit:
            self.alien_direction *= -1
            for alien in self.aliens:
                alien.drop_down()
        else:
            for alien in self.aliens:
                alien.move(self.alien_direction)
    
    def check_game_over(self):
        # Check if aliens reached the player area (not bottom)
        for alien in self.aliens:
            if alien.y + alien.height >= self.player.y - 50:
                return True
        return False
        
    def draw_text(self, text, x, y, color=WHITE):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
        
    def run(self):
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()
                        
            # Handle continuous key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()
                
            # Update game objects
            self.player.update_bullets()
            
            # Move aliens with timing
            self.alien_move_timer += 1
            if self.alien_move_timer >= self.alien_move_delay:
                self.move_aliens()
                self.alien_move_timer = 0
                
            self.check_collisions()
            
            # Check game over
            if self.check_game_over():
                print(f"Game Over! Aliens reached you! Final Score: {self.score}")
                running = False
            elif not self.aliens:
                print(f"You Win! All aliens defeated! Final Score: {self.score}")
                running = False
                
            # Draw everything
            self.screen.fill(BLACK)
            self.player.draw(self.screen)
            
            for alien in self.aliens:
                alien.draw(self.screen)
                
            # Draw UI
            self.draw_text(f"Score: {self.score}", 10, 10)
            self.draw_text(f"Aliens: {len(self.aliens)}", 10, 50)
            self.draw_text("Use ARROW KEYS to move, SPACE to shoot", 10, SCREEN_HEIGHT - 30)
            
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

def main():
    print("=== SPACE INVADERS ===")
    print("Controls:")
    print("- Left/Right Arrow Keys: Move")
    print("- Spacebar: Shoot")
    print("- Close window to quit")
    print("\nStarting game...")
    
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
