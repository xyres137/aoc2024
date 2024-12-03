import re
from collections import Counter
from typing import List, Tuple


def parse_input() -> Tuple[List, List]:
    with open("resources/day_1", "r") as f:
        data = f.readlines()

    left = []
    right = []

    for line in data:
        result = re.search(pattern=r"(\d+)\s+(\d+)", string=line)
        left.append(int(result.group(1)))
        right.append(int(result.group(2)))

    return left, right


def find_total_difference(input: Tuple[List, List]) -> int:
    left, right = input
    total = 0

    for a, b in zip(sorted(left), sorted(right)):
        total += abs(a - b)

    return total


def find_similarity_score(input: Tuple[List, List]) -> int:
    left, right = input
    right_occ = Counter(right)

    total = 0
    for num in left:
        total += num * right_occ[num]

    return total


parsed_input = parse_input()
day_1_result = find_total_difference(parsed_input)
day_2_result = find_similarity_score(parsed_input)

print("Results:")
print(f"Day 1: {day_1_result}")
print(f"Day 2: {day_2_result}")
