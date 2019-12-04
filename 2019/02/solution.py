import sys


def getGrid():
    with open("input.txt") as file:
        return [int(value) for value in file.readline().split(",")]


def process(grid):
    position = 0
    result = None

    while not result:
        opcode = grid[position]
        if opcode == 1:
            grid[grid[position + 3]] = (
                grid[grid[position + 1]] + grid[grid[position + 2]]
            )
        elif opcode == 2:
            grid[grid[position + 3]] = (
                grid[grid[position + 1]] * grid[grid[position + 2]]
            )
        elif opcode == 99:
            result = grid[0]
        else:
            raise ValueError(opcode)
        position += 4

    return result


grid = getGrid()

grid[1] = 12
grid[2] = 2

part_1 = process(grid)

assert part_1 == 2890696
print("Part 1:", part_1)

for noun in range(100):
    for verb in range(100):
        grid = getGrid()

        grid[1] = noun
        grid[2] = verb

        part_2 = process(grid)

        if part_2 == 19690720:
            part_2 = 100 * noun + verb
            assert part_2 == 8226
            print("Part 2:", part_2)
            sys.exit(0)
