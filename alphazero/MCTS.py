import numpy as np
from reversi.common import *

class MCTS:
    def __init__(self):
        self.C = 1.0

    def search(self, board, num_playouts):
        legal_move_num = len(board.legal_moves)
        prob_list = []
        uct_score, try_count, win_count = [1] * legal_move_num, [0] * legal_move_num, [0] * legal_move_num
        current_turn = board.turn
        board.remember()
        for i in range(num_playouts):
            move = board.legal_moves[i] if i<legal_move_num else np.random.choice(board.legal_moves, p=prob_list)
            move_index = board.legal_moves.index(move)
            try_count[move_index] += 1
            board.push(move)
            result = self.playout(board)
            if result==current_turn: win_count[move_index] += 1
            uct_score[move_index] = win_count[move_index]/try_count[move_index] + self.C * np.sqrt(np.log(i+1)/try_count[move_index])
            prob_list = converse_prob(uct_score)
            board.pop()
        return board.legal_moves[np.argmax(try_count)]

    def playout(self, board):
        while not board.end:
            next_move = np.random.choice(board.legal_moves)
            board.push(next_move)
        return board.result()