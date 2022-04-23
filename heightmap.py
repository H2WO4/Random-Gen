import random as rnd 
from typing import Callable, TypeVar

from PIL import Image


# Define type shortcuts
T = TypeVar('T')
grid = list[list[T]]
coords = tuple[int, int]
color = tuple[int, int, int]

def init_grid(size: int, all_values: list[int]) -> grid[list[int]]:
    return [[all_values for _ in range(size)] for _ in range(size)]

def collapse(inGrid: grid[list[int]]) -> grid[int]:
    width, height = len(inGrid[0]), len(inGrid)
    outGrid: grid[int] = [[-1 for _ in range(width)] for _ in range(height)]

    to_do: list[coords] = [(x, y) for y in range(height) for x in range(width)]

    rnd.shuffle(to_do)

    while len(to_do) > 0:
        sort_lambda: Callable[[coords], int] = lambda coords: -len(inGrid[coords[0]][coords[1]])
        to_do.sort(key=sort_lambda)

        x, y = to_do.pop()
        update(inGrid, outGrid, x, y)

    return outGrid

def update(inGrid: grid[list[int]], outGrid: grid[int], x: int, y: int) -> None:
    vals: list[int] = inGrid[x][y]

    val = rnd.choice(vals)
    inGrid[x][y] = [val]
    outGrid[x][y] = val

    propagate(inGrid, x, y)

def propagate(inGrid: grid[list[int]], sourceX: int, sourceY: int) -> None:
    width, height = len(inGrid[0]), len(inGrid)
    to_do: list[tuple[coords, coords]] = []
    done: list[coords] = [(sourceX, sourceY)]

    add_neighbors(to_do, sourceX, sourceY, width, height)

    while len(to_do) > 0:
        (baseX, baseY), (x, y) = to_do.pop()
        done.append((x, y))

        newVals = [val for val in inGrid[x][y] if any(is_valid(val2, val) for val2 in inGrid[baseX][baseY])]
        if newVals != inGrid[x][y]:
            inGrid[x][y] = newVals
            add_neighbors(to_do, x, y, height, width)

def add_neighbors(to_do: list[tuple[coords, coords]], x: int, y: int, width: int, height: int) -> None:
    if 0 <= x+1 < width:
        to_do.append(((x, y), (x+1, y)))
    if 0 <= y+1 < height:
        to_do.append(((x, y), (x, y+1)))
    if 0 <= x-1 < width:
        to_do.append(((x, y), (x-1, y)))
    if 0 <= y-1 < height:
        to_do.append(((x, y), (x, y-1)))

def is_valid(val1: int, val2: int) -> bool:
    return abs(val1 - val2) <= 4


def int_to_color(input: int) -> color:
    return (round(255 / values * input), round(255 / values * input), round(255 / values * input))

size = 100
values = 16

all_values = [*range(values)]

test = init_grid(size, all_values)

output = collapse(test)
outImg = [int_to_color(val) for line in output for val in line]

out = Image.new('RGB', (size, size))
out.putdata(outImg) # type: ignore

out = out.resize((size * 8, size * 8), Image.NEAREST)

out.save('out.png')