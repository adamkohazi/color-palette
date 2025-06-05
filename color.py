#color.py
import numpy as np
from recordclass import recordclass
import colorsys





# Matrices to convert between CIE linear RGB and CIE-XYZ
CM_CIERGBtoCIEXYZ = np.array([
    [0.49000, 0.31000, 0.20000],
    [0.17697, 0.81240, 0.01063],
    [0.00000, 0.01000, 0.99000]
])
CM_CIEXYZtoCIERGB = np.linalg.inv(CM_CIERGBtoCIEXYZ)

# Matrices to convert between linear RGB and CIE-XYZ
CM_RGBtoCIEXYZ = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041]
])
CM_CIEXYZtoRGB = np.linalg.inv(CM_RGBtoCIEXYZ)

# Matrix to convert from XYZ to LMS
CM_CIEXYZ_LMS = np.array([
    [0.8189330101, 0.3618667424, -0.1288597137],
    [0.0329845436, 0.9293118715, 0.0361456387],
    [0.0482003018, 0.2643662691, 0.6338517070]
])
CM_LMS_CIEXYZ = np.linalg.inv(CM_CIEXYZ_LMS)

# Matrix to convert from LMS to Oklab
CM_LMS_OKLAB = np.array([
    [0.2104542553, 0.7936177850, -0.0040720468],
    [1.9779984951, -2.4285922050, 0.4505937099],
    [0.0259040371, 0.7827717662, -0.8086757660]
])
CM_OKLAB_LMS = np.linalg.inv(CM_LMS_OKLAB)

class Color(object):
    def __init__(self, xyz=[0,0,0]):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*xyz)
    
    # Helper functions
    @staticmethod
    def RGB_to_sRGB(rgb):
        srgb = [12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055 for c in rgb]
        return recordclass('sRGB', ['R', 'G', 'B'])(*srgb)
    
    @staticmethod
    def sRGB_to_RGB(srgb):
        rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
        return recordclass('RGB', ['R', 'G', 'B'])(*rgb)

    # CIE XYZ color space
    def set_XYZ(self, xyz):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*xyz)
    
    def to_XYZ(self):
        return self._xyz
    
    # CIE XYZ color space
    def set_RGB(self, rgb):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*CM_RGBtoCIEXYZ.dot(rgb))
    
    # sRGB color space
    def set_sRGB(self, srgb):
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(*CM_RGBtoCIEXYZ.dot(self.sRGB_to_RGB(srgb)))

    def set_sRGB255(self, rgb):
       self.set_sRGB(tuple(component/255 for component in rgb))

    def set_sRGB_hex(self, hex):
        # Only work on last 6 characters
        hex = hex[-6:]
        rgb = tuple(int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        self.set_sRGB(rgb)
    
    def set_OKLAB(self, lab):
        # Convert Oklab to LMS
        lms = CM_OKLAB_LMS.dot(lab)

        # Apply cube nonlinearity
        lms = np.power(lms, 3)

        # Convert XYZ to LMS
        x, y, z = CM_LMS_CIEXYZ.dot(self.lms)
        self._xyz = recordclass('XYZ', ['X', 'Y', 'Z'])(x, y, z)


    
    # Linear RGB
    def to_RGB(self):
        return recordclass('RGB', ['R', 'G', 'B'])(*(min(max(0.0, component), 1.0) for component in CM_CIEXYZtoRGB.dot(self._xyz))) # Clamp values
    
    def to_RGBA(self):
        return recordclass('RGB', ['R', 'G', 'B', 'A'])(*self.to_RGB(), 1.0)

    # Gamma corrected RGB
    def to_sRGB(self):
        return recordclass('sRGB', ['R', 'G', 'B'])(*self.RGB_to_sRGB(self.to_RGB()))
    
    def to_sRGBA(self):
        return recordclass('sRGB', ['R', 'G', 'B', 'A'])(*self.RGB_to_sRGB(self.to_RGB()), 1.0)
    
    def to_sRGB255(self):
        return recordclass('sRGB255', ['R', 'G', 'B'])(*(int(component*255) for component in self.RGB_to_sRGB(self.to_RGB())))
    
    def to_HSB(self):
        rgb = self.to_RGB()

        # Return the final HSB color
        return recordclass('HSB', ['H', 'S', 'B'])(*colorsys.rgb_to_hsv(*rgb))
    
    def to_CIELAB(self):
        # Helper function for the transformation
        def f(t):
            d = 6.0/29
            if t > d**3:
                return t ** (1/3)
            else:
                return t / 3.0 * d**(-2) + (4.0/29)

        # Reference white point D65
        Xn = 95.0489
        Yn = 100
        Zn = 108.884

        # Reference white point D50 (printing industry)
        # Xn = 96.4212
        # Yn = 100
        # Zn = 82.5188

        L = 116.0 * f(100.0*self._xyz.Y / Yn) - 16
        a = 500.0 * (f(100.0*self._xyz.X / Xn) - f(100.0*self._xyz.Y / Yn))
        b = 200.0 * (f(100.0*self._xyz.Y / Yn) - f(100.0*self._xyz.Z / Zn))

        # Return the final color
        return recordclass('CIELAB', ['L', 'a', 'b'])(L, a, b)
    
    def to_OKLAB(self):
        # Convert XYZ to LMS
        lms = CM_CIEXYZ_LMS.dot(self._xyz)

        # Apply cube root nonlinearity
        lms = np.cbrt(lms)

        # Convert LMS to Oklab
        L, a, b = CM_LMS_OKLAB.dot(lms)

        # Return the final color
        return recordclass('Oklab', ['L', 'a', 'b'])(L, a, b)