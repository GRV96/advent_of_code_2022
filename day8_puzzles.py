from pathlib import Path
from sys import argv

from data_reading import data_from_lines


class _VisibleCoords:

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

	def _watch_column_internal(desc):
		if desc:
			prev_height = tree_grid[-1][col_j]
			start_i = grid_size - 2
			stop_i = 0
			step_i = -1

		else:
			prev_height = tree_grid[0][col_j]
			start_i = 1
			stop_i = grid_size - 1
			step_i = 1

		# The trees on the edge are visible.
		visible_coords.add((stop_i, col_j))

		for i in range(start_i, stop_i, step_i): # Column index
			height = tree_grid[i][col_j]

			if height > prev_height:
				visible_coords.add((i, col_j))
				prev_height = height

	_watch_column_internal(False)
	_watch_column_internal(True)


def _watch_row(tree_grid, row_i, visible_coords):
	tree_row = tree_grid[row_i]
	tree_row_len = len(tree_row)

	def _watch_row_internal(desc):
		if desc:
			prev_height = tree_row[-1]
			start_j = tree_row_len - 2
			stop_j = 0
			step_j = -1

		else:
			prev_height = tree_row[0]
			start_j = 1
			stop_j = tree_row_len - 1
			step_j = 1

		# The trees on the edges are visible.
		visible_coords.add((row_i, stop_j))

		for j in range(start_j, stop_j, step_j): # Column index
			height = tree_row[j]

			if height > prev_height:
				visible_coords.add((row_i, j))
				prev_height = height

	_watch_row_internal(False)
	_watch_row_internal(True)


def _print_tree_grid(visible_trees):
	for i in range(grid_size):
		row = list()

		for j in range(grid_size):

			if (i, j) in visible_trees.coords:
				row.append("V")

			else:
				row.append("x")

		print(" ".join(row))


def _tree_scenic_score(tree_grid, tree_i, tree_j):
	scenic_score = 1
	tree_height = tree_grid[tree_i][tree_j]

	def _look_at_trees(inc_i, inc_j):
		i = tree_i
		j = tree_j
		sawn_trees = 0

		while True:
			i += inc_i
			j += inc_j

			try:
				height = tree_grid[i][j]
				print(f"({i}, {j}): {height}")
			except IndexError:
				break

			if i >= 0 and j >= 0:
				sawn_trees += 1
				print("V")
			else:
				break

			if height >= tree_height:
				break

		return sawn_trees

	sawn_trees = _look_at_trees(1, 0)
	print(f"Trees: {sawn_trees}")
	if sawn_trees > 0:
		scenic_score *= sawn_trees

	sawn_trees = _look_at_trees(-1, 0)
	print(f"Trees: {sawn_trees}")
	if sawn_trees > 0:
		scenic_score *= sawn_trees

	sawn_trees = _look_at_trees(0, 1)
	print(f"Trees: {sawn_trees}")
	if sawn_trees > 0:
		scenic_score *= sawn_trees

	sawn_trees = _look_at_trees(0, -1)
	print(f"Trees: {sawn_trees}")
	if sawn_trees > 0:
		scenic_score *= sawn_trees

	print(f"Tree ({tree_i}, {tree_j}): {scenic_score}\n")

	return scenic_score


data_path = Path(argv[1])

tree_grid = data_from_lines(data_path, lambda line: [int(dgt) for dgt in line])
grid_size = len(tree_grid)

visible_trees = _VisibleCoords()
visible_trees.coords.extend(
	[(0, 0),
	(0, grid_size-1),
	(grid_size-1, 0),
	(grid_size-1, grid_size-1)])

for i in range(1, grid_size-1): # Line index
	_watch_row(tree_grid, i, visible_trees)

for j in range(1, grid_size-1): # Column index
	_watch_column(tree_grid, j, visible_trees)

print(len(visible_trees.coords))

max_scenic_score = 0
for i in range(grid_size):

	for j in range(grid_size):
		scenic_score = _tree_scenic_score(tree_grid, i, j)

		if scenic_score > max_scenic_score:
			max_scenic_score = scenic_score

print(max_scenic_score)
