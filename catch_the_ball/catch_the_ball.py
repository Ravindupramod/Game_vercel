"""
⚽ Catch the Ball
Catch falling balls with your basket!

Controls:
- Left/Right arrows to move
- R to restart, ESC to quit
"""

import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 500
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
BROWN = (139, 90, 43)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("⚽ Catch the Ball")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()
    
    def reset(self):
        self.basket_x = WIDTH // 2
        self.balls = []
        self.score = 0
        self.missed = 0
        self.spawn_timer = 0
        self.game_over = False
    
    def spawn_ball(self):
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        self.balls.append({
            'x': random.randint(30, WIDTH - 30),
            'y': -20,
            'speed': random.uniform(3, 6),
            'color': random.choice(colors),
            'radius': random.randint(15, 25)
        })
    
    def update(self):
        if self.game_over:
            return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.basket_x -= 8
        if keys[pygame.K_RIGHT]: self.basket_x += 8
        self.basket_x = max(40, min(WIDTH - 40, self.basket_x))
        
        self.spawn_timer += 1
        if self.spawn_timer >= 40:
            self.spawn_ball()
            self.spawn_timer = 0
        
        for ball in self.balls[:]:
            ball['y'] += ball['speed']
            
            # Check catch
            if (ball['y'] + ball['radius'] >= HEIGHT - 50 and 
                abs(ball['x'] - self.basket_x) < 50):
                self.score += 1
                self.balls.remove(ball)
            # Check miss
            elif ball['y'] > HEIGHT:
                self.missed += 1
                self.balls.remove(ball)
                if self.missed >= 5:
                    self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw balls
        for ball in self.balls:
            pygame.draw.circle(self.screen, ball['color'], 
                             (int(ball['x']), int(ball['y'])), ball['radius'])
        
        # Draw basket
        pygame.draw.arc(self.screen, BROWN, 
                       (self.basket_x - 40, HEIGHT - 60, 80, 60), 
                       3.14, 0, 8)
        pygame.draw.rect(self.screen, BROWN, 
                        (self.basket_x - 40, HEIGHT - 40, 80, 10))
        
        # Draw HUD
        text = self.font.render(f"Score: {self.score}  Missed: {self.missed}/5", True, WHITE)
        self.screen.blit(text, (10, 10))
        
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            text = self.font.render(f"Game Over! Score: {self.score}", True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
            text2 = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
            
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
