import numpy as np
import string
import json

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

def extra_value(input_list):
    return [element[0] for element in input_list]

def deserialize(serialized_str):
    # JSON配列の最後の閉じ括弧の位置を見つける
    last_bracket = serialized_str.rfind(']')
    if last_bracket == -1:
        raise ValueError("Invalid serialized string format.")
    
    # ボードのJSON部分とturn部分に分割
    board_json = serialized_str[:last_bracket + 1]
    turn_str = serialized_str[last_bracket + 1:]
    
    # JSONをデコードしてNumPy配列に変換
    board_list = json.loads(board_json)
    board = np.array(board_list)
    
    # turnを整数に変換
    try:
        turn = int(turn_str)
    except ValueError:
        raise ValueError("Invalid turn value.")
    
    return board, turn