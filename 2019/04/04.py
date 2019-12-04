import re

pattern = re.compile(r"(1{2,}|2{2,}|3{2,}|4{2,}|5{2,}|6{2,}|7{2,}|8{2,}|9{2,}|0{2,})")
increasing = re.compile(r"^\d*(?=\d{6}(\d*)$)0*1*2*3*4*5*6*7*8*9*\1$")


def count(match_condition):
    count = 0
    for password in map(str, range(353096, 843212)):
        if any(match_condition(match) for match in pattern.findall(password)):
            count += 1 if increasing.findall(password) else 0
    return count


print(
    "Part 1:",
    count(lambda match: match),
    "Part 2:",
    count(lambda match: len(match) == 2),
)
