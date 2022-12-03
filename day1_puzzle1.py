from pathlib import Path
from sys import argv

from data_reading import lines_from_file


data_path = Path(argv[1])

calorie_lines = lines_from_file(data_path)
calorie_lines.append("")

calories = 0
max_calories = 0

for line in calorie_lines:
	try:
		calories += int(line)

	except:
		max_calories = max(calories, max_calories)
		calories = 0

print(max_calories)
