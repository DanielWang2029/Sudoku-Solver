

# this is the foundation of the solver visualization in GUI
from typing import List


# determine whether the arr could be solved and return the changed board
def solve(arr: List[List[int]]):
    s = RecursionSolver(arr)
    s.solve()
    s.print_board()
    return s.get_board()


class RecursionSolver:
    def __init__(self, arr: List[List[int]]):
        assert arr, 'Input board size err, require 9 * 9, found None or empty'
        assert len(arr) == 9, f'Input board size err, require 9 * 9, found {len(arr)} * n'
        assert len(arr[0]) == 9, f'Input board size err, require 9 * 9, found {len(arr)} * {len(arr[0])}'
        self.board = arr

    def get_board(self) -> List[List[int]]:
        return self.board

    def solve(self) -> bool:
        i, j = self.find_next()

        if i == -1 or j == -1:
            return True

        for val in range(1, 10):
            if self.check_if_valid((i, j, val)):
                self.board[i][j] = val

                if self.solve():
                    return True

                self.board[i][j] = 0

        return False

    # find the next empty spot
    def find_next(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    return i, j
        return -1, -1

    def check_if_valid(self, tpl) -> bool:

        assert len(tpl) == 3, f'Invalid input, length of input should be 3, got {len(tpl)}'

        i, j, value = tpl

        if value not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False

        # check for row and column
        for ind in range(9):
            if self.board[i][ind] == value or self.board[ind][j] == value:
                return False

        # check for box
        for p in range(i // 3 * 3, i // 3 * 3 + 3):
            for q in range(j // 3 * 3, j // 3 * 3 + 3):
                if self.board[p][q] == value:
                    return False

        return True

    # print a sudoku board
    def print_board(self):
        print()

        print(f'  {self.board[0][0]}  {self.board[0][1]}  {self.board[0][2]}  '
              f'|  {self.board[0][3]}  {self.board[0][4]}  {self.board[0][5]}  '
              f'|  {self.board[0][6]}  {self.board[0][7]}  {self.board[0][8]}  ')

        print(f'  {self.board[1][0]}  {self.board[1][1]}  {self.board[1][2]}  '
              f'|  {self.board[1][3]}  {self.board[1][4]}  {self.board[1][5]}  '
              f'|  {self.board[1][6]}  {self.board[1][7]}  {self.board[1][8]}  ')

        print(f'  {self.board[2][0]}  {self.board[2][1]}  {self.board[2][2]}  '
              f'|  {self.board[2][3]}  {self.board[2][4]}  {self.board[2][5]}  '
              f'|  {self.board[2][6]}  {self.board[2][7]}  {self.board[2][8]}  ')

        print('— — — — — — — — — — — — — — — — — —')

        print(f'  {self.board[3][0]}  {self.board[3][1]}  {self.board[3][2]}  '
              f'|  {self.board[3][3]}  {self.board[3][4]}  {self.board[3][5]}  '
              f'|  {self.board[3][6]}  {self.board[3][7]}  {self.board[3][8]}  ')

        print(f'  {self.board[4][0]}  {self.board[4][1]}  {self.board[4][2]}  '
              f'|  {self.board[4][3]}  {self.board[4][4]}  {self.board[4][5]}  '
              f'|  {self.board[4][6]}  {self.board[4][7]}  {self.board[4][8]}  ')

        print(f'  {self.board[5][0]}  {self.board[5][1]}  {self.board[5][2]}  '
              f'|  {self.board[5][3]}  {self.board[5][4]}  {self.board[5][5]}  '
              f'|  {self.board[5][6]}  {self.board[5][7]}  {self.board[5][8]}  ')

        print('— — — — — — — — — — — — — — — — — —')

        print(f'  {self.board[6][0]}  {self.board[6][1]}  {self.board[6][2]}  '
              f'|  {self.board[6][3]}  {self.board[6][4]}  {self.board[6][5]}  '
              f'|  {self.board[6][6]}  {self.board[6][7]}  {self.board[6][8]}  ')

        print(f'  {self.board[7][0]}  {self.board[7][1]}  {self.board[7][2]}  '
              f'|  {self.board[7][3]}  {self.board[7][4]}  {self.board[7][5]}  '
              f'|  {self.board[7][6]}  {self.board[7][7]}  {self.board[7][8]}  ')

        print(f'  {self.board[8][0]}  {self.board[8][1]}  {self.board[8][2]}  '
              f'|  {self.board[8][3]}  {self.board[8][4]}  {self.board[8][5]}  '
              f'|  {self.board[8][6]}  {self.board[8][7]}  {self.board[8][8]}  ')

        print()


# test case

# solve([[7, 8, 0, 4, 0, 0, 1, 2, 0],
#        [6, 0, 0, 0, 7, 5, 0, 0, 9],
#        [0, 0, 0, 6, 0, 1, 0, 7, 8],
#        [0, 0, 7, 0, 4, 0, 2, 6, 0],
#        [0, 0, 1, 0, 5, 0, 9, 3, 0],
#        [9, 0, 4, 0, 6, 0, 0, 0, 5],
#        [0, 7, 0, 3, 0, 0, 0, 1, 2],
#        [1, 2, 0, 0, 0, 7, 4, 0, 0],
#        [0, 4, 9, 2, 0, 6, 0, 0, 7]])
