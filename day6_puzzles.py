from pathlib import Path
from sys import argv

from data_reading import lines_from_file


def _find_first_repeated_char(signal, w_start, w_length):
	char_indices = dict()
	repeated_char_index = -1

	for i in range(w_start, w_start+w_length):
		char = signal[i]

		if char in char_indices.keys():
			repeated_char_index = char_indices[char]
			break

		else:
			char_indices[char] = i

	return repeated_char_index


def _find_marker_end(signal, start, window_length):
	index = start
	while True:
		index_found = _find_first_repeated_char(signal, index, window_length)

		if index_found < 0:
			break

		else:
			index = index_found + 1

	marker_end = index + window_length
	return marker_end


data_path = Path(argv[1])

signal = lines_from_file(data_path)[0]

packet_m_e = _find_marker_end(signal, 0, 4)
message_m_e = _find_marker_end(signal, 0, 14)

print(f"Packet marker end: {packet_m_e}")
print(f"Message marker end: {message_m_e}")
