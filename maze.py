from graphics import Line, Point
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

        if seed is not None:
            self._seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

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
        self._cells[i][j]._visited = True
        while True:
            to_visit = []
            if self._cells[i][j].has_left_wall == True:
                if i > 0:
                    to_visit.append(self._cells[i-1][j])
            if self._cells[i][j].has_right_wall == True:
                if i < self._num_cols-1:
                    to_visit.append(self._cells[i+1][j])
            if self._cells[i][j].has_top_wall == True:
                if j > 0:
                    to_visit.append(self._cells[i][j-1])
            if self._cells[i][j].has_bottom_wall == True:
                if j < self._num_rows-1:
                    to_visit.append(self._cells[i][j+1])
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            directions = {
                "right": (1, 0, "right", "left"),
                "left": (-1, 0, "left", "right"),
                "down": (0, 1, "bottom", "top"),
                "up": (0, -1, "top", "bottom"),
            }
            direction = random.choice(list(directions.keys()))
            di, dj, current_wall, neighbor_wall = directions[direction]
            neighbor_i, neighbor_j = i + di, j + dj
            if 0 <= neighbor_i < self._num_cols and 0 <= neighbor_j < self._num_rows:
                self._cells[i][j].break_walls(current_wall)
                self._cells[neighbor_i][neighbor_j].break_walls(neighbor_wall)
                self._break_walls_r(neighbor_i, neighbor_j)
