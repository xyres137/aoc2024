import dataclasses
from functools import reduce
from typing import List, Tuple

from sortedcontainers import SortedSet


def parse_input() -> str:
    with open("resources/day_9") as f:
        data = f.read()

    return data


memory_str = parse_input()


@dataclasses.dataclass(frozen=True)
class Segment:
    start: int
    size: int


@dataclasses.dataclass(frozen=True)
class Block(Segment):
    id: int

    def explode(self) -> List["Block"]:
        return [
            Block(id=self.id, start=self.start + i, size=1) for i in range(self.size)
        ]


@dataclasses.dataclass(frozen=True)
class Free(Segment):
    def explode(self) -> List["Free"]:
        if self.size > 0:
            return [Free(start=self.start + i, size=1) for i in range(self.size)]

        return []


def split(input_str: str) -> Tuple[List[Block], List[Free]]:
    blocks = []
    free = []

    block_id = 0
    idx = 0

    for i, c in enumerate(input_str):
        size = int(c)
        if i % 2 == 0:
            blocks.append(Block(id=block_id, start=idx, size=size))
            block_id += 1
        elif size > 0:
            free.append(Free(start=idx, size=size))

        idx += size

    return blocks, free


def rearrange(blocks: List[Block], free: List[Free]):
    s_blocks = SortedSet(blocks, key=lambda x: x.start)
    s_free = SortedSet(free, key=lambda x: x.start)

    for block in reversed(blocks):
        for fr in s_free:
            if fr.start > block.start:
                break

            if fr.size >= block.size:
                to_move = Block(id=block.id, start=fr.start, size=block.size)

                # Update registry
                s_blocks.add(to_move)
                s_blocks.discard(block)

                # Update free space
                remaining_fr = Free(
                    start=fr.start + block.size, size=fr.size - block.size
                )
                if remaining_fr.size > 0:
                    s_free.add(remaining_fr)

                s_free.discard(fr)
                break

    return s_blocks, s_free


def checksum_for_single_moves(blocks: List[Block], free: List[Free]):
    b_exp = reduce(lambda x, y: x + y, [list(b.explode()) for b in blocks])
    f_exp = reduce(lambda x, y: x + y, [f.explode() for f in free])

    b_rearranged, f_rearranged = rearrange(b_exp, f_exp)

    s = 0
    for block in b_rearranged:
        s += sum(
            [block.id * idx for idx in range(block.start, block.start + block.size)]
        )

    return s


def checksum_for_bulk_moves(blocks: List[Block], free: List[Free]):
    b_rearranged, f_rearranged = rearrange(blocks, free)

    s = 0
    for block in b_rearranged:
        s += sum(
            [block.id * idx for idx in range(block.start, block.start + block.size)]
        )

    return s


input = parse_input()
blocks, free = split(input)

print(checksum_for_single_moves(blocks, free))
print(checksum_for_bulk_moves(blocks, free))
