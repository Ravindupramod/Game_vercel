"""
🔢 2048
Slide tiles to combine and reach 2048!

Controls:
- Arrow keys to slide tiles
- ESC to quit, R to restart
"""

import pygame
import random
import sys
import asyncio

pygame.init()

SIZE = 450
GRID = 4
CELL = SIZE // GRID

# Elegant color palette
BG_COLOR = (250, 248, 239)
BOARD_BG = (187, 173, 160)
EMPTY_CELL = (205, 193, 180)
WHITE = (255, 255, 255)
DARK_TEXT = (119, 110, 101)

# Tile colors with gradients
COLORS = {
    0: ((205, 193, 180), (195, 183, 170)),
    2: ((238, 228, 218), (228, 218, 208)),
    4: ((237, 224, 200), (227, 214, 190)),
    8: ((242, 177, 121), (232, 167, 111)),
    16: ((245, 149, 99), (235, 139, 89)),
    32: ((246, 124, 95), (236, 114, 85)),
    64: ((246, 94, 59), (236, 84, 49)),
    128: ((237, 207, 114), (227, 197, 104)),
    256: ((237, 204, 97), (227, 194, 87)),
    512: ((237, 200, 80), (227, 190, 70)),
    1024: ((237, 197, 63), (227, 187, 53)),
    2048: ((237, 194, 46), (227, 184, 36)),
}

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIZE, SIZE + 100))
        pygame.display.set_caption("🔢 2048")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 52)
        self.small_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        self.reset()
    
    def reset(self):
        self.grid = [[0] * GRID for _ in range(GRID)]
        self.score = 0
        self.high_score = getattr(self, 'high_score', 0)
        self.game_over = False
        self.won = False
        self.spawn()
        self.spawn()
    
    def spawn(self):
        empty = [(r, c) for r in range(GRID) for c in range(GRID) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2
    
    def slide(self, row):
        new = [x for x in row if x != 0]
        for i in range(len(new) - 1):
            if new[i] == new[i + 1]:
                new[i] *= 2
                self.score += new[i]
                if new[i] == 2048:
                    self.won = True
                new[i + 1] = 0
        new = [x for x in new if x != 0]
        return new + [0] * (GRID - len(new))
    
    def move(self, direction):
        old = [row[:] for row in self.grid]
        
        if direction == 'left':
            self.grid = [self.slide(row) for row in self.grid]
        elif direction == 'right':
            self.grid = [self.slide(row[::-1])[::-1] for row in self.grid]
        elif direction == 'up':
            cols = [[self.grid[r][c] for r in range(GRID)] for c in range(GRID)]
            cols = [self.slide(col) for col in cols]
            self.grid = [[cols[c][r] for c in range(GRID)] for r in range(GRID)]
        elif direction == 'down':
            cols = [[self.grid[r][c] for r in range(GRID)] for c in range(GRID)]
            cols = [self.slide(col[::-1])[::-1] for col in cols]
            self.grid = [[cols[c][r] for c in range(GRID)] for r in range(GRID)]
        
        if self.grid != old:
            self.spawn()
            self.high_score = max(self.high_score, self.score)
            self.check_game_over()
    
    def check_game_over(self):
        for r in range(GRID):
            for c in range(GRID):
                if self.grid[r][c] == 0:
                    return
                if c < GRID - 1 and self.grid[r][c] == self.grid[r][c + 1]:
                    return
                if r < GRID - 1 and self.grid[r][c] == self.grid[r + 1][c]:
                    return
        self.game_over = True
    
    def draw_tile(self, val, r, c):
        x, y = c * CELL + 10, r * CELL + 105
        w, h = CELL - 20, CELL - 20
        
        colors = COLORS.get(val, COLORS[2048])
        
        # Shadow
        pygame.draw.rect(self.screen, (150, 140, 130), (x + 3, y + 3, w, h), border_radius=6)
        
        # Main tile
        pygame.draw.rect(self.screen, colors[0], (x, y, w, h), border_radius=6)
        
        # Top highlight
        pygame.draw.rect(self.screen, colors[1], (x, y + h - 8, w, 8), border_radius=6)
        
        if val:
            text_color = DARK_TEXT if val < 8 else WHITE
            font = self.font if val < 1000 else self.small_font
            text = font.render(str(val), True, text_color)
            self.screen.blit(text, (x + w // 2 - text.get_width() // 2, y + h // 2 - text.get_height() // 2))
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Header
        title = self.title_font.render("2048", True, DARK_TEXT)
        self.screen.blit(title, (20, 20))
        
        # Score boxes
        pygame.draw.rect(self.screen, BOARD_BG, (SIZE - 200, 15, 90, 50), border_radius=6)
        pygame.draw.rect(self.screen, BOARD_BG, (SIZE - 100, 15, 90, 50), border_radius=6)
        
        score_label = self.small_font.render("SCORE", True, WHITE)
        best_label = self.small_font.render("BEST", True, WHITE)
        score_val = self.small_font.render(str(self.score), True, WHITE)
        best_val = self.small_font.render(str(self.high_score), True, WHITE)
        
        self.screen.blit(score_label, (SIZE - 185, 18))
        self.screen.blit(score_val, (SIZE - 185, 40))
        self.screen.blit(best_label, (SIZE - 85, 18))
        self.screen.blit(best_val, (SIZE - 85, 40))
        
        # Board
        pygame.draw.rect(self.screen, BOARD_BG, (5, 100, SIZE - 10, SIZE - 10), border_radius=8)
        
        # Tiles
        for r in range(GRID):
            for c in range(GRID):
                self.draw_tile(self.grid[r][c], r, c)
        
        # Overlays
        if self.game_over or self.won:
            overlay = pygame.Surface((SIZE - 10, SIZE - 10), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 180))
            self.screen.blit(overlay, (5, 100))
            
            msg = "You Win! 🎉" if self.won else "Game Over!"
            color = (255, 180, 0) if self.won else DARK_TEXT
            text = self.title_font.render(msg, True, color)
            hint = self.small_font.render("Press R to restart", True, DARK_TEXT)
            
            self.screen.blit(text, (SIZE // 2 - text.get_width() // 2, SIZE // 2 + 50))
            self.screen.blit(hint, (SIZE // 2 - hint.get_width() // 2, SIZE // 2 + 100))
        
        pygame.display.flip()
    
    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if not self.game_over:
                        if event.key == pygame.K_LEFT: self.move('left')
                        elif event.key == pygame.K_RIGHT: self.move('right')
                        elif event.key == pygame.K_UP: self.move('up')
                        elif event.key == pygame.K_DOWN: self.move('down')
            
            self.draw()
            self.clock.tick(60)

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())