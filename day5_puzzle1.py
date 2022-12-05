from pathlib import Path
from sys import argv, exit

from data_reading import lines_from_file


_EMPTY_STR = ""
_HYPHEN = "-"
_SPACE = " "


def _get_top_crates(crate_stacks):
	top_crates = list()

	for crate_stack in crate_stacks:
		try:
			top_crate = crate_stack[-1]
		except IndexError:
			top_crate = _HYPHEN

		top_crates.append(top_crate)

	return top_crates


def _move_crates(crate_stacks, quantity, source_i, destination_i):
	source_stack = crate_stacks[source_i]
	destination_stack = crate_stacks[destination_i]

	crates_to_move = source_stack[-quantity:]
	crates_to_move.reverse()
	del source_stack[-quantity:]

	destination_stack.extend(crates_to_move)


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


def _parse_crate_move(crate_move):
	elements = crate_move.split(_SPACE)
	quantity = int(elements[1])
	source = int(elements[3]) - 1
	destination = int(elements[5]) - 1
	return quantity, source, destination


def _print_top_crates(crate_stacks):
	top_crates = _get_top_crates(crate_stacks)
	print(_EMPTY_STR.join(top_crates))


data_path = Path(argv[1])

lines = lines_from_file(data_path)

delimitation = lines.index(_EMPTY_STR)
crate_lines = lines[:delimitation]
crate_lines.reverse()
move_lines = lines[delimitation+1:]

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

for move_line in move_lines:
	quantity, source, destination = _parse_crate_move(move_line)
	_move_crates(crate_stacks, quantity, source, destination)

_print_top_crates(crate_stacks)
