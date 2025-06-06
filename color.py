#color.py
import color_model
from recordclass import recordclass

class Color(object):
    def __init__(self, xyz=[0,0,0]):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*xyz)

    def set(self, color_model, components):
        self._xyz.X, self._xyz.Y, self._xyz.Z = color_model.to_CIEXYZ(components)
    
    def get(self, color_model):
        return recordclass(color_model.short_name, color_model.component_names)(*color_model.from_CIEXYZ(self._xyz))