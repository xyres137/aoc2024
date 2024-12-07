import re
from typing import List, Tuple


def parse_input():
    with open("resources/day_7", "r") as f:
        data = f.read().splitlines()

        parsed_input = []
        for line in data:
            split = line.split(" ")
            result = int(re.match(r"(\d+):", split[0]).group(1))
            numbers = list(map(int, split[1:]))
            parsed_input.append((result, numbers))

        return parsed_input


def powerset(s):
    x = len(s)
    components = []
    for i in range(1 << x):
        components.append({s[j] for j in range(x) if (i & (1 << j))})

    return components


def find_correct_results(input: List[Tuple[int, List[int]]]) -> List[int]:
    correct = []
    for result, numbers in input:
        is_correct = False

        for mul_choice in powerset(range(1, len(numbers))):
            temp = numbers[0]
            for i in range(1, len(numbers)):
                if i in mul_choice:
                    temp *= numbers[i]
                else:
                    temp += numbers[i]

                if temp > result:
                    break

            if temp == result:
                is_correct = True
                break

        if is_correct:
            correct.append(result)

    return correct


def find_correct_results_with_concat(input: List[Tuple[int, List[int]]]) -> List[int]:
    correct = []
    for result, numbers in input:
        is_correct = False

        for mul_choice in powerset(range(1, len(numbers))):
            for concat_choice in powerset(list(mul_choice)):
                temp = numbers[0]

                for i in range(1, len(numbers)):
                    if i in concat_choice:
                        temp = int(f"{temp}{numbers[i]}")
                    elif i in mul_choice:
                        temp *= numbers[i]
                    else:
                        temp += numbers[i]

                    if temp > result:
                        break

                if temp == result:
                    is_correct = True
                    break

        if is_correct:
            correct.append(result)

    return correct


input = parse_input()
print(sum(find_correct_results(input)))
print(sum(find_correct_results_with_concat(input)))
