"""
🐸 Frogger
Help the frog cross the road and river!

Controls:
- Arrow keys to move
- R to restart, ESC to quit
"""

import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 50
ROWS = 12
GREEN = (50, 150, 50)
DARK_GREEN = (30, 100, 30)
GRAY = (80, 80, 80)
BLUE = (50, 100, 200)
BROWN = (139, 90, 43)
RED = (200, 50, 50)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🐸 Frogger")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()
    
    def reset(self):
        self.frog = [WIDTH // 2, HEIGHT - CELL]
        self.cars = []
        self.logs = []
        self.score = 0
        self.lives = 3
        self.on_log = None
        self.game_over = False
        
        # Create cars (rows 7-10)
        for row in range(7, 11):
            speed = random.choice([-3, -2, 2, 3])
            for _ in range(3):
                self.cars.append({
                    'x': random.randint(0, WIDTH),
                    'y': row * CELL,
                    'speed': speed,
                    'width': random.randint(60, 100),
                    'color': random.choice([RED, YELLOW, (100, 100, 255)])
                })
        
        # Create logs (rows 2-5)
        for row in range(2, 6):
            speed = random.choice([-2, -1, 1, 2])
            for _ in range(3):
                self.logs.append({
                    'x': random.randint(0, WIDTH),
                    'y': row * CELL,
                    'speed': speed,
                    'width': random.randint(80, 150)
                })
    
    def move_frog(self, dx, dy):
        if self.game_over:
            return
        self.frog[0] = max(0, min(WIDTH - CELL, self.frog[0] + dx))
        self.frog[1] = max(0, min(HEIGHT - CELL, self.frog[1] + dy))
        self.on_log = None
        
        # Check if reached top
        if self.frog[1] == 0:
            self.score += 10
            self.frog = [WIDTH // 2, HEIGHT - CELL]
    
    def update(self):
        if self.game_over:
            return
        
        # Move cars
        for car in self.cars:
            car['x'] += car['speed']
            if car['x'] > WIDTH + 50: car['x'] = -car['width']
            if car['x'] < -car['width'] - 50: car['x'] = WIDTH
        
        # Move logs
        for log in self.logs:
            log['x'] += log['speed']
            if log['x'] > WIDTH + 50: log['x'] = -log['width']
            if log['x'] < -log['width'] - 50: log['x'] = WIDTH
        
        # Move frog with log
        if self.on_log:
            self.frog[0] += self.on_log['speed']
        
        frog_rect = pygame.Rect(self.frog[0], self.frog[1], CELL - 5, CELL - 5)
        
        # Check car collision
        for car in self.cars:
            car_rect = pygame.Rect(car['x'], car['y'] + 5, car['width'], CELL - 10)
            if frog_rect.colliderect(car_rect):
                self.die()
                return
        
        # Check if in water
        if 2 * CELL <= self.frog[1] < 6 * CELL:
            on_log = False
            for log in self.logs:
                log_rect = pygame.Rect(log['x'], log['y'], log['width'], CELL)
                if frog_rect.colliderect(log_rect):
                    on_log = True
                    self.on_log = log
                    break
            if not on_log:
                self.die()
        
        # Check boundaries
        if self.frog[0] < 0 or self.frog[0] > WIDTH - CELL:
            self.die()
    
    def die(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self.frog = [WIDTH // 2, HEIGHT - CELL]
            self.on_log = None
    
    def draw(self):
        self.screen.fill(GREEN)
        
        # Draw water
        pygame.draw.rect(self.screen, BLUE, (0, CELL, WIDTH, 5 * CELL))
        
        # Draw road
        pygame.draw.rect(self.screen, GRAY, (0, 6 * CELL, WIDTH, 5 * CELL))
        for y in range(7, 11):
            pygame.draw.line(self.screen, WHITE, (0, y * CELL + CELL // 2), 
                           (WIDTH, y * CELL + CELL // 2), 2)
        
        # Draw goal zone
        pygame.draw.rect(self.screen, DARK_GREEN, (0, 0, WIDTH, CELL))
        
        # Draw logs
        for log in self.logs:
            pygame.draw.rect(self.screen, BROWN, 
                           (log['x'], log['y'] + 5, log['width'], CELL - 10), border_radius=5)
        
        # Draw cars
        for car in self.cars:
            pygame.draw.rect(self.screen, car['color'],
                           (car['x'], car['y'] + 8, car['width'], CELL - 16), border_radius=5)
        
        # Draw frog
        pygame.draw.circle(self.screen, (100, 200, 100), 
                          (self.frog[0] + CELL // 2, self.frog[1] + CELL // 2), CELL // 2 - 5)
        pygame.draw.circle(self.screen, WHITE, (self.frog[0] + 12, self.frog[1] + 15), 5)
        pygame.draw.circle(self.screen, WHITE, (self.frog[0] + 35, self.frog[1] + 15), 5)
        
        # Draw HUD
        text = self.font.render(f"Score: {self.score}  Lives: {self.lives}", True, WHITE)
        self.screen.blit(text, (10, HEIGHT - 35))
        
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            text = self.font.render(f"Game Over! Score: {self.score}", True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if event.key == pygame.K_UP: self.move_frog(0, -CELL)
                    if event.key == pygame.K_DOWN: self.move_frog(0, CELL)
                    if event.key == pygame.K_LEFT: self.move_frog(-CELL, 0)
                    if event.key == pygame.K_RIGHT: self.move_frog(CELL, 0)
            
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
