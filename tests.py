import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_small_cells(self):
        num_cols = 3
        num_rows = 3
        m2 = Maze(2, 1, num_rows, num_cols, 8, 8)
        self.assertEqual(
            len(m2._cells[1]),
            num_cols,
        )
        self.assertEqual(
            len(m2._cells),
            num_rows,
        )
    
    def test_maze_entrance(self):
        num_cols = 12
        num_rows = 10
        m3 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m3._cells[0][0].has_top_wall,
            False,
        )
        
    def test_maze_exit(self):
        num_cols = 12
        num_rows = 10
        m4 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m4._cells[num_cols-1][num_rows-1].has_bottom_wall,
            False,
        )

    def test_maze_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        for col in m1._cells:
            for cell in col:
                self.assertEqual(cell.visited, False)

if __name__ == "__main__":
    unittest.main()