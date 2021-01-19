from math import exp
import numpy as np
import random
import time


class AnnealingSolver:

    # 3*81: rows, cols, 3x3
    optimal_energy = -243

    # marks original values
    def get_fixed_positions(self, sudoku):
        original = []
        for row in sudoku:
            original.append([-1 if x > 0 else 0 for x in row])
        return np.array(original)


    # initial step to fill empty slots with random nr
    def fill_empty_with_random(self, sudoku, fixed_positions):
        # get count of missing values
        vals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i, row in enumerate(sudoku):
            for j, col in enumerate(row):
                if sudoku[i][j] != 0:
                    vals[sudoku[i][j] - 1] += 1
        
        missing_vals = [9-x for x in vals]
        
        # fill missing values with missing_vals randomly
        for i, row in enumerate(sudoku):
            for j, col in enumerate(row):
                if fixed_positions[i][j] != -1:
                    while True:
                        rand = random.randint(0, 8)
                        if missing_vals[rand] != 0:
                            sudoku[i][j] = rand + 1
                            missing_vals[rand] += -1
                            break


    # calculate fitness
    def calc_energy(self, sudoku):
        energy = 0
        for i, row in enumerate(sudoku):
            energy += len(np.unique(sudoku[i]))
        
        # columns
        transposed = sudoku.transpose()
        for i, col in enumerate(transposed):
            energy += len(np.unique(transposed[i]))
        
        # every 3x3 TODO ugly
        from_row, to_row = 0, 3
        from_col, to_col = 0, 3
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 0, 3
        from_col, to_col = 3, 6
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 0, 3
        from_col, to_col = 6, 9
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 3, 6
        from_col, to_col = 0, 3
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 3, 6
        from_col, to_col = 3, 6
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 3, 6
        from_col, to_col = 6, 9
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 6, 9
        from_col, to_col = 0, 3
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 6, 9
        from_col, to_col = 3, 6
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        from_row, to_row = 6, 9
        from_col, to_col = 6, 9
        values = []
        sub_arr = sudoku[from_row:to_row, from_col:to_col]
        for sub_row in sub_arr:
            for val in sub_row:
                values.append(val)
        energy += len(np.unique(values))

        return -energy


    # switch places of 2 random numbers
    def create_random_neighbor(self, sudoku, fixed_positions):
        while True:
            i1 = random.randint(0, 8)
            j1 = random.randint(0, 8)
            i2 = random.randint(0, 8)
            j2 = random.randint(0, 8)
            
            if fixed_positions[i1][j1] == -1 or fixed_positions[i2][j2] == -1:
                continue
            
            v1 = sudoku[i1][j1]
            v2 = sudoku[i2][j2]

            if v1 == v2:
                continue

            sudoku[i1][j1] = v2
            sudoku[i2][j2] = v1
            break
        
        return sudoku


    def solve(self, sudoku):
        original_sudoku = sudoku.copy()
        fixed_positions = self.get_fixed_positions(original_sudoku)
        
        current_best = sudoku.copy()
        self.fill_empty_with_random(current_best, fixed_positions)

        max_temp = 20
        for temp in range(max_temp, 0, -1):
            for epoch in range(10000):
                energy_current = self.calc_energy(current_best)
                next_neigbhour = self.create_random_neighbor(current_best.copy(), fixed_positions)
                energy_new = self.calc_energy(next_neigbhour)
                
                # found the solution
                if energy_new == self.optimal_energy:
                    # print('solution with temp', temp)
                    # print('remaining epochs', epoch)
                    return next_neigbhour.flatten()
                
                delta_energy = energy_current - energy_new
                r = random.random()
                if delta_energy > 0:
                    current_best = next_neigbhour.copy()
                elif delta_energy != 0 and exp((delta_energy*max_temp)/(temp)) > r:
                    current_best = next_neigbhour.copy()
