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
_SLASH = "/"
_SPACE = " "


class Directory:

	def __init__(self, path):
		self._path = path
		self._content = dict()
		self._size = 0

	def __str__(self):
		return self.__class__.__name__\
			+ f" {self._path} ({self._size}): {list(self._content.keys())}"

	@property
	def content(self):
		return self._content

	@property
	def path(self):
		return self._path

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, new_size):
		self._size = new_size


class _PuzzleCalculator:

	def __init__(self):
		self._filtered_sum = 0
		self._dir_to_del = None

	def calculate(self, file_tree):
		file_tree_size = self._explore_file_tree(file_tree)
		file_tree.size = file_tree_size
		return self._filtered_sum, self._dir_to_del

	def _eval_del_candidate(self, req_mem, deletion_candidate):
		candidate_size = deletion_candidate.size

		if candidate_size >= req_mem:

			if self._dir_to_del is None:
				self._dir_to_del = deletion_candidate

			else:
				if candidate_size < self._dir_to_del.size:
					print(candidate_size)
					self._dir_to_del = deletion_candidate

	def _explore_file_tree(self, file_tree):
		dir_size = 0

		for value in file_tree.content.values():

			if isinstance(value, Directory):
				dir_size += self._explore_file_tree(value)
				value.size = dir_size
				self._eval_del_candidate(30000000, value)

			else:
				dir_size += value

		if dir_size <= 100000:
			self._filtered_sum += dir_size

		return dir_size


def _calculate_dir_size(directory):
	for value in directory.content.values():

		if isinstance(value, int):
			directory.size += value

		elif isinstance(value, Directory):
			directory.size += value.size


def _print_dir_struct(dir_struct, tabs=""):
	for key, value in dir_struct.content.items():

		if isinstance(value, Directory):
			print(f"{tabs}{key}:")
			_print_dir_struct(value, tabs+"\t")

		else:
			print(f"{tabs}{key}: {value}")


data_path = Path(argv[1])

console_lines = lines_from_file(data_path)
num_lines = len(console_lines)

file_tree = Directory(_SLASH)
pwd_path = [_SLASH]
pwd = file_tree


def _get_pwd():
	pwd = file_tree

	for dir_name in pwd_path[1:]:
		pwd = pwd.content[dir_name]

	return pwd


line_index = 0
while line_index < num_lines:
	line = console_lines[line_index]

	if _CMD_CD in line:
		dir_name = line[_CMD_CD_LEN:]

		if dir_name == pwd.path:
			pass

		elif dir_name == _PARENT_DIR:
			pwd_path.pop()
			dir_name = pwd_path[-1]
			pwd = _get_pwd()

		else:
			pwd_path.append(dir_name)

			if dir_name not in pwd.content:
				pwd.content[dir_name] =\
					Directory(_SLASH + _SLASH.join(pwd_path[1:]))

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
				created_dir = Directory(
					_SLASH + _SLASH.join(pwd_path[1:]) + second)
				pwd.content[second] = created_dir

			elif first[0] in _DIGITS:
				pwd.content[second] = int(first)

calculator = _PuzzleCalculator()
filtered_sum, dir_to_del = calculator.calculate(file_tree)
print(f"Puzzle 1: {filtered_sum}")
print(f"Puzzle 2: {dir_to_del.size}")
