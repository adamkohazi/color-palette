#color.py
import numpy as np
from recordclass import recordclass
import colorsys
from dataclasses import dataclass
from typing import Tuple, Callable
from enum import Enum


AxisType = Enum('AxisType', 'distance angle')

@dataclass
class ColorModel:
    ID: str
    name: str
    component_names: Tuple[str, str, str]
    ranges: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]
    to_CIEXYZ: Callable[[Tuple[float, float, float]], Tuple[float, float, float]]
    from_CIEXYZ: Callable[[Tuple[float, float, float]], Tuple[float, float, float]]

CIEXYZ = ColorModel(
    ID = 'CIEXYZ',
    name = 'CIE XYZ',
    component_names = ('X', 'Y', 'Z'),
    ranges = ((0,1), (0,1), (0,1)),
    to_CIEXYZ = lambda xyz: xyz,
    from_CIEXYZ = lambda xyz: xyz
)

# Matrices to convert between CIE linear RGB and CIE XYZ
CM_CIERGBtoCIEXYZ = np.array([
    [0.49000, 0.31000, 0.20000],
    [0.17697, 0.81240, 0.01063],
    [0.00000, 0.01000, 0.99000]])
CM_CIEXYZtoCIERGB = np.linalg.inv(CM_CIERGBtoCIEXYZ)

# Matrices to convert between linear RGB and CIE XYZ
CM_RGBtoCIEXYZ = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041]])
CM_CIEXYZtoRGB = np.linalg.inv(CM_RGBtoCIEXYZ)

CIERGB = ColorModel(
    ID = 'CIERGB',
    name = 'CIE linear RGB',
    component_names = ('R', 'G', 'B'),
    ranges = ((0,1), (0,1), (0,1)),
    to_CIEXYZ = lambda rgb: CM_RGBtoCIEXYZ.dot(rgb),
    from_CIEXYZ = lambda xyz: tuple(min(max(0.0, component), 1.0) for component in CM_CIEXYZtoRGB.dot(xyz))
)

# Helper functions
def RGB_to_sRGB(rgb):
    return tuple(12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055 for c in rgb)

def sRGB_to_RGB(srgb):
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb)

SRGB = ColorModel(
    ID = 'sRGB',
    name = 'standard RGB',
    component_names = ('R', 'G', 'B'),
    ranges = ((0,1), (0,1), (0,1)),
    to_CIEXYZ = lambda srgb: CIERGB.to_CIEXYZ(sRGB_to_RGB(srgb)),
    from_CIEXYZ = lambda xyz: RGB_to_sRGB(CIERGB.from_CIEXYZ(xyz))
)

SRGB255 = ColorModel(
    ID = 'sRGB255',
    name = '24-bit standard RGB',
    component_names = ('R', 'G', 'B'),
    ranges = ((0,255), (0,255), (0,255)),
    to_CIEXYZ = lambda srgb255: SRGB.to_CIEXYZ(tuple(component/255 for component in srgb255)),
    from_CIEXYZ = lambda xyz: tuple(int(component*255) for component in SRGB.from_CIEXYZ(xyz))
)

# Matrix to convert from XYZ to LMS
CM_CIEXYZ_LMS = np.array([
    [0.8189330101, 0.3618667424, -0.1288597137],
    [0.0329845436, 0.9293118715, 0.0361456387],
    [0.0482003018, 0.2643662691, 0.6338517070]])
CM_LMS_CIEXYZ = np.linalg.inv(CM_CIEXYZ_LMS)

# Matrix to convert from LMS to Oklab
CM_LMS_OKLAB = np.array([
    [0.2104542553, 0.7936177850, -0.0040720468],
    [1.9779984951, -2.4285922050, 0.4505937099],
    [0.0259040371, 0.7827717662, -0.8086757660]])
CM_OKLAB_LMS = np.linalg.inv(CM_LMS_OKLAB)

def OKLAB_to_XYZ(lab):
    # Convert Oklab to LMS
    lms = CM_OKLAB_LMS.dot(lab)
    # Apply cube nonlinearity
    lms = np.power(lms, 3)
    # Convert XYZ to LMS
    x, y, z = CM_LMS_CIEXYZ.dot(lms)
    return (x, y, z)

def XYZ_to_OKLAB(xyz):
    # Convert XYZ to LMS
    lms = CM_CIEXYZ_LMS.dot(xyz)
    # Apply cube root nonlinearity
    lms = np.cbrt(lms)
    # Convert LMS to Oklab
    L, a, b = CM_LMS_OKLAB.dot(lms)
    # Return the final color
    return (L, a, b)

OKLAB = ColorModel(
    ID = 'Oklab',
    name = 'Oklab',
    component_names = ('L', 'a', 'b'),
    ranges = ((0,1), (-0.5,0.5), (-0.5,0.5)),
    to_CIEXYZ = OKLAB_to_XYZ,
    from_CIEXYZ = XYZ_to_OKLAB
)

HSV = ColorModel(
    ID = 'HSV',
    name = 'HSV in sRGB',
    component_names = ('H', 'S', 'V'),
    ranges = ((0,1), (0,1), (0,1)),
    to_CIEXYZ = lambda hsb: SRGB.to_CIEXYZ(colorsys.hsv_to_rgb(*hsb)),
    from_CIEXYZ = lambda xyz: colorsys.rgb_to_hsv(*SRGB.from_CIEXYZ(xyz))
)

RYB = ColorModel(
    ID='RYB',
    name='Red-Yellow-Blue',
    component_names=('R', 'Y', 'B'),
    ranges=((0, 1), (0, 1), (0, 1)),
    to_CIEXYZ=lambda ryb: np.dot([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ], ryb),
    from_CIEXYZ=lambda xyz: tuple(min(max(0.0, c), 1.0) for c in np.dot([
        [ 3.2404542, -1.5371385, -0.4985314],
        [-0.9692660,  1.8760108,  0.0415560],
        [ 0.0556434, -0.2040259,  1.0572252]
    ], xyz))
)

# CIE LAB
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

color_models = [CIEXYZ, CIERGB, SRGB, SRGB255, OKLAB, HSV]