import numpy as np
import sys
import time
from Sudoku.Generator import *
from Solvers.AnnealingSolver import AnnealingSolver
from Solvers.BacktrackingSolver import BacktrackingSolver
from Solvers.GraphSolver import GraphSolver


class Solver:

    def __init__(self, difficulty):
        self.difficulty = difficulty

    # solve with every solver, report result, report time
    def solve(self):
        self.print_sudoku(sudoku)
        self.solve_and_report(AnnealingSolver(), sudoku, 'Simulated Annealing')
        self.solve_and_report(BacktrackingSolver(), sudoku, 'Backtracking')
        self.solve_and_report(GraphSolver(), sudoku, 'Graph coloring with backtracking')


    def solve_and_report(self, solver, sudoku, method):
        start = time.time()
        result = solver.solve(sudoku.copy())
        end = time.time()
        print('\n', method, 'took', (end-start), 'seconds')
        self.print_sudoku(result)


    def generate_sudoku(self, difficulty):
        gen = Generator('base.txt')
        gen.randomize(100)
        initial = gen.board.copy()
        gen.reduce_via_logical(difficulty[0])

        if difficulty[1] != 0:
            gen.reduce_via_random(difficulty[1])
        
        sudoku = gen.board.get_board_array()
        return np.array(sudoku).reshape(9, 9)


    def print_sudoku(self, sudoku):
        output = []
        for row in sudoku:
            my_set = map(str, [x for x in row])
            new_set = []
            for x in my_set:
                if x == '0':
                    new_set.append("_")
                else:
                    new_set.append(x)
            output.append('|'.join(new_set))
        print('\r\n'.join(output))
        print()


difficulties = {
    'easy': (35, 0), 
    'medium': (81, 5), 
    'hard': (81, 10), 
    'extreme': (81, 15)
}

difficulty = difficulties[sys.argv[1]]
Solver(difficulty).solve()
