from pathlib import Path
from sys import argv

from data_reading import lines_from_file


_CMD_PROMPT = "$"
_CMD_CD = _CMD_PROMPT + " cd "
_CMD_CD_LEN = len(_CMD_CD)
_CMD_LS = _CMD_PROMPT + " ls"

_DIGITS = "0123456789"
_DIR_MARK = "dir"
_PARENT_DIR = ".."
_SPACE = " "


class Directory:

	def __init__(self, name, content=dict()):
		self._name = name
		self._content = content
		self._size = 0

	@property
	def content(self):
		return self._content

	@property
	def name(self):
		return self._name

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, new_size):
		self._size = new_size


def _calculate_dir_size(directory):
	for value in directory.content.values():

		if isinstance(value, int):
			directory.size += value

		elif isinstance(value, Directory):
			directory.size += value.size

	print(f"{directory.name}: {directory.size}")


data_path = Path(argv[1])

console_lines = lines_from_file(data_path)
num_lines = len(console_lines)

file_tree = Directory("/")
dir_path = list()
pwd = file_tree
size_sum = 0


def _update_size_sum(directory):
	_calculate_dir_size(directory)
	size = directory.size

	if size <= 100000:
		return size

	return 0


def _go_to_pwd():
	pwd = file_tree

	for dir_name in dir_path:
		pwd = pwd.content[dir_name]


line_index = 0
while line_index < num_lines:
	line = console_lines[line_index]

	if _CMD_CD in line:
		dir_name = line[_CMD_CD_LEN:]

		if dir_name == _PARENT_DIR:
			size_sum += _update_size_sum(pwd)
			dir_path.pop()
			dir_name = dir_path[-1]
			_go_to_pwd()

		else:
			dir_path.append(dir_name)

			if dir_name not in pwd.content:
				pwd.content[dir_name] = Directory(dir_name)

			pwd = pwd.content[dir_name]

		line_index += 1

	elif line == _CMD_LS:

		while True:
			line_index += 1

			try:
				line = console_lines[line_index]
			except IndexError:
				break

			if line[0] == _CMD_PROMPT:
				break

			content = line.split(_SPACE)
			first = content[0]
			second = content[1]

			if first == _DIR_MARK:
				pwd.content[second] = Directory(second)

			elif first[0] in _DIGITS:
				pwd.content[second] = int(first)

size_sum += _update_size_sum(file_tree)

print(size_sum)
