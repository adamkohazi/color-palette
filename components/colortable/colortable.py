
import palette
import color_model

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, OptionProperty, ListProperty
from components.colorbox.colorbox import ColorBox

class ColorTable(BoxLayout):
    # These need to be set from outside
    palette = ObjectProperty(None)

    spinner_values = ListProperty([model.short_name for model in color_model.color_models])

    color_model_1 = StringProperty("SRGB")
    color_model_2 = StringProperty("XYZ")

    def on_palette(self, instance, value):
        if isinstance(value, palette.Palette):
            self.update()
        else:
            pass
    
    def on_color_model_1(self, instance, value):
        model_1 = next((cm for cm in color_model.color_models if cm.short_name == self.color_model_1), None)

        self.ids.cm_1_1, self.ids.cm_1_2, self.ids.cm_1_3 = model_1.component_names

        for row in self.ids.color_entries.children:
            row.color_model_1 = model_1
    
    def on_color_model_2(self, instance, value):
        model_2 = next((cm for cm in color_model.color_models if cm.short_name == self.color_model_2), None)

        self.ids.cm_2_1, self.ids.cm_2_2, self.ids.cm_2_3 = model_2.component_names

        for row in self.ids.color_entries.children:
            row.color_model_2 = model_2

    def update(self):
        # Set the correct number of rows
        while(len(self.ids.color_entries.children) < len(self.palette._colors)):
            # Create new row if needed
            index = len(self.ids.color_entries.children)
            new_row = ColorBox(
                color = self.palette._colors[index],
                color_model_1 = next((cm for cm in color_model.color_models if cm.short_name == self.color_model_1), None),
                color_model_2 = next((cm for cm in color_model.color_models if cm.short_name == self.color_model_2), None)
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