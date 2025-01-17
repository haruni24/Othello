import numpy as np
from reversi.common import *

class MCTS:
    def __init__(self):
        self.C = 1.0
        self.DEPLOY_THRESHOLD = 20
        self.board = None
        self.current_turn = None

    def calculate_utc(self, move, try_count, win_count, board_address):
        move_index = self.board.legal_moves.index(move)
        try_count[move_index] += 1
        self.board.push(move)
        result = self.playout()
        if result==self.current_turn: win_count[move_index] += 1
        self.board.pop(board_address)
        return win_count[move_index]/try_count[move_index] + self.C * np.sqrt(np.log(move_index+1)/(try_count[move_index]+1e-6))

    def spread(self,uct_score, try_count, win_count):
        board_address = 1
        self.board.remember(board_address)
        if len(try_count)==0:
            for move in self.board.legal_moves:
                try_count.append(0)
                win_count.append(0)
                uct_score.append(self.calculate_utc(move, try_count, win_count, board_address))
        else:
            next_index = np.argmax(uct_score)
            uct_score[next_index] = self.calculate_utc(self.board.legal_moves[next_index], try_count, win_count, board_address)

    def search(self, board, num_playouts):
        self.board = board
        board_address = 0
        legal_move_num = len(self.board.legal_moves)
        uct_score, try_count, win_count = [1] * legal_move_num, [0] * legal_move_num, [0] * legal_move_num
        leaf_uct_score, leaf_try_count, leaf_win_count = [[]] * legal_move_num, [[]] * legal_move_num, [[]] * legal_move_num
        self.current_turn = self.board.turn
        self.board.remember(board_address)
        for i in range(num_playouts):
            move = self.board.legal_moves[i] if i<legal_move_num else self.board.legal_moves[np.argmax(uct_score)]
            move_index = self.board.legal_moves.index(move)
            if(try_count[move_index]>self.DEPLOY_THRESHOLD):
                self.spread(leaf_uct_score[move_index], leaf_try_count[move_index], leaf_win_count[move_index])
            try_count[move_index] += 1
            self.board.push(move)
            result = self.playout()
            if result==self.current_turn: win_count[move_index] += 1
            uct_score[move_index] = win_count[move_index]/try_count[move_index] + self.C * np.sqrt(np.log(i+1)/(try_count[move_index]+1e-6))
            self.board.pop(board_address)
        return self.board.legal_moves[np.argmax(try_count)]

    def playout(self):
        while not self.board.end:
            next_move = np.random.choice(self.board.legal_moves)
            self.board.push(next_move)
        return self.board.result()