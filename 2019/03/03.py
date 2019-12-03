with open("input.txt") as file:
    wires = list(map(lambda line: line.strip().split(","), file.readlines()))


def wireToMatrix(wire, matrix):
    x = 0
    y = 0

    def markLocation():
        matrix[x, y] = 1

    markLocation()

    for movement in wire:
        direction = movement[:1]
        steps = int(movement[1:])
        if direction == "U":
            for i in range(steps):
                y = y + 1
                markLocation()
        elif direction == "D":
            for i in range(steps):
                y = y - 1
                markLocation()
        elif direction == "L":
            for i in range(steps):
                x = x - 1
                markLocation()
        elif direction == "R":
            for i in range(steps):
                x = x + 1
                markLocation()
        else:
            raise r"Unknown direction {direction}"


wire1 = wires[0]
wire2 = wires[1]
matrix1 = {}
matrix2 = {}

wireToMatrix(wire1, matrix1)
wireToMatrix(wire2, matrix2)


def findIntersections(wire, matrix):
    x = 0
    y = 0

    intersections = {}

    for movement in wire:
        direction = movement[:1]
        steps = int(movement[1:])
        if direction == "U":
            for i in range(steps):
                y = y + 1
                if (x, y) in matrix:
                    intersections[x, y] = True
        elif direction == "D":
            for i in range(steps):
                y = y - 1
                if (x, y) in matrix:
                    intersections[x, y] = True
        elif direction == "L":
            for i in range(steps):
                x = x - 1
                if (x, y) in matrix:
                    intersections[x, y] = True
        elif direction == "R":
            for i in range(steps):
                x = x + 1
                if (x, y) in matrix:
                    intersections[x, y] = True
        else:
            raise r"Unknown direction {direction}"

    return intersections.keys()


intersections = findIntersections(wire1, matrix2)

distances = {}
for intersection in intersections:
    x = intersection[0]
    y = intersection[1]
    distances[x, y] = abs(x) + abs(y)

print(min(distances.values()))


def wireStepsToIntersection(intersection, wire):
    x = 0
    y = 0

    totalSteps = 0

    for movement in wire:
        direction = movement[:1]
        steps = int(movement[1:])
        if direction == "U":
            for i in range(steps):
                y = y + 1
                totalSteps = totalSteps + 1
                if intersection == (x, y):
                    return totalSteps
        elif direction == "D":
            for i in range(steps):
                y = y - 1
                totalSteps = totalSteps + 1
                if intersection == (x, y):
                    return totalSteps
        elif direction == "L":
            for i in range(steps):
                x = x - 1
                totalSteps = totalSteps + 1
                if intersection == (x, y):
                    return totalSteps
        elif direction == "R":
            for i in range(steps):
                x = x + 1
                totalSteps = totalSteps + 1
                if intersection == (x, y):
                    return totalSteps
        else:
            raise r"Unknown direction {direction}"


steps = []
for intersection in intersections:
    totalSteps = 0
    totalSteps = totalSteps + wireStepsToIntersection(intersection, wire1)
    totalSteps = totalSteps + wireStepsToIntersection(intersection, wire2)
    steps.append(totalSteps)

print(min(steps))
