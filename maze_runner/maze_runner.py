"""
🏃 Maze Runner
Navigate through the maze to reach the exit!

Controls:
- Arrow keys to move
- R for new maze, ESC to quit
"""

import pygame
import random
import sys

pygame.init()

CELL = 25
COLS, ROWS = 25, 21
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL

WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
GREEN = (50, 200, 100)
RED = (200, 50, 50)
BLUE = (50, 100, 200)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 40))
        pygame.display.set_caption("🏃 Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.reset()
    
    def reset(self):
        self.maze = self.generate_maze()
        self.player = [1, 1]
        self.exit_pos = [COLS - 2, ROWS - 2]
        self.maze[self.exit_pos[1]][self.exit_pos[0]] = 0
        self.moves = 0
        self.won = False
    
    def generate_maze(self):
        maze = [[1] * COLS for _ in range(ROWS)]
        
        def carve(x, y):
            maze[y][x] = 0
            dirs = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 < nx < COLS - 1 and 0 < ny < ROWS - 1 and maze[ny][nx] == 1:
                    maze[y + dy // 2][x + dx // 2] = 0
                    carve(nx, ny)
        
        carve(1, 1)
        return maze
    
    def move(self, dx, dy):
        if self.won:
            return
        nx, ny = self.player[0] + dx, self.player[1] + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS and self.maze[ny][nx] == 0:
            self.player = [nx, ny]
            self.moves += 1
            if self.player == self.exit_pos:
                self.won = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        for y in range(ROWS):
            for x in range(COLS):
                if self.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, WHITE, (x * CELL, y * CELL + 40, CELL, CELL))
        
        # Draw exit
        ex, ey = self.exit_pos
        pygame.draw.rect(self.screen, GREEN, (ex * CELL + 3, ey * CELL + 43, CELL - 6, CELL - 6))
        
        # Draw player
        px, py = self.player
        pygame.draw.circle(self.screen, RED, (px * CELL + CELL // 2, py * CELL + CELL // 2 + 40), CELL // 3)
        
        # Draw header
        pygame.draw.rect(self.screen, BLUE, (0, 0, WIDTH, 40))
        text = self.font.render(f"Moves: {self.moves}", True, WHITE)
        self.screen.blit(text, (10, 10))
        
        if self.won:
            text = self.font.render("🎉 You escaped!", True, GREEN)
            self.screen.blit(text, (WIDTH // 2 - 60, 10))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                    if event.key == pygame.K_UP: self.move(0, -1)
                    if event.key == pygame.K_DOWN: self.move(0, 1)
                    if event.key == pygame.K_LEFT: self.move(-1, 0)
                    if event.key == pygame.K_RIGHT: self.move(1, 0)
            
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
