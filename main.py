import random
import copy
import time

class OthelloGame:
    def __init__(self):
        # Initialize 8x8 board with starting pieces
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        
        # Tracking game state
        self.current_player = 'B'
        self.move_history = []
        self.difficulty = 'hard'

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i, row in enumerate(self.board):
            print(f"{i} {' '.join(row)}")
        print(f"Current Player: {self.current_player}")

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != ' ':
            return False

        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ' and self.board[r][c] != player:
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == ' ':
                        break
                    if self.board[r][c] == player:
                        return True
                    r += d_row
                    c += d_col
        return False

    def get_valid_moves(self, player):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col, player):
            return False

        self.board[row][col] = player
        self.move_history.append((row, col, player))

        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ':
                if self.board[r][c] == player:
                    for flip_r, flip_c in to_flip:
                        self.board[flip_r][flip_c] = player
                    break
                to_flip.append((r, c))
                r += d_row
                c += d_col

        return True

    def count_pieces(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return black_count, white_count

    def is_game_over(self):
        return (len(self.get_valid_moves('B')) == 0 and 
                len(self.get_valid_moves('W')) == 0)

    def switch_player(self):
        self.current_player = 'W' if self.current_player == 'B' else 'B'

    def ai_move(self):
        valid_moves = self.get_valid_moves(self.current_player)
        if not valid_moves:
            return None

        # Advanced AI strategy with minimax
        best_move = None
        best_score = float('-inf') if self.current_player == 'B' else float('inf')
        
        for move in valid_moves:
            game_copy = copy.deepcopy(self)
            game_copy.make_move(move[0], move[1], self.current_player)
            score = game_copy.evaluate_board()
            
            if self.current_player == 'B':
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        
        return best_move

    def evaluate_board(self):
        board_weights = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]
        
        score = 0
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == 'B':
                    score += board_weights[row][col]
                elif self.board[row][col] == 'W':
                    score -= board_weights[row][col]
        
        return score

    def game_review(self):
        print("\n--- Game Review ---")
        black_moves = [m for m in self.move_history if m[2] == 'B']
        white_moves = [m for m in self.move_history if m[2] == 'W']

        print("Black's Moves:")
        if black_moves:
            for i, (row, col, _) in enumerate(black_moves, 1):
                print(f"Move {i}: ({row}, {col})")
        
        print("\nWhite's Moves:")
        if white_moves:
            for i, (row, col, _) in enumerate(white_moves, 1):
                print(f"Move {i}: ({row}, {col})")

        black_count, white_count = self.count_pieces()
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
            print("Computer is thinking...")
            time.sleep(1)  # Simulate thinking time
            ai_move = game.ai_move()
            game.make_move(ai_move[0], ai_move[1], game.current_player)
            print(f"The computer placed piece at ({ai_move[0]}, {ai_move[1]})")

        game.print_board()
        game.switch_player()

    game.game_review()

if __name__ == "__main__":
    main()