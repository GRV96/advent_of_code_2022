from pathlib import Path
from sys import argv

from data_reading import data_from_lines


_ROCK = "A"
_PAPER = "B"
_SCISSORS = "C"

_LOOSE = "X"
_DRAW = "Y"
_WIN = "Z"

_SHAPE_SCORES = {\
	_ROCK: 1,
	_PAPER: 2,
	_SCISSORS: 3}

_SPACE = " "


def _choose_shape(opponent, strategy):
	shape = ""

	if opponent == _ROCK:
		if strategy == _LOOSE:
			shape = _SCISSORS
		elif strategy == _DRAW:
			shape = _ROCK
		elif strategy == _WIN:
			shape = _PAPER

	elif opponent == _PAPER:
		if strategy == _LOOSE:
			shape = _ROCK
		elif strategy == _DRAW:
			shape = _PAPER
		elif strategy == _WIN:
			shape = _SCISSORS

	elif opponent == _SCISSORS:
		if strategy == _LOOSE:
			shape = _PAPER
		elif strategy == _DRAW:
			shape = _SCISSORS
		elif strategy == _WIN:
			shape = _ROCK

	return shape


def _rock_paper_scissors_round(opponent, strategy):
	shape = _choose_shape(opponent, strategy)
	score = _SHAPE_SCORES[shape]
	score += _score_for_outcome(opponent, shape)
	return score


def _rock_paper_scissors_round_raw_data(data):
	split_data = data.split(_SPACE)
	opponent = split_data[0]
	strategy = split_data[1]
	return _rock_paper_scissors_round(opponent, strategy)


def _score_for_outcome(opponent, player):
	score = -1

	if opponent == _ROCK:
		if player == _ROCK:
			score = 3
		elif player == _PAPER:
			score = 6
		elif player == _SCISSORS:
			score = 0

	elif opponent == _PAPER:
		if player == _ROCK:
			score = 0
		elif player == _PAPER:
			score = 3
		elif player == _SCISSORS:
			score = 6

	elif opponent == _SCISSORS:
		if player == _ROCK:
			score = 6
		elif player == _PAPER:
			score = 0
		elif player == _SCISSORS:
			score = 3

	return score


data_path = Path(argv[1])
scores = data_from_lines(data_path, _rock_paper_scissors_round_raw_data)
print(sum(scores))
