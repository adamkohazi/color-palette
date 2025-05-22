
import color

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ColorProperty


class ColorBox(BoxLayout):
    color = ObjectProperty(None)

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
        rgba = self.color.to_RGBA()
        self.background_color = rgba

        rgb = self.color.to_RGB255()
        self.rgb_hex = '#{:02X}{:02X}{:02X}'.format(*rgb)

        color_components = self.color.to_RGB()
        self.color_model_1_component_1 = '{:.2f}'.format(color_components[0])
        self.color_model_1_component_2 = '{:.2f}'.format(color_components[1])
        self.color_model_1_component_3 = '{:.2f}'.format(color_components[2])

        color_components = self.color.to_XYZ()
        self.color_model_2_component_1 = '{:.2f}'.format(color_components[0])
        self.color_model_2_component_2 = '{:.2f}'.format(color_components[1])
        self.color_model_2_component_3 = '{:.2f}'.format(color_components[2])