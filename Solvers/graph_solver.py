import numpy as np


class GraphSolver:

    dimension = 9
    possible_colors = [x for x in range(1, 10)]

    # def order_vertices_by_uncolored_neigbhors(vertices):
    #   # add uncolored count
    #   for v in vertices:
    #     cnt = 0
    #     for av in v.adjacent_vertices:
    #       if av.color == 0:
    #         cnt += 1
    #     v.initial_uncolored_neigbors = cnt

    #   l = vertices.tolist()
    #   l.sort(key=lambda x: x.initial_uncolored_neigbors, reverse=True)
    #   return np.array(l)


    def is_complete(self, vertices):
        if not self.is_valid(vertices):
            return False
    
        for v in vertices:
            if v.color == 0:
                return False
    
        return True


    def is_valid(self, vertices):
        for v in vertices:
            tmp_colors = [0 for x in range(9)]
            for av in v.adjacent_vertices:
                if av.color != 0 and v.color == av.color:
                    return False
      
                if av.color != 0:
                    tmp_colors[av.color - 1] += 1
            for c in tmp_colors:
                if c > 3:
                    return False
        return True


    def get_graph_array(self, sudoku):
        a = []
        for row in sudoku:
            for col in row:
                a.append(col.color)
        return a


    def color_vertices(self, sudoku, vertices, c, ii):
        for i in range(ii, len(vertices)):
            while True:
                if c > len(self.possible_colors):
                    v.color = 0
                    return False
      
                v = vertices[i]
      
                if v.color != 0:
                    break

                # try new value
                v.color = c
                if self.is_valid(vertices) == False:
                    v.color = 0
                    c += 1
                else:
                    if self.is_complete(vertices):
                        return True
                    
                    if self.color_vertices(sudoku, vertices, 1, i+1):
                        return True
                    else:
                        # try next color
                        v.color = 0
                        c += 1
                        if c > len(self.possible_colors):
                            return False


    def create_sudoku_vertices(self, sudoku):
        vertices_sudoku = []
        for row in sudoku:
            for color_value in row:
                vertices_sudoku.append(Vertex(color_value))

        return np.array(vertices_sudoku).reshape(dimension, dimension)


    def create_adjacency_links(self, sudoku):
        cols = [x for x in range(self.dimension)]
        for i, row in enumerate(sudoku):
            for j, col in enumerate(row):
                current_vertix = sudoku[i][j]

                # column adjacencies
                for k, col in enumerate(row):
                    if j != k:
                        current_vertix.add_adjacent_vertex(sudoku[i][k])
      
                # row adjacencies
                for k, row in enumerate(sudoku):
                    for c in cols:
                        if j == c and k != i:
                            current_vertix.add_adjacent_vertex(sudoku[k][j])

                # 3x3 adjacencies
                # actually takes 2x2 that isn't covered by rows and columns
                from_row, to_row, from_col, to_col = 0,0,0,0
                if i <= 2:
                    from_row = 0
                    to_row = 3
                elif 3 <= i <= 5:
                    from_row = 3
                    to_row = 6
                elif i >= 6:
                    from_row = 6
                    to_row = 9
                
                if j <= 2:
                    from_col = 0
                    to_col = 3
                elif 3 <= j <= 5:
                    from_col = 3
                    to_col = 6
                elif j >= 6:
                    from_col = 6
                    to_col = 9
                
                # todo this gave the biggest boost
                for sub_i, sub_row in enumerate(sudoku[from_row:to_row]):
                    for sub_j, val in enumerate(sub_row[from_col:to_col]):
                        if i != sub_i+from_row and j != sub_j+from_col:
                            current_vertix.add_adjacent_vertex(sudoku[sub_i+from_row][sub_j+from_col])


    def solve(self, sudoku):
        sudoku = self.create_sudoku_vertices(sudoku)
        self.create_adjacency_links(sudoku)
        vertices = sudoku.flatten()
        self.color_vertices(sudoku, vertices, 1, 0)
        return self.get_graph_array(sudoku)


class Vertex():
    def __init__(self, color = 0):
        self.color = color
        self.adjacent_vertices = []
    
    def add_adjacent_vertex(self, vertex):
        self.adjacent_vertices.append(vertex)
