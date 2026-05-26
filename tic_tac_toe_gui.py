import tkinter as tk
from tkinter import messagebox
import math
import winsound
import random

# ---------- Game Logic ----------
def check_winner(game_board):
    win_patterns = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for pattern in win_patterns:
        if game_board[pattern[0]] == game_board[pattern[1]] == game_board[pattern[2]] != " ":
            return game_board[pattern[0]]
    if " " not in game_board:
        return "Draw"
    return None

def minimax(game_board, depth, alpha, beta, is_maximizing):
    result = check_winner(game_board)
    if result == "X": return -10
    if result == "O": return 10
    if result == "Draw": return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if game_board[i] == " ":
                game_board[i] = "O"
                score = minimax(game_board, depth+1, alpha, beta, False)
                game_board[i] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if game_board[i] == " ":
                game_board[i] = "X"
                score = minimax(game_board, depth+1, alpha, beta, True)
                game_board[i] = " "
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score

def ai_move(game_board, difficulty="Medium"):
    possible_moves = []
    for i in range(9):
        if game_board[i] == " ":
            game_board[i] = "O"
            score = minimax(game_board, 0, -math.inf, math.inf, False)
            game_board[i] = " "
            possible_moves.append((i, score))

    if difficulty == "Hard":
        return max(possible_moves, key=lambda x: x[1])[0]
    elif difficulty == "Easy":
        return random.choice(possible_moves)[0]
    elif difficulty == "Medium":
        if random.random() < 0.7:
            return max(possible_moves, key=lambda x: x[1])[0]
        else:
            return random.choice(possible_moves)[0]

# ---------- Tkinter GUI ----------
def player_click(i):
    global game_board, player_points, ai_points, tie_points
    if game_board[i] == " ":
        game_board[i] = "X"
        cells[i].config(text="X", fg="green", bg="lightyellow")
        winsound.Beep(700, 150)
        result = check_winner(game_board)
        if result:
            finish_game(result)
            return
        ai_choice = ai_move(game_board, difficulty=current_difficulty.get())
        game_board[ai_choice] = "O"
        cells[ai_choice].config(text="O", fg="red", bg="lightblue")  # AI text is red
        winsound.Beep(400, 150)
        result = check_winner(game_board)
        if result:
            finish_game(result)

def finish_game(result):
    global player_points, ai_points, tie_points
    if result == "Draw":
        tie_points += 1
        messagebox.showinfo("Result", "It's a tie! Well played.")
    elif result == "X":
        player_points += 1
        messagebox.showinfo("Victory", "Great Job!")
    else:
        ai_points += 1
        messagebox.showinfo("Defeat", "AI Dominates! Try Again!")
    update_scoreboard()
    reset_game()

def reset_game():
    global game_board
    game_board = [" "]*9
    for c in cells:
        c.config(text=" ", bg="white")

def update_scoreboard():
    score_label.config(
        text=f"Player: {player_points}   AI: {ai_points}   Ties: {tie_points}"
    )

root = tk.Tk()
root.title("Tic Tac Toe - CODSOFT Internship")
game_board = [" "]*9
cells = []
player_points = 0
ai_points = 0
tie_points = 0

# Difficulty Menu
current_difficulty = tk.StringVar(value="Medium")
difficulty_menu = tk.OptionMenu(root, current_difficulty, "Easy", "Medium", "Hard")
difficulty_menu.config(font=("Arial", 14, "bold"), bg="lightgreen")
difficulty_menu.grid(row=0, column=0, columnspan=3, sticky="we")

# Scoreboard
score_label = tk.Label(root, text="Player: 0   AI: 0   Ties: 0",
                       font=("Arial", 20, "bold"), fg="darkblue")
score_label.grid(row=1, column=0, columnspan=3)

# Grid Buttons
for i in range(9):
    b = tk.Button(root, text=" ", width=10, height=3,
                  font=("Arial", 22, "bold"),
                  bg="white",
                  command=lambda i=i: player_click(i))
    b.grid(row=(i//3)+2, column=i%3)
    cells.append(b)

# Restart Button
restart_btn = tk.Button(root, text="New Game", font=("Arial", 16, "bold"),
                        bg="orange", command=reset_game)
restart_btn.grid(row=5, column=0, columnspan=3, sticky="we")

root.mainloop()


