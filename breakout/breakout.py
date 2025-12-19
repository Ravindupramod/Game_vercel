"""
🧱 Breakout
Break all the bricks with the ball!

Controls:
- Left/Right arrows or A/D to move paddle
- SPACE to launch ball
- ESC to quit, R to restart
"""

import pygame
import sys
import asyncio
import math

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_SIZE = 12
BRICK_WIDTH, BRICK_HEIGHT = 75, 25

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
COLORS = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,127,255), (139,0,255)]

class Paddle:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2
        self.y = WINDOW_HEIGHT - 50
        self.speed = 10
    
    def move(self, direction):
        self.x = max(0, min(WINDOW_WIDTH - PADDLE_WIDTH, self.x + direction * self.speed))
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=5)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

class Ball:
    def __init__(self, paddle):
        self.paddle = paddle
        self.reset()
    
    def reset(self):
        self.x = self.paddle.x + PADDLE_WIDTH // 2
        self.y = self.paddle.y - BALL_SIZE
        self.angle = -math.pi / 4
        self.speed = 6
        self.active = False
    
    def update(self):
        if not self.active:
            self.x = self.paddle.x + PADDLE_WIDTH // 2
            self.y = self.paddle.y - BALL_SIZE
            return
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        if self.x <= 0 or self.x >= WINDOW_WIDTH - BALL_SIZE:
            self.angle = math.pi - self.angle
        if self.y <= 0:
            self.angle = -self.angle
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BALL_SIZE // 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - BALL_SIZE//2, self.y - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

class Brick:
    def __init__(self, x, y, color, points):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
        self.color = color
        self.points = points
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🧱 Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.reset()
    
    def reset(self):
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = []
        self.score, self.lives = 0, 3
        self.game_over = self.victory = False
        for row in range(6):
            for col in range(10):
                self.bricks.append(Brick(col * BRICK_WIDTH + 10, row * BRICK_HEIGHT + 60, 
                                        COLORS[row], (6 - row) * 10))
    
    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: self.reset()
                    if event.key == pygame.K_SPACE: self.ball.active = True
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: self.paddle.move(-1)
            if keys[pygame.K_RIGHT]: self.paddle.move(1)
            
            if not self.game_over and not self.victory:
                self.ball.update()
                if self.ball.get_rect().colliderect(self.paddle.get_rect()) and self.ball.active:
                    hit_pos = (self.ball.x - self.paddle.x) / PADDLE_WIDTH
                    self.ball.angle = -math.pi/2 + (hit_pos - 0.5) * math.pi * 0.6
                for brick in self.bricks[:]:
                    if self.ball.get_rect().colliderect(brick.rect):
                        self.score += brick.points
                        self.bricks.remove(brick)
                        self.ball.angle = -self.ball.angle
                        break
                if self.ball.y > WINDOW_HEIGHT:
                    self.lives -= 1
                    self.ball.reset() if self.lives > 0 else None
                    self.game_over = self.lives <= 0
                self.victory = not self.bricks
            
            self.screen.fill(BLACK)
            for brick in self.bricks: brick.draw(self.screen)
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            self.screen.blit(self.font.render(f"Score: {self.score}  Lives: {self.lives}", True, WHITE), (10, 10))
            if self.game_over or self.victory:
                text = "YOU WIN!" if self.victory else "GAME OVER"
                self.screen.blit(self.font.render(text, True, WHITE), (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2))
            pygame.display.flip()
            self.clock.tick(60)

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())