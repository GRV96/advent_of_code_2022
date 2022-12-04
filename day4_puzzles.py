from pathlib import Path
from sys import argv, exit

from data_reading import data_from_lines


class _Range:

	def __init__(self, lower, upper):
		self._lower = lower
		self._upper = upper

	def __repr__(self):
		return self.__class__.__name__ + f"({self._lower}, {self._upper})"

	def contains_num(self, number):
		return self._lower <= number and number <= self._upper

	def contains_range(self, other):
		return self._lower <= other._lower and self._upper >= other._upper

	def overlaps(self, other):
		return self.contains_num(other._lower) or self.contains_num(other._upper)


def _get_ranges_from_pair(pair):
	ranges = pair.split(",")
	range1 = ranges[0].split("-")
	range2 = ranges[1].split("-")
	return\
			_Range(int(range1[0]), int(range1[1])),\
			_Range(int(range2[0]), int(range2[1]))


data_path = Path(argv[1])

puzzle_num = int(argv[2])
if puzzle_num == 1:
	detection = lambda r1, r2: r1.contains_range(r2) or r2.contains_range(r1)
elif puzzle_num == 2:
	detection = lambda r1, r2: r1.overlaps(r2) or r2.overlaps(r1)
else:
	print("ERROR! The puzzle numbers are 1 and 2.")
	exit()

pairs = data_from_lines(data_path, _get_ranges_from_pair)

overlaps = 0
for pair in pairs:
	range1 = pair[0]
	range2 = pair[1]

	if detection(range1, range2):
		overlaps += 1

print(overlaps)
