from anytree import Node, RenderTree, AsciiStyle, Walker

debug = False
with open("input.txt") as file:
    input = [line.strip() for line in file.readlines()]

nodes = {}

for connection in input:
    around, orbit = connection.split(")")
    orbit_node = nodes.get(orbit)
    if not orbit_node:
        nodes[orbit] = Node(orbit)
        orbit_node = nodes.get(orbit)
    around_node = nodes.get(around)
    if not around_node:
        nodes[around] = Node(around)
        around_node = nodes.get(around)
    orbit_node.parent = around_node

walker = Walker()

you = nodes.get("YOU").parent
san = nodes.get("SAN").parent

path = walker.walk(you, san)
upwards, common, downwards = path


print(len(upwards) + len(downwards))

# count = 0

# for orbit, around in orbits.items():
#     count += 1  # direct
#     next = orbits.get(around)
#     while next:
#         count += 1  # indirect
#         next = orbits.get(next)

# print("Part1 :", count)


# def findChildren(parent):
#     children = []
#     for orbit, around in orbits.items():
#         if around == parent:
#             children.append(orbit)

#     return children


# def findParent(current):
#     return orbits.get(current)


# found = False
# start = orbits.get("YOU")
# end = orbits.get("SAN")


# def walk(start, end, hops=0):
#     debug and print("start", start)
#     children = findChildren(start)
#     debug and print("children", children)
#     for child in children:
#         debug and print("visit", child, hops)
#         if child == end:
#             debug and print("found", child, end, hops)
#             return hops
#         else:
#             hops += 1
#             result = walk(child, end, hops)
#             if result:
#                 return result

#     return None


# parent_hops = 0
# current = start
# while current and not found:
#     child_hops = walk(current, end)
#     if not child_hops:
#         current = findParent(current)
#         debug and print("new current", current)
#         if current:
#             parent_hops += 1
#             debug and print("parent hops", parent_hops)
#             if current == end:
#                 found = True
#     else:
#         found = True

#     if found:
#         print("Part 2:", parent_hops + child_hops)

