"""
🔴 Connect Four
Drop discs to connect four in a row!

Controls:
- 1-7 keys to drop disc in column
- Click on column to drop
- ESC to quit, R to restart
"""

import pygame
import sys
import asyncio

pygame.init()

COLS, ROWS = 7, 6
CELL_SIZE = 80
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 1) * CELL_SIZE

BLUE = (0, 100, 200)
BLACK = (20, 20, 30)
RED = (255, 50, 50)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🔴 Connect Four")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.reset()
    
    def reset(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current = 1
        self.winner = 0
        self.game_over = False
    
    def drop(self, col):
        if self.game_over or col < 0 or col >= COLS:
            return False
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current
                if self.check_win(row, col):
                    self.winner = self.current
                    self.game_over = True
                elif all(self.board[0][c] != 0 for c in range(COLS)):
                    self.game_over = True
                else:
                    self.current = 3 - self.current
                return True
        return False
    
    def check_win(self, row, col):
        p = self.board[row][col]
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1
            for d in [1, -1]:
                r, c = row + dr*d, col + dc*d
                while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == p:
                    count += 1
                    r += dr*d
                    c += dc*d
            if count >= 4:
                return True
        return False
    
    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if pygame.K_1 <= event.key <= pygame.K_7:
                        self.drop(event.key - pygame.K_1)
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self.drop(event.pos[0] // CELL_SIZE)
            
            self.screen.fill(BLACK)
            
            # Draw board
            for row in range(ROWS):
                for col in range(COLS):
                    pygame.draw.rect(self.screen, BLUE, 
                                   (col * CELL_SIZE, (row + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    color = BLACK
                    if self.board[row][col] == 1: color = RED
                    elif self.board[row][col] == 2: color = YELLOW
                    pygame.draw.circle(self.screen, color,
                                      (col * CELL_SIZE + CELL_SIZE // 2, 
                                       (row + 1) * CELL_SIZE + CELL_SIZE // 2), 35)
            
            # Draw preview
            if not self.game_over:
                mx = pygame.mouse.get_pos()[0]
                color = RED if self.current == 1 else YELLOW
                pygame.draw.circle(self.screen, color, (mx, CELL_SIZE // 2), 35)
            
            # Status
            if self.game_over:
                if self.winner:
                    text = f"{'Red' if self.winner == 1 else 'Yellow'} Wins!"
                else:
                    text = "Draw!"
                self.screen.blit(self.font.render(text, True, WHITE), (WIDTH // 2 - 80, 10))
            
            pygame.display.flip()
            self.clock.tick(60)

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())