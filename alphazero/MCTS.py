import numpy as np
from reversi.common import *

class MCTS:
    def __init__(self):
        pass

    def search(self, board, num_playouts):
        winning_rates = []
        current_turn = board.turn
        board.remember()
        for move in board.legal_moves:
            win_count = 0
            for _ in range(num_playouts):
                board.push(move)
                result = self.playout(board)
                if result==current_turn: win_count+=1
                board.pop()
            winning_rates.append(win_count/num_playouts)
        return board.legal_moves[np.argmax(winning_rates)]

    def playout(self, board):
        while not board.end:
            next_move = np.random.choice(board.legal_moves)
            board.push(next_move)
        return board.result()