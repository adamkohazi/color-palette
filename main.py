#main.py
import palette
import color

import matplotlib.pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import *
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from components.colorbox.colorbox import ColorBox
from components.colordiagram.colordiagram import ColorDiagram
from components.paramcontrol.paramcontrol import ParamControl


class MainApp(App):

    def build(self):
        # Initialize palette
        self.palette = palette.Palette()
        # Color palette of the GUI
        self.palette.append(color.Color.from_RGB_hex("#000000"))
        self.palette.append(color.Color.from_RGB_hex("#222222"))
        self.palette.append(color.Color.from_RGB_hex("#3B3B3B"))
        self.palette.append(color.Color.from_RGB_hex("#6B6B6B"))
        self.palette.append(color.Color.from_RGB_hex("#E2E2E2"))

        # Set window size
        Window.size = (960, 600)

        # Draw UI
        self.root = Builder.load_file("main.kv")

        # Draw initial elements
        Clock.schedule_once(self.initialize)
        return self.root

    def initialize(self, dt):
        # Bind the buttons only once everything is built
        self.root.ids.randomize.generate_palette = self.palette.generate_RGB_random
        self.root.ids.cosine.generate_palette = self.palette.generate_RGB_cosine

        self.root.ids.diagram1.palette = self.palette
        self.root.ids.diagram2.palette = self.palette

        # Keep updating display
        Clock.schedule_interval(self.update, 1.0/10.0)
        pass

    def update(self, dt):
        # Set the correct number of rows
        while(len(self.root.ids.palette_table.children) < len(self.palette._colors)):
            # Create new row if needed
            index = len(self.root.ids.palette_table.children)
            new_row = ColorBox(color = self.palette._colors[index])
            self.root.ids.palette_table.add_widget(new_row)
            # Bind the remove button to remove that color from the palette
            def remove_color(instance):
                index = len(self.root.ids.palette_table.children)-self.root.ids.palette_table.children.index(instance)-1
                print("deleting index: ", index)
                self.palette.pop(index)
                self.root.ids.palette_table.remove_widget(instance)

            new_row.remove = remove_color

        # Update table
        for row, color in zip(self.root.ids.palette_table.children, reversed(self.palette._colors)):
            row.color = color
            row.update()
        
        # Update graphs
        self.root.ids.diagram1.update()
        self.root.ids.diagram2.update()

if __name__ == "__main__":
    MainApp().run()