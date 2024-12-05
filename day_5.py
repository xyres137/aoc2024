import dataclasses
from typing import Dict, Set, Tuple, List
import re
from functools import cmp_to_key


def parse_input() -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    with open("resources/day_5", "r") as f:
        data = iter(f.read().splitlines())

        rules = {}
        updates = []
        while line := next(data):
            match = re.match(r"(\d+)\|(\d+)", line)
            l, r = int(match.group(1)), int(match.group(2))

            if l in rules.keys():
                rules[l].add(r)
            else:
                rules[l] = {r}

            if r not in rules.keys():
                rules[r] = set()

        for upd in data:
            updates.append(list(map(int, upd.split(","))))

        return rules, updates


@dataclasses.dataclass
class UpdateReport:
    seq: List[int]
    init_status: bool
    mid: int


def get_initial_status_and_mid(
    rules: Dict[int, Set[int]], upd: List[int]
) -> UpdateReport:
    correct = all(upd[i] in rules[upd[i - 1]] for i in range(1, len(upd)))
    if correct:
        return UpdateReport(init_status=True, seq=upd, mid=upd[len(upd) // 2])

    fixed = sorted(upd, key=cmp_to_key(lambda x, y: 1 if y in rules[x] else -1))
    return UpdateReport(init_status=False, seq=fixed, mid=fixed[len(fixed) // 2])


rules, updates = parse_input()
reports = [get_initial_status_and_mid(rules, upd) for upd in updates]

print(f"Midpoint sum for correct: {sum(report.mid for report in reports if report.init_status)}")
print(f"Midpoint sum for incorrect: {sum(report.mid for report in reports if not report.init_status)}")
