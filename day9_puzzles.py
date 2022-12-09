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

	elif number > 0:
		return -1

	else:
		return 0


data_path = Path(argv[1])
moves = data_from_lines(data_path, _parse_move)

head = Coordinates(0, 0)
tail = Coordinates(0, 0)
tail_positions = set()


def _move_head(delta_x, delta_y):
	head.move(delta_x, delta_y)
	dist_x, dist_y = tail.dist_x_y(head)

	print(f"Head: {head}")
	print(f"Tail: {tail}")
	print(f"Distance: ({dist_x}, {dist_y})")

	sign_x = _sign(dist_x)
	sign_y = _sign(dist_y)

	if dist_x == 0 and dist_y != 0:
		print("Vertical")
		x_move = dist_x
		y_move = dist_y-(1*sign_y)

	elif dist_x != 0 and dist_y == 0:
		print("Horizontal")
		x_move = dist_x-(1*sign_x)
		y_move = dist_y

	elif abs(dist_x) > 0 and abs(dist_y) > 0:
		x_move = sign_x
		y_move = sign_y

	else:
		print(f"Head: {head}")
		print(f"Tail: {tail}")
		print(f"Distance: ({dist_x}, {dist_y})")
		exit()

	new_position = (tail.x + x_move, tail.y + y_move)
	tail_positions.add(new_position)
	tail.move(x_move, y_move)
	print(f"Moving to {new_position}")
	print(f"Tail: {tail}")


for move in moves:
	direction = move.direction
	distance = move.distance
	print(f"\n{move}")

	if direction == _UP:
		for _ in range(distance):
			_move_head(0, 1)

	elif direction == _DOWN:
		for _ in range(distance):
			_move_head(0, -1)

	elif direction == _LEFT:
		for _ in range(distance):
			_move_head(-1, 0)

	elif direction == _RIGHT:
		for _ in range(distance):
			_move_head(1, 0)

print(len(tail_positions))
