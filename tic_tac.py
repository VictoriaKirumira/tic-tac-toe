import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        # Initialize game variables
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player_symbol = "X"
        self.computer_symbol = "O"
        self.current_player = "Player"
        self.first_game = True
        self.winner = None
        self.player_score = 0
        self.computer_score = 0

        # Create a 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text="", font=('Arial', 40), width=5, height=2, 
                                   command=lambda r=row, c=col: self.on_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        # Create labels for scores
        self.player_score_label = tk.Label(self.root, text=f"Player: {self.player_score}", font=('Arial', 20))
        self.player_score_label.grid(row=3, column=0, columnspan=2)

        self.computer_score_label = tk.Label(self.root, text=f"Computer: {self.computer_score}", font=('Arial', 20))
        self.computer_score_label.grid(row=3, column=2, columnspan=2)

        # Allow player to choose X or O
        self.choose_symbol()

    def choose_symbol(self):
        # Ask player if they want to be X or O
        choice = messagebox.askquestion("Choose Symbol", "Do you want to play as X?")
        if choice == 'yes':
            self.player_symbol = "X"
            self.computer_symbol = "O"
        else:
            self.player_symbol = "O"
            self.computer_symbol = "X"
        
        # Player starts the first game
        self.current_player = "Player"
    
    def on_click(self, row, col):
        if self.board[row][col] == "" and self.current_player == "Player":
            self.board[row][col] = self.player_symbol
            self.buttons[row][col].config(text=self.player_symbol)
            
            if self.check_winner(self.player_symbol):
                self.update_score("Player")
                self.show_winner("Player")
            elif self.check_tie():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "Computer"
                self.computer_move()
    
    def computer_move(self):
        # Simple computer AI: select a random empty spot
        available_moves = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        if available_moves:
            row, col = random.choice(available_moves)
            self.board[row][col] = self.computer_symbol
            self.buttons[row][col].config(text=self.computer_symbol)
            
            if self.check_winner(self.computer_symbol):
                self.update_score("Computer")
                self.show_winner("Computer")
            elif self.check_tie():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "Player"
    
    def check_winner(self, symbol):
        # Check rows, columns, and diagonals for a winner
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == symbol:
                self.highlight_winning_line([(i, 0), (i, 1), (i, 2)])
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == symbol:
                self.highlight_winning_line([(0, i), (1, i), (2, i)])
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
            self.highlight_winning_line([(0, 0), (1, 1), (2, 2)])
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            self.highlight_winning_line([(0, 2), (1, 1), (2, 0)])
            return True
        return False
    
    def check_tie(self):
        for row in self.board:
            if "" in row:
                return False
        return True
    
    def highlight_winning_line(self, winning_cells):
        for row, col in winning_cells:
            self.buttons[row][col].config(bg="green")
    
    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.winner = winner
        self.reset_game()
    
    def update_score(self, winner):
        # Add 5 points to the winner's score
        if winner == "Player":
            self.player_score += 5
        elif winner == "Computer":
            self.computer_score += 5
        
        # Update the score labels
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")

    def reset_game(self):
        # Reset the board for a new game
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", bg="SystemButtonFace")
        
        # Determine who goes first in the next game
        if not self.first_game and self.winner == "Computer":
            self.current_player = "Computer"
            self.computer_move()
        else:
            self.current_player = "Player"
        
        self.first_game = False

# Create the main window
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
