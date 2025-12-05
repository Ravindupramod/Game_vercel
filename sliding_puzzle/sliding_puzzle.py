"""
🧩 Sliding Puzzle
Slide tiles to arrange numbers 1-15!

Controls:
- Arrow keys to slide tiles
- R to shuffle, ESC to quit
"""

import pygame
import random
import sys

pygame.init()

SIZE = 450
GRID = 4
CELL = SIZE // GRID

# Beautiful color palette
BG_TOP = (20, 30, 60)
BG_BOTTOM = (40, 50, 90)
TILE_COLORS = [
    (255, 107, 107),  # Coral
    (255, 159, 67),   # Orange
    (254, 202, 87),   # Yellow
    (29, 209, 161),   # Teal
    (72, 219, 251),   # Cyan
    (95, 39, 205),    # Purple
    (200, 80, 192),   # Pink
    (46, 134, 222),   # Blue
]
WHITE = (255, 255, 255)
SHADOW = (15, 20, 40)
GOLD = (255, 215, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIZE, SIZE + 80))
        pygame.display.set_caption("🧩 Sliding Puzzle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 56)
        self.title_font = pygame.font.Font(None, 38)
        self.small_font = pygame.font.Font(None, 28)
        self.reset()
    
    def draw_gradient(self):
        for y in range(SIZE + 80):
            ratio = y / (SIZE + 80)
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SIZE, y))
    
    def reset(self):
        self.tiles = list(range(1, 16)) + [0]
        self.moves = 0
        self.shuffle()
        self.start_time = pygame.time.get_ticks()
    
    def shuffle(self):
        for _ in range(200):
            empty = self.tiles.index(0)
            er, ec = empty // GRID, empty % GRID
            dirs = []
            if er > 0: dirs.append(-GRID)
            if er < 3: dirs.append(GRID)
            if ec > 0: dirs.append(-1)
            if ec < 3: dirs.append(1)
            d = random.choice(dirs)
            self.tiles[empty], self.tiles[empty + d] = self.tiles[empty + d], self.tiles[empty]
        self.moves = 0
    
    def move(self, direction):
        empty = self.tiles.index(0)
        er, ec = empty // GRID, empty % GRID
        
        moves = {'up': (1, 0), 'down': (-1, 0), 'left': (0, 1), 'right': (0, -1)}
        dr, dc = moves[direction]
        nr, nc = er + dr, ec + dc
        
        if 0 <= nr < GRID and 0 <= nc < GRID:
            new_pos = nr * GRID + nc
            self.tiles[empty], self.tiles[new_pos] = self.tiles[new_pos], self.tiles[empty]
            self.moves += 1
    
    def is_solved(self):
        return self.tiles == list(range(1, 16)) + [0]
    
    def get_tile_color(self, num):
        return TILE_COLORS[(num - 1) % len(TILE_COLORS)]
    
    def draw_tile(self, num, r, c):
        x, y = c * CELL + 10, r * CELL + 85
        w, h = CELL - 20, CELL - 20
        
        color = self.get_tile_color(num)
        
        # Shadow
        pygame.draw.rect(self.screen, SHADOW, (x + 4, y + 4, w, h), border_radius=12)
        
        # Main tile
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=12)
        
        # Highlight (top-left gradient effect)
        highlight = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(self.screen, highlight, (x, y, w, 8), border_radius=12)
        
        # Number
        text = self.font.render(str(num), True, WHITE)
        shadow_text = self.font.render(str(num), True, SHADOW)
        self.screen.blit(shadow_text, (x + w//2 - text.get_width()//2 + 2, y + h//2 - text.get_height()//2 + 2))
        self.screen.blit(text, (x + w//2 - text.get_width()//2, y + h//2 - text.get_height()//2))
    
    def draw(self):
        self.draw_gradient()
        
        # Header
        title = self.title_font.render("🧩 Sliding Puzzle", True, WHITE)
        self.screen.blit(title, (SIZE // 2 - title.get_width() // 2, 15))
        
        # Stats
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        moves_text = self.small_font.render(f"Moves: {self.moves}", True, GOLD)
        time_text = self.small_font.render(f"Time: {elapsed}s", True, (150, 200, 255))
        self.screen.blit(moves_text, (20, 55))
        self.screen.blit(time_text, (SIZE - time_text.get_width() - 20, 55))
        
        # Draw tiles
        for i, tile in enumerate(self.tiles):
            r, c = i // GRID, i % GRID
            if tile != 0:
                self.draw_tile(tile, r, c)
        
        if self.is_solved():
            overlay = pygame.Surface((SIZE, SIZE + 80), pygame.SRCALPHA)
            overlay.fill((20, 30, 50, 220))
            self.screen.blit(overlay, (0, 0))
            
            text = self.title_font.render("🎉 SOLVED! 🎉", True, GOLD)
            stats = self.small_font.render(f"Completed in {self.moves} moves!", True, WHITE)
            hint = self.small_font.render("Press R for new puzzle", True, (150, 200, 255))
            
            self.screen.blit(text, (SIZE // 2 - text.get_width() // 2, SIZE // 2 - 20))
            self.screen.blit(stats, (SIZE // 2 - stats.get_width() // 2, SIZE // 2 + 30))
            self.screen.blit(hint, (SIZE // 2 - hint.get_width() // 2, SIZE // 2 + 70))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if event.key == pygame.K_UP: self.move('up')
                    if event.key == pygame.K_DOWN: self.move('down')
                    if event.key == pygame.K_LEFT: self.move('left')
                    if event.key == pygame.K_RIGHT: self.move('right')
            
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
