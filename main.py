#main.py
import palette
import color
from color_model import CIERGB

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import *
from kivy.clock import Clock
from kivy.core.window import Window

# Custom widgets
from components.colorbox.colorbox import ColorBox
from components.colortable.colortable import ColorTable
from components.colordiagram.colordiagram import ColorDiagram
from components.paramcontrol.paramcontrol import ParamControl


class MainApp(App):

    def build(self):
        # Initialize palette
        self.palette = palette.Palette()
        # Color palette of the GUI
        for hex in ["#000000", "#222222", "#3B3B3B", "#6B6B6B", "#E2E2E2"]:
            c = color.Color()
            hex = hex[-6:]
            rgb = tuple(int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4))
            c.set(CIERGB, rgb)
            self.palette.append(c)

        # Set window size
        Window.size = (960, 620)

        # Draw UI
        self.root = Builder.load_file("main.kv")

        # Draw initial elements
        Clock.schedule_once(self.initialize)
        return self.root

    def initialize(self, dt):
        # Bind the buttons only once everything is built
        self.root.ids.randomize.generate_palette = self.palette.generate_sRGB_random
        self.root.ids.cosine.generate_palette = self.palette.generate_sRGB_cosine

        # Set the working palette for the UI elemenets
        self.root.ids.color_entry_table.palette = self.palette
        self.root.ids.diagram1.palette = self.palette
        self.root.ids.diagram2.palette = self.palette

        # Keep updating display
        Clock.schedule_interval(self.update, 1.0/10.0)
        pass

    def update(self, dt):
        self.root.ids.color_entry_table.update()
        
        # Update graphs
        self.root.ids.diagram1.update()
        self.root.ids.diagram2.update()

if __name__ == "__main__":
    MainApp().run()