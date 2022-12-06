from pathlib import Path
from sys import argv

from data_reading import lines_from_file


def _spot_first_repeated_char(signal, w_start, w_length):
	read_chars = list()
	repeated_char_index = -1

	for i in range(w_start, w_start+w_length):
		char = signal[i]

		if char in read_chars:
			repeated_char_index = i

		else:
			read_chars.append(char)

	return repeated_char_index


data_path = Path(argv[1])

signal = lines_from_file(data_path)[0]

index = 0
while True:
	index_spotted = _spot_first_repeated_char(signal, index, 4)

	if index_spotted < 0:
		break

	else:
		index = index_spotted + 1

print(index)
