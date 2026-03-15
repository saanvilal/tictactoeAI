import random

PLAYER_X = 'X'  
PLAYER_O = 'O'  
EMPTY = ' '


def print_board(board):
    
    for row in range(3):
        print(" | ".join(board[row]))
        if row < 2:
            print("---------")
    print("\n")


def check_winner(board, player):
   
    for row in range(3):
        if all([board[row][col] == player for col in range(3)]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):  
        return True
    if all([board[i][2 - i] == player for i in range(3)]): 
        return True
    return False


def is_board_full(board):
   
    return all([board[row][col] != EMPTY for row in range(3) for col in range(3)])


def get_empty_positions(board):

    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY]


def minimax(board, depth, is_maximizing, alpha, beta, difficulty):
    
    if check_winner(board, PLAYER_X):
        return -10 + depth
    if check_winner(board, PLAYER_O):
        return 10 - depth
    if is_board_full(board):
        return 0 

    if depth >= difficulty:
        return 0  
        
    if is_maximizing:
        max_eval = float('-inf')
        for (row, col) in get_empty_positions(board):
            board[row][col] = PLAYER_O  
            eval = minimax(board, depth + 1, False, alpha, beta, difficulty)
            board[row][col] = EMPTY 
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
   
    best_val = float('-inf')
    best_moves = []  

    for (row, col) in get_empty_positions(board):
        board[row][col] = PLAYER_O
        move_val = minimax(board, 0, False, float('-inf'), float('inf'), difficulty)
        board[row][col] = EMPTY

        if move_val > best_val:
            best_val = move_val
            best_moves = [(row, col)]
        elif move_val == best_val:
            best_moves.append((row, col))

    
    return random.choice(best_moves)


def player_move(board):
    
    while True:
        try:
            move = input("Enter your move (1-9) or type 'q' to quit: ")
            if move.lower() == 'q': 
                print("Thanks for playing!")
                return 'quit'  
            move = int(move) - 1 
            row, col = divmod(move, 3) 
            if board[row][col] == EMPTY:  
                board[row][col] = PLAYER_X 
                break  
            else:
                print("This position is already taken! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Please choose a number between 1 and 9.")


def handle_draw(board):
    
    if is_board_full(board):
        print_board(board) 
        print("It's a draw!") 
        if input("Would you like to play again? (y/n): ").lower() == 'y':
            play_game() 
        else:
            print("Thanks for playing!")  
            return True  
    return False  


def play_game():
    
    print("Welcome to Tic-Tac-Toe!")
    mode = input("Choose game mode: (1) Player vs AI (2) Player vs Player: ")
    if mode == '1':  # Player vs AI mode
        difficulty = int(input("Choose AI difficulty (1: Easy, 2: Medium, 3: Hard): "))
        board = [[EMPTY] * 3 for _ in range(3)]  # Create an empty board
        current_player = PLAYER_X  # Player X starts first

        while True:
            print_board(board) 

            if current_player == PLAYER_X:  
                if player_move(board) == 'quit': 
                    break 
                if check_winner(board, PLAYER_X):
                    print_board(board)
                    print("Player X wins!")
                    break
                current_player = PLAYER_O  
            else:  
                print("Thinking...")
                row, col = best_move(board, difficulty)  
                board[row][col] = PLAYER_O  
                if check_winner(board, PLAYER_O): 
                    print_board(board)
                    print("Player O (AI) wins!")
                    break
                current_player = PLAYER_X 

            if handle_draw(board):
                break

    elif mode == '2':  
        board = [[EMPTY] * 3 for _ in range(3)] 
        current_player = PLAYER_X  

        while True:
            print_board(board) 

            if current_player == PLAYER_X:  
                if player_move(board) == 'quit':
                    break
                if check_winner(board, PLAYER_X):
                    print_board(board)
                    print("Player X wins!")
                    break
                current_player = PLAYER_O 
            else:
                if player_move(board) == 'quit': 
                    break
                if check_winner(board, PLAYER_O): 
                    print_board(board)
                    print("Player O wins!")
                    break
                current_player = PLAYER_X  

            if handle_draw(board):  
                break

    else:
        print("Invalid choice! Please choose '1' for Player vs AI or '2' for Player vs Player.")
        play_game()


if __name__ == "__main__":
    play_game()
