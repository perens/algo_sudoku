import numpy as np
import time


class Backtracking:

  dimension = 9
  possible_nrs = [x for x in range(1, 10)]

  def is_complete(self, sudoku, i, j):
      if not self.is_valid(sudoku, i, j):
        return False
      
      for row in sudoku:
        for val in row:
          if val == 0:
            return False
      
      return True


  def is_valid(self, sudoku, i_inp, j_inp):
    # rows
    for row in sudoku:
      row_nrs = []
      for i, element in enumerate(row):
        row_nrs.append(element)
      
      for nr in self.possible_nrs:
        row_nrs = np.array(row_nrs)
        cnt = (row_nrs == nr).sum()
        if cnt > 1:
          return False
    
    # columns
    columns = sudoku.transpose()
    for row in columns:
      row_nrs = []
      for i, element in enumerate(row):
        row_nrs.append(element)
      
      for nr in self.possible_nrs:
        row_nrs = np.array(row_nrs)
        cnt = (row_nrs == nr).sum()
        if cnt > 1:
          return False
    
    # 3x3 check
    from_row, to_row, from_col, to_col = 0,0,0,0
    if i_inp <= 2:
        from_row = 0
        to_row = 3
    elif 3 <= i_inp <= 5:
        from_row = 3
        to_row = 6
    elif i_inp >= 6:
        from_row = 6
        to_row = 9

    if j_inp <= 2:
        from_col = 0
        to_col = 3
    elif 3 <= j_inp <= 5:
        from_col = 3
        to_col = 6
    elif j_inp >= 6:
        from_col = 6
        to_col = 9

    nrs = []
    for sub_i, sub_row in enumerate(sudoku[from_row:to_row]):
      for sub_j, val in enumerate(sub_row[from_col:to_col]):
        if i_inp != sub_i+from_row and j_inp != sub_j+from_col:
          nrs.append(sudoku[sub_i+from_row][sub_j+from_col])
    
    for nr in self.possible_nrs:
      nrs = np.array(nrs)
      cnt = (nrs == nr).sum()
      if cnt > 1:
        return False
    
    return True


  def solve_sudoku(self, sudoku, c, ii, jj):
    for i in range(ii, self.dimension):
      for j in range(jj, self.dimension):
        
        if sudoku[i][j] != 0:
          continue

        while True:
          if c > len(self.possible_nrs):
            sudoku[i][j] = 0
            return False

          # try new value
          sudoku[i][j] = c
          if self.is_valid(sudoku, i, j) == False:
            sudoku[i][j] = 0
            c += 1
            
          else:
            if self.is_complete(sudoku, i, j):
              return True
            
            # new indexes for backtracking
            k,l = 0,0
            if (j+1) < self.dimension and (i+1) < self.dimension:
              k += 1
            elif (j+1) > self.dimension and (i+1) < self.dimension:
              k += 1
              l = 0
            else:
              k = 0
              l = 0
            
            if self.solve_sudoku(sudoku, 1, k, l):
              return True
            else:
              # try next color
              sudoku[i][j] = 0
              c += 1
              if c > len(self.possible_nrs):
                return False


  def print_sudoku(self, sudoku):
    for row in sudoku:
      r = []
      for col in row:
        r.append(col)
      print(r)
    

  def solve(self, sudoku):
    self.solve_sudoku(sudoku, 1, 0, 0)
    return sudoku.flatten()
