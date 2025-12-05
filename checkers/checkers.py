"""
🔲 Checkers
Classic checkers board game!

Controls:
- Click piece to select, click destination to move
- ESC to quit, R to restart
"""

import pygame
import sys

pygame.init()

SIZE = 600
CELL = SIZE // 8
RED = (200, 50, 50)
BLACK = (30, 30, 30)
WHITE = (240, 240, 240)
CREAM = (255, 220, 180)
BROWN = (139, 90, 43)
GREEN = (50, 200, 50)

class Piece:
    def __init__(self, row, col, color):
        self.row, self.col = row, col
        self.color = color
        self.king = False
    
    def draw(self, screen):
        x = self.col * CELL + CELL // 2
        y = self.row * CELL + CELL // 2
        pygame.draw.circle(screen, self.color, (x, y), CELL // 2 - 8)
        pygame.draw.circle(screen, WHITE if self.color == RED else (80, 80, 80), (x, y), CELL // 2 - 8, 3)
        if self.king:
            pygame.draw.circle(screen, (255, 215, 0), (x, y), 12)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption("🔲 Checkers")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.reset()
    
    def reset(self):
        self.pieces = []
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.pieces.append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.pieces.append(Piece(row, col, RED))
        self.selected = None
        self.turn = RED
        self.valid_moves = []
    
    def get_piece(self, row, col):
        for p in self.pieces:
            if p.row == row and p.col == col:
                return p
        return None
    
    def get_valid_moves(self, piece):
        moves = []
        directions = [(-1, -1), (-1, 1)] if piece.color == RED else [(1, -1), (1, 1)]
        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = piece.row + dr, piece.col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if not self.get_piece(nr, nc):
                    moves.append((nr, nc, None))
                else:
                    target = self.get_piece(nr, nc)
                    if target.color != piece.color:
                        jr, jc = nr + dr, nc + dc
                        if 0 <= jr < 8 and 0 <= jc < 8 and not self.get_piece(jr, jc):
                            moves.append((jr, jc, target))
        return moves
    
    def move(self, piece, row, col, captured):
        piece.row, piece.col = row, col
        if captured:
            self.pieces.remove(captured)
        if (piece.color == RED and row == 0) or (piece.color == BLACK and row == 7):
            piece.king = True
        self.turn = BLACK if self.turn == RED else RED
    
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = CREAM if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(self.screen, color, (col * CELL, row * CELL, CELL, CELL))
        
        for move in self.valid_moves:
            pygame.draw.circle(self.screen, GREEN, 
                             (move[1] * CELL + CELL // 2, move[0] * CELL + CELL // 2), 15)
        
        for piece in self.pieces:
            piece.draw(self.screen)
        
        if self.selected:
            x = self.selected.col * CELL + CELL // 2
            y = self.selected.row * CELL + CELL // 2
            pygame.draw.circle(self.screen, GREEN, (x, y), CELL // 2 - 5, 4)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col, row = event.pos[0] // CELL, event.pos[1] // CELL
                    piece = self.get_piece(row, col)
                    
                    if self.selected:
                        for move in self.valid_moves:
                            if move[0] == row and move[1] == col:
                                self.move(self.selected, row, col, move[2])
                                break
                        self.selected = None
                        self.valid_moves = []
                    elif piece and piece.color == self.turn:
                        self.selected = piece
                        self.valid_moves = self.get_valid_moves(piece)
            
            self.draw_board()
            
            # Check win
            red_count = sum(1 for p in self.pieces if p.color == RED)
            black_count = sum(1 for p in self.pieces if p.color == BLACK)
            if red_count == 0 or black_count == 0:
                winner = "Red" if black_count == 0 else "Black"
                text = self.font.render(f"{winner} Wins!", True, WHITE)
                self.screen.blit(text, (SIZE // 2 - text.get_width() // 2, SIZE // 2))
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
