import dataclasses
from typing import Tuple, List

import numpy as np


def parse_input() -> np.ndarray:
    with open("resources/day_10", "r") as f:
        data = f.read().splitlines()

        return np.array([list(map(int, line)) for line in data])


GridPoint = Tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Node:
    value: int
    p: GridPoint
    neighbors: List["Node"]


def get_neighbors(p: GridPoint, grid: np.ndarray) -> List[Node]:
    d, _ = grid.shape
    diffs = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    x, y = p
    neighbors = []

    for dx, dy in diffs:
        v, w = x + dx, y + dy
        if max(v, w) < d and min(v, w) >= 0 and grid[v, w] - grid[x, y] == 1:
            neighbors.append(
                Node(
                    value=int(grid[v, w]),
                    p=(v, w),
                    neighbors=get_neighbors((v, w), grid),
                )
            )

    return neighbors


def find_all_trails(origin: Node, target_v: int, path=None):
    if path is None:
        path = []

    path = path + [origin.p]

    if origin.value == target_v:
        return [path]

    paths = []
    for neighbor in origin.neighbors:
        if neighbor.p not in path:
            new_paths = find_all_trails(neighbor, target_v, path)
            for p in new_paths:
                paths.append(p)

    return paths


arr = parse_input()
trailheads = []

for idx, v in np.ndenumerate(arr):
    if v == 0:
        trailheads.append(Node(value=v, p=idx, neighbors=get_neighbors(idx, arr)))

results = {}
for head in trailheads:
    paths = find_all_trails(head, 9)
    results[head.p] = {
        "rating": len(paths),
        "score": len(set(path[-1] for path in paths)),
    }

print(results)

print("Total score:", sum([result["score"] for result in results.values()]))
print("Total rating:", sum([result["rating"] for result in results.values()]))
