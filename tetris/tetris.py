"""
🟦 Tetris
Classic block stacking puzzle game!

Controls:
- Left/Right arrows to move
- Up arrow to rotate
- Down arrow to soft drop
- SPACE to hard drop
- R to restart, ESC to quit
"""

import pygame
import random
import sys
import asyncio

pygame.init()

CELL = 30
COLS, ROWS = 10, 20
WIDTH = COLS * CELL + 180
HEIGHT = ROWS * CELL

# Beautiful color palette
BG_TOP = (15, 20, 40)
BG_BOTTOM = (25, 30, 55)
BOARD_BG = (20, 25, 45)
GRID_COLOR = (35, 40, 65)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
SHADOW = (10, 15, 30)

# Vibrant piece colors with gradients
COLORS = [
    ((0, 220, 220), (0, 180, 180)),     # I - Cyan
    ((220, 220, 0), (180, 180, 0)),     # O - Yellow
    ((180, 0, 220), (140, 0, 180)),     # T - Purple
    ((0, 220, 100), (0, 180, 80)),      # S - Green
    ((220, 60, 60), (180, 40, 40)),     # Z - Red
    ((0, 100, 220), (0, 80, 180)),      # J - Blue
    ((220, 140, 0), (180, 110, 0)),     # L - Orange
]

SHAPES = [
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[0,1,0],[1,1,1]],
    [[0,1,1],[1,1,0]],
    [[1,1,0],[0,1,1]],
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]],
]

class Piece:
    def __init__(self):
        idx = random.randint(0, 6)
        self.shape = [row[:] for row in SHAPES[idx]]
        self.color = COLORS[idx]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🟦 Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 32)
        self.reset()
    
    def draw_gradient(self):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
            g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
            b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
    
    def reset(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.drop_time = 0
        self.game_over = False
        self.high_score = getattr(self, 'high_score', 0)
    
    def valid(self, piece, dx=0, dy=0):
        for r, row in enumerate(piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    nx, ny = piece.x + c + dx, piece.y + r + dy
                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return False
                    if ny >= 0 and self.board[ny][nx]:
                        return False
        return True
    
    def lock(self):
        for r, row in enumerate(self.piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    y = self.piece.y + r
                    if y < 0:
                        self.game_over = True
                        self.high_score = max(self.high_score, self.score)
                        return
                    self.board[y][self.piece.x + c] = self.piece.color
        self.clear_lines()
        self.piece = self.next_piece
        self.next_piece = Piece()
        if not self.valid(self.piece):
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
    
    def clear_lines(self):
        lines = 0
        for r in range(ROWS - 1, -1, -1):
            if all(self.board[r]):
                del self.board[r]
                self.board.insert(0, [None] * COLS)
                lines += 1
        points = [0, 100, 300, 500, 800]
        self.score += points[lines] * self.level
        self.lines += lines
        self.level = self.lines // 10 + 1
    
    def drop(self):
        if self.valid(self.piece, dy=1):
            self.piece.y += 1
        else:
            self.lock()
    
    def hard_drop(self):
        while self.valid(self.piece, dy=1):
            self.piece.y += 1
            self.score += 2
        self.lock()
    
    def draw_block(self, x, y, color, ghost=False):
        if ghost:
            pygame.draw.rect(self.screen, (*color[0], 50), (x, y, CELL - 2, CELL - 2), border_radius=4, width=2)
        else:
            # Shadow
            pygame.draw.rect(self.screen, SHADOW, (x + 3, y + 3, CELL - 2, CELL - 2), border_radius=4)
            # Main block
            pygame.draw.rect(self.screen, color[0], (x, y, CELL - 2, CELL - 2), border_radius=4)
            # Highlight
            pygame.draw.rect(self.screen, color[1], (x, y, CELL - 2, 6), border_radius=4)
    
    def update(self):
        if self.game_over:
            return
        self.drop_time += 1
        speed = max(3, 25 - self.level * 2)
        if self.drop_time >= speed:
            self.drop()
            self.drop_time = 0
    
    def draw(self):
        self.draw_gradient()
        
        # Board background
        pygame.draw.rect(self.screen, BOARD_BG, (0, 0, COLS * CELL, HEIGHT))
        
        # Grid
        for x in range(0, COLS * CELL, CELL):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (COLS * CELL, y))
        
        # Placed blocks
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c]:
                    self.draw_block(c * CELL, r * CELL, self.board[r][c])
        
        # Ghost piece
        if not self.game_over:
            ghost_y = self.piece.y
            while self.valid(self.piece, dy=ghost_y - self.piece.y + 1):
                ghost_y += 1
            for r, row in enumerate(self.piece.shape):
                for c, cell in enumerate(row):
                    if cell:
                        self.draw_block((self.piece.x + c) * CELL, (ghost_y + r) * CELL, self.piece.color, ghost=True)
        
        # Current piece
        if not self.game_over:
            for r, row in enumerate(self.piece.shape):
                for c, cell in enumerate(row):
                    if cell:
                        self.draw_block((self.piece.x + c) * CELL, (self.piece.y + r) * CELL, self.piece.color)
        
        # Sidebar
        sidebar_x = COLS * CELL + 15
        
        # Next piece box
        pygame.draw.rect(self.screen, BOARD_BG, (sidebar_x, 10, 150, 100), border_radius=8)
        next_text = self.title_font.render("NEXT", True, WHITE)
        self.screen.blit(next_text, (sidebar_x + 55, 18))
        
        for r, row in enumerate(self.next_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    self.draw_block(sidebar_x + 40 + c * 20, 50 + r * 20, self.next_piece.color)
        
        # Stats
        pygame.draw.rect(self.screen, BOARD_BG, (sidebar_x, 130, 150, 180), border_radius=8)
        
        stats = [
            ("SCORE", str(self.score), GOLD),
            ("LINES", str(self.lines), (100, 200, 255)),
            ("LEVEL", str(self.level), (100, 255, 150)),
            ("BEST", str(self.high_score), (255, 150, 200)),
        ]
        
        for i, (label, value, color) in enumerate(stats):
            y_pos = 145 + i * 42
            label_text = self.font.render(label, True, WHITE)
            value_text = self.font.render(value, True, color)
            self.screen.blit(label_text, (sidebar_x + 15, y_pos))
            self.screen.blit(value_text, (sidebar_x + 15, y_pos + 18))
        
        # Game over overlay
        if self.game_over:
            overlay = pygame.Surface((COLS * CELL, HEIGHT), pygame.SRCALPHA)
            overlay.fill((20, 25, 45, 220))
            self.screen.blit(overlay, (0, 0))
            
            text = self.title_font.render("GAME OVER", True, (255, 100, 120))
            hint = self.font.render("Press R to restart", True, (150, 200, 255))
            self.screen.blit(text, (COLS * CELL // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
            self.screen.blit(hint, (COLS * CELL // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if not self.game_over:
                        if event.key == pygame.K_LEFT and self.valid(self.piece, dx=-1):
                            self.piece.x -= 1
                        if event.key == pygame.K_RIGHT and self.valid(self.piece, dx=1):
                            self.piece.x += 1
                        if event.key == pygame.K_UP:
                            old = [row[:] for row in self.piece.shape]
                            self.piece.rotate()
                            if not self.valid(self.piece):
                                self.piece.shape = old
                        if event.key == pygame.K_DOWN:
                            self.drop()
                        if event.key == pygame.K_SPACE:
                            self.hard_drop()
            
            self.update()
            self.draw()
            self.clock.tick(60)

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())