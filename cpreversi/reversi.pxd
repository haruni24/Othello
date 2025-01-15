cdef extern from "reversi.h":
    void is_legal(int *board, int x, int y, int turn)