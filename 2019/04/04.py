import re

pattern = re.compile(r"(1{2,}|2{2,}|3{2,}|4{2,}|5{2,}|6{2,}|7{2,}|8{2,}|9{2,}|0{2,})")
count = 0
for password in range(353096, 843212):
    if any(len(match) == 2 for match in pattern.findall(str(password))):
        increasing = True
        current = 0
        for digit in map(int, list(str(password))):
            if digit >= current:
                current = digit
            else:
                increasing = False
        count += 1 if increasing else 0
print(count)
