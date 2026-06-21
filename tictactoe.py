"""
╔══════════════════════════════════════╗
║   AI Tic-Tac-Toe  |  Minimax Agent  ║
╚══════════════════════════════════════╝
Human = X   |   AI = O
"""

import os
import time

# ─── Score tracking ──────────────────────────────────────────────────────────
score = {"wins": 0, "losses": 0, "draws": 0}


# ─── Board helpers ───────────────────────────────────────────────────────────
def make_board():
    return [" "] * 9


def print_board(board):
    symbols = []
    for i, cell in enumerate(board):
        if cell == "X":
            symbols.append("\033[92mX\033[0m")   # green
        elif cell == "O":
            symbols.append("\033[91mO\033[0m")   # red
        else:
            symbols.append(f"\033[90m{i+1}\033[0m")  # grey number hint

    print()
    print(f"  {symbols[0]} │ {symbols[1]} │ {symbols[2]}")
    print("  ──┼───┼──")
    print(f"  {symbols[3]} │ {symbols[4]} │ {symbols[5]}")
    print("  ──┼───┼──")
    print(f"  {symbols[6]} │ {symbols[7]} │ {symbols[8]}")
    print()


WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # cols
    (0, 4, 8), (2, 4, 6),               # diagonals
]


def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return None


def is_full(board):
    return " " not in board


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == " "]


# ─── Minimax algorithm ───────────────────────────────────────────────────────
def minimax(board, is_maximizing, alpha=-float("inf"), beta=float("inf")):
    winner = check_winner(board)
    if winner == "O":
        return 10
    if winner == "X":
        return -10
    if is_full(board):
        return 0

    if is_maximizing:
        best = -float("inf")
        for move in available_moves(board):
            board[move] = "O"
            score_val = minimax(board, False, alpha, beta)
            board[move] = " "
            best = max(best, score_val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float("inf")
        for move in available_moves(board):
            board[move] = "X"
            score_val = minimax(board, True, alpha, beta)
            board[move] = " "
            best = min(best, score_val)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def ai_best_move(board):
    best_score = -float("inf")
    best_move = None
    for move in available_moves(board):
        board[move] = "O"
        move_score = minimax(board, False)
        board[move] = " "
        if move_score > best_score:
            best_score = move_score
            best_move = move
    return best_move


# ─── Display helpers ─────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("\033[96m╔══════════════════════════════════════╗\033[0m")
    print("\033[96m║   AI Tic-Tac-Toe  |  Minimax Agent  ║\033[0m")
    print("\033[96m╚══════════════════════════════════════╝\033[0m")
    print(f"  \033[92mYou (X)\033[0m  Wins: {score['wins']}  "
          f"Losses: {score['losses']}  Draws: {score['draws']}")
    print()


def print_result(result):
    if result == "win":
        print("\033[92m🎉  You win! Great moves!\033[0m")
    elif result == "loss":
        print("\033[91m🤖  AI wins! Minimax never misses.\033[0m")
    else:
        print("\033[93m🤝  It's a draw! Perfect play from both sides.\033[0m")


# ─── Single game ─────────────────────────────────────────────────────────────
def play_game():
    board = make_board()
    current = "X"   # human always goes first

    while True:
        clear()
        print_header()

        if current == "X":
            print("  \033[93mYour turn — pick a square (1–9):\033[0m")
        else:
            print("  \033[91mAI is thinking…\033[0m")

        print_board(board)

        if current == "X":
            # Human move
            while True:
                try:
                    raw = input("  Enter position (1-9): ").strip()
                    if raw.lower() == "q":
                        return "quit"
                    pos = int(raw) - 1
                    if pos < 0 or pos > 8:
                        print("  \033[91mEnter a number between 1 and 9.\033[0m")
                        continue
                    if board[pos] != " ":
                        print("  \033[91mThat square is taken! Choose another.\033[0m")
                        continue
                    board[pos] = "X"
                    break
                except ValueError:
                    print("  \033[91mInvalid input. Enter a number 1–9 or 'q' to quit.\033[0m")
        else:
            # AI move
            time.sleep(0.4)   # brief pause so it feels like it's thinking
            move = ai_best_move(board)
            board[move] = "O"

        winner = check_winner(board)
        if winner:
            clear()
            print_header()
            print_board(board)
            if winner == "X":
                score["wins"] += 1
                print_result("win")
            else:
                score["losses"] += 1
                print_result("loss")
            return "done"

        if is_full(board):
            clear()
            print_header()
            print_board(board)
            score["draws"] += 1
            print_result("draw")
            return "done"

        # Swap turn
        current = "O" if current == "X" else "X"


# ─── Main loop ────────────────────────────────────────────────────────────────
def main():
    clear()
    print("\033[96m╔══════════════════════════════════════╗\033[0m")
    print("\033[96m║   AI Tic-Tac-Toe  |  Minimax Agent  ║\033[0m")
    print("\033[96m╚══════════════════════════════════════╝\033[0m")
    print()
    print("  \033[97mYou play as \033[92mX\033[97m.  AI plays as \033[91mO\033[97m.")
    print("  Pick squares by entering their number (1–9).")
    print("  Type \033[93m'q'\033[97m during a game to quit.\033[0m")
    print()

    while True:
        result = play_game()
        if result == "quit":
            break

        print()
        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            break

    # Final scoreboard
    print()
    print("\033[96m─────── Final Scoreboard ───────\033[0m")
    print(f"  \033[92mWins   : {score['wins']}\033[0m")
    print(f"  \033[91mLosses : {score['losses']}\033[0m")
    print(f"  \033[93mDraws  : {score['draws']}\033[0m")
    print("\033[96m────────────────────────────────\033[0m")
    print("  Thanks for playing! 🎮")
    print()


if __name__ == "__main__":
    main()
