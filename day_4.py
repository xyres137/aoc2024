from functools import reduce
from typing import List, Dict, Tuple, Set
import numpy as np


def parse_input() -> Dict[str, Set[Tuple[int, int]]]:
    with open("resources/day_4") as f:
        data = f.read().splitlines()

        occ = {letter: set() for letter in {"X", "M", "A", "S"}}
        for i in range(len(data)):
            for j in range(len(data[i])):
                occ[data[i][j]].add((i, j))

        return occ


def find_xmas_occurrences(occ: Dict[str, Set[Tuple[int, int]]]):
    total = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for i, j in occ["X"]:
        total += sum(
            [
                (tuple(np.add((i, j), d)) in occ["M"])
                and (tuple(np.add((i, j), np.multiply(2, d))) in occ["A"])
                and (tuple(np.add((i, j), np.multiply(3, d))) in occ["S"])
                for d in directions
            ]
        )

    return total


def find_crossed_mas_occurrences(occ: Dict[str, Set[Tuple[int, int]]]):
    total = 0
    for i, j in occ["A"]:
        b = np.array(
            [
                [(i - 1, j - 1), (i + 1, j - 1)],
                [(i - 1, j + 1), (i + 1, j + 1)]
            ]
        )

        total += sum(
            [
                set(map(tuple, rm[0])).issubset(occ["M"]) and set(map(tuple, rm[1])).issubset(occ["S"])
                for rm in [np.rot90(b, k) for k in range(0, 4)]
            ]
        )
    return total


print(find_xmas_occurrences(parse_input()))
print(find_crossed_mas_occurrences(parse_input()))
