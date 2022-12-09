from pathlib import Path
from sys import argv

from data_reading import data_from_lines


_DOWN = "D"
_LEFT = "L"
_RIGHT = "R"
_UP = "U"

_SPACE = " "


class Coordinates:

	def __init__(self, x, y):
		self._x = x
		self._y = y

	def __repr__(self):
		return self.__class__.__name__ + str(self)

	def __str__(self):
		return f"({self._x}, {self._y})"

	def dist_x_y(self, other):
		dist_x = other._x - self._x
		dist_y = other._y - self._y
		return dist_x, dist_y

	def move(self, delta_x, delta_y):
		self._x += delta_x
		self._y += delta_y

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

class Knot:

	def __init__(self, coordinates, next_knot):
		self._coordinates = coordinates
		self._unique_positions = set()
		self._next_knot = next_knot

	def get_num_positions(self):
		return len(self._unique_positions)

	def move(self, delta_x, delta_y):
		self._coordinates.move(delta_x, delta_y)
		self._unique_positions.add((self._coordinates.x, self._coordinates.y))

		if self._next_knot is not None:
			self._pull_next_knot()

	def _pull_next_knot(self):
		dist_x, dist_y =\
			self._next_knot._coordinates.dist_x_y(self._coordinates)

		sign_x = _sign(dist_x)
		sign_y = _sign(dist_y)

		if dist_x == 0 and dist_y != 0:
			x_move = dist_x
			y_move = dist_y-(1*sign_y)

		elif dist_x != 0 and dist_y == 0:
			x_move = dist_x-(1*sign_x)
			y_move = dist_y

		elif abs(dist_x) <= 1 and abs(dist_y) <= 1:
			x_move = 0
			y_move = 0

		elif abs(dist_x) > 0 and abs(dist_y) > 0:
			x_move = sign_x
			y_move = sign_y

		self._next_knot.coordinates.move(x_move, y_move)

	@property
	def coordinates(self):
		return self._coordinates

	@property
	def next_knot(self):
		return self._next_knot


class Move:

	def __init__(self, direction, distance):
		self._direction = direction
		self._distance = distance

	def __repr__(self):
		return self.__class__.__name__\
			+ f"(\"{self._direction}\", {self._distance})"

	@property
	def direction(self):
		return self._direction

	@property
	def distance(self):
		return self._distance


def _parse_move(move_line):
	elements = move_line.split(_SPACE)
	direction = elements[0]
	distance = int(elements[1])
	return Move(direction, distance)


def _sign(number):
	if number > 0:
		return 1

	elif number < 0:
		return -1

	else:
		return 0


data_path = Path(argv[1])
moves = data_from_lines(data_path, _parse_move)

#head = Coordinates(0, 0)
#tail = Coordinates(0, 0)
tail_positions = set()

tail = Knot(Coordinates(0, 0), None)
knot = tail
for _ in range(9):
	prev_knot = Knot(Coordinates(0, 0), knot)
	knot = prev_knot
head = knot


def _move_head(delta_x, delta_y):
	head.move(delta_x, delta_y)
	dist_x, dist_y = tail.dist_x_y(head)

	sign_x = _sign(dist_x)
	sign_y = _sign(dist_y)

	if dist_x == 0 and dist_y != 0:
		x_move = dist_x
		y_move = dist_y-(1*sign_y)

	elif dist_x != 0 and dist_y == 0:
		x_move = dist_x-(1*sign_x)
		y_move = dist_y

	elif abs(dist_x) <= 1 and abs(dist_y) <= 1:
		x_move = 0
		y_move = 0

	elif abs(dist_x) > 0 and abs(dist_y) > 0:
		x_move = sign_x
		y_move = sign_y

	else:
		exit()

	new_position = (tail.x + x_move, tail.y + y_move)
	tail_positions.add(new_position)
	tail.move(x_move, y_move)


for move in moves:
	direction = move.direction
	distance = move.distance

	if direction == _UP:
		for _ in range(distance):
			head.move(0, 1)

	elif direction == _DOWN:
		for _ in range(distance):
			head.move(0, -1)

	elif direction == _LEFT:
		for _ in range(distance):
			head.move(-1, 0)

	elif direction == _RIGHT:
		for _ in range(distance):
			head.move(1, 0)

print(tail.get_num_positions())
