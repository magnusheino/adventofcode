import sys
from collections import Counter, defaultdict
from itertools import permutations
from queue import Queue
import threading

import logging

logging.basicConfig(
    level=logging.DEBUG, format="(%(threadName)-10s) %(message)s",
)


def getGrid():
    with open("input.txt") as file:
        grid = defaultdict(int)
        for index, value in enumerate(
            [int(value) for value in file.readline().split(",")]
        ):
            grid[index] = value

        return grid


class Computer(threading.Thread):
    def __init__(self, name, input, output):
        super().__init__()
        self.grid = getGrid()
        self.input = input
        self.output = output
        self.name = name

    def run(self):
        logging.info("Running '%s'", self.name)
        try:
            self.execute()
        finally:
            logging.info("'%s' exited", self.name)

    def execute(self):

        position = 0
        relative_base = 0
        done = False

        while not done:
            parameters = str(self.grid[position])

            logging.debug("Parameters: %s", parameters)

            opcode = int(parameters[-2:])

            logging.debug("Opcode: %s", opcode)

            param_1_mode = int(parameters[-3:-2] or "0") if len(parameters) > 1 else 0
            param_2_mode = int(parameters[-4:-3] or "0") if len(parameters) > 1 else 0
            param_3_mode = int(parameters[-5:-4] or "0") if len(parameters) > 1 else 0

            logging.debug(
                "Exec: %s %s %s %s", opcode, param_1_mode, param_2_mode, param_3_mode
            )

            def read(mode, pos):
                logging.debug("Read %s value: %s", mode, pos)
                value = None
                if mode == 0:
                    value = self.grid[pos]
                elif mode == 2:
                    value = self.grid[pos + relative_base]
                elif mode == 1:
                    value = pos
                else:
                    raise ValueError(mode)
                logging.debug("Value: %s", value)
                return value

            def write(mode, pos, value):
                logging.debug("Write: %s %s", pos, value)
                if mode == 0:
                    self.grid[pos] = value
                elif mode == 2:
                    self.grid[pos + relative_base] = value
                else:
                    raise ValueError(mode)

            if opcode == 1:
                logging.debug("ADD")
                # ADD
                write(
                    param_3_mode,
                    self.grid[position + 3],
                    read(param_1_mode, self.grid[position + 1])
                    + read(param_2_mode, self.grid[position + 2]),
                )
                position += 4
            elif opcode == 2:
                logging.debug("MULTIPLY")
                # MULTIPLY
                write(
                    param_3_mode,
                    self.grid[position + 3],
                    read(param_1_mode, self.grid[position + 1])
                    * read(param_2_mode, self.grid[position + 2]),
                )
                position += 4
            elif opcode == 3:
                logging.debug("INPUT")
                write(param_1_mode, self.grid[position + 1], int(self.input.get()))
                position += 2
            elif opcode == 4:
                logging.debug("OUTPUT")
                # OUTPUT
                output_value = read(param_1_mode, self.grid[position + 1])
                logging.debug("Output: %s", output_value)
                position += 2
                self.output.put(output_value)
            elif opcode == 5:
                logging.debug("JUMP-IF-TRUE")
                # JUMP-IF-TRUE
                if read(param_1_mode, self.grid[position + 1]) != 0:
                    position = read(param_2_mode, self.grid[position + 2])
                else:
                    position += 3
            elif opcode == 6:
                logging.debug("JUMP-IF-FALSE")
                # JUMP-IF-FALSE
                if read(param_1_mode, self.grid[position + 1]) == 0:
                    position = read(param_2_mode, self.grid[position + 2])
                else:
                    position += 3
            elif opcode == 7:
                logging.debug("LESS-THAN")
                # LESS-THAN
                if read(param_1_mode, self.grid[position + 1]) < read(
                    param_2_mode, self.grid[position + 2]
                ):
                    write(param_3_mode, self.grid[position + 3], 1)
                else:
                    write(param_3_mode, self.grid[position + 3], 0)
                position += 4
            elif opcode == 8:
                logging.debug("EQUALS")
                # EQUALS
                if read(param_1_mode, self.grid[position + 1]) == read(
                    param_2_mode, self.grid[position + 2]
                ):
                    write(param_3_mode, self.grid[position + 3], 1)
                else:
                    write(param_3_mode, self.grid[position + 3], 0)
                position += 4
            elif opcode == 9:
                logging.debug("RELATIVE BASE OFFSET")
                relative_base += read(param_1_mode, self.grid[position + 1])
                position += 2
            elif opcode == 99:
                logging.debug("EXIT")
                # EXIT
                position += 1
                done = True
            else:
                raise ValueError(opcode)


input = Queue()
output = Queue()
computer = Computer("Computer", input, output)

input.put(1)

computer.run()
# computer.start()
# computer.join()

print(output.get_nowait())
