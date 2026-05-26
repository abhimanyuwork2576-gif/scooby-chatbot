import math

def print_board(board):
    for i in range(3):
        print(board[i*3:(i+1)*3])

def check_winner(board):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8], # rows
        [0,3,6],[1,4,7],[2,5,8], # cols
        [0,4,8],[2,4,6]          # diagonals
    ]
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] != " ":
            return board[cond[0]]
    if " " not in board:
        return "Draw"
    return Nonepython 


def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == "X": return -10
    if winner == "O": return 10
    if winner == "Draw": return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth+1, alpha, beta, False)
                board[i] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth+1, alpha, beta, True)
                board[i] = " "
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# Game Loop
board = [" "]*9
while True:
    print_board(board)
    human = int(input("Enter your move (0-8): "))
    if board[human] == " ":
        board[human] = "X"
    else:
        print("Invalid move!")
        continue

    if check_winner(board): break

    ai = best_move(board)
    board[ai] = "O"

    if check_winner(board): break

print_board(board)
print("Winner:", check_winner(board))

