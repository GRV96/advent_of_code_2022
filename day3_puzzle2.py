from pathlib import Path
from sys import argv

from data_reading import data_from_lines


#def _find_badge_type(rucksacks):
#	for rucksack in rucksacks:


def _common_letter_in_strings(str1, str2, ignored):
	for letter1 in str1:

		for letter2 in str2:

			if letter1 == letter2 and letter1 not in ignored:
				return letter1

	return None


data_path = Path(argv[1])

rucksacks = data_from_lines(data_path)
num_rucksacks = len(rucksacks)

priorities = dict()
counter = 0
for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
	counter += 1
	priorities[letter] = counter

priority_sum = 0
group_index = 0
for group_index in range(0, num_rucksacks, 3):
	group = rucksacks[group_index: group_index+3]

	ignored = list()
	badge = None
	while badge is None:
		candidate = _common_letter_in_strings(group[0], group[1], ignored)

		if candidate in group[2]:
			ignored.append(candidate)

		else:
			badge = candidate

	priority_sum += priorities[badge]

print(priority_sum)
