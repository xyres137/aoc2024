import math
from itertools import product

import numpy as np


def parse_input():
    with open("resources/day_8", "r") as f:
        data = f.read().splitlines()
        return np.array([list(s) for s in data])


def is_within_bounds(z, size: int) -> bool:
    return min(z[0], z[1]) >= 0 and max(z[0], z[1]) < size


def get_antinodes_for_pair(p, q, size: int):
    return {tuple(z) for z in [2 * q - p, 2 * p - q] if is_within_bounds(z, size)}


def get_all_antinodes_for_pair(p, q, size: int):
    d = q - p

    d = (d / math.gcd(d[0], d[1])).astype(dtype=np.int64)

    antinodes = set()
    scale = 0
    while True:
        v, w = p + scale * d, p - scale * d
        tv = is_within_bounds(v, size)
        tw = is_within_bounds(w, size)

        if tv:
            antinodes.add(tuple(v))
        if tw:
            antinodes.add(tuple(w))

        scale += 1

        if not (tv or tw):
            break

    return antinodes


def find_antinodes(input: np.ndarray):
    size = len(input)
    r = range(size)

    antennas = {}
    antinodes = set()
    for i, j in product(r, r):
        if (p := input[i, j]) != ".":
            if p not in antennas.keys():
                antennas[p] = {(i, j)}
                continue

            for x, y in antennas[p]:
                new = get_antinodes_for_pair(np.array([i, j]), np.array([x, y]), size)
                antinodes.update(new)

            antennas[p].add((i, j))

    return antinodes


def find_all_antinodes(input: np.ndarray):
    size = len(input)
    r = range(size)

    antennas = {}
    antinodes = set()
    for i, j in product(r, r):
        if (p := input[i, j]) != ".":
            if p not in antennas.keys():
                antennas[p] = {(i, j)}
                continue

            for x, y in antennas[p]:
                new = get_all_antinodes_for_pair(
                    np.array([i, j]), np.array([x, y]), size
                )
                antinodes.update(new)

            antennas[p].add((i, j))

    return antinodes


input = parse_input()
print(len(find_antinodes(input)))
print(len(find_all_antinodes(input)))
