import numpy as np
import string

BLACK = 1
WHITE = -1
EMPTY = 0

def move_from_pos(pos):
    col = string.ascii_uppercase.index(pos[0].upper())
    row = int(pos[1]) - 1
    return (col, row)

def move_to_pos(x, y):
    col = string.ascii_uppercase[x]
    row = y + 1
    return f"{col}{row}"