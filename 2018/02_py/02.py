from collections import Counter
import sys

boxes = []

with open('02_input.txt') as file:
    boxes = list(map(lambda line: line.strip(), file.readlines()))

def part1():
    has2 = 0
    has3 = 0

    for count in [Counter(box).values() for box in boxes]:
        has2 += 2 in count
        has3 += 3 in count

    checksum = has2 * has3

    print(checksum)

def part2():
    pass

part1()
part2()