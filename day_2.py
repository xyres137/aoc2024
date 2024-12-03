from typing import List


def parse_input() -> List[List[int]]:
    with open("resources/day_2", "r") as f:
        data = f.readlines()

    reports = []
    for line in data:
        levels = list(map(int, line.split(" ")))
        reports.append(levels)

    return reports


def diff_seq(seq: List[int]) -> List[int]:
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def check_safe(diffs: List[int]) -> bool:
    inc = [1 <= d <= 3 for d in diffs]
    if not sum([x is False for x in inc]):
        return True

    return False


def check_semi_safe(diffs: List[int]) -> bool:
    inc = [1 <= d <= 3 for d in diffs]

    s = sum([x is False for x in inc])
    if s == 0:
        return True

    idx = inc.index(False)
    if s == 1:
        if (
            (idx == 0)
            or (idx == len(diffs) - 1)
            or (1 <= diffs[idx] + diffs[idx + 1] <= 3)
        ):
            return True

    if s == 2:
        if (inc[idx + 1] is False) and (1 <= diffs[idx] + diffs[idx + 1] <= 3):
            return True

    return False


def find_safe_reports(diffs: List[List[int]]) -> int:
    return sum([check_safe(diff) or check_safe([-x for x in diff]) for diff in diffs])


def find_safe_reports_with_dampener(diffs: List[List[int]]) -> int:
    return sum(
        [check_semi_safe(diff) or check_semi_safe([-x for x in diff]) for diff in diffs]
    )


reports = parse_input()
diffs = list(map(diff_seq, reports))

print(find_safe_reports(diffs))
print(find_safe_reports_with_dampener(diffs))
