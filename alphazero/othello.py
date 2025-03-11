import numpy as np
import torch
import json
from copy import deepcopy

EMPTY = 0
BLACK = 1
WHITE = 2

ACTION_SPACE = 64


def encode_state(board, player):
    input_board = np.zeros((3, 8, 8))
    input_board[0] = (board==player)
    input_board[1] = (board==3-player)
    input_board[2] = (board==EMPTY)

    return torch.from_numpy(input_board).float()

def is_legal_move(board, move, player):
    x, y = move%8, move//8
    total = 0
    if board[y][x]!=EMPTY : return False
    for dx in range(-1,2):
        for dy in range(-1,2):
            if total>0: return total
            sx,sy = x,y
            k = 0
            while True:
                sx,sy = dx+sx,dy+sy
                if sx>7 or sx<0 or sy>7 or sy<0 or board[sy][sx]==EMPTY: break
                if board[sy][sx]==3-player: k+=1
                if board[sy][sx]==player:
                    total+=k
                    break
    return total

def get_legal_moves(board, player):
    legal_moves = []

    for i in range(ACTION_SPACE):
        if is_legal_move(board, i, player):
            legal_moves.append(i)

    return legal_moves

def step(board, move, player):
    x, y = move%8, move//8
    new_board = deepcopy(board)
    new_board[y][x] = player
    for dx in range(-1,2):
        for dy in range(-1,2):
            if dx==0 and dy==0: continue
            sx,sy = x,y
            k = 0
            while True:
                sx,sy = dx+sx,dy+sy
                if sx>7 or sx<0 or sy>7 or sy<0 or board[sy][sx]==EMPTY: break
                if board[sy][sx]==3-player: k+=1
                if board[sy][sx]==player:
                    for i in range(k):
                        new_board[sy-dy*i][sx-dx*i] = player
                    break
    return new_board

def is_done(board):
    return len(get_legal_moves(board, BLACK))==0 and len(get_legal_moves(board, WHITE))==0

def get_result(board, player):
    count = np.count_nonzero(board==BLACK) - np.count_nonzero(board==WHITE)
    if count>0 and player==BLACK: return 1
    if count<0 and player==WHITE: return 1
    if count>0 and player==WHITE: return -1
    if count<0 and player==BLACK: return -1
    return 0

def get_initial_board():
    board = np.zeros((8, 8))
    board[3][3] = WHITE
    board[4][4] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    return board