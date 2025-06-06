#palette.py
import color
import random
import math
from color_model import SRGB

class Palette(object):
    def __init__(self):
        self._colors = []
    
    @property
    def palette_size(self) -> int:
        return len(self._colors)
    
    def append(self, new_color=None):
        if new_color is None:
            self._colors.append(color.Color())
        else:
            self._colors.append(new_color)
    
    def pop(self, index = None):
        if index is None:
            self._colors.pop()
        else:
            self._colors.pop(index)
    
    def generate_sRGB_random(self, *args):
        for c in self._colors:
            c.set(SRGB, (random.random(), random.random(), random.random()))
    
    def generate_sRGB_cosine(self, a_r, b_r, c_r, d_r, a_g, b_g, c_g, d_g, a_b, b_b, c_b, d_b):
        for index in range(len(self._colors)):
            phase = index / len(self._colors)
            red = a_r + b_r * math.cos(2*math.pi * (c_r * phase + d_r))
            green = a_g + b_g * math.cos(2*math.pi * (c_g * phase + d_g))
            blue = a_b + b_b * math.cos(2*math.pi * (c_b * phase + d_b))
            self._colors[index].set(SRGB, (red, green, blue))
