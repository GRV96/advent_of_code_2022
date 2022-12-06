_NEW_LINE = "\n"

_FILE_MODE_R = "r"


def convert_list_content(some_list, conversion):
	# conversion is a function that takes a list item as its
	# only argument and transforms it into a usable value.
	for i in range(len(some_list)):
		item = some_list[i]

		if isinstance(item, list):
			convert_list_content(item, conversion)

		else:
			try:
				some_list[i] = conversion(item)
			except:
				pass


def data_from_lines(data_path, conversion=None):
	# data_path is of type pathlib.Path.
	# conversion is a function that takes a line as its
	# only argument and transforms it into usable data.
	lines = lines_from_file(data_path)
	data = list()

	if conversion is None:
		conv_or_not = lambda line: line
	else:
		conv_or_not = lambda line: conversion(line)

	# Even when no conversion is needed, data must go through
	# this loop so that all empty lines are eliminated.
	for line in lines:
		if len(line) > 0:
			data.append(conv_or_not(line))

	return data


def lines_from_file(path):
	# path is of type pathlib.Path.
	with path.open(mode=_FILE_MODE_R) as data_file:
		content = data_file.read()

	return content.split(_NEW_LINE)
