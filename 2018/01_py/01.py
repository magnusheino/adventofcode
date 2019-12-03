changes = []


with open('01_input.txt') as file:
    changes = list(map(lambda line: line.strip(), file.readlines()))

result = sum([int(change) for change in changes]) 

print(result)