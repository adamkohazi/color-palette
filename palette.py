#palette.py
import color
import random
import math

class Palette(object):
    def __init__(self):
        self._colors = []

    @property
    def colors(self):
        return list(self._colors)
    
    @property
    def palette_size(self) -> int:
        return len(self._colors)
    
    def append(self, new_color=None):
        if new_color is None:
            if len(self._colors) > 0:
                self._colors.append(color.Color.copy(self._colors[-1]))
            else:
                self._colors.append(color.Color())
        else:
            self._colors.append(new_color)
    
    def pop(self, index = None):
        if index is None:
            self._colors.pop()
        else:
            self._colors.pop(index)
        print("Color popped. Remaining: ", len(self._colors))
    
    def generate_RGB_random(self):
        self._colors = [color.Color.from_RGB((random.random(), random.random(), random.random())) for _ in self._colors]
    
    def generate_RGB_cosine(self, a, b, c, d):
        dp = math.pi * 2.0 / len(self._colors)
        for index in range(len(self._colors)):
            phase = index * dp
            red = a[0] + b[0] * math.cos(c[0] * phase + d[0])
            green = a[1] + b[1] * math.cos(c[1] * phase + d[1])
            blue = a[2] + b[2] * math.cos(c[2] * phase + d[2])
            self._colors[index] = color.Color.from_RGB((red, green, blue))
