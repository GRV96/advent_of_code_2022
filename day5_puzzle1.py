from pathlib import Path
from sys import argv, exit

from data_reading import lines_from_file


_EMPTY_STR = ""


def _parse_crate_line(crate_line):
	crates = list()

	crate_index = 0
	while True:
		try:
			crate = crate_line[4*crate_index + 1]
		except IndexError:
			break

		crate_index += 1
		crates.append(crate)

	return crates


data_path = Path(argv[1])

lines = lines_from_file(data_path)

delimitation = lines.index(_EMPTY_STR)
crate_lines = lines[:delimitation]
crate_lines.reverse()
move_lines = lines[delimitation:]

crate_nums = _parse_crate_line(crate_lines[0])
num_crates = len(crate_nums)
crate_stacks = [list() for _ in range(num_crates)]
for crate_line in crate_lines[1:]:
	crates = _parse_crate_line(crate_line)

	for crate_index in range(num_crates):
		crate = crates[crate_index]

		if crate.strip() != _EMPTY_STR:
			# The lowest crate is a index 0.
			crate_stacks[crate_index].append(crate)

print(crate_stacks)
