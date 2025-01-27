import numpy as np
from reversi.common import *

class Board:
    def __init__(self):
        self.reset()
        self.cash = [[np.zeros((8, 8), dtype=np.int8), self.turn, self.legal_moves]]

    def __str__(self):
        return str(self.board)

    def reset(self):
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.board[4, 3] = self.board[3, 4] = BLACK
        self.board[3, 3] = self.board[4, 4] = WHITE
        self.turn = BLACK
        self.legal_moves = self.get_legal_moves()
        self.end = False
    
    def get_legal_moves(self):
        moves = []
        for y in range(8):
            for x in range(8):
                if self.is_legal((x, y)):
                    moves.append(move_to_pos(x, y))
        return moves
    
    def is_legal(self, move):
        if isinstance(move, str): move = move_from_pos(move)
        x, y = move[0], move[1]
        total = 0
        if self.board[y][x]!=EMPTY : return False
        for dx in range(-1,2):
            for dy in range(-1,2):
                if total>0: return total
                sx,sy = x,y
                k = 0
                while True:
                    sx,sy = dx+sx,dy+sy
                    if sx>7 or sx<0 or sy>7 or sy<0 or self.board[sy][sx]==EMPTY: break
                    if self.board[sy][sx]==-self.turn: k+=1
                    if self.board[sy][sx]==self.turn:
                        total+=k
                        break
        return total
    
    def put_stone(self, x, y):
        self.board[y][x] = self.turn
        for dx in range(-1,2):
            for dy in range(-1,2):
                sx,sy = x,y
                k = 0
                while True:
                    sx,sy = dx+sx,dy+sy
                    if sx>7 or sx<0 or sy>7 or sy<0 or self.board[sy][sx]==EMPTY: break
                    if self.board[sy][sx]==-self.turn: k+=1
                    if self.board[sy][sx]==self.turn:
                        for i in range(k):
                            sx,sy = sx-dx,sy-dy
                            self.board[sy][sx] = self.turn
                        break
    
    def push(self, move):
        if isinstance(move, str): move = move_from_pos(move)
        if not(move_to_pos(move[0], move[1]) in self.legal_moves): return -1
        x, y = move[0], move[1]
        self.put_stone(x, y)
        self.turn = -self.turn
        self.legal_moves = self.get_legal_moves()
        if(len(self.legal_moves)==0):
            self.turn = -self.turn
            self.legal_moves = self.get_legal_moves()
            if(len(self.legal_moves)==0): self.end = True

    def result(self):
        if self.end==False: return 0
        sum_board = np.sum(self.board)
        if sum_board>0: return BLACK
        elif sum_board<0: return WHITE
        else: return 0

    def remember(self, address):
        if len(self.cash)<address+1:
            self.cash.append([np.zeros((8, 8), dtype=np.int8), self.turn, self.legal_moves.copy()])
        self.cash[address][0] = self.board.copy()
        self.cash[address][1] = self.turn
        self.cash[address][2] = self.legal_moves.copy()

    def pop(self, address):
        self.board = self.cash[address][0].copy()
        self.turn = self.cash[address][1]
        self.legal_moves = self.cash[address][2].copy()
        self.end = False

    def cash_clear(self):
        self.cash = [[np.zeros((8, 8), dtype=np.int8), self.turn, self.legal_moves]]

    def legal_mask(self):
        mask = np.zeros((8, 8), dtype=np.int8)
        for move in self.legal_moves:
            x, y = move_from_pos(move)
            mask[y][x] = 1
        return mask

    def get_state(self):
        state = np.zeros((3, 8, 8), dtype=np.float32)
        state[0] = (self.board==self.turn).astype(np.float32)
        state[1] = (self.board==-self.turn).astype(np.float32)
        state[2] = self.legal_mask().astype(np.float32)
        return state
    
    def is_end(self):
        if len(self.legal_moves)==0:
            self.turn = -self.turn
            if len(self.get_legal_moves())==0:
                self.end = True
                return True
        return False
    
    def from_json(self, json_data):
        self.board, self.turn = deserialize(json_data)
        self.legal_moves = self.get_legal_moves()
        self.end = self.is_end()