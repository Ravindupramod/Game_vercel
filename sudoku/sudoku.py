"""
📊 Sudoku
Fill the grid with numbers 1-9!

Controls:
- Click cell to select
- 1-9 to enter number
- Delete/Backspace to clear
- R to new puzzle
"""

import tkinter as tk
import random

class Sudoku:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("📊 Sudoku")
        self.window.configure(bg='#2c3e50')
        self.cells = {}
        self.selected = None
        self.create_ui()
        self.new_puzzle()
        self.window.bind('r', lambda e: self.new_puzzle())
    
    def create_ui(self):
        title = tk.Label(self.window, text="Sudoku", font=('Arial', 20, 'bold'), 
                        bg='#2c3e50', fg='white')
        title.grid(row=0, column=0, columnspan=9, pady=10)
        
        for r in range(9):
            for c in range(9):
                bg = '#ecf0f1' if ((r // 3) + (c // 3)) % 2 == 0 else '#bdc3c7'
                cell = tk.Label(self.window, text='', font=('Arial', 18), width=3, height=1,
                               bg=bg, relief='raised', borderwidth=1)
                cell.grid(row=r + 1, column=c, padx=1, pady=1)
                cell.bind('<Button-1>', lambda e, r=r, c=c: self.select(r, c))
                self.cells[(r, c)] = cell
        
        self.window.bind('<Key>', self.key_press)
        
        btn = tk.Button(self.window, text="New Game", font=('Arial', 12),
                       bg='#3498db', fg='white', command=self.new_puzzle)
        btn.grid(row=10, column=0, columnspan=9, pady=10)
    
    def generate_solved(self):
        base = list(range(1, 10))
        random.shuffle(base)
        grid = [[0] * 9 for _ in range(9)]
        
        def fill(grid):
            for r in range(9):
                for c in range(9):
                    if grid[r][c] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for n in nums:
                            if self.is_valid(grid, r, c, n):
                                grid[r][c] = n
                                if fill(grid):
                                    return True
                                grid[r][c] = 0
                        return False
            return True
        
        fill(grid)
        return grid
    
    def is_valid(self, grid, row, col, num):
        if num in grid[row]: return False
        if num in [grid[r][col] for r in range(9)]: return False
        br, bc = 3 * (row // 3), 3 * (col // 3)
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if grid[r][c] == num: return False
        return True
    
    def new_puzzle(self):
        self.solution = self.generate_solved()
        self.puzzle = [row[:] for row in self.solution]
        self.fixed = [[False] * 9 for _ in range(9)]
        
        # Remove numbers
        for _ in range(45):
            r, c = random.randint(0, 8), random.randint(0, 8)
            while self.puzzle[r][c] == 0:
                r, c = random.randint(0, 8), random.randint(0, 8)
            self.puzzle[r][c] = 0
        
        for r in range(9):
            for c in range(9):
                val = self.puzzle[r][c]
                if val:
                    self.fixed[r][c] = True
                    self.cells[(r, c)].config(text=str(val), fg='#2c3e50')
                else:
                    self.cells[(r, c)].config(text='', fg='#3498db')
        self.selected = None
    
    def select(self, r, c):
        if self.selected:
            pr, pc = self.selected
            bg = '#ecf0f1' if ((pr // 3) + (pc // 3)) % 2 == 0 else '#bdc3c7'
            self.cells[(pr, pc)].config(bg=bg)
        
        if not self.fixed[r][c]:
            self.selected = (r, c)
            self.cells[(r, c)].config(bg='#f39c12')
    
    def key_press(self, event):
        if not self.selected: return
        r, c = self.selected
        
        if event.char in '123456789':
            num = int(event.char)
            self.puzzle[r][c] = num
            color = '#27ae60' if num == self.solution[r][c] else '#e74c3c'
            self.cells[(r, c)].config(text=str(num), fg=color)
            self.check_win()
        elif event.keysym in ('Delete', 'BackSpace'):
            self.puzzle[r][c] = 0
            self.cells[(r, c)].config(text='')
    
    def check_win(self):
        if self.puzzle == self.solution:
            tk.messagebox.showinfo("Congratulations!", "You solved the puzzle! 🎉")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    Sudoku().run()
