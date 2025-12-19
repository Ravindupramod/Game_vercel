import asyncio
"""
⭕ Tic Tac Toe
Two-player strategy game!

Controls:
- Click on a cell to place your mark
- ESC to quit, R to restart
"""

import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("⭕ Tic Tac Toe")
        self.window.configure(bg='#1a1a2e')
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.window.bind('<Escape>', lambda e: self.window.quit())
        self.window.bind('r', lambda e: self.reset())
    
    def create_widgets(self):
        title = tk.Label(self.window, text="Tic Tac Toe", font=('Arial', 24, 'bold'),
                        bg='#1a1a2e', fg='#eee')
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        self.status = tk.Label(self.window, text="Player X's turn", font=('Arial', 14),
                              bg='#1a1a2e', fg='#00d4ff')
        self.status.grid(row=1, column=0, columnspan=3, pady=5)
        
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.window, text='', font=('Arial', 36, 'bold'),
                               width=4, height=2, bg='#16213e', fg='#fff',
                               activebackground='#0f3460',
                               command=lambda r=i, c=j: self.click(r, c))
                btn.grid(row=i + 2, column=j, padx=3, pady=3)
                self.buttons[i][j] = btn
        
        reset_btn = tk.Button(self.window, text="New Game", font=('Arial', 12),
                             bg='#e94560', fg='white', command=self.reset)
        reset_btn.grid(row=5, column=0, columnspan=3, pady=10)
    
    def click(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            color = '#00d4ff' if self.current_player == 'X' else '#e94560'
            self.buttons[row][col].config(text=self.current_player, fg=color)
            
            if self.check_winner():
                self.status.config(text=f"Player {self.current_player} wins! 🎉")
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            elif self.is_full():
                self.status.config(text="It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status.config(text=f"Player {self.current_player}'s turn")
    
    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != '': return True
            if b[0][i] == b[1][i] == b[2][i] != '': return True
        if b[0][0] == b[1][1] == b[2][2] != '': return True
        if b[0][2] == b[1][1] == b[2][0] != '': return True
        return False
    
    def is_full(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))
    
    def reset(self):
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='')
        self.status.config(text="Player X's turn")
    
    async def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    TicTacToe().run()