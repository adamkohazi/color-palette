#color.py
import numpy as np
from recordclass import recordclass
import colorsys

# Conversion matrices
CM_RGBtoXYZ = np.array([[0.49, 0.31, 0.2], [0.17697, 0.8124, 0.01063], [0, 0.01, 0.99]])
CM_XYZtoRGB = np.linalg.inv(CM_RGBtoXYZ)

class Color(object):
    def __init__(self, xyz=[0,0,0]):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*xyz)

    @classmethod
    def copy(cls, color):
        return cls(color.to_XYZ())
    
    @classmethod
    def from_RGB(cls, rgb):
        return cls(CM_RGBtoXYZ.dot(rgb))

    @classmethod
    def from_RGB255(cls, rgb):
        return cls.from_RGB(tuple(component/255 for component in rgb))

    @classmethod
    def from_RGB_hex(cls, hex):
        # Only work on last 6 characters
        hex = hex[-6:]
        rgb = tuple(int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        return cls.from_RGB(rgb)

    def set_XYZ(self, xyz):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*xyz)
    
    def set_RGB(self, rgb):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*CM_RGBtoXYZ.dot(rgb))

    def set_RGB255(self, rgb):
       self.set_RGB(tuple(component/255 for component in rgb))

    def set_RGB_hex(self, hex):
        # Only work on last 6 characters
        hex = hex[-6:]
        rgb = tuple(int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        self.set_RGB(rgb)

    def to_XYZ(self):
        return self._xyz
    
    def to_RGB(self):
        return recordclass('RGB', ['R', 'G', 'B'])(*(min(max(0.0, component), 1.0) for component in CM_XYZtoRGB.dot(self._xyz))) # Clamp values
    
    def to_RGBA(self):
        return recordclass('RGB', ['R', 'G', 'B', 'A'])(*self.to_RGB(), 1.0)
    
    def to_RGB255(self):
        return recordclass('RGB255', ['R', 'G', 'B'])(*(int(component*255) for component in self.to_RGB()))
    
    def to_HSB(self):
        rgb = self.to_RGB()

        # Return the final HSB color
        return recordclass('HSB', ['H', 'S', 'B'])(*colorsys.rgb_to_hsv(*rgb))
    
    def to_CIELAB(self):
        # Helper function for the transformation
        def f(t):
            d = 6/29
            if t > d**3:
                return t ** (1/3)
            else:
                return t / 3 * d**(-2) + 4/29

        # Reference white point D65
        Xn = 95.0489
        Yn = 100
        Zn = 108.884

        # Reference white point D50 (printing industry)
        # Xn = 96.4212
        # Yn = 100
        # Zn = 82.5188

        L = 116 / f(self._xyz.Y / Yn) - 16
        a = 500 / f(self._xyz.X / Xn) - f(self._xyz.Y / Yn)
        b = 200 / f(self._xyz.Y / Yn) - f(self._xyz.Z / Zn)

        # Return the final LAB color
        return recordclass('Lab', ['L', 'a', 'b'])(*colorsys.rgb_to_hsv((L, a, b)))
