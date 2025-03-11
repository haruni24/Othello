import numpy as np
import json
from copy import deepcopy
import tensorflow as tf

class MCTS:
    def __init__(self, network):
        self.C = 1.0
        self.EXPAND_THRESHOLD = 20
        self.board_to_str = lambda board: json.dumps(board.board.tolist()) + str(board.turn)
        self.calculate_utc = lambda state: self.W[state] / self.N[state] + self.C * np.sqrt(np.log(self.total_simulate + 1) / (self.N[state] + 1e-6))
        self.W = {}
        self.N = {}
        self.P = {}
        self.UCT = {}
        self.total_simulate = 0
        self.network = network

    def evaluate(self, board):
        # board.end なら終局結果、それ以外はネットワーク評価を用いる
        if board.end:
            return board.result()
        state = board.get_state().reshape(1, 8, 8, 1).astype('float32')
        # ネットワークは policy, value の2出力を返す
        _, value = self.network.predict(state, verbose=0)
        return value[0][0]

    def playout(self, board):
        board = deepcopy(board)
        return self.evaluate(board)
    
    def start_search(self, board, board_address, current_turn):
        start_state = self.board_to_str(board)
        self.UCT[start_state] = [0] * len(board.legal_moves)
        for i, move in enumerate(board.legal_moves):
            self.total_simulate += 1
            board.push(move)
            state = self.board_to_str(board)
            self.W[state], self.N[state] = 0, 0
            # ここではランダムシミュレーションの代わりにネットワーク評価を利用
            result = self.playout(board)
            if result == current_turn:
                self.W[state] += 1
            self.N[state] += 1
            self.UCT[start_state][i] = self.calculate_utc(state)
            board.pop(board_address)

    def search(self, board, simulation_num):
        self.total_simulate = 0
        current_turn = board.turn
        board_address = 0
        board.remember(board_address)
        start_state = self.board_to_str(board)
        self.start_search(board, board_address, current_turn)
        for self.total_simulate in range(self.total_simulate, simulation_num):
            move_index = np.argmax(self.UCT[start_state])
            move = board.legal_moves[move_index]
            board.push(move)
            state = self.board_to_str(board)
            if self.N.get(state, 0) > self.EXPAND_THRESHOLD and not board.end:
                result = self.expand(board, current_turn)
            else:
                result = self.playout(board)
            if result == current_turn:
                self.W[state] = self.W.get(state, 0) + 1
            self.N[state] = self.N.get(state, 0) + 1
            self.UCT[start_state][move_index] = self.calculate_utc(state)
            board.pop(board_address)
        # 次の手として最もUTCが高いものを返す
        return board.legal_moves[np.argmax(self.UCT[start_state])]

    def expand(self, board, current_turn):
        board = deepcopy(board)
        board_address = 0
        board.remember(board_address)
        start_state = self.board_to_str(board)
        if start_state not in self.UCT:
            self.UCT[start_state] = [0] * len(board.legal_moves)
            self.start_search(board, board_address, current_turn)
        max_value = max(self.UCT[start_state])
        # 最大値と等しいインデックスを候補とする
        indices = np.argwhere(np.array(self.UCT[start_state]) == max_value).flatten()
        move_index = np.random.choice(indices)
        move = board.legal_moves[move_index]
        board.push(move)
        state = self.board_to_str(board)
        if self.N.get(state, 0) > self.EXPAND_THRESHOLD and not board.end:
            result = self.expand(board, current_turn)
        else:
            result = self.playout(board)
        if result == current_turn:
            self.W[state] = self.W.get(state, 0) + 1
        self.N[state] = self.N.get(state, 0) + 1
        self.UCT[start_state][move_index] = self.calculate_utc(state)
        return result
    
    def prepare_data(self, board_module):
        x_train = []
        y_train = []
        learning_board = board_module.Board()
        for uct_key in self.UCT.keys():
            y_board = np.zeros((8, 8), dtype=np.float32)
            learning_board.from_json(uct_key)
            input_data = learning_board.get_state()
            x_train.append(input_data)
            for i, move in enumerate(learning_board.legal_moves):
                x, y = move_from_pos(move)
                y_board[y][x] = self.UCT[uct_key][i]
            y_train.append(y_board.flatten())
        return (np.array(x_train).reshape(-1, 8, 8, 1).astype('float32'),
                np.array(y_train).astype('float32'))