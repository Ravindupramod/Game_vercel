"""
🐦 Flappy Bird
Tap to fly through the pipes!

Controls:
- SPACE or UP arrow to flap
- ESC to quit
- R to restart after game over
"""

import pygame
import random
import sys

pygame.init()

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 180
PIPE_SPEED = 3

# Colors
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 223, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.size = 30
        self.angle = 0
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Update angle based on velocity
        self.angle = max(-30, min(30, -self.velocity * 3))
    
    def draw(self, screen):
        # Bird body
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size // 2)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.size // 2, 2)
        
        # Eye
        eye_x = self.x + 8
        eye_y = self.y - 5
        pygame.draw.circle(screen, WHITE, (int(eye_x), int(eye_y)), 6)
        pygame.draw.circle(screen, BLACK, (int(eye_x + 2), int(eye_y)), 3)
        
        # Beak
        beak_points = [
            (self.x + 15, self.y),
            (self.x + 25, self.y + 5),
            (self.x + 15, self.y + 8)
        ]
        pygame.draw.polygon(screen, ORANGE, beak_points)
        
        # Wing
        wing_y_offset = 3 if self.velocity < 0 else -3
        wing_rect = pygame.Rect(self.x - 10, self.y + wing_y_offset, 15, 10)
        pygame.draw.ellipse(screen, ORANGE, wing_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, WINDOW_HEIGHT - 150 - PIPE_GAP)
        self.passed = False
    
    def update(self):
        self.x -= PIPE_SPEED
    
    def draw(self, screen):
        # Top pipe
        top_height = self.gap_y
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, top_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, top_height - 30, PIPE_WIDTH + 10, 30))
        
        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP
        bottom_height = WINDOW_HEIGHT - bottom_y
        pygame.draw.rect(screen, GREEN, (self.x, bottom_y, PIPE_WIDTH, bottom_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, bottom_y, PIPE_WIDTH + 10, 30))
    
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, WINDOW_HEIGHT - self.gap_y - PIPE_GAP)
        return [top_rect, bottom_rect]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐦 Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.reset()
    
    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.high_score = getattr(self, 'high_score', 0)
        self.game_over = False
        self.started = False
        self.pipe_timer = 0
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r and self.game_over:
                    self.reset()
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not self.started:
                        self.started = True
                    if not self.game_over:
                        self.bird.flap()
        return True
    
    def spawn_pipe(self):
        self.pipes.append(Pipe(WINDOW_WIDTH))
    
    def update(self):
        if self.game_over or not self.started:
            return
        
        self.bird.update()
        
        # Spawn pipes
        self.pipe_timer += 1
        if self.pipe_timer >= 90:
            self.spawn_pipe()
            self.pipe_timer = 0
        
        # Update pipes
        for pipe in self.pipes[:]:
            pipe.update()
            
            # Check if bird passed pipe
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
            
            # Remove off-screen pipes
            if pipe.x + PIPE_WIDTH < 0:
                self.pipes.remove(pipe)
        
        # Check collisions
        bird_rect = self.bird.get_rect()
        
        # Check ground and ceiling
        if self.bird.y - self.bird.size // 2 <= 0 or self.bird.y + self.bird.size // 2 >= WINDOW_HEIGHT:
            self.game_over = True
        
        # Check pipe collisions
        for pipe in self.pipes:
            for rect in pipe.get_rects():
                if bird_rect.colliderect(rect):
                    self.game_over = True
        
        if self.game_over:
            self.high_score = max(self.high_score, self.score)
    
    def draw(self):
        # Sky
        self.screen.fill(SKY_BLUE)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw ground
        pygame.draw.rect(self.screen, BROWN, (0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20))
        pygame.draw.rect(self.screen, GREEN, (0, WINDOW_HEIGHT - 25, WINDOW_WIDTH, 10))
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(str(self.score), True, WHITE)
        score_shadow = self.font.render(str(self.score), True, BLACK)
        self.screen.blit(score_shadow, (WINDOW_WIDTH // 2 - score_text.get_width() // 2 + 2, 52))
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        # Draw start message
        if not self.started and not self.game_over:
            start_text = self.small_font.render("Press SPACE to start", True, WHITE)
            self.screen.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, WINDOW_HEIGHT // 2))
        
        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
            high_score_text = self.small_font.render(f"Best: {self.high_score}", True, YELLOW)
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 80))
            self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 10))
            self.screen.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 25))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 70))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
