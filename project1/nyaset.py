import numpy as np
import othello_board
import itertools

boards = othello_board.Board()

# 文字から座標への変換
def move_to_coords(move):
    letters = 'abcdefgh'
    if move[0] not in letters or not move[1].isdigit() or not (1 <= int(move[1]) <= 8):
        raise ValueError(f"Invalid move format: {move}")
    x = letters.index(move[0])
    y = int(move[1]) - 1
    return x, y

def board_into_two_types(board):
    black_board = np.zeros((8, 8), dtype=int)
    white_board = np.zeros((8, 8), dtype=int)
    black_board[board==othello_board.BLACK] = 1
    white_board[board==othello_board.WHITE] = 1
    return black_board, white_board

def isPass():
    for y in range(8):
        for x in range(8):
            if boards.canReturn(x,y,boards.turn):
                return False
    return True

# 全ての棋譜を解析しNumpy配列に変換
def kifu_to_numpy(kifu):
    moves = [kifu[i:i+2] for i in range(0, len(kifu), 2)]
    board_list = []
    next_moves = []
    boards.boardInit()

    for move in moves:
        next_move = np.zeros((8, 8), dtype=int)

        x, y = move_to_coords(move)
        next_move[y][x] = 1
        next_moves.append(next_move)
        if boards.turn==othello_board.BLACK:
            black_board,white_board = board_into_two_types(boards.board)
        else:
            white_board,black_board = board_into_two_types(boards.board)
        board_list.append([black_board,white_board])

        boards.putStone(x, y, boards.turn)
        boards.changeTurn()
        if isPass():
            boards.changeTurn()
            if isPass():
                boards.boardInit()

    return np.array(board_list), np.array(next_moves)

def load(num=20):
    boards_list = np.array([])
    next_moves_list = []
    # ファイルの読み込み
    for i in range(num):
        with open((f'NyasetData/000000{i}.txt' if i<10 else f'NyasetData/00000{i}.txt'), 'r') as file:
            kifu_data = file.read().strip().replace('\n','')

        print(f'succesfully loaded NyasetData/000000{i}.txt' if i<10 else f'succesfully loaded NyasetData/00000{i}.txt')
    
        # 棋譜をNumpy配列に変換
        board_list, next_moves = kifu_to_numpy(kifu_data)
        #boards_list.append(board_list)
        if len(boards_list)==0:
            boards_list = board_list
        else:
            boards_list = np.concatenate([boards_list,board_list])
        next_moves_list.append(next_moves)

    #boards_list = [item for sublist in board_list for item in sublist]
    #list(itertools.chain.from_iterable(boards_list))
    next_moves_list = [item for sublist in next_moves_list for item in sublist]
    return np.array(boards_list),np.array(next_moves_list)

if __name__=='__main__':
    boards,next_moves = load(2)
    # 結果を表示
    print("Boards:")
    print(boards[1])
    print("Next Moves:")
    print(next_moves[1])
    print("boards.shape:",boards.shape)
    print("next_moves.shape:",next_moves.shape)
