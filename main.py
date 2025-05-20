#main.py
import palette
import color
import numpy as np
import matplotlib.pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import *
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.instructions import Canvas

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle, Rectangle, Color


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

        # Keep updating display
        Clock.schedule_interval(self.update, 1.0/10.0)
        pass

    def update(self, dt):
        self.palette._colors[0]._xyz.X += 0.001
        self.update_table()
        pass

    def draw_graph(self):
        types = (
            self.root.ids.graph1_type,
            self.root.ids.graph2_type,
            self.root.ids.graph3_type,
            self.root.ids.graph4_type
        )

        areas = (
            self.root.ids.graph1_area,
            self.root.ids.graph2_area,
            self.root.ids.graph3_area,
            self.root.ids.graph4_area
        )

        for graph_type, graph_area in zip(types, areas):
            # Remove earlier entries
            graph_area.clear_widgets()

            # Prepare data
            xs = [color.to_RGB().R for color in self.palette._colors]
            ys = [color.to_RGB().G for color in self.palette._colors]
            zs = [color.to_RGB().B for color in self.palette._colors]

            # Prepare chart
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            
            ax.scatter(xs, ys, zs, marker='o')

            ax.set_xlabel('R')
            ax.set_ylabel('G')
            ax.set_zlabel('B')

            # Draw content
            graph_area.add_widget(FigureCanvasKivyAgg(fig))

    def update_table(self):
        for index, row in enumerate(self.root.ids.palette_table.children):
            row.row_color.rgba = self.palette._colors[index].to_RGBA()

    def draw_table(self, *args):
        # Remove earlier entries
        self.root.ids.palette_table.clear_widgets()

        # Set the correct number of rows
        self.root.ids.palette_table.rows = len(self.palette._colors)

        print("drawing table with ", len(self.palette._colors), " colors.")

        # Draw content
        for index, color in enumerate(self.palette._colors):
            # Create new row
            row = BoxLayout(
                orientation = 'horizontal',
                size_hint_y = None,
                height = 30,
            )

            # Visualize color using row background
            with row.canvas.before:
                row_color = Color(*color.to_RGBA())
                row_background = Rectangle(pos=row.pos, size=row.size)

            # Tie the row and rectangle together
            row.bind(
                pos=lambda instance, value, widget=row, shape=row_background: setattr(shape, 'pos', widget.pos),
                size=lambda instance, value, widget=row, shape=row_background: setattr(shape, 'size', widget.size)
            )
            self.root.ids.palette_table.add_widget(row)

            # Remove color button
            btn = Button(
                size_hint_x = None,
                width = 30,
                text = '-',
            )
            # Actions
            btn.bind(on_press=self.draw_table) # This is executed second
            btn.bind(on_press=lambda instance, i=index: self.palette.pop(i)) # This is executed first

            row.add_widget(btn)

            # RGB values
            row.add_widget(Label(
                size_hint_x = None,
                width = 100,
                text = '#{:02X}{:02X}{:02X}'.format(*color.to_RGB255())
            ))
            # R, G, B values
            color_components = color.to_RGB()
            row.add_widget(Label(
                text = "{:.2f}".format(color_components[0])
            ))
            row.add_widget(Label(
                text = "{:.2f}".format(color_components[1])
            ))
            row.add_widget(Label(
                text = "{:.2f}".format(color_components[2])
            ))

            # X, Y, Z values
            color_components = color.to_XYZ()
            row.add_widget(Label(
                text = "{:.2f}".format(color_components[0])
            ))
            row.add_widget(Label(
                text = "{:.2f}".format(color_components[1])
            ))
            row.add_widget(Label(
                text = "{:.2f}".format(color_components[2])
            ))

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

        self.init_graph()

if __name__ == "__main__":
    MainApp().run()