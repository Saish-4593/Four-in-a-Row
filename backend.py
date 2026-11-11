import numpy as np

ROWS = 6
COLS = 7

EMPTY = 0
HUMAN = 1
AI = 2

SEARCH_DEPTH = 6
COL_ORDER = [3, 2, 4, 1, 5, 0, 6]


class ConnectFourGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.current_turn = HUMAN
        self.game_over = False
        self.winner = None
        self.winning_coords = []
        self.move_history = []
        self.cache = {}

    def is_valid_col(self, board, col):
        return 0 <= col < COLS and board[ROWS - 1][col] == EMPTY

    # Alias for compatibility with earlier versions
    def is_valid_location(self, board, col):
        return self.is_valid_col(board, col)

    def get_valid_cols(self, board):
        return [c for c in COL_ORDER if board[ROWS - 1][c] == EMPTY]

    def get_open_row(self, board, col):
        for r in range(ROWS):
            if board[r][col] == EMPTY:
                return r
        return None

    def check_win(self, board, piece):
        for c in range(COLS - 3):
            for r in range(ROWS):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True, [(r, c + i) for i in range(4)]

        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True, [(r + i, c) for i in range(4)]

        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True, [(r + i, c + i) for i in range(4)]

        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True, [(r - i, c + i) for i in range(4)]

        return False, []

    def eval_window(self, board, window, coords, piece):
        score = 0
        opp = HUMAN if piece == AI else AI

        my_count = window.count(piece)
        opp_count = window.count(opp)
        empty_count = window.count(EMPTY)

        if my_count > 0 and opp_count > 0:
            return 0

        if my_count == 4:
            return 100000

        if my_count == 3 and empty_count == 1:
            idx = window.index(EMPTY)
            r, c = coords[idx]
            supported = (r == 0) or (board[r - 1][c] != EMPTY)
            even_row = (r + 1) % 2 == 0

            if supported:
                score += 120
            else:
                if piece == AI and even_row:
                    score += 75
                elif piece == HUMAN and not even_row:
                    score += 75
                else:
                    score += 40

        elif my_count == 2 and empty_count == 2:
            score += 12

        if opp_count == 3 and empty_count == 1:
            idx = window.index(EMPTY)
            r, c = coords[idx]
            supported = (r == 0) or (board[r - 1][c] != EMPTY)
            odd_row = (r + 1) % 2 == 1

            if supported:
                score -= 140
            else:
                if opp == HUMAN and odd_row:
                    score -= 90
                else:
                    score -= 55

        elif opp_count == 2 and empty_count == 2:
            score -= 10

        return score

    def score_board(self, board, piece):
        score = 0
        opp = HUMAN if piece == AI else AI

        center = list(board[:, COLS // 2])
        score += center.count(piece) * 18
        score -= center.count(opp) * 14

        for c in (2, 4):
            col_vals = list(board[:, c])
            score += col_vals.count(piece) * 6
            score -= col_vals.count(opp) * 5

        for r in range(ROWS):
            for c in range(COLS - 3):
                w = [board[r][c + i] for i in range(4)]
                coords = [(r, c + i) for i in range(4)]
                score += self.eval_window(board, w, coords, piece)

        for c in range(COLS):
            for r in range(ROWS - 3):
                w = [board[r + i][c] for i in range(4)]
                coords = [(r + i, c) for i in range(4)]
                score += self.eval_window(board, w, coords, piece)

        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                w = [board[r + i][c + i] for i in range(4)]
                coords = [(r + i, c + i) for i in range(4)]
                score += self.eval_window(board, w, coords, piece)

        for r in range(3, ROWS):
            for c in range(COLS - 3):
                w = [board[r - i][c + i] for i in range(4)]
                coords = [(r - i, c + i) for i in range(4)]
                score += self.eval_window(board, w, coords, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizing):
        valid_cols = self.get_valid_cols(board)

        ai_won, _ = self.check_win(board, AI)
        if ai_won:
            return None, 1000000 + depth

        human_won, _ = self.check_win(board, HUMAN)
        if human_won:
            return None, -1000000 - depth

        if not valid_cols:
            return None, 0

        if depth == 0:
            return None, self.score_board(board, AI)

        key = (board.tobytes(), depth, maximizing)
        if key in self.cache:
            return self.cache[key]

        if maximizing:
            best_val = -float("inf")
            best_col = valid_cols[0]
            for col in valid_cols:
                row = self.get_open_row(board, col)
                board[row][col] = AI
                _, val = self.minimax(board, depth - 1, alpha, beta, False)
                board[row][col] = EMPTY

                if val > best_val:
                    best_val = val
                    best_col = col
                alpha = max(alpha, best_val)
                if alpha >= beta:
                    break
            res = (best_col, int(best_val))
        else:
            best_val = float("inf")
            best_col = valid_cols[0]
            for col in valid_cols:
                row = self.get_open_row(board, col)
                board[row][col] = HUMAN
                _, val = self.minimax(board, depth - 1, alpha, beta, True)
                board[row][col] = EMPTY

                if val < best_val:
                    best_val = val
                    best_col = col
                beta = min(beta, best_val)
                if alpha >= beta:
                    break
            res = (best_col, int(best_val))

        self.cache[key] = res
        return res

    def get_best_ai_move(self):
        valid_cols = self.get_valid_cols(self.board)
        if not valid_cols:
            return None

        for col in valid_cols:
            row = self.get_open_row(self.board, col)
            self.board[row][col] = AI
            won, _ = self.check_win(self.board, AI)
            self.board[row][col] = EMPTY
            if won:
                return col

        for col in valid_cols:
            row = self.get_open_row(self.board, col)
            self.board[row][col] = HUMAN
            won, _ = self.check_win(self.board, HUMAN)
            self.board[row][col] = EMPTY
            if won:
                return col

        self.cache.clear()
        col, _ = self.minimax(self.board, SEARCH_DEPTH, -float("inf"), float("inf"), True)
        return col if col is not None else valid_cols[0]

    def play_human_move(self, col):
        if self.game_over or self.current_turn != HUMAN:
            return False
        if not self.is_valid_col(self.board, col):
            return False

        row = self.get_open_row(self.board, col)
        self.board[row][col] = HUMAN
        self.move_history.append((HUMAN, row, col))

        won, coords = self.check_win(self.board, HUMAN)
        if won:
            self.game_over = True
            self.winner = HUMAN
            self.winning_coords = coords
        elif not self.get_valid_cols(self.board):
            self.game_over = True
            self.winner = 0
        else:
            self.current_turn = AI

        return True

    def play_ai_move(self):
        if self.game_over or self.current_turn != AI:
            return None

        col = self.get_best_ai_move()
        if col is None:
            return None

        row = self.get_open_row(self.board, col)
        self.board[row][col] = AI
        self.move_history.append((AI, row, col))

        won, coords = self.check_win(self.board, AI)
        if won:
            self.game_over = True
            self.winner = AI
            self.winning_coords = coords
        elif not self.get_valid_cols(self.board):
            self.game_over = True
            self.winner = 0
        else:
            self.current_turn = HUMAN

        return col


# Alias so old or new imports both work
ConnectFourBackend = ConnectFourGame