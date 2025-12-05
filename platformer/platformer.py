"""
🎮 Platformer
Jump and run to reach the flag!

Controls:
- Left/Right arrows to move
- SPACE to jump
- R to restart, ESC to quit
"""

import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 450

# Beautiful sky gradient colors
SKY_TOP = (135, 206, 250)
SKY_BOTTOM = (200, 230, 255)

# Platform colors
GRASS = (80, 180, 80)
GRASS_TOP = (100, 220, 100)
DIRT = (139, 90, 60)
DIRT_DARK = (100, 65, 40)

# Player colors
PLAYER_BODY = (255, 100, 100)
PLAYER_FACE = (255, 200, 180)
PLAYER_EYE = (50, 50, 50)

# Decorative colors
CLOUD = (255, 255, 255)
SUN = (255, 230, 100)
FLAG_RED = (255, 60, 60)
FLAG_POLE = (200, 200, 200)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 35, 45)
        self.vy = 0
        self.on_ground = False
        self.facing_right = True
        self.walk_frame = 0
    
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 6
            self.facing_right = False
            self.walk_frame += 0.3
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 6
            self.facing_right = True
            self.walk_frame += 0.3
        
        self.vy += 0.8
        self.rect.y += self.vy
        
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p['rect']):
                if self.vy > 0:
                    self.rect.bottom = p['rect'].top
                    self.vy = 0
                    self.on_ground = True
        
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        if self.rect.top > HEIGHT:
            self.rect.topleft = (50, 300)
            self.vy = 0
    
    def jump(self):
        if self.on_ground:
            self.vy = -16
    
    def draw(self, screen):
        x, y = self.rect.x, self.rect.y
        
        # Body bounce animation
        bounce = abs(math.sin(self.walk_frame)) * 3 if self.on_ground else 0
        
        # Shadow
        pygame.draw.ellipse(screen, (0, 0, 0, 50), (x, self.rect.bottom - 5, 35, 10))
        
        # Body
        pygame.draw.rect(screen, PLAYER_BODY, (x + 5, y + 15 - bounce, 25, 30), border_radius=8)
        
        # Head
        pygame.draw.circle(screen, PLAYER_FACE, (x + 17, y + 12 - bounce), 14)
        
        # Eyes
        eye_offset = 4 if self.facing_right else -4
        pygame.draw.circle(screen, WHITE, (x + 17 + eye_offset, y + 10 - bounce), 5)
        pygame.draw.circle(screen, PLAYER_EYE, (x + 17 + eye_offset + 1, y + 10 - bounce), 2)
        
        # Smile
        pygame.draw.arc(screen, PLAYER_EYE, (x + 10, y + 8 - bounce, 14, 14), 3.5, 6, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🎮 Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 28)
        self.reset()
    
    def draw_sky(self):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * ratio)
            g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * ratio)
            b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
    
    def draw_clouds(self):
        clouds = [(100, 60), (300, 40), (550, 70), (700, 30)]
        for cx, cy in clouds:
            pygame.draw.ellipse(self.screen, CLOUD, (cx, cy, 80, 40))
            pygame.draw.ellipse(self.screen, CLOUD, (cx + 20, cy - 15, 60, 35))
            pygame.draw.ellipse(self.screen, CLOUD, (cx + 50, cy, 70, 35))
    
    def draw_sun(self):
        pygame.draw.circle(self.screen, SUN, (700, 80), 50)
        # Sun rays
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x1 = 700 + math.cos(rad) * 55
            y1 = 80 + math.sin(rad) * 55
            x2 = 700 + math.cos(rad) * 70
            y2 = 80 + math.sin(rad) * 70
            pygame.draw.line(self.screen, SUN, (x1, y1), (x2, y2), 3)
    
    def reset(self):
        self.player = Player(50, 300)
        self.platforms = [
            {'rect': pygame.Rect(0, 380, 220, 70)},
            {'rect': pygame.Rect(270, 320, 160, 25)},
            {'rect': pygame.Rect(480, 260, 160, 25)},
            {'rect': pygame.Rect(350, 190, 120, 25)},
            {'rect': pygame.Rect(520, 130, 160, 25)},
            {'rect': pygame.Rect(700, 190, 100, 25)},
        ]
        self.goal = pygame.Rect(750, 145, 35, 45)
        self.won = False
        self.coins_collected = 0
    
    def draw_platform(self, p):
        rect = p['rect']
        # Dirt layer
        pygame.draw.rect(self.screen, DIRT, rect)
        pygame.draw.rect(self.screen, DIRT_DARK, (rect.x, rect.y + rect.height - 5, rect.width, 5))
        # Grass layer
        pygame.draw.rect(self.screen, GRASS, (rect.x, rect.y, rect.width, 12))
        pygame.draw.rect(self.screen, GRASS_TOP, (rect.x, rect.y, rect.width, 5))
        # Grass blades
        for gx in range(rect.x + 5, rect.x + rect.width - 5, 15):
            pygame.draw.line(self.screen, GRASS_TOP, (gx, rect.y), (gx - 3, rect.y - 8), 2)
            pygame.draw.line(self.screen, GRASS_TOP, (gx + 5, rect.y), (gx + 8, rect.y - 6), 2)
    
    def draw_flag(self):
        # Pole
        pygame.draw.rect(self.screen, FLAG_POLE, (self.goal.x + 5, self.goal.y - 10, 6, self.goal.height + 10))
        # Flag
        flag_wave = math.sin(pygame.time.get_ticks() * 0.005) * 3
        points = [
            (self.goal.x + 11, self.goal.y - 5),
            (self.goal.x + 45 + flag_wave, self.goal.y + 10),
            (self.goal.x + 11, self.goal.y + 25)
        ]
        pygame.draw.polygon(self.screen, FLAG_RED, points)
        # Star on flag
        pygame.draw.circle(self.screen, GOLD, (self.goal.x + 28, self.goal.y + 10), 6)
    
    def draw(self):
        self.draw_sky()
        self.draw_sun()
        self.draw_clouds()
        
        for p in self.platforms:
            self.draw_platform(p)
        
        self.draw_flag()
        self.player.draw(self.screen)
        
        if self.won:
            # Victory overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 150))
            self.screen.blit(overlay, (0, 0))
            
            text = self.font.render("🎉 You Win! 🎉", True, (50, 50, 50))
            hint = self.small_font.render("Press R to play again", True, (80, 80, 80))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if event.key == pygame.K_SPACE: self.player.jump()
            
            if not self.won:
                self.player.update(self.platforms)
                if self.player.rect.colliderect(self.goal):
                    self.won = True
            
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
