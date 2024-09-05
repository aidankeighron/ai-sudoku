from sudoku import Sudoku

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