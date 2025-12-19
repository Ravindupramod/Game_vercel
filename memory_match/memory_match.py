"""
🎴 Memory Match
Flip cards to find matching pairs!

Controls:
- Click cards to flip
- R to restart
"""

import pygame
import random
import sys
import asyncio

pygame.init()

SIZE = 520
GRID = 4
CELL = SIZE // GRID
SYMBOLS = ['🎮', '🎯', '🎪', '🎨', '🎭', '🎵', '🎲', '🎸']

# Vibrant color palette
BG_GRADIENT_TOP = (25, 25, 50)
BG_GRADIENT_BOTTOM = (45, 45, 80)
CARD_BACK = (60, 70, 120)
CARD_BACK_HIGHLIGHT = (80, 90, 150)
CARD_FRONT = (255, 255, 255)
CARD_MATCHED = (80, 200, 120)
CARD_MATCHED_GLOW = (100, 255, 150)
ACCENT = (255, 100, 150)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
SHADOW = (20, 20, 40)

class Card:
    def __init__(self, row, col, symbol):
        self.row, self.col = row, col
        self.symbol = symbol
        self.revealed = False
        self.matched = False
        self.flip_anim = 0
        self.glow = 0
    
    def update(self):
        if self.matched and self.glow < 20:
            self.glow += 1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIZE, SIZE + 80))
        pygame.display.set_caption("🎴 Memory Match")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)
        self.title_font = pygame.font.Font(None, 42)
        self.small_font = pygame.font.Font(None, 28)
        self.reset()
    
    def draw_gradient_bg(self):
        for y in range(SIZE + 80):
            ratio = y / (SIZE + 80)
            r = int(BG_GRADIENT_TOP[0] + (BG_GRADIENT_BOTTOM[0] - BG_GRADIENT_TOP[0]) * ratio)
            g = int(BG_GRADIENT_TOP[1] + (BG_GRADIENT_BOTTOM[1] - BG_GRADIENT_TOP[1]) * ratio)
            b = int(BG_GRADIENT_TOP[2] + (BG_GRADIENT_BOTTOM[2] - BG_GRADIENT_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SIZE, y))
    
    def reset(self):
        cards = SYMBOLS[:8] * 2
        random.shuffle(cards)
        self.cards = [[Card(r, c, cards[r * GRID + c]) for c in range(GRID)] for r in range(GRID)]
        self.selected = []
        self.moves = 0
        self.pairs_found = 0
        self.wait_timer = 0
        self.game_won = False
        self.start_time = pygame.time.get_ticks()
    
    def get_card(self, row, col):
        if 0 <= row < GRID and 0 <= col < GRID:
            return self.cards[row][col]
        return None
    
    def click(self, row, col):
        card = self.get_card(row, col)
        if not card or self.wait_timer > 0 or card.matched or card.revealed:
            return
        if len(self.selected) < 2:
            card.revealed = True
            self.selected.append(card)
            if len(self.selected) == 2:
                self.moves += 1
                if self.selected[0].symbol == self.selected[1].symbol:
                    self.selected[0].matched = True
                    self.selected[1].matched = True
                    self.pairs_found += 1
                    self.selected = []
                    if self.pairs_found == 8:
                        self.game_won = True
                else:
                    self.wait_timer = 45
    
    def update(self):
        if self.wait_timer > 0:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                for card in self.selected:
                    card.revealed = False
                self.selected = []
        
        for row in self.cards:
            for card in row:
                card.update()
    
    def draw_card(self, card):
        x = card.col * CELL + 15
        y = card.row * CELL + 90
        w, h = CELL - 30, CELL - 30
        
        # Shadow
        shadow_rect = pygame.Rect(x + 4, y + 4, w, h)
        pygame.draw.rect(self.screen, SHADOW, shadow_rect, border_radius=12)
        
        if card.matched:
            # Glow effect for matched cards
            glow_size = card.glow
            glow_rect = pygame.Rect(x - glow_size//2, y - glow_size//2, w + glow_size, h + glow_size)
            glow_surf = pygame.Surface((w + glow_size, h + glow_size), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*CARD_MATCHED_GLOW, 100), glow_surf.get_rect(), border_radius=14)
            self.screen.blit(glow_surf, glow_rect)
            
            pygame.draw.rect(self.screen, CARD_MATCHED, (x, y, w, h), border_radius=12)
            symbol = self.font.render(card.symbol, True, WHITE)
            self.screen.blit(symbol, (x + w//2 - 18, y + h//2 - 18))
        elif card.revealed:
            pygame.draw.rect(self.screen, CARD_FRONT, (x, y, w, h), border_radius=12)
            pygame.draw.rect(self.screen, ACCENT, (x, y, w, h), width=3, border_radius=12)
            symbol = self.font.render(card.symbol, True, (50, 50, 80))
            self.screen.blit(symbol, (x + w//2 - 18, y + h//2 - 18))
        else:
            # Card back with pattern
            pygame.draw.rect(self.screen, CARD_BACK, (x, y, w, h), border_radius=12)
            pygame.draw.rect(self.screen, CARD_BACK_HIGHLIGHT, (x, y, w, h), width=2, border_radius=12)
            # Decorative pattern
            pygame.draw.circle(self.screen, CARD_BACK_HIGHLIGHT, (x + w//2, y + h//2), 20, 2)
            pygame.draw.circle(self.screen, CARD_BACK_HIGHLIGHT, (x + w//2, y + h//2), 10)
    
    def draw(self):
        self.draw_gradient_bg()
        
        # Header
        title = self.title_font.render("🎴 Memory Match", True, WHITE)
        self.screen.blit(title, (SIZE // 2 - title.get_width() // 2, 15))
        
        # Stats
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        moves_text = self.small_font.render(f"Moves: {self.moves}", True, GOLD)
        time_text = self.small_font.render(f"Time: {elapsed}s", True, (150, 200, 255))
        pairs_text = self.small_font.render(f"Pairs: {self.pairs_found}/8", True, CARD_MATCHED_GLOW)
        
        self.screen.blit(moves_text, (20, 55))
        self.screen.blit(time_text, (SIZE // 2 - time_text.get_width() // 2, 55))
        self.screen.blit(pairs_text, (SIZE - pairs_text.get_width() - 20, 55))
        
        # Draw cards
        for row in self.cards:
            for card in row:
                self.draw_card(card)
        
        if self.game_won:
            overlay = pygame.Surface((SIZE, SIZE + 80), pygame.SRCALPHA)
            overlay.fill((20, 20, 40, 200))
            self.screen.blit(overlay, (0, 0))
            
            win_text = self.title_font.render("🎉 You Won! 🎉", True, GOLD)
            stats_text = self.small_font.render(f"Completed in {self.moves} moves and {elapsed} seconds!", True, WHITE)
            restart_text = self.small_font.render("Press R to play again", True, (150, 200, 255))
            
            self.screen.blit(win_text, (SIZE // 2 - win_text.get_width() // 2, SIZE // 2 - 40))
            self.screen.blit(stats_text, (SIZE // 2 - stats_text.get_width() // 2, SIZE // 2 + 20))
            self.screen.blit(restart_text, (SIZE // 2 - restart_text.get_width() // 2, SIZE // 2 + 60))
        
        pygame.display.flip()
    
    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                    if event.key == pygame.K_r: self.reset()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_won:
                    x, y = event.pos
                    if y > 80:
                        col, row = (x - 15) // CELL, (y - 90) // CELL
                        if 0 <= row < GRID and 0 <= col < GRID:
                            self.click(row, col)
            
            self.update()
            self.draw()
            self.clock.tick(60)

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())