"""
🔨 Whack-a-Mole
Click the moles before they hide!

Controls:
- Click moles to whack them
- R to restart, ESC to quit
"""

import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 500
BROWN = (139, 90, 43)
DARK_BROWN = (100, 60, 20)
GREEN = (50, 150, 50)
BLACK = (20, 20, 30)
WHITE = (255, 255, 255)

class Mole:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visible = False
        self.timer = 0
        self.hit = False
    
    def update(self):
        if self.visible:
            self.timer -= 1
            if self.timer <= 0:
                self.visible = False
                self.hit = False
    
    def show(self):
        if not self.visible:
            self.visible = True
            self.timer = random.randint(40, 80)
            self.hit = False
    
    def draw(self, screen):
        # Draw hole
        pygame.draw.ellipse(screen, DARK_BROWN, (self.x - 50, self.y + 20, 100, 40))
        pygame.draw.ellipse(screen, BLACK, (self.x - 40, self.y + 25, 80, 30))
        
        if self.visible and not self.hit:
            # Draw mole
            pygame.draw.circle(screen, BROWN, (self.x, self.y), 35)
            pygame.draw.circle(screen, BROWN, (self.x, self.y + 30), 25)
            # Eyes
            pygame.draw.circle(screen, WHITE, (self.x - 12, self.y - 5), 8)
            pygame.draw.circle(screen, WHITE, (self.x + 12, self.y - 5), 8)
            pygame.draw.circle(screen, BLACK, (self.x - 12, self.y - 5), 4)
            pygame.draw.circle(screen, BLACK, (self.x + 12, self.y - 5), 4)
            # Nose
            pygame.draw.circle(screen, (255, 150, 150), (self.x, self.y + 10), 8)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🔨 Whack-a-Mole")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()
    
    def reset(self):
        positions = [(150, 150), (300, 150), (450, 150),
                    (150, 280), (300, 280), (450, 280),
                    (150, 410), (300, 410), (450, 410)]
        self.moles = [Mole(x, y) for x, y in positions]
        self.score = 0
        self.time_left = 30 * 60  # 30 seconds
        self.spawn_timer = 0
        self.game_over = False
    
    def update(self):
        if self.game_over:
            return
        
        self.time_left -= 1
        if self.time_left <= 0:
            self.game_over = True
        
        for mole in self.moles:
            mole.update()
        
        self.spawn_timer += 1
        if self.spawn_timer >= 30:
            hidden = [m for m in self.moles if not m.visible]
            if hidden:
                random.choice(hidden).show()
            self.spawn_timer = 0
    
    def click(self, pos):
        for mole in self.moles:
            if mole.visible and not mole.hit:
                dist = ((pos[0] - mole.x) ** 2 + (pos[1] - mole.y) ** 2) ** 0.5
                if dist < 40:
                    mole.hit = True
                    mole.visible = False
                    self.score += 1
    
    def draw(self):
        self.screen.fill(GREEN)
        
        for mole in self.moles:
            mole.draw(self.screen)
        
        # Draw HUD
        text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))
        time_text = self.font.render(f"Time: {self.time_left // 60}", True, WHITE)
        self.screen.blit(time_text, (WIDTH - 120, 10))
        
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            text = self.font.render(f"Time's Up! Score: {self.score}", True, WHITE)
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
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self.click(event.pos)
            
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
