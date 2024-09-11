from sudoku import Sudoku
import numpy as np

# Difficulty: % of cells that are empty
def generate(seed=-1, width=3, height=3, difficulty=0.5) -> Sudoku:
    if seed == -1:
        puzzle = Sudoku(width=width, height=height).difficulty(difficulty)
    else:
        puzzle = Sudoku(width=width, height=height, seed=seed).difficulty(difficulty)
    # puzzle.show()
    # puzzle.solve()

    return puzzle
#  Currently assumes 3x3 board
def create(board: list) -> Sudoku:
    puzzle = Sudoku(3, board=board)

    return puzzle
class Board():

    def __init__(self, difficulty=0.4, seed=-1):
        self.reset(True, difficulty, seed)
    
    def get_board(self):
        return self._board
    
    def get_sodoku(self):
        return self._sodoku
    
    def get_board_1d(self):
        return self._board.flatten()
    
    def set_board(self, row, col, value):
        self._board[row, col] = value

    def is_valid_move(self, row, col, value):
        for i in range(9):
            #  Check if value exists in rows or cols
            if self._board[row, i] == value or self._board[i, col] == value:
                return False
        i, j = row//3, col//3
        for row in range(i*3, i*3+3):
            for col in range (j*3, j*3+3):
                # Check if value exits in subsection
                if self._board[row, col] == value:
                    return False
        return True

    def reset(self, regenerate, difficulty=0.4, seed=-1):
        if regenerate:
            self._sodoku = generate(width=3, height=3, difficulty=difficulty, seed=seed)
            self._board = Sudoku._copy_board(self._sodoku.board)
            self._board = np.array(self._board)
            self._board = np.where(self._board == None, 0, self._board)
        else:
            self._clear()

    def validate(self):
        return self._sodoku.validate()
    
    def solve(self):
        return self._sodoku.solve()
    
    def possible_answers(self):
        answers = []
        current_board = Sudoku._copy_board(self._sodoku.board)
        solved_sudoku = create(current_board).solve()

        for i in range(len(current_board)):
            for j in range(len(current_board[i])):
                if current_board[i][j] != solved_sudoku.board[i][j]:
                    answers.append([i,j, solved_sudoku.board[i][j]])

        return answers

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
    