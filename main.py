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

from components.colorbox.colorbox import ColorBox
from components.colordiagram.colordiagram import ColorDiagram


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
        Window.size = (600, 800)

        # Draw UI
        self.root = Builder.load_file("main.kv")

        # Draw initial elements
        Clock.schedule_once(self.initialize)
        return self.root

    def initialize(self, dt):
        # Redraw table
        self.draw_table()

        self.root.ids.diagram1.palette = self.palette

        # Keep updating display
        Clock.schedule_interval(self.update, 1.0/10.0)
        pass

    def update(self, dt):
        # Alter color palette
        self.palette._colors[0]._xyz.X += 0.005
        self.palette._colors[0]._xyz.X %= 1.0

        # Update table
        for row in self.root.ids.palette_table.children:
            row.update()
        
        # Update graphs

    def draw_table(self, *args):
        # Remove earlier entries
        self.root.ids.palette_table.clear_widgets()

        # Set the correct number of rows
        self.root.ids.palette_table.rows = len(self.palette._colors)

        # Draw content
        for pallette_color in self.palette.colors:
            # Create new row
            self.root.ids.palette_table.add_widget(ColorBox(color = pallette_color))

    def generate(self):
        generator_type = self.root.ids.generator_type.text
        if generator_type == 'RGB random':
            self.palette.generate_RGB_random()
        elif generator_type == 'RGB cosine':
            pass
        elif generator_type == 'monochrome':
            pass
        else:
            pass

if __name__ == "__main__":
    MainApp().run()