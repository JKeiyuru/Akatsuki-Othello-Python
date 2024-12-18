import random
import copy
import time

class OthelloGame:
    def __init__(self):
        # Board initialization
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        
        self.current_player = 'B'
        self.move_history = []

    def is_valid_move(self, row, col, player):
        pass
        # Move validation logic
        # Full implementation of checking move legality

    def get_valid_moves(self, player):
        # Find all valid moves for a player
        moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves

    def make_move(self, row, col, player):
        pass
        # Core move implementation
        # Logic for placing piece and flipping opponent pieces

    def is_game_over(self):
        # Check if no more moves are possible
        return (len(self.get_valid_moves('B')) == 0 and 
                len(self.get_valid_moves('W')) == 0)

    def count_pieces(self):
        # Count black and white pieces
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return black_count, white_count

   
    def game_review(self, game):
        print("\n--- Game Review ---")
        black_moves = [m for m in game.move_history if m[2] == 'B']
        white_moves = [m for m in game.move_history if m[2] == 'W']

    print("Black's Moves:")
    for i, (row, col, _) in enumerate(black_moves, 1):
        print(f"Move {i}: ({row}, {col})")
    
    print("\nWhite's Moves:")
    for i, (row, col, _) in enumerate(white_moves, 1):
        print(f"Move {i}: ({row}, {col})")

    black_count, white_count = game.count_pieces()
    print(f"\nFinal Score - Black: {black_count}, White: {white_count}")
    
    if black_count > white_count:
        print("Black wins!")
    elif white_count > black_count:
        print("White wins!")
    else:
        print("It's a draw!")



def main():
    print("Welcome to Othello!")
    mode = input("Choose mode (1: Player vs Player, 2: Player vs AI): ")

    game = OthelloGame()
    game.print_board()

    while not game.is_game_over():
        valid_moves = game.get_valid_moves(game.current_player)
        
        if not valid_moves:
            print(f"No valid moves for {game.current_player}. Skipping turn.")
            game.switch_player()
            continue
        
        if mode == '1' or (mode == '2' and game.current_player == 'B'):
            # Human player
            print(f"Valid moves for {game.current_player}: {valid_moves}")
            while True:
                try:
                    row = int(input("Enter row (0-7): "))
                    col = int(input("Enter column (0-7): "))
                    if (row, col) in valid_moves:
                        game.make_move(row, col, game.current_player)
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter numbers.")
        else:
            # AI player
            print("AI is thinking...")
            time.sleep(1)  # Simulate thinking time
            ai_move = game.ai_move()
            game.make_move(ai_move[0], ai_move[1], game.current_player)
            print(f"AI placed piece at ({ai_move[0]}, {ai_move[1]})")
    
        game.print_board()
        game.switch_player()
    
    game.game_review()
    if name == "main":
        main()