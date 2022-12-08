from pathlib import Path
from sys import argv

from data_reading import data_from_lines


class VisibleCoords:

	def __init__(self):
		self._coords = list()

	def add(self, coords):
		if coords in self._coords:
			return False

		self._coords.append(coords)
		return True

	@property
	def coords(self):
		return self._coords


def _watch_column(tree_grid, col_j, visible_coords):
	grid_size = len(tree_grid)

	# The tree on the edge is visible.
	visible_coords.add((0, col_j))

	def _watch_column_internal(desc):
		if desc:
			prev_height = tree_grid[grid_size - 1][col_j]
			start_i = grid_size - 2
			stop_i = 0
			step_i = -1

		else:
			prev_height = tree_grid[0][col_j]
			start_i = 1
			stop_i = grid_size
			step_i = 1

		for i in range(start_i, stop_i, step_i): # Column index
			height = tree_grid[i][col_j]

			if height >= prev_height:
				visible_coords.add((i, col_j))
				prev_height = height

			else:
				break

	_watch_column_internal(False)
	_watch_column_internal(True)


def _watch_row(tree_grid, row_i, visible_coords):
	tree_row = tree_grid[row_i]
	tree_row_len = len(tree_row)

	# The tree on the edge is visible.
	visible_coords.add((row_i, 0))

	def _watch_row_internal(desc):
		if desc:
			prev_height = tree_row[tree_row_len - 1]
			start_j = tree_row_len - 2
			stop_j = 0
			step_j = -1

		else:
			prev_height = tree_row[0]
			start_j = 1
			stop_j = tree_row_len - 1
			step_j = 1

		for j in range(start_j, stop_j, step_j): # Column index
			height = tree_row[j]

			if height >= prev_height:
				visible_coords.add((row_i, j))
				prev_height = height

			else:
				break

	_watch_row_internal(False)
	_watch_row_internal(True)


data_path = Path(argv[1])

tree_grid = data_from_lines(data_path, lambda line: [int(dgt) for dgt in line])
grid_size = len(tree_grid)

visible_trees = VisibleCoords()
visible_trees.coords.extend(
	[(0, 0), (0, grid_size), (grid_size, 0), (grid_size, grid_size)])

for i in range(1, grid_size-1): # Line index
	_watch_row(tree_grid, i, visible_trees)

for j in range(1, grid_size-1): # Column index
	_watch_column(tree_grid, j, visible_trees)

print(len(visible_trees.coords))
