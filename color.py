#color.py
import numpy as np
from recordclass import recordclass

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
        # Find the minimum, maximum of the R, G, and B components
        rgb = self.to_RGB()
        maxm = max(rgb)
        minm = min(rgb)
        # Calculate the saturation of the color, based on difference between components
        delta = maxm - minm
        saturation = delta/maxm
        # Calculate the brightness of the color
        brightness = 1.0/maxm

        # If there's no difference between the max and min values (i.e., the color is grayscale)
        if delta <= 0:
            return recordclass('HSB', ['H', 'S', 'B'])(0, saturation, brightness)

        # If the red component is dominant
        if rgb.R == maxm:
            hue = (rgb.G - rgb.B) / delta

        # If the green component is dominant
        elif rgb.G == maxm:
            hue = 2 + (rgb.B - rgb.R) / delta

        # If the blue component is dominant
        else:
            hue = 4 + (rgb.R - rgb.G) / delta

        # Normalize hue to be in the range [0, 1]
        hue = (hue/6) % 1.0

        # Return the final HSB color
        return recordclass('HSB', ['H', 'S', 'B'])(hue, saturation, brightness)