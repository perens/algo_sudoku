import sys
from Sudoku.Generator import *

class Solver:

    def __init__(self, board):
        self.board = board.copy()

    def solve(self):
        print(self.board)


difficulties = {
    'easy': (35, 0), 
    'medium': (81, 5), 
    'hard': (81, 10), 
    'extreme': (81, 15)
}

difficulty = difficulties[sys.argv[1]]
gen = Generator('base.txt')
gen.randomize(100)
initial = gen.board.copy()
gen.reduce_via_logical(difficulty[0])

if difficulty[1] != 0:
    gen.reduce_via_random(difficulty[1])
final = gen.board.copy()

Solver(gen.board.get_board_array()).solve()
