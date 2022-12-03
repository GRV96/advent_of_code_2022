from pathlib import Path
from sys import argv

from data_reading import data_from_lines


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
	badge = None

	for item in rucksacks[group_index]:
		if item in rucksacks[group_index+1]\
				and item in rucksacks[group_index+2]:
			badge = item

	priority_sum += priorities[badge]

print(priority_sum)
