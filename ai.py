from __future__ import annotations
from sudoku import Sudoku
from numpy import ndarray
from board import create
from board import Board

def solve_ai(board: Board):
    ...


def possible_answers(board: Board):
    answers = []
    current_board = Sudoku._copy_board(board.get_sodoku().board)
    solved_sudoku = create(current_board).solve()

    for i in range(len(current_board)):
        for j in range(len(current_board[i])):
            if current_board[i][j] != solved_sudoku.board[i][j]:
                answers.append([i,j, solved_sudoku.board[i][j]])

    return answers