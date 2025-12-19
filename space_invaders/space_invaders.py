"""
👾 Space Invaders
Classic arcade shooter - destroy the alien invasion!

Controls:
- Left/Right arrows or A/D to move
- SPACE to shoot
- ESC to quit
- R to restart after game over
"""

import pygame
import random
import sys
import asyncio

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (150, 0, 255)

class Player:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - 60
        self.speed = 7
        self.color = GREEN
    
    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
    
    def draw(self, screen):
        # Draw spaceship shape
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, self.color, points)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
    def __init__(self, x, y, direction=-1, color=YELLOW):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 15
        self.speed = 10
        self.direction = direction
        self.color = color
    
    def update(self):
        self.y += self.speed * self.direction
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Alien:
    def __init__(self, x, y, alien_type=0):
        self.width = 40
        self.height = 30
        self.x = x
        self.y = y
        self.alien_type = alien_type
        self.colors = [CYAN, PURPLE, RED]
        self.points = [10, 20, 30]
    
    def draw(self, screen):
        color = self.colors[self.alien_type % 3]
        # Draw alien body
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=5)
        # Draw eyes
        eye_y = self.y + 8
        pygame.draw.circle(screen, WHITE, (self.x + 12, eye_y), 5)
        pygame.draw.circle(screen, WHITE, (self.x + 28, eye_y), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 12, eye_y), 2)
        pygame.draw.circle(screen, BLACK, (self.x + 28, eye_y), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_points(self):
        return self.points[self.alien_type % 3]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
        
    def reset_game(self):
        self.player = Player()
        self.bullets = []
        self.aliens = []
        self.score = 0
        self.game_over = False
        
        # Create alien grid
        for row in range(5):
            for col in range(10):
                x = 50 + col * 60
                y = 50 + row * 40
                self.aliens.append(Alien(x, y, row))
                
        self.alien_direction = 1
        self.alien_speed = 1
        self.alien_move_counter = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.bullets.append(Bullet(self.player.x + self.player.width // 2 - 2, self.player.y))
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        
        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-1)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(1)
        
        return True

    def update(self):
        if self.game_over:
            return

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0 or bullet.y > WINDOW_HEIGHT:
                self.bullets.remove(bullet)
        
        # Update aliens
        move_aliens = False
        self.alien_move_counter += 1
        if self.alien_move_counter >= 60 - min(50, self.score // 10): # Speed up as score increases
            self.alien_move_counter = 0
            move_aliens = True
            
        edge_hit = False
        if move_aliens:
            for alien in self.aliens:
                alien.x += 10 * self.alien_direction
                if alien.x <= 0 or alien.x + alien.width >= WINDOW_WIDTH:
                    edge_hit = True
            
            if edge_hit:
                self.alien_direction *= -1
                for alien in self.aliens:
                    alien.y += 20
                    if alien.y + alien.height >= self.player.y:
                        self.game_over = True

        # Collisions
        player_rect = self.player.get_rect()
        for alien in self.aliens:
            if player_rect.colliderect(alien.get_rect()):
                self.game_over = True
            
        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for alien in self.aliens[:]:
                if bullet_rect.colliderect(alien.get_rect()):
                    self.aliens.remove(alien)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.score += alien.get_points()
                    break
        
        if not self.aliens:
            self.game_over = True # Win condition effectively, or next level could be added

    def draw(self):
        self.screen.fill(BLACK)
        
        self.player.draw(self.screen)
        
        for alien in self.aliens:
            alien.draw(self.screen)
            
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
            
        pygame.display.flip()

    async def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            # This is crucial for web capability
            await asyncio.sleep(0) 

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
