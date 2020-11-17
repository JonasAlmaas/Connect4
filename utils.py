import math


def get_radial_pos(radius, angle):
    x = radius * math.sin(math.pi * 2 * angle / 360)
    y = radius * math.cos(math.pi * 2 * angle / 360)
    return (x, y)
