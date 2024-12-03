import re


def parse_input() -> str:
    with open("resources/day_3", "r") as f:
        data = f.read()
        return data


def add_all_multiplications(input: str) -> int:
    matches = re.finditer(r"mul\((\d+),(\d+)\)", input)
    return sum([int(match.group(1)) * int(match.group(2)) for match in matches])


def match_midpoint(match: re.Match[str]) -> int:
    return (match.start() + match.end()) // 2


def add_multiplications_with_toggle(input: str) -> int:
    mul_ops = {
        match_midpoint(match): match
        for match in re.finditer(r"mul\((\d+),(\d+)\)", input)
    }
    toggle_on_points = {
        match_midpoint(match): 1 for match in re.finditer(r"do\(\)", input)
    }
    toggle_off_points = {
        match_midpoint(match): 0 for match in re.finditer(r"don't\(\)", input)
    }
    merged = dict(sorted((mul_ops | toggle_on_points | toggle_off_points).items()))

    total = 0
    enabled = True
    for i, m in merged.items():
        if isinstance(m, re.Match) and enabled:
            total += int(m.group(1)) * int(m.group(2))

        if m == 0:
            enabled = False

        if m == 1:
            enabled = True

    return total


input = parse_input()

print(f"All multiplications: {add_all_multiplications(input)}")
print(f"Conditional multiplications: {add_multiplications_with_toggle(input)}")
