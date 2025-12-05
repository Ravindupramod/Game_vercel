"""
💣 Minesweeper
Find all mines without detonating!

Controls:
- Left click to reveal
- Right click to flag
- R to restart
"""

import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, rows=10, cols=10, mines=15):
        self.rows, self.cols, self.mine_count = rows, cols, mines
        self.window = tk.Tk()
        self.window.title("💣 Minesweeper")
        self.window.configure(bg='#333')
        self.buttons = {}
        self.reset()
        self.window.bind('r', lambda e: self.reset())
    
    def reset(self):
        for btn in self.buttons.values():
            btn.destroy()
        self.buttons = {}
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.flagged = [[False] * self.cols for _ in range(self.rows)]
        self.game_over = False
        self.first_click = True
        
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.window, width=2, height=1, font=('Arial', 12, 'bold'),
                               bg='#666', activebackground='#888')
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, r=r, c=c: self.reveal(r, c))
                btn.bind('<Button-3>', lambda e, r=r, c=c: self.toggle_flag(r, c))
                self.buttons[(r, c)] = btn
    
    def place_mines(self, first_r, first_c):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)
                    if abs(r - first_r) > 1 or abs(c - first_c) > 1]
        mines = random.sample(positions, min(self.mine_count, len(positions)))
        for r, c in mines:
            self.board[r][c] = -1
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1:
                    count = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                               if 0 <= r+dr < self.rows and 0 <= c+dc < self.cols
                               and self.board[r+dr][c+dc] == -1)
                    self.board[r][c] = count
    
    def reveal(self, r, c):
        if self.game_over or self.flagged[r][c] or self.revealed[r][c]:
            return
        
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
        
        self.revealed[r][c] = True
        btn = self.buttons[(r, c)]
        
        if self.board[r][c] == -1:
            btn.config(text='💣', bg='red')
            self.game_over = True
            self.reveal_all()
            messagebox.showinfo("Game Over", "💥 BOOM! You hit a mine!")
        elif self.board[r][c] == 0:
            btn.config(text='', bg='#ccc', relief='sunken')
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr, nc)
        else:
            colors = ['', 'blue', 'green', 'red', 'purple', 'maroon', 'cyan', 'black', 'gray']
            btn.config(text=str(self.board[r][c]), fg=colors[self.board[r][c]], 
                      bg='#ccc', relief='sunken')
        
        self.check_win()
    
    def toggle_flag(self, r, c):
        if self.game_over or self.revealed[r][c]:
            return
        self.flagged[r][c] = not self.flagged[r][c]
        self.buttons[(r, c)].config(text='🚩' if self.flagged[r][c] else '')
    
    def reveal_all(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.buttons[(r, c)].config(text='💣', bg='#ff6666')
    
    def check_win(self):
        unrevealed = sum(1 for r in range(self.rows) for c in range(self.cols)
                        if not self.revealed[r][c])
        if unrevealed == self.mine_count:
            self.game_over = True
            messagebox.showinfo("Congratulations!", "🎉 You won!")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    Minesweeper().run()
