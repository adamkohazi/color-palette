#palette.py
import color
import random

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
