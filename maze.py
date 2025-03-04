from cell import Cell
import time, random

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            seed=None,
            win=None,
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()

    def _create_cells(self):
        for i in range(self._num_cols):
            cols = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                cols.append(cell)
            self._cells.append(cols)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        cell = self._cells[i][j]
        x1 = self._x1 + (i * self._cell_size_x)
        y1 = self._y1 + (j * self._cell_size_y)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        
        cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit_list = []

            if i > 0 and not self._cells[i-1][j].visited:
                to_visit_list.append((i-1, j))
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                to_visit_list.append((i+1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit_list.append((i, j-1))
            if j < self._num_rows-1 and not self._cells[i][j+1].visited:
                to_visit_list.append((i, j+1))
            if len(to_visit_list) == 0:
                self._draw_cell(i, j)
                return
            
            direction_index = random.randrange(len(to_visit_list))
            next_index = to_visit_list[direction_index]
            
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False

            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False

            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False

            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        time.sleep(0.1)
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self._num_cols-1][self._num_rows-1]:
            return True
        directions = []
        if i > 0:
            directions.append((i-1, j))
        if i < self._num_cols - 1:
            directions.append((i+1, j))
        if j > 0:
            directions.append((i, j-1))
        if j < self._num_rows:
            directions.append((i, j+1))
        
        for d0, d1 in directions:
            print(f"{d0}, {d1}")
            can_move = False

            if d0 == i - 1 and d1 == j and not self._cells[i][j].has_left_wall and not self._cells[d0][d1].visited:
                can_move = True
            elif d0 == i + 1 and d1 == j and not self._cells[i][j].has_right_wall and not self._cells[d0][d1].visited:
                can_move = True
            elif d0 == i and d1 == j - 1 and not self._cells[i][j].has_top_wall and not self._cells[d0][d1].visited:
                can_move = True
            elif d0 == i and d1 == j + 1 and not self._cells[i][j].has_bottom_wall and not self._cells[d0][d1].visited:
                can_move = True

            print(can_move)
            if can_move:
                print("moving")
                self._cells[i][j].draw_move(self._cells[d0][d1])
                if self._solve_r(d0, d1):
                    print("found")
                    return True
                print("no move")
                self._cells[i][j].draw_move(self._cells[d0][d1], True)
        return False

