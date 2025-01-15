import numpy as np

class MCTS:
    def __init__(self):
        pass

    def search(self, board, num_playouts):
        for move in board.legal_moves:
            board.push(move)
            for _ in range(num_playouts):
                self.play_out(board)
            board.pop()

    def playout(self, board):
        while not board.end:
            next_move = np.random.choice(board.legal_moves)
            board.push(next_move)
        return board.result()