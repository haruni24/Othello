#include <stdio.h>

int to_index(int x, int y){
    return y*8+x;
}

int is_legal(int *board, int x, int y, int turn){
    if(board[to_index(x, y)] != 0) return 0;
    int dx, dy;
    for(dx=-1; dx<=1; dx++){
        for(dy=-1; dy<=1; dy++){
            if(dx==0 && dy==0) continue;
            int nx=x+dx, ny=y+dy;
            while(0<=nx && nx<8 && 0<=ny && ny<8){
                if(board[to_index(nx, ny)] == 0) break;
                if(board[to_index(nx, ny)] == turn){
                    if(nx-x==dx && ny-y==dy) break;
                    return 1;
                }
                nx += dx;
                ny += dy;
            }
        }
    }
    return 0;
}