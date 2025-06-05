
import palette

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, OptionProperty
from components.colorbox.colorbox import ColorBox

class ColorTable(BoxLayout):
    # These need to be set from outside
    palette = ObjectProperty(None)
    color_model_1 = OptionProperty('sRGB', options=['RGB', 'sRGB', '24-bit sRGB', 'HSB', 'XYZ', 'CIELAB', 'OKLAB'])
    color_model_2 = OptionProperty('XYZ', options=['RGB', 'sRGB', '24-bit sRGB', 'HSB', 'XYZ', 'CIELAB', 'OKLAB'])

    def on_palette(self, instance, value):
        if isinstance(value, palette.Palette):
            self.update()
        else:
            pass
    
    def on_color_model_1(self, instance, value):
        for row in self.ids.color_entries.children:
            row.color_model_1 = self.color_model_1
    
    def on_color_model_2(self, instance, value):
        for row in self.ids.color_entries.children:
            row.color_model_2 = self.color_model_2

    def update(self):
        # Set the correct number of rows
        while(len(self.ids.color_entries.children) < len(self.palette._colors)):
            # Create new row if needed
            index = len(self.ids.color_entries.children)
            new_row = ColorBox(color = self.palette._colors[index], color_model_1 = self.color_model_1, color_model_2 = self.color_model_2)
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