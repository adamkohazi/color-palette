
import palette
import color_model

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, OptionProperty, ListProperty
from components.colorbox.colorbox import ColorBox

class ColorTable(BoxLayout):
    # These need to be set from outside
    palette = ObjectProperty(None)

    spinner_values = ListProperty([model.ID for model in color_model.color_models])

    color_model_1 = ObjectProperty(color_model.SRGB)
    color_model_2 = ObjectProperty(color_model.CIEXYZ)

    # First representation of color
    color_model_1_component_1 = StringProperty('') # First color component, e.g. "R"
    color_model_1_component_2 = StringProperty('') # Second color component, e.g. "G"
    color_model_1_component_3 = StringProperty('') # Third color component, e.g. "B"

    # Second representation of color
    color_model_2_component_1 = StringProperty('') # First color component, e.g. "H"
    color_model_2_component_2 = StringProperty('') # Second color component, e.g. "S"
    color_model_2_component_3 = StringProperty('') # Third color component, e.g. "B"

    def on_palette(self, instance, value):
        if isinstance(value, palette.Palette):
            self.update()
        else:
            pass
    
    def set_color_model_1(self, ID):
        self.color_model_1 = next((cm for cm in color_model.color_models if cm.ID == ID), None)
    
    def on_color_model_1(self, instance, value):
        if isinstance(value, color_model.ColorModel):
            self.color_model_1_component_1, self.color_model_1_component_2, self.color_model_1_component_3 = self.color_model_1.component_names

            # Update color model for every row
            for row in self.ids.color_entries.children:
                row.color_model_1 = self.color_model_1
    
    def set_color_model_2(self, ID):
        self.color_model_2 = next((cm for cm in color_model.color_models if cm.ID == ID), None)
    
    def on_color_model_2(self, instance, value):
        if isinstance(value, color_model.ColorModel):
            self.color_model_2_component_1, self.color_model_2_component_2, self.color_model_2_component_3 = self.color_model_2.component_names
            
            # Update color model for every row
            for row in self.ids.color_entries.children:
                row.color_model_2 = self.color_model_2

    def update(self):
        # Set the correct number of rows
        while(len(self.ids.color_entries.children) < len(self.palette._colors)):
            # Create new row if needed
            index = len(self.ids.color_entries.children)
            new_row = ColorBox(
                color = self.palette._colors[index],
                color_model_1 = self.color_model_1,
                color_model_2 = self.color_model_2
            )
            self.ids.color_entries.add_widget(new_row)
            # Bind the remove button to remove that color from the palette
            def remove_color(instance):
                index = len(self.ids.color_entries.children)-self.ids.color_entries.children.index(instance)-1
                print("deleting index: ", index)
                self.palette.pop(index)
                self.ids.color_entries.remove_widget(instance)

            new_row.remove = remove_color

        # Update table
        for row, color in zip(self.ids.color_entries.children, reversed(self.palette._colors)):
            row.color = color
            row.update()