#include <iostream>
#include <vector>
#include <string>
#include <cctype>
#include <random>
#include <utility>

using namespace std;

// 定数の定義
const int BLACK = 1;
const int WHITE = -1;
const int EMPTY = 0;

// ユーティリティ関数
pair<int, int> move_from_pos(const string& pos) {
    if (pos.length() < 2) {
        throw invalid_argument("Invalid position format.");
    }
    char col_char = toupper(pos[0]);
    int col = col_char - 'A';
    int row = stoi(pos.substr(1)) - 1;
    return make_pair(col, row);
}

string move_to_pos(int x, int y) {
    if (x < 0 || x > 7 || y < 0 || y > 7) {
        throw out_of_range("Coordinates out of range.");
    }
    char col_char = 'A' + x;
    int row = y + 1;
    return string(1, col_char) + to_string(row);
}

class Board {
public:
    Board() {
        reset();
    }

    void reset() {
        board = vector<vector<int>>(8, vector<int>(8, EMPTY));
        board[4][3] = board[3][4] = BLACK;
        board[3][3] = board[4][4] = WHITE;
        turn = BLACK;
        legal_moves = get_legal_moves();
        end = false;
    }

    void put_stone(int x, int y) {
        board[y][x] = turn;
        // 反転処理
        for (int dx = -1; dx <= 1; ++dx) {
            for (int dy = -1; dy <= 1; ++dy) {
                if (dx == 0 && dy == 0) continue;
                int sx = x + dx;
                int sy = y + dy;
                int k = 0;
                // 方向に向かって探索
                while (sx >= 0 && sx < 8 && sy >= 0 && sy < 8 && board[sy][sx] == -turn) {
                    k++;
                    sx += dx;
                    sy += dy;
                }
                if (k > 0 && sx >= 0 && sx < 8 && sy >= 0 && sy < 8 && board[sy][sx] == turn) {
                    // 反転
                    int flip_x = x + dx;
                    int flip_y = y + dy;
                    for (int i = 0; i < k; ++i) {
                        board[flip_y][flip_x] = turn;
                        flip_x += dx;
                        flip_y += dy;
                    }
                }
            }
        }
    }

    int push(const string& move_str) {
        pair<int, int> move = move_from_pos(move_str);
        if (!is_legal(move)) {
            return -1;
        }
        put_stone(move.first, move.second);
        turn = -turn;
        legal_moves = get_legal_moves();
        if (legal_moves.empty()) {
            turn = -turn;
            legal_moves = get_legal_moves();
            if (legal_moves.empty()) {
                end = true;
            }
        }
        return 0;
    }

    string to_string_board() const {
        string board_str;
        for (const auto& row : board) {
            for (const auto& cell : row) {
                char c;
                if (cell == BLACK) c = 'B';
                else if (cell == WHITE) c = 'W';
                else c = '.';
                board_str += c;
                board_str += ' ';
            }
            board_str += '\n';
        }
        return board_str;
    }

    // ゲッター
    bool is_end() const {
        return end;
    }

    const vector<string>& get_legal_moves_ref() const {
        return legal_moves;
    }

private:
    vector<vector<int>> board;
    int turn;
    bool end;
    vector<string> legal_moves;

    vector<string> get_legal_moves() const {
        vector<string> moves;
        for (int y = 0; y < 8; ++y) {
            for (int x = 0; x < 8; ++x) {
                if (is_legal(make_pair(x, y))) {
                    moves.push_back(move_to_pos(x, y));
                }
            }
        }
        return moves;
    }

    bool is_legal(const pair<int, int>& move) const {
        int x = move.first;
        int y = move.second;
        if (board[y][x] != EMPTY) return false;

        int opponent = -turn;
        bool legal = false;

        for (int dx = -1; dx <=1; ++dx) {
            for (int dy = -1; dy <=1; ++dy) {
                if (dx == 0 && dy == 0) continue;
                int sx = x + dx;
                int sy = y + dy;
                int count = 0;
                while (sx >=0 && sx <8 && sy >=0 && sy <8 && board[sy][sx] == opponent) {
                    count++;
                    sx += dx;
                    sy += dy;
                }
                if (count >0 && sx >=0 && sx <8 && sy >=0 && sy <8 && board[sy][sx] == turn) {
                    legal = true;
                    break;
                }
            }
            if (legal) break;
        }
        return legal;
    }
};

// テスト用メイン関数
int main() {
    Board board;

    // ランダム数生成器の初期化
    random_device rd;  // 非決定的な乱数生成器
    mt19937 gen(rd()); // メルセンヌ・ツイスタエンジン

    for (int i = 1; i <= 1000; ++i) {
        board.reset();

        // ゲームプレイ
        while (!board.is_end()) {
            const vector<string>& moves = board.get_legal_moves_ref();
            if (moves.empty()) {
                break; // 合法手がない場合、ターンをスキップ
            }

            // 合法手からランダムに選択
            uniform_int_distribution<> dis(0, moves.size() - 1);
            string selected_move = moves[dis(gen)];

            // 石を置く
            board.push(selected_move);
        }

        // ゲーム終了後にボードを出力
        cout << "Game " << i << " End:\n" << board.to_string_board() << endl;
    }

    return 0;
}