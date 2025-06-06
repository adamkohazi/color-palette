
import color
from color_model import CIEXYZ, CIERGB, SRGB, SRGB255, OKLAB, HSB

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, OptionProperty, StringProperty, ColorProperty


class ColorBox(BoxLayout):
    # These need to be set from outside
    color = ObjectProperty(None)
    color_model_1 = OptionProperty('sRGB', options=['RGB', 'sRGB', '24-bit sRGB', 'HSB', 'XYZ', 'CIELAB', 'OKLAB'])
    color_model_2 = OptionProperty('XYZ', options=['RGB', 'sRGB', '24-bit sRGB', 'HSB', 'XYZ', 'CIELAB', 'OKLAB'])

    # Background and hex code
    background_color = ColorProperty([1, 1, 1, 1]) # Background color
    rgb_hex = StringProperty('') # RGB hex code

    # First representation of color
    color_model_1_component_1 = StringProperty('') # First color component, e.g. "R"
    color_model_1_component_2 = StringProperty('') # Second color component, e.g. "G"
    color_model_1_component_3 = StringProperty('') # Third color component, e.g. "B"

    # Second representation of color
    color_model_2_component_1 = StringProperty('') # First color component, e.g. "H"
    color_model_2_component_2 = StringProperty('') # Second color component, e.g. "S"
    color_model_2_component_3 = StringProperty('') # Third color component, e.g. "B"

    def on_color(self, instance, value):
        if isinstance(value, color.Color):
            self.update()
        else:
            pass
    
    def update(self):
        self.background_color = (*self.color.get(SRGB), 1.0)
        self.rgb_hex = '#{:02X}{:02X}{:02X}'.format(*self.color.get(SRGB255))

        if self.color_model_1 == 'RGB': 
            color_components = self.color.get(CIERGB)
        elif self.color_model_1 == 'sRGB': 
            color_components = self.color.get(SRGB)
        elif self.color_model_1 == '24-bit sRGB': 
            color_components = self.color.get(SRGB255)
        elif self.color_model_1 == 'HSB': 
            color_components = self.color.get(HSB)
        elif self.color_model_1 == 'XYZ': 
            color_components = self.color.get(CIEXYZ)
        #elif self.color_model_1 == 'CIELAB': 
        #    color_components = self.color.to_CIELAB()
        elif self.color_model_1 == 'OKLAB': 
            color_components = self.color.get(OKLAB)

        self.color_model_1_component_1 = '{:.2f}'.format(color_components[0])
        self.color_model_1_component_2 = '{:.2f}'.format(color_components[1])
        self.color_model_1_component_3 = '{:.2f}'.format(color_components[2])

        if self.color_model_2 == 'RGB': 
            color_components = self.color.get(CIERGB)
        elif self.color_model_2 == 'sRGB': 
            color_components = self.color.get(SRGB)
        elif self.color_model_2 == '24-bit sRGB': 
            color_components = self.color.get(SRGB255)
        elif self.color_model_2 == 'HSB': 
            color_components = self.color.get(HSB)
        elif self.color_model_2 == 'XYZ': 
            color_components = self.color.get(CIEXYZ)
        #elif self.color_model_2 == 'CIELAB': 
        #    color_components = self.color.to_CIELAB()
        elif self.color_model_2 == 'OKLAB': 
            color_components = self.color.get(OKLAB)

        self.color_model_2_component_1 = '{:.2f}'.format(color_components[0])
        self.color_model_2_component_2 = '{:.2f}'.format(color_components[1])
        self.color_model_2_component_3 = '{:.2f}'.format(color_components[2])