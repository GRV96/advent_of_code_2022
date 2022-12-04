from pathlib import Path
from sys import argv

from data_reading import data_from_lines


class _Range:

	def __init__(self, lower, upper):
		self._lower = lower
		self._upper = upper

	def __repr__(self):
		return self.__class__.__name__ + f"({self._lower}, {self._upper})"

	def contains(self, number):
		return self._lower <= number and number <= self._upper

	def includes(self, other):
		return self._lower <= other._lower and self._upper >= other._upper

	def overlaps(self, other):
		return self.contains(other._lower) or self.contains(other._upper)


def _get_ranges_from_pair(pair):
	ranges = pair.split(",")
	range1 = ranges[0].split("-")
	range2 = ranges[1].split("-")
	return\
			_Range(int(range1[0]), int(range1[1])),\
			_Range(int(range2[0]), int(range2[1]))


data_path = Path(argv[1])

pairs = data_from_lines(data_path, _get_ranges_from_pair)

overlaps = 0
for pair in pairs:
	range1 = pair[0]
	range2 = pair[1]
	x = repr(range1) + ", " + repr(range2)
	o = ": F"

#	if range1.includes(range2) or range2.includes(range1):
	if range1.overlaps(range2) or range2.overlaps(range1):
		overlaps += 1
		o = ": T"

	print(x + o)

print(overlaps)
