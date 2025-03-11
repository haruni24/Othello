class Game:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = 1  # 1 for player 1, -1 for player 2
        self.winner = None

    def initialize_board(self):
        return [[0 for _ in range(8)] for _ in range(8)]

    def apply_move(self, move):
        x, y = move
        if self.is_valid_move(x, y):
            self.board[y][x] = self.current_turn
            self.current_turn *= -1  # Switch turns
            self.check_winner()

    def is_valid_move(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8 and self.board[y][x] == 0

    def check_winner(self):
        # Implement logic to check for a winner
        # This is a placeholder for actual win-checking logic
        if self.is_board_full():
            self.winner = 0  # Draw
        # Additional win-checking logic would go here

    def is_board_full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def get_legal_moves(self):
        return [(x, y) for x in range(8) for y in range(8) if self.is_valid_move(x, y)]

    def reset_game(self):
        self.board = self.initialize_board()
        self.current_turn = 1
        self.winner = None

    def get_game_state(self):
        return {
            'board': self.board,
            'current_turn': self.current_turn,
            'winner': self.winner
        }