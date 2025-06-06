
import color
import color_model

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, OptionProperty, StringProperty, ColorProperty

models = [model.short_name for model in color_model.color_models]
model1 = 'sRGB'
model2 = 'XYZ'

class ColorBox(BoxLayout):
    # These need to be set from outside
    color = ObjectProperty(None)
    color_model_1 = OptionProperty(model1, options=models)
    color_model_2 = OptionProperty(model2, options=models)

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
        self.background_color = (*self.color.get(color_model.SRGB), 1.0)
        self.rgb_hex = '#{:02X}{:02X}{:02X}'.format(*self.color.get(color_model.SRGB255))

        model = next((cm for cm in color_model.color_models if cm.short_name == self.color_model_1), None)
        color_components = self.color.get(model)

        self.color_model_1_component_1 = '{:.2f}'.format(color_components[0])
        self.color_model_1_component_2 = '{:.2f}'.format(color_components[1])
        self.color_model_1_component_3 = '{:.2f}'.format(color_components[2])

        model = next((cm for cm in color_model.color_models if cm.short_name == self.color_model_2), None)
        color_components = self.color.get(model)

        self.color_model_2_component_1 = '{:.2f}'.format(color_components[0])
        self.color_model_2_component_2 = '{:.2f}'.format(color_components[1])
        self.color_model_2_component_3 = '{:.2f}'.format(color_components[2])