import cython
import numpy as np
cimport numpy as cnp
from common import *

cdef class Board:
    def __init__(self):
        cdef cnp.ndarray board = np.zeros((8, 8), dtype=np.int8)
        cdef:
            int turn, end
            list legal_moves
        self.reset()

    def __str__(self):
        return str(self.board)

    cpdef reset(self):
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.board[4, 3] = self.board[3, 4] = BLACK
        self.board[3, 3] = self.board[4, 4] = WHITE
        self.turn = BLACK
        self.legal_moves = self.get_legal_moves()
        self.end = False
    
    cdef get_legal_moves(self):
        cdef list moves = []
        for y in range(8):
            for x in range(8):
                if self.is_legal((x, y)):
                    moves.append(move_to_pos(x, y))
        return moves
    
    cdef is_legal(self, list move):
        cdef int x, y,total
        cdef int dx, dy, sx, sy, k
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
    
    cdef put_stone(self, x, y):
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
    
    cpdef push(self, move):
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