from typing import Tuple

import numpy as np


def parse_input() -> Tuple[np.ndarray, np.ndarray]:
    with open("resources/day_6", "r") as f:
        data = f.read().splitlines()

    array = np.array([list(row) for row in data])
    position = np.argwhere(array == "^")[0]

    return position, array


def walk(init: np.ndarray, array: np.ndarray) -> int:
    position = init
    direction = np.array([-1, 0])
    visited = set()
    visited.add(tuple(position))

    n, _ = array.shape

    while True:
        next_position = position + direction
        v, w = next_position

        if min(v, w) < 0 or max(v, w) >= n:
            break

        if array[v, w] in {".", "^"}:
            position = next_position
            visited.add(tuple(position))
        elif array[v, w] == "#":
            direction = change_direction(direction)

    return len(visited)


rotation_matrix = np.array([[0, 1], [-1, 0]])


def change_direction(direction: np.ndarray) -> np.ndarray:
    return rotation_matrix @ direction


p, arr = parse_input()
print(walk(p, arr))
