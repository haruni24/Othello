from dataclasses import dataclass
import ray
import numpy as np
import torch

from network import PVNet
from MCTS import MCTS
import othello

@ray.remote(num_cpus=1, num_gpus=0)
def selfplay(weights, num_mcts_simulations, dirichlet_alpha=0.35):
    @dataclass
    class Sample:
        board: np.ndarray
        mcts_policy: np.ndarray
        player: int
        reward: int

    record = []
    board = othello.get_initial_board()

    network = PVNet()
    network(othello.encode_state(board))
    network.set_weights(weights)

    mcts = MCTS(network, alpha=dirichlet_alpha)

    current_player = othello.BLACK
    done = False
    i = 0
    while not done:
        mcts_policy = mcts.search(board, current_player, num_mcts_simulations)
        if i < 10:
            move = np.random.choice(range(othello.ACTION_SPACE), p=mcts_policy)

        else:
            move = np.random.choice(np.where(mcts_policy == mcts_policy.max())[0])

        record.append(Sample(board, mcts_policy, current_player, None))

        board = othello.step(board, move, current_player)
        current_player = 3 - current_player

        i += 1

    for sample in record:
        sample.reward = othello.get_result(sample.board, sample.player)

    return record
