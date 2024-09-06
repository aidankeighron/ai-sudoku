from generator import generate, create

class Board():

    def __init__(self, difficulty=0.4, seed=-1):
        self.reset(True, difficulty, seed)
    
    def get_board(self):
        return self._board
    
    def set_board(self, row, col, value):
        self._board[row][col] = value

    def is_valid_move(self, row, col, value):
        for i in range(9):
            #  Check if value exists in rows or cols
            if self._board[row][i] == value or self._board[i][col] == value:
                return False
        i, j = row//3, col//3
        for row in range(i*3, i*3+3):
            for col in range (j*3, j*3+3):
                # Check if value exits in subsection
                if self._board[row][col] == value:
                    return False
        return True

    def reset(self, regenerate, difficulty=0.4, seed=-1):
        if regenerate:
            self._sodoku = generate(width=3, height=3, difficulty=difficulty, seed=seed)
            self._board = self._sodoku.board
        else:
            self._clear()

    def validate(self):
        return self._sodoku.validate()
    
    def solve(self):
        return self._sodoku.solve()

    def _clear(self):
        self._board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    