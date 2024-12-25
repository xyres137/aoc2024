import json
from typing import Tuple

import numpy as np


def parse_input() -> np.ndarray:
    with open("resources/day_12", "r") as f:
        data = f.read().splitlines()

        return np.array([list(line) for line in data])


GridPoint = Tuple[int, int]


def get_neighbors(p: GridPoint, grid: np.ndarray):
    d, _ = grid.shape
    diffs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    x, y = p
    neighbors = []
    inner_boundary = []

    for dx, dy in diffs:
        v, w = x + dx, y + dy
        if max(v, w) < d and min(v, w) >= 0 and grid[v, w] == grid[x, y]:
            neighbors.append((v, w))
        else:
            inner_boundary.append((x, y))

    return neighbors, inner_boundary


def run_dfs_for_vertex(p: GridPoint, grid: np.ndarray):
    visited = set()
    total_inner_boundary = []
    s = [p]

    while s:
        current = s.pop()
        if current not in visited:
            visited.add(current)

            neighbors, inner_boundary = get_neighbors(current, grid)
            total_inner_boundary.extend(inner_boundary)

            for neighbor in neighbors:
                s.append(neighbor)

    return str(grid[p]), visited, total_inner_boundary


def add_or_append(k, v, d):
    if k in d.keys():
        d[k].append(v)
    else:
        d[k] = [v]


def find_sides(component, component_boundary):
    centroid = np.mean(np.array(list(component)), axis=0)
    traversal = sorted(
        component_boundary,
        key=lambda p: np.angle(np.subtract(p, centroid).view(np.complex128)),
    )

    sides = 1
    px, py = traversal[0]

    for x, y in traversal[1:]:
        if (x != px and y != py) or (x == px and y == py):
            sides += 1

        px = x
        py = y

    v, w = traversal[0]
    if (px == v or py == w) and ((px == v) != (py == w)):
        sides -= 1

    return sides


def find_connected_components(grid: np.ndarray):
    cc = {}
    already_found = set()
    for idx, _ in np.ndenumerate(grid):
        if idx not in already_found:
            value, component, component_inner_boundary = run_dfs_for_vertex(idx, grid)

            add_or_append(
                value,
                {
                    "area": len(component),
                    "perimeter": len(component_inner_boundary),
                },
                cc,
            )

            already_found = already_found.union(component)

    return cc


input = parse_input()
cc = find_connected_components(input)

print(json.dumps(cc))

total_price = 0

for letter, areas in cc.items():
    total_price += sum([area["area"] * area["perimeter"] for area in areas])

print(f"Total price: {total_price}")
