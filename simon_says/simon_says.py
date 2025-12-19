"""
🔔 Simon Says
Memory pattern game - repeat the sequence!

Controls:
- Click colored buttons or use 1-4 keys
- R to restart, ESC to quit
"""

import pygame
import random
import sys
import asyncio

pygame.init()

SIZE = 450

# Vibrant neon colors
COLORS_DIM = [(180, 30, 60), (30, 150, 60), (30, 60, 180), (180, 150, 30)]
COLORS_BRIGHT = [(255, 80, 120), (80, 255, 120), (80, 120, 255), (255, 230, 80)]
COLORS_GLOW = [(255, 150, 180), (150, 255, 180), (150, 180, 255), (255, 245, 150)]

BG_TOP = (15, 20, 35)
BG_BOTTOM = (30, 35, 60)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
SHADOW = (10, 15, 25)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIZE, SIZE + 100))
        pygame.display.set_caption("🔔 Simon Says")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 26)
        self.reset()
    
    def draw_gradient(self):
        for y in range(SIZE + 100):
            ratio = y / (SIZE + 100)
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SIZE, y))
    
    def reset(self):
        self.sequence = []
        self.player_seq = []
        self.state = 'showing'
        self.show_idx = 0
        self.show_timer = 0
        self.flash = -1
        self.flash_timer = 0
        self.score = 0
        self.high_score = getattr(self, 'high_score', 0)
        self.game_over = False
        self.next_round()
    
    def next_round(self):
        self.sequence.append(random.randint(0, 3))
        self.player_seq = []
        self.state = 'showing'
        self.show_idx = 0
        self.show_timer = 60
    
    def flash_button(self, idx):
        self.flash = idx
        self.flash_timer = 20
    
    def check_input(self, idx):
        if self.game_over or self.state != 'playing':
            return
        
        self.player_seq.append(idx)
        self.flash_button(idx)
        
        if self.player_seq[-1] != self.sequence[len(self.player_seq) - 1]:
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
            return
        
        if len(self.player_seq) == len(self.sequence):
            self.score += 1
            self.state = 'waiting'
            self.show_timer = 50
    
    def update(self):
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0:
                self.flash = -1
        
        if self.game_over:
            return
        
        if self.state == 'showing':
            self.show_timer -= 1
            if self.show_timer <= 0:
                if self.show_idx < len(self.sequence):
                    self.flash_button(self.sequence[self.show_idx])
                    self.show_idx += 1
                    self.show_timer = max(20, 40 - self.score * 2)
                else:
                    self.state = 'playing'
        
        elif self.state == 'waiting':
            self.show_timer -= 1
            if self.show_timer <= 0:
                self.next_round()
    
    def draw_button(self, idx, x, y, w, h):
        is_flashing = self.flash == idx
        
        # Shadow
        pygame.draw.rect(self.screen, SHADOW, (x + 5, y + 5, w, h), border_radius=20)
        
        # Main button
        color = COLORS_BRIGHT[idx] if is_flashing else COLORS_DIM[idx]
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=20)
        
        # Glow effect when flashing
        if is_flashing:
            glow_surf = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*COLORS_GLOW[idx], 80), glow_surf.get_rect(), border_radius=25)
            self.screen.blit(glow_surf, (x - 10, y - 10))
        
        # Inner highlight
        highlight = tuple(min(255, c + 30) for c in color)
        pygame.draw.rect(self.screen, highlight, (x + 5, y + 5, w - 10, 15), border_radius=10)
    
    def draw(self):
        self.draw_gradient()
        
        # Header
        title = self.title_font.render("🔔 Simon Says", True, WHITE)
        self.screen.blit(title, (SIZE // 2 - title.get_width() // 2, 15))
        
        # Stats
        score_text = self.font.render(f"Score: {self.score}", True, GOLD)
        high_text = self.small_font.render(f"Best: {self.high_score}", True, (150, 200, 255))
        self.screen.blit(score_text, (SIZE // 2 - score_text.get_width() // 2, 55))
        self.screen.blit(high_text, (SIZE // 2 - high_text.get_width() // 2, 85))
        
        # Draw buttons (2x2 grid)
        positions = [(50, 120), (235, 120), (50, 305), (235, 305)]
        for i, (x, y) in enumerate(positions):
            self.draw_button(i, x, y, 165, 165)
        
        # Status message
        if self.game_over:
            status = self.font.render("Game Over! Press R", True, (255, 100, 120))
        elif self.state == 'showing':
            status = self.font.render("Watch carefully...", True, (150, 200, 255))
        else:
            status = self.font.render("Your turn!", True, (100, 255, 150))
        
        self.screen.blit(status, (SIZE // 2 - status.get_width() // 2, SIZE + 55))
        
        pygame.display.flip()
    
    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        self.check_input(event.key - pygame.K_1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    positions = [(50, 120, 215, 285), (235, 120, 400, 285), 
                                (50, 305, 215, 470), (235, 305, 400, 470)]
                    for i, (x1, y1, x2, y2) in enumerate(positions):
                        if x1 <= x <= x2 and y1 <= y <= y2:
                            self.check_input(i)
            
            self.update()
            self.draw()
            self.clock.tick(60)

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())