import numpy as np
import random
import time

class TabuSolver:

    possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self):
        self.tabu_sudokus = []

    def create_tabu_list(self, sudoku):
        tabu_list = []
        for row in sudoku:
            tabu_list.append([-1 if x > 0 else 0 for x in row])
        return np.array(tabu_list)


    # Returns all possible values for the position or None
    def get_possible_value(self, sudoku, row_idx, col_idx):
        values = self.possible_values.copy()
        
        values_in_row = sudoku[row_idx]
        for row_val in values_in_row:
            if row_val in values:
                values.remove(row_val)
        
        values_in_column = sudoku.transpose()[col_idx]
        for col_val in values_in_column:
            if col_val in values:
                values.remove(col_val)
        
        # possible values in the 3x3
        from_row, to_row, from_col, to_col = 0,0,0,0
        if row_idx <= 2:
            from_row = 0
            to_row = 3
        elif 3 <= row_idx <= 5:
            from_row = 3
            to_row = 6
        elif row_idx >= 6:
            from_row = 6
            to_row = 9
        
        if col_idx <= 2:
            from_col = 0
            to_col = 3
        elif 3 <= col_idx <= 5:
            from_col = 3
            to_col = 6
        elif col_idx >= 6:
            from_col = 6
            to_col = 9
        
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                if val in values:
                    values.remove(val)
        
        # shuffle and return
        random.shuffle(values)
        return values


    def is_complete(self, sudoku):
        # if not self.is_valid(sudoku, -1, -1, False):
        #     return False
        
        for row in sudoku:
            for val in row:
                if val == 0:
                    return False
        
        return True


    def is_valid(self, sudoku,  row_idx, col_idx, test_33):
        # rows
        for row in sudoku:
            for possible_value in self.possible_values:
                cnt = (row == possible_value).sum()
                if cnt > 1:
                    return False
        
        # columns
        columns = sudoku.transpose()
        for column in columns:
            for possible_value in self.possible_values:
                cnt = (column == possible_value).sum()
                if cnt > 1:
                    return False
        
        if test_33 == False:
            return True

        # 3x3
        from_row, to_row, from_col, to_col = 0,0,0,0
        if row_idx <= 2:
            from_row = 0
            to_row = 3
        elif 3 <= row_idx <= 5:
            from_row = 3
            to_row = 6
        elif row_idx >= 6:
            from_row = 6
            to_row = 9

        if col_idx <= 2:
            from_col = 0
            to_col = 3
        elif 3 <= col_idx <= 5:
            from_col = 3
            to_col = 6
        elif col_idx >= 6:
            from_col = 6
            to_col = 9

        nrs = []
        for sub_i, sub_row in enumerate(sudoku[from_row:to_row]):
            for sub_j, val in enumerate(sub_row[from_col:to_col]):
                if row_idx != sub_i+from_row and col_idx != sub_j+from_col:
                    nrs.append(sudoku[sub_i+from_row][sub_j+from_col])
        
        for nr in self.possible_values:
            nrs = np.array(nrs)
            cnt = (nrs == nr).sum()
            if cnt > 1:
                return False
        
        return True


    def get_tabu_lock(self, sudoku):
        tmp = sudoku.flatten()
        zeros = (len(tmp) - np.count_nonzero(tmp))
        if zeros < 5:
            return 0
        return (zeros/2)


    def is_new_fitter(self, best_sudoku, sudoku, row_idx, col_idx):
        if self.is_valid(sudoku,  row_idx, col_idx, True):
            best_filled  = np.count_nonzero(best_sudoku)
            sudoku_filled = np.count_nonzero(sudoku)
            
            if sudoku_filled > best_filled:
                return True
        
        return False


    def solve(self, sudoku):
        original = sudoku.copy()
        best_sudoku = sudoku.copy()
        self.tabu_sudokus.append(original.copy())
        
        tabu_list = self.create_tabu_list(sudoku)
        
        step_back = -5
        iterations_with_prev_tabu = 100
        
        while True:
            for row_idx, row in enumerate(sudoku):
                for col_idx, col in enumerate(row):

                    # initial state cell, move on
                    if tabu_list[row_idx][col_idx] == -1:
                        continue

                    # locked, move on
                    if tabu_list[row_idx][col_idx] > 0:
                        continue

                    # new cycle, update tabu values
                    for i, row in enumerate(tabu_list):
                        for j, col in enumerate(row):
                            if tabu_list[i][j] > 0:
                                tabu_list[i][j] = tabu_list[i][j] - 1
                    
                    # find the possible value for position
                    values = self.get_possible_value(sudoku, row_idx, col_idx)

                    # no possible steps, take some steps back
                    if len(values) == 0:
                        
                        if -step_back >= len(self.tabu_sudokus):
                            step_back = -len(self.tabu_sudokus) + 1
                        
                        sudoku = self.tabu_sudokus[-step_back].copy()
                        del self.tabu_sudokus[len(self.tabu_sudokus) + step_back:]
                        iterations_with_prev_tabu -= 1
                        
                        if iterations_with_prev_tabu == 0:
                            step_back -= 5
                            iterations_with_prev_tabu = 100
                        
                        continue
                    
                    # try values
                    for val in values:
                        sudoku[row_idx][col_idx] = val

                        if self.is_complete(sudoku):
                            return sudoku

                        if self.is_new_fitter(best_sudoku, sudoku, row_idx, col_idx):
                            best_sudoku = sudoku.copy()
                            self.tabu_sudokus.append(best_sudoku.copy())
                            
                            # lock the position for some cycles
                            tabu_list[row_idx][col_idx] = self.get_tabu_lock(sudoku)
                        
        return sudoku
