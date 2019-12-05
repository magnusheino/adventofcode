import sys


def getGrid():
    with open("input.txt") as file:
        return [int(value) for value in file.readline().split(",")]


def process(grid):
    position = 0
    result = None

    while not result:
        parameters = str(grid[position])

        print("Parameters: ", parameters)

        opcode = int(parameters[-2:])

        print("Opcode: ", opcode)

        param_1_mode = int(parameters[-3:-2] or "0") if len(parameters) > 1 else 0
        param_2_mode = int(parameters[-4:-3] or "0") if len(parameters) > 1 else 0
        param_3_mode = int(parameters[-5:-4] or "0") if len(parameters) > 1 else 0

        print("Exec: ", opcode, param_1_mode, param_2_mode, param_3_mode)

        def read(mode, param):
            print("Read", "immediate" if mode == 1 else "position", "value: ", param)
            value = grid[param] if mode == 0 else param
            print("Value: ", value)
            return value

        def write(pos, value):
            print("Write: ", pos, value)
            grid[pos] = value

        if opcode == 1:
            print("ADD")
            # ADD
            write(
                grid[position + 3],
                read(param_1_mode, grid[position + 1])
                + read(param_2_mode, grid[position + 2]),
            )
            position += 4
        elif opcode == 2:
            print("MULTIPLY")
            # MULTIPLY
            write(
                grid[position + 3],
                read(param_1_mode, grid[position + 1])
                * read(param_2_mode, grid[position + 2]),
            )
            position += 4
        elif opcode == 3:
            print("INPUT")
            # INPUT
            write(grid[position + 1], int(input("Input: ")))
            position += 2
        elif opcode == 4:
            print("OUTPUT")
            # OUTPUT
            print("Output: ", read(param_1_mode, grid[position + 1]))
            position += 2
        elif opcode == 5:
            print("JUMP-IF-TRUE")
            # JUMP-IF-TRUE
            if read(param_1_mode, grid[position + 1]) != 0:
                position = read(param_2_mode, grid[position + 2])
            else:
                position += 3
        elif opcode == 6:
            print("JUMP-IF-FALSE")
            # JUMP-IF-FALSE
            if read(param_1_mode, grid[position + 1]) == 0:
                position = read(param_2_mode, grid[position + 2])
            else:
                position += 3
        elif opcode == 7:
            print("LESS-THAN")
            # LESS-THAN
            if read(param_1_mode, grid[position + 1]) < read(
                param_2_mode, grid[position + 2]
            ):
                write(grid[position + 3], 1)
            else:
                write(grid[position + 3], 0)
            position += 4
        elif opcode == 8:
            print("EQUALS")
            # EQUALS
            if read(param_1_mode, grid[position + 1]) == read(
                param_2_mode, grid[position + 2]
            ):
                write(grid[position + 3], 1)
            else:
                write(grid[position + 3], 0)
            position += 4

        elif opcode == 99:
            print("EXIT")
            # EXIT
            result = grid[0]
            position += 1
        else:
            raise ValueError(opcode)

    return result


grid = getGrid()

part_1 = process(grid)

