import sys
from collections import Counter

import logging
import itertools


def grouper(inputs, n, fillvalue=None):
    iters = [iter(inputs)] * n
    return list(itertools.zip_longest(*iters, fillvalue=fillvalue))


logging.basicConfig(
    level=logging.INFO, format="(%(threadName)-10s) %(message)s",
)


def get_image_data():
    with open("input.txt") as file:
        return [int(value) for value in file.read()]


def get_image_data_str():
    with open("input.txt") as file:
        return file.readline()


image_data = get_image_data()
width = 25
height = 6
resolution = width * height

number_of_layers = len(image_data) // resolution

logging.debug("Image consists of %s layers", number_of_layers)

image = {}

lines = grouper(image_data, width)
layers = grouper(lines, height)
image = grouper(layers, number_of_layers)

layer_count = {}

for index, layer in enumerate(layers):
    flat_layer = list(itertools.chain(*layer))
    layer_count[index] = Counter(flat_layer)

layer_with_fewest_zeros = min(layer_count.items(), key=lambda count: count[1][0])


part1 = layer_with_fewest_zeros[1][1] * layer_with_fewest_zeros[1][2]
assert part1 == 1716
logging.info("Part 1: %s", part1)

decoded_image_data = []


for line in range(height):
    for pixel in range(width):
        pixel_values = []
        for layer in layers:
            pixel_value = layer[line][pixel]
            if pixel_value != 2:
                decoded_image_data.append(pixel_value)
                break

assert len(decoded_image_data) == resolution


print("Part 2")
decoded_image = grouper(decoded_image_data, width)
for line in decoded_image:
    print("".join(map(str, line)).replace("1", "*").replace("0", " "))
