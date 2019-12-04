with open("input.txt") as file:
    masses = map(int, file.readlines())


def fuel_for_mass(mass):
    fuel = mass // 3 - 2
    return fuel if fuel > 0 else 0


fuel = [fuel_for_mass(mass) for mass in masses]

total_fuel = sum(fuel)

assert total_fuel == 3301059

print("Part 1:", total_fuel)


for mass in fuel:
    extra_fuel = mass
    while extra_fuel:
        extra_fuel = fuel_for_mass(extra_fuel)
        total_fuel += extra_fuel


assert total_fuel == 4948732

print("Part 2:", total_fuel)
