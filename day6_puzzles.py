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

		else:
			char_indices[char] = i

	return repeated_char_index


def _find_marker_index(signal, start, window_length, find_end):
	index = start
	while True:
		index_found = _find_first_repeated_char(signal, index, window_length)

		if index_found < 0:
			break

		else:
			index = index_found + 1

	if find_end:
		marker_index = index + window_length

	else:
		marker_index = index

	return marker_index


data_path = Path(argv[1])

signal = lines_from_file(data_path)[0]

packet_m_e = _find_marker_index(signal, 0, 4, True)
message_m_e = _find_marker_index(signal, packet_m_e+1, 14, False)

print(f"Packet marker end: {packet_m_e}")
print(f"Message marker end: {message_m_e}")
