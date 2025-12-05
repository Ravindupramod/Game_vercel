"""
🐍 Snake Game
Classic snake game - eat food to grow, don't hit yourself!

Controls:
- Arrow keys or WASD to move
- ESC to quit, SPACE to restart
"""

import pygame
import random
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Vibrant color palette
BG_TOP = (15, 20, 35)
BG_BOTTOM = (25, 35, 55)
GRID_COLOR = (35, 45, 70)
SNAKE_HEAD = (100, 255, 150)
SNAKE_BODY = (60, 200, 120)
SNAKE_BODY_ALT = (50, 180, 100)
FOOD_COLOR = (255, 100, 120)
FOOD_GLOW = (255, 150, 170)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
SHADOW = (10, 15, 25)

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        self.body.insert(0, new_head)
    
    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.pulse = 0
        self.spawn()
    
    def spawn(self, snake_body=None):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if snake_body is None or self.position not in snake_body:
                break
    
    def update(self):
        self.pulse = (self.pulse + 0.15) % (3.14159 * 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.reset()
    
    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake.body)
        self.score = 0
        self.high_score = getattr(self, 'high_score', 0)
        self.game_over = False
    
    def draw_gradient_bg(self):
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
    
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.change_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.change_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.change_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.change_direction(RIGHT)
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.food.update()
        self.snake.move()
        
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += 10
            self.food.spawn(self.snake.body)
        
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
    
    def draw(self):
        self.draw_gradient_bg()
        self.draw_grid()
        
        # Draw food with glow
        import math
        food_x, food_y = self.food.position
        pulse_size = int(math.sin(self.food.pulse) * 3)
        
        # Glow
        glow_rect = pygame.Rect(
            food_x * GRID_SIZE - pulse_size - 3,
            food_y * GRID_SIZE - pulse_size - 3,
            GRID_SIZE + pulse_size * 2 + 6,
            GRID_SIZE + pulse_size * 2 + 6
        )
        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*FOOD_GLOW, 80), glow_surf.get_rect(), border_radius=8)
        self.screen.blit(glow_surf, glow_rect)
        
        # Food
        food_rect = pygame.Rect(food_x * GRID_SIZE + 2, food_y * GRID_SIZE + 2, GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.rect(self.screen, FOOD_COLOR, food_rect, border_radius=6)
        
        # Draw snake
        for i, segment in enumerate(self.snake.body):
            x, y = segment
            
            if i == 0:
                # Head with glow
                color = SNAKE_HEAD
                rect = pygame.Rect(x * GRID_SIZE + 1, y * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)
                pygame.draw.rect(self.screen, color, rect, border_radius=6)
                # Eyes
                dir_x, dir_y = self.snake.direction
                eye_offset_x = 5 + dir_x * 3
                eye_offset_y = 5 + dir_y * 3
                pygame.draw.circle(self.screen, (40, 40, 40), (x * GRID_SIZE + eye_offset_x + 3, y * GRID_SIZE + eye_offset_y + 3), 3)
                pygame.draw.circle(self.screen, (40, 40, 40), (x * GRID_SIZE + GRID_SIZE - eye_offset_x - 3, y * GRID_SIZE + eye_offset_y + 3), 3)
            else:
                color = SNAKE_BODY if i % 2 == 0 else SNAKE_BODY_ALT
                rect = pygame.Rect(x * GRID_SIZE + 2, y * GRID_SIZE + 2, GRID_SIZE - 4, GRID_SIZE - 4)
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
        
        # HUD
        score_text = self.font.render(f"Score: {self.score}", True, GOLD)
        high_text = self.font.render(f"Best: {self.high_score}", True, (150, 200, 255))
        self.screen.blit(score_text, (15, 10))
        self.screen.blit(high_text, (WINDOW_WIDTH - high_text.get_width() - 15, 10))
        
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((15, 20, 35, 200))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.big_font.render("GAME OVER", True, FOOD_COLOR)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to restart", True, (150, 200, 255))
            
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 70))
            self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(12)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()
