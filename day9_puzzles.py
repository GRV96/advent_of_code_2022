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

		print(f"Self: {self._coordinates}")
		print(f"Next: {self._next_knot._coordinates}")
		print(f"Distance: ({dist_x}, {dist_y})")

		sign_x = _sign(dist_x)
		sign_y = _sign(dist_y)
		print(f"Signs: ({sign_x}, {sign_y})")

		if dist_x == 0 and dist_y != 0:
			print("Vertical")
			x_move = dist_x
			y_move = dist_y-(1*sign_y)

		elif dist_x != 0 and dist_y == 0:
			print("Horizontal")
			x_move = dist_x-(1*sign_x)
			y_move = dist_y

		elif abs(dist_x) <= 1 and abs(dist_y) <= 1:
			x_move = 0
			y_move = 0

		elif abs(dist_x) > 0 and abs(dist_y) > 0:
			print("Diagonal")
			x_move = sign_x
			y_move = sign_y

		self._next_knot.move(x_move, y_move)
		print(f"Moving of ({x_move}, {y_move}) to {self._next_knot.coordinates}")

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


def _get_knot(rope, knot_i):
	knot = rope

	for _ in range(knot_i):
		try:
			knot = knot.next_knot
		except AttributeError:
			break

	return knot

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

puzzle_num = int(argv[2])
if puzzle_num == 1:
	start_i = 0
	start_j = 0
	num_knots = 2
elif puzzle_num == 2:
	start_i = 11
	start_j = 5
	num_knots = 10
else:
	print("ERROR! The puzzle numbers are 1 and 2.")
	exit()

tail_positions = set()

tail = Knot(Coordinates(start_i, start_j), None)
knot = tail
for _ in range(num_knots-1):
	prev_knot = Knot(Coordinates(start_i, start_j), knot)
	knot = prev_knot
head = knot
#print(head.next_knot)
#print(tail.next_knot)

#counter = 0
#while True:
#	knot = _get_knot(head, counter)

#	if knot is None:
#		break

#	if knot.next_knot is None:
#		print(f"{counter}: x")

#	else:
#		knot = knot.next_knot
#		print(f"{counter}: ->")

#	counter += 1


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
	print(f"\n{move}")
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

	print(tail.coordinates)
#	print(_get_knot(head, 1).coordinates)

print(tail.get_num_positions())
