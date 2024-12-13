import typing


def parse_input() -> typing.List[int]:
    with open("resources/day_11", "r") as f:
        data = list(map(int, f.read().split(" ")))
        return data


input = parse_input()

cache = {}


def blink_until_stopped(value: int, remaining: int):
    if (value, remaining) in cache.keys():
        return cache[(value, remaining)]

    if remaining <= 0:
        return 1

    else:
        if value == 0:
            result = blink_until_stopped(1, remaining - 1)
        elif (digits_count := len(str(value))) % 2 == 0:
            left_value = value // (10 ** (digits_count // 2))
            right_value = value % (10 ** (digits_count // 2))
            result = blink_until_stopped(
                left_value, remaining - 1
            ) + blink_until_stopped(right_value, remaining - 1)
        else:
            result = blink_until_stopped(value * 2024, remaining - 1)

        cache[(value, remaining)] = result
        return result


result_1 = sum([blink_until_stopped(stone, 25) for stone in input])
result_2 = sum([blink_until_stopped(stone, 75) for stone in input])

print(f"Day 1: {result_1}")
print(f"Day_2: {result_2}")
