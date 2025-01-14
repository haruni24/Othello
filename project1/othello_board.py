import numpy as np
from copy import deepcopy

BLACK = 1
WHITE = -1
EMPTY = 0

class Board:
    def __init__(self):
        self.turn = BLACK
        self.board = np.zeros((8,8))

    def boardInit(self):
        self.board = np.zeros((8,8))
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[3][3] = WHITE
        self.board[4][4] = WHITE

    def canReturn(self,x,y,color):
        total = 0
        if self.board[y][x]!=EMPTY : return False
        for dx in range(-1,2):
            for dy in range(-1,2):
                if total>0:
                    return total>0
                sx,sy = x,y
                k = 0
                while True:
                    sx,sy = dx+sx,dy+sy
                    if sx>7 or sx<0 or sy>7 or sy<0 or self.board[sy][sx]==EMPTY:
                        break
                    if self.board[sy][sx]==-color:
                        k+=1
                    if self.board[sy][sx]==color:
                        total+=k
                        break
        return total>0
    
    def putStone(self,x,y,color):
        self.board[y][x] = color
        for dx in range(-1,2):
            for dy in range(-1,2):
                sx,sy = x,y
                k = 0
                while True:
                    sx,sy = dx+sx,dy+sy
                    if sx>7 or sx<0 or sy>7 or sy<0 or self.board[sy][sx]==EMPTY:
                        break
                    if self.board[sy][sx]==-color:
                        k+=1
                    if self.board[sy][sx]==color:
                        for i in range(k):
                            sx,sy = sx-dx,sy-dy
                            self.board[sy][sx] = color
                        break

    def countStone(self):
        b = list(self.board.count(BLACK))
        w = list(self.board.count(WHITE))
        return b,w

    def changeTurn(self):
        self.turn *= -1