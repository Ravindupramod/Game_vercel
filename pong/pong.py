"""
🏓 Pong
Classic two-player paddle game!

Controls:
- Player 1 (Left): W/S keys
- Player 2 (Right): Up/Down arrows
- SPACE to start/restart
- ESC to quit
"""

import pygame
import sys
import asyncio

pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
WINNING_SCORE = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

class Paddle:
    def __init__(self, x, color):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = x
        self.y = WINDOW_HEIGHT // 2 - self.height // 2
        self.speed = 8
        self.color = color
        self.score = 0
    
    def move(self, direction):
        self.y += direction * self.speed
        self.y = max(0, min(WINDOW_HEIGHT - self.height, self.y))
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=5)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.size = BALL_SIZE
        self.reset()
    
    def reset(self, direction=1):
        self.x = WINDOW_WIDTH // 2 - self.size // 2
        self.y = WINDOW_HEIGHT // 2 - self.size // 2
        self.speed_x = 5 * direction
        self.speed_y = 5
        self.active = False
    
    def update(self):
        if not self.active:
            return
        
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off top and bottom
        if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.size:
            self.speed_y *= -1
            self.y = max(0, min(WINDOW_HEIGHT - self.size, self.y))
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size), border_radius=3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🏓 Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.reset()
    
    def reset(self):
        self.paddle1 = Paddle(30, CYAN)
        self.paddle2 = Paddle(WINDOW_WIDTH - 30 - PADDLE_WIDTH, MAGENTA)
        self.ball = Ball()
        self.game_over = False
        self.winner = None
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    elif not self.ball.active:
                        self.ball.active = True
        
        if not self.game_over:
            keys = pygame.key.get_pressed()
            # Player 1 controls
            if keys[pygame.K_w]:
                self.paddle1.move(-1)
            if keys[pygame.K_s]:
                self.paddle1.move(1)
            # Player 2 controls
            if keys[pygame.K_UP]:
                self.paddle2.move(-1)
            if keys[pygame.K_DOWN]:
                self.paddle2.move(1)
        
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.ball.update()
        
        # Check paddle collisions
        ball_rect = self.ball.get_rect()
        
        if ball_rect.colliderect(self.paddle1.get_rect()):
            self.ball.speed_x = abs(self.ball.speed_x)
            # Add spin based on where ball hits paddle
            relative_y = (self.ball.y + self.ball.size / 2) - (self.paddle1.y + PADDLE_HEIGHT / 2)
            self.ball.speed_y = relative_y * 0.1
            self.ball.x = self.paddle1.x + PADDLE_WIDTH
        
        if ball_rect.colliderect(self.paddle2.get_rect()):
            self.ball.speed_x = -abs(self.ball.speed_x)
            relative_y = (self.ball.y + self.ball.size / 2) - (self.paddle2.y + PADDLE_HEIGHT / 2)
            self.ball.speed_y = relative_y * 0.1
            self.ball.x = self.paddle2.x - self.ball.size
        
        # Check scoring
        if self.ball.x <= 0:
            self.paddle2.score += 1
            self.ball.reset(-1)
        elif self.ball.x >= WINDOW_WIDTH - self.ball.size:
            self.paddle1.score += 1
            self.ball.reset(1)
        
        # Check for winner
        if self.paddle1.score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 1"
        elif self.paddle2.score >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 2"
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw center line
        for y in range(0, WINDOW_HEIGHT, 30):
            pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH // 2 - 2, y, 4, 15))
        
        # Draw paddles
        self.paddle1.draw(self.screen)
        self.paddle2.draw(self.screen)
        
        # Draw ball
        self.ball.draw(self.screen)
        
        # Draw scores
        score1_text = self.font.render(str(self.paddle1.score), True, CYAN)
        score2_text = self.font.render(str(self.paddle2.score), True, MAGENTA)
        self.screen.blit(score1_text, (WINDOW_WIDTH // 4, 20))
        self.screen.blit(score2_text, (3 * WINDOW_WIDTH // 4 - score2_text.get_width(), 20))
        
        # Draw instructions
        if not self.ball.active and not self.game_over:
            instructions = self.small_font.render("Press SPACE to start", True, WHITE)
            self.screen.blit(instructions, (WINDOW_WIDTH // 2 - instructions.get_width() // 2, WINDOW_HEIGHT - 50))
        
        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            winner_color = CYAN if self.winner == "Player 1" else MAGENTA
            winner_text = self.font.render(f"{self.winner} Wins!", True, winner_color)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            
            self.screen.blit(winner_text, (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 30))
        
        pygame.display.flip()
    
    async def run(self):
        running = True
        while running:
            await asyncio.sleep(0)
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())