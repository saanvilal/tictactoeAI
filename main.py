import random

# Define constants for the board
PLAYER_X = 'X'  # Player X's symbol
PLAYER_O = 'O'  # AI's symbol (Player O)
EMPTY = ' '     # Empty space on the board


def print_board(board):
    """Prints the current state of the Tic-Tac-Toe board."""
    for row in range(3):
        print(" | ".join(board[row]))
        if row < 2:
            print("---------")
    print("\n")


def check_winner(board, player):
    """Checks if the given player has won the game."""
    for row in range(3):
        if all([board[row][col] == player for col in range(3)]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):  # Top-left to bottom-right
        return True
    if all([board[i][2 - i] == player for i in range(3)]):  # Top-right to bottom-left
        return True
    return False


def is_board_full(board):
    """Checks if the board is completely full."""
    return all([board[row][col] != EMPTY for row in range(3) for col in range(3)])


def get_empty_positions(board):
    """Returns a list of empty positions on the board."""
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY]


def minimax(board, depth, is_maximizing, alpha, beta, difficulty):
    """The Minimax algorithm to decide the best move for the AI."""
    if check_winner(board, PLAYER_X):
        return -10 + depth
    if check_winner(board, PLAYER_O):
        return 10 - depth
    if is_board_full(board):
        return 0  # Neutral score if the board is full

    if depth >= difficulty:
        return 0  # Stop recursion if the depth exceeds difficulty

    if is_maximizing:
        max_eval = float('-inf')
        for (row, col) in get_empty_positions(board):
            board[row][col] = PLAYER_O  # AI's move
            eval = minimax(board, depth + 1, False, alpha, beta, difficulty)
            board[row][col] = EMPTY  # Undo move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for (row, col) in get_empty_positions(board):
            board[row][col] = PLAYER_X  # Player's move
            eval = minimax(board, depth + 1, True, alpha, beta, difficulty)
            board[row][col] = EMPTY  # Undo move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def best_move(board, difficulty):
    """Finds the best move for the AI using the minimax algorithm."""
    best_val = float('-inf')
    best_moves = []  # List to store moves with the best evaluation

    for (row, col) in get_empty_positions(board):
        board[row][col] = PLAYER_O
        move_val = minimax(board, 0, False, float('-inf'), float('inf'), difficulty)
        board[row][col] = EMPTY

        if move_val > best_val:
            best_val = move_val
            best_moves = [(row, col)]  # New best move found, reset the list
        elif move_val == best_val:
            best_moves.append((row, col))  # Add this move to the list of best moves

    # If there are multiple best moves, randomly choose one
    return random.choice(best_moves)


def player_move(board):
    """Prompts the player to make a move with validation."""
    while True:
        try:
            move = input("Enter your move (1-9) or type 'q' to quit: ")
            if move.lower() == 'q':  # Allow the player to quit
                print("Thanks for playing!")
                return 'quit'  # Return 'quit' to end the game
            move = int(move) - 1  # Convert to 0-indexed
            row, col = divmod(move, 3)  # Convert move to row and column
            if board[row][col] == EMPTY:  # Make sure the position is empty
                board[row][col] = PLAYER_X  # Mark the player's move
                break  # Exit the loop if the move is valid
            else:
                print("This position is already taken! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Please choose a number between 1 and 9.")


def handle_draw(board):
    """Checks if the game is a draw and asks if the player wants to restart."""
    if is_board_full(board):
        print_board(board)  # Display the final board
        print("It's a draw!")  # Inform the player that the game is a draw
        if input("Would you like to play again? (y/n): ").lower() == 'y':
            play_game()  # Restart the game if the player says 'yes'
        else:
            print("Thanks for playing!")  # Exit the game if the player says 'no'
            return True  # Return True to indicate the game has ended
    return False  # Return False if it's not a draw


def play_game():
    """Main function to start and control the game."""
    print("Welcome to Tic-Tac-Toe!")
    mode = input("Choose game mode: (1) Player vs AI (2) Player vs Player: ")
    if mode == '1':  # Player vs AI mode
        difficulty = int(input("Choose AI difficulty (1: Easy, 2: Medium, 3: Hard): "))
        board = [[EMPTY] * 3 for _ in range(3)]  # Create an empty board
        current_player = PLAYER_X  # Player X starts first

        while True:
            print_board(board)  # Display the current board

            if current_player == PLAYER_X:  # Player's turn
                if player_move(board) == 'quit':  # Let the player make a move
                    break  # Exit if the player quits
                if check_winner(board, PLAYER_X):  # Check if the player wins
                    print_board(board)
                    print("Player X wins!")
                    break
                current_player = PLAYER_O  # Switch to AI's turn
            else:  # AI's turn
                print("AI is thinking...")
                row, col = best_move(board, difficulty)  # Let AI decide the best move
                board[row][col] = PLAYER_O  # Mark AI's move
                if check_winner(board, PLAYER_O):  # Check if the AI wins
                    print_board(board)
                    print("Player O (AI) wins!")
                    break
                current_player = PLAYER_X  # Switch to player's turn

            if handle_draw(board):  # Check if the game is a draw
                break

    elif mode == '2':  # Player vs Player mode
        board = [[EMPTY] * 3 for _ in range(3)]  # Create an empty board
        current_player = PLAYER_X  # Player X starts first

        while True:
            print_board(board)  # Display the current board

            if current_player == PLAYER_X:  # Player X's turn
                if player_move(board) == 'quit':  # Let Player X make a move
                    break
                if check_winner(board, PLAYER_X):  # Check if Player X wins
                    print_board(board)
                    print("Player X wins!")
                    break
                current_player = PLAYER_O  # Switch to Player O's turn
            else:  # Player O's turn
                if player_move(board) == 'quit':  # Let Player O make a move
                    break
                if check_winner(board, PLAYER_O):  # Check if Player O wins
                    print_board(board)
                    print("Player O wins!")
                    break
                current_player = PLAYER_X  # Switch to Player X's turn

            if handle_draw(board):  # Check if the game is a draw
                break

    else:
        print("Invalid choice! Please choose '1' for Player vs AI or '2' for Player vs Player.")
        play_game()


if __name__ == "__main__":
    play_game()