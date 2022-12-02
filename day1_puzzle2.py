from pathlib import Path
from sys import argv

from data_reading import lines_from_file


data_path = Path(argv[1])

calorie_lines = lines_from_file(data_path)
calorie_lines.append("")

elf_calories = [0]
calories = 0

for line in calorie_lines:
	try:
		calories += int(line)
	
	except:
		elf_calories.append(calories)
		calories = 0

elf_calories.sort()

print(sum(elf_calories[-3:]))
