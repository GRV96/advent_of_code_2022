from pathlib import Path
from sys import argv

from data_reading import data_from_lines


_SHAPE_SCORES =\
	{"A": 1,
	"X": 1,
	"B": 2,
	"Y": 2,
	"C": 3,
	"Z": 3}

_SPACE = " "


def _rock_paper_scissors_round(opponent, player):
	score = _SHAPE_SCORES[player]

	score += _score_for_shapes(opponent, player)

	return score


def _rock_paper_scissors_round_raw_data(data):
	shapes = data.split(_SPACE)
	opponent = shapes[0]
	player = shapes[1]
	return _rock_paper_scissors_round(opponent, player)


def _score_for_shapes(opponent, player):
	score = -1

	if opponent == "A":
		if player == "X":
			score = 3
		elif player == "Y":
			score = 6
		elif player == "Z":
			score = 0

	elif opponent == "B":
		if player == "X":
			score = 0
		elif player == "Y":
			score = 3
		elif player == "Z":
			score = 6

	elif opponent == "C":
		if player == "X":
			score = 6
		elif player == "Y":
			score = 0
		elif player == "Z":
			score = 3

	return score


data_path = Path(argv[1])

scores = data_from_lines(data_path, _rock_paper_scissors_round_raw_data)
print(sum(scores))
