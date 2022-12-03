from pathlib import Path
from sys import argv

from data_reading import data_from_lines


def _find_separate_identical_items(comp1, comp2):
	for item1 in comp1:

		if item1 in comp2:
			return item1

	return ""


def _split_rucksack(content):
	middle = len(content)/2
	middle = int(middle)
	return content[:middle], content[middle:]


data_path = Path(argv[1])

rucksacks = data_from_lines(data_path, _split_rucksack)

priorities = dict()
counter = 0
for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
	counter += 1
	priorities[letter] = counter

priority_sum = 0
for rucksack in rucksacks:
	separate_items = _find_separate_identical_items(rucksack[0], rucksack[1])
	priority = priorities[separate_items]
	priority_sum += priority

print(priority_sum)
