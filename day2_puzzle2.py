from pathlib import Path
from sys import argv

from data_reading import data_from_lines


_SHAPE_SCORES =\
	{"A": 1,
	"B": 2,
	"C": 3}

_SPACE = " "


def _choose_shape(opponent, strategy):
	shape = ""

	if opponent == "A":
		if strategy == "X":
			shape = "C"
		elif strategy == "Y":
			shape = "A"
		elif strategy == "Z":
			shape = "B"

	elif opponent == "B":
		if strategy == "X":
			shape = "A"
		elif strategy == "Y":
			shape = "B"
		elif strategy == "Z":
			shape = "C"

	elif opponent == "C":
		if strategy == "X":
			shape = "B"
		elif strategy == "Y":
			shape = "C"
		elif strategy == "Z":
			shape = "A"

	return shape


def _rock_paper_scissors_round(opponent, strategy):
	shape = _choose_shape(opponent, strategy)
	score = _SHAPE_SCORES[shape]
	score += _score_for_shapes(opponent, shape)
	return score


def _rock_paper_scissors_round_raw_data(data):
	split_data = data.split(_SPACE)
	opponent = split_data[0]
	strategy = split_data[1]
	return _rock_paper_scissors_round(opponent, strategy)


def _score_for_shapes(opponent, player):
	score = -1

	if opponent == "A":
		if player == "A":
			score = 3
		elif player == "B":
			score = 6
		elif player == "C":
			score = 0

	elif opponent == "B":
		if player == "A":
			score = 0
		elif player == "B":
			score = 3
		elif player == "C":
			score = 6

	elif opponent == "C":
		if player == "A":
			score = 6
		elif player == "B":
			score = 0
		elif player == "C":
			score = 3

	return score


data_path = Path(argv[1])
scores = data_from_lines(data_path, _rock_paper_scissors_round_raw_data)
print(sum(scores))
