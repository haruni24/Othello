import numpy as np
import json
import network
import othello
from copy import deepcopy
import torch

class MCTS:
    def __init__(self, network, alpha, c_puct=1.0, epsilion=0.25):
        self.network = network
        self.c_puct = c_puct
        self.alpha = alpha
        self.eps = epsilion

        self.P = {}
        self.N = {}
        self.W = {}
        self.next_boards = {}

        # NumPy配列をJSONシリアライズするために、tolist()で変換する
        self.state_to_str = lambda state, player: json.dumps(state.tolist() if isinstance(state, np.ndarray) else state) + str(player)

    def search(self, root_state, current_player, num_simulations):
        s = self.state_to_str(root_state, current_player)
        if s not in self.P:
            _ = self.expand(root_state, current_player)

        legal_moves = othello.get_legal_moves(root_state, current_player)
        
        # 合法手がない場合、一様分布を返す
        if not legal_moves:
            return np.ones(othello.ACTION_SPACE) / othello.ACTION_SPACE
            
        non_legal_moves = [move for move in range(othello.ACTION_SPACE) if move not in legal_moves]
        
        for _ in range(num_simulations):
            U = [self.c_puct * self.P[s][move] * np.sqrt(sum(self.N[s]) + 1e-8) / (1 + self.N[s][move]) 
                for move in range(othello.ACTION_SPACE)]
            Q = [q / n if n != 0 else q for q, n in zip(self.W[s], self.N[s])]
            
            # リストをNumPy配列に変換
            scores = np.array([q + u for q, u in zip(Q, U)])
            # ここで非合法手のスコアを-infに設定
            for move in non_legal_moves:
                scores[move] = -np.inf

            # 最大値のインデックスが空でないことを確認
            max_indices = np.where(scores == scores.max())[0]
            if len(max_indices) == 0:
                # 全て-infの場合など、合法手からランダムに選択
                best_move = np.random.choice(legal_moves)
            else:
                best_move = np.random.choice(max_indices)
                
            next_board = self.next_boards[s][best_move]

            # next_boardがNoneでないことを確認
            if next_board is not None:
                v = -self.evalute(next_board, 3 - current_player)
                self.W[s][best_move] += v
                self.N[s][best_move] += 1
        
        # sum(self.N[s])が0の場合の対策
        n_sum = sum(self.N[s])
        if n_sum > 0:
            mcts_policy = np.array([n / n_sum for n in self.N[s]])
        else:
            # シミュレーションが進まなかった場合、合法手に均等な確率を割り当てる
            mcts_policy = np.zeros(othello.ACTION_SPACE)
            for move in legal_moves:
                mcts_policy[move] = 1.0 / len(legal_moves)
                
        return mcts_policy

    def expand(self, board, current_player):
        s = self.state_to_str(board, current_player)

        nn_policy, nn_value = self.network(othello.encode_state(board, current_player))
        nn_policy, nn_value = nn_policy.detach().numpy()[0], nn_value.detach().numpy()[0]

        self.P[s] = nn_policy
        self.N[s] = np.zeros(othello.ACTION_SPACE)
        self.W[s] = np.zeros(othello.ACTION_SPACE)

        legal_moves = othello.get_legal_moves(board, current_player)
        self.next_boards[s] = [
            othello.step(board, move, current_player) 
            if move in legal_moves else None
            for move in range(othello.ACTION_SPACE)]
        
        return nn_value
    
    def evalute(self, board, current_player):
        # boardがNoneの場合の対策
        if board is None:
            return 0  # または適切なデフォルト値
            
        s = self.state_to_str(board, current_player)

        if othello.is_done(board):
            reward = othello.get_result(board, current_player)
            return reward
        elif s not in self.P:
            return self.expand(board, current_player)
        else:
            U = [self.c_puct * self.P[s][move] * np.sqrt(sum(self.N[s]) + 1e-8) / (1 + self.N[s][move]) 
                for move in range(othello.ACTION_SPACE)]
            Q = [q / n if n != 0 else q for q, n in zip(self.W[s], self.N[s])]

            legal_moves = othello.get_legal_moves(board, current_player)
            
            # 合法手がない場合のチェック
            if not legal_moves:
                return 0
                
            non_legal_moves = [move for move in range(othello.ACTION_SPACE) if move not in legal_moves]

            # リストをNumPy配列に変換
            scores = np.array([q + u for q, u in zip(Q, U)])
            # ここで非合法手のスコアを-infに設定
            for move in non_legal_moves:
                scores[move] = -np.inf

            # 最大値のインデックスが空でないことを確認
            max_indices = np.where(scores == scores.max())[0]
            if len(max_indices) == 0:
                # 全て-infの場合など、合法手からランダムに選択
                best_move = np.random.choice(legal_moves)
            else:
                best_move = np.random.choice(max_indices)
                
            next_board = self.next_boards[s][best_move]

            # next_boardがNoneでないことを確認
            if next_board is None:
                return 0  # またはデフォルト値
                
            v = -self.evalute(next_board, 3 - current_player)

            self.W[s][best_move] += v
            self.N[s][best_move] += 1

            return v
