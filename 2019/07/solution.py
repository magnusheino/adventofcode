import sys
from collections import Counter
from itertools import permutations
from queue import Queue
import threading

import logging

logging.basicConfig(
    level=logging.INFO, format="(%(threadName)-10s) %(message)s",
)


def getGrid():
    with open("input.txt") as file:
        return [int(value) for value in file.readline().split(",")]


class Amplifier(threading.Thread):
    def __init__(self, amplifier, input, output):
        super().__init__()
        self.grid = getGrid()
        self.input = input
        self.output = output
        self.amplifier = amplifier

    def run(self):
        logging.info("Running amplifier '%s'", self.amplifier)
        try:
            self.amplify()
        finally:
            logging.info("Amplifier '%s' exited", self.amplifier)

    def amplify(self):

        position = 0

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

            def read(mode, param):
                logging.debug(
                    "Read %s value: %s", "immediate" if mode == 1 else "position", param
                )
                value = self.grid[param] if mode == 0 else param
                logging.debug("Value: %s", value)
                return value

            def write(pos, value):
                logging.debug("Write: %s %s", pos, value)
                self.grid[pos] = value

            if opcode == 1:
                logging.debug("ADD")
                # ADD
                write(
                    self.grid[position + 3],
                    read(param_1_mode, self.grid[position + 1])
                    + read(param_2_mode, self.grid[position + 2]),
                )
                position += 4
            elif opcode == 2:
                logging.debug("MULTIPLY")
                # MULTIPLY
                write(
                    self.grid[position + 3],
                    read(param_1_mode, self.grid[position + 1])
                    * read(param_2_mode, self.grid[position + 2]),
                )
                position += 4
            elif opcode == 3:
                logging.debug("INPUT")
                write(self.grid[position + 1], int(self.input.get()))
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
                    write(self.grid[position + 3], 1)
                else:
                    write(self.grid[position + 3], 0)
                position += 4
            elif opcode == 8:
                logging.debug("EQUALS")
                # EQUALS
                if read(param_1_mode, self.grid[position + 1]) == read(
                    param_2_mode, self.grid[position + 2]
                ):
                    write(self.grid[position + 3], 1)
                else:
                    write(self.grid[position + 3], 0)
                position += 4

            elif opcode == 99:
                logging.debug("EXIT")
                # EXIT
                position += 1
                done = True
            else:
                raise ValueError(opcode)


class Amplifiers:
    def __init__(self):
        super().__init__()
        self.Ain = Queue()
        self.Bin = Queue()
        self.Cin = Queue()
        self.Din = Queue()
        self.Ein = Queue()
        self.A = Amplifier("A", self.Ain, self.Bin)
        self.B = Amplifier("B", self.Bin, self.Cin)
        self.C = Amplifier("C", self.Cin, self.Din)
        self.D = Amplifier("D", self.Din, self.Ein)
        self.E = Amplifier("E", self.Ein, self.Ain)

        for amplifier in [self.A, self.B, self.C, self.D, self.E]:
            amplifier.start()

    def get_thrust_signal(self, phase_setting):
        logging.info("Running amplifiers with phase setting %s", phase_setting)
        self.Ain.put(phase_setting[0])
        self.Bin.put(phase_setting[1])
        self.Cin.put(phase_setting[2])
        self.Din.put(phase_setting[3])
        self.Ein.put(phase_setting[4])

        self.Ain.put(0)
        for amplifier in [self.A, self.B, self.C, self.D, self.E]:
            amplifier.join()
        logging.info("All amplifiers have exited")
        result = self.Ain.get_nowait()
        logging.info("Result: %s", result)
        return result


def get_max_thrust_signal(phase_range):
    signals = {}

    for phase_setting in permutations(phase_range):
        signal = Amplifiers().get_thrust_signal(phase_setting)
        signals[signal] = phase_setting

    maxium_signal = max(signals.keys())
    return (signals[maxium_signal], maxium_signal)


phase_setting, signal = get_max_thrust_signal(range(5))
assert phase_setting == (3, 1, 4, 2, 0)
assert signal == 92663
print("Part 1: Phase setting", phase_setting, "gives max signal", signal)


phase_setting, signal = get_max_thrust_signal(range(5, 10))
assert phase_setting == (7, 8, 6, 9, 5)
assert signal == 14365052
print("Part 2: Phase setting", phase_setting, "gives max signal", signal)

