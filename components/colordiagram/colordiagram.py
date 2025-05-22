
import palette

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

import matplotlib.pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class ColorDiagram(BoxLayout):
    palette = ObjectProperty(None)

    def on_palette(self, instance, value):
        print('on_palette')
        if isinstance(value, palette.Palette):
            self.update()
        else:
            pass
    
    def update(self):
        if self.diagram_type.text == 'RGB':
            pass

    def create(self):
        # Clear area
        self.diagram_area.clear_widgets()

        if self.diagram_type.text == 'None':
            return
        
        # Prepare chart
        fig = plt.figure()

        if self.diagram_type.text == 'RGB':
            print("plotting")
            plot = fig.add_subplot(projection='3d')
        
            for color in self.palette._colors:
                rgb = color.to_RGB()
                plot.scatter(rgb.R, rgb.B, rgb.G, marker='o', color=rgb)

            # Set labels
            plot.set_xlabel('R')
            plot.set_ylabel('G')

            # Set axes white
            plot.xaxis.label.set_color('white')
            plot.yaxis.label.set_color('white')
            plot.tick_params(axis='x', colors='white')
            plot.tick_params(axis='y', colors='white')
            plot.tick_params(axis='z', colors='white')
        
            # Set dark background
            fig.patch.set_facecolor((0.23, 0.23, 0.23))
            plot.patch.set_facecolor((0.23, 0.23, 0.23))

        # Draw content
        self.diagram_area.add_widget(FigureCanvasKivyAgg(fig))