import numpy as np
import string

BLACK = 1
WHITE = -1
EMPTY = 0
DRAW = 0

def move_from_pos(pos):
    col = string.ascii_uppercase.index(pos[0].upper())
    row = int(pos[1]) - 1
    return (col, row)

def move_to_pos(x, y):
    col = string.ascii_uppercase[x]
    row = y + 1
    return f"{col}{row}"

def converse_prob(element_list):
    element_sum = sum(element_list)
    prob = [element/element_sum for element in element_list]
    return prob