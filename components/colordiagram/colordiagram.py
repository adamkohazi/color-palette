
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
        if self.diagram_type.text == 'None':
            return
        
        for point, color in zip(self.points, self.palette.colors):
            # Update point color
            rgb = color.to_RGB()
            point.set_color(rgb)

            if self.diagram_type.text == 'RGB':
                # Update 3D scatter plot
                point._offsets3d = ([rgb.R], [rgb.G], [rgb.B])
        
            elif self.diagram_type.text == 'RG':
                # Update 2D scatter plot
                point.set_offsets((rgb.R, rgb.G))
            
            elif self.diagram_type.text == 'GB':
                # Update 2D scatter plot
                point.set_offsets((rgb.G, rgb.B))
            
            elif self.diagram_type.text == 'RB':
                # Update 2D scatter plot
                point.set_offsets((rgb.R, rgb.B))

        plt.draw()

    def create(self):
        # Clear area
        self.diagram_area.clear_widgets()
        self.points = []

        if self.diagram_type.text == 'None':
            return
        
        # Prepare chart
        self.figure = plt.figure()

        if self.diagram_type.text == 'RGB':
            # 3D scatter plot
            self.axes = self.figure.add_subplot(projection='3d')

            # Plot point by point, each with own color
            for color in self.palette._colors:
                rgb = color.to_RGB()
                point = self.axes.scatter(rgb.R, rgb.G, rgb.B, s=50.0, marker='o', color=rgb)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))
            self.axes.set_zlim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('R')
            self.axes.set_ylabel('G')
            
            # 3rd axis
            self.axes.tick_params(axis='z', colors='white')
        
        if self.diagram_type.text == 'RG':
            # 2D scatter plot
            self.axes = self.figure.add_subplot()

            # Plot point by point, each with own color
            for color in self.palette._colors:
                rgb = color.to_RGB()
                point = self.axes.scatter(rgb.R, rgb.G, s=50.0, marker='o', color=rgb)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('R')
            self.axes.set_ylabel('G')
        
        if self.diagram_type.text == 'GB':
            # 2D scatter plot
            self.axes = self.figure.add_subplot()

            # Plot point by point, each with own color
            for color in self.palette._colors:
                rgb = color.to_RGB()
                point = self.axes.scatter(rgb.G, rgb.B, s=50.0, marker='o', color=rgb)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('G')
            self.axes.set_ylabel('B')

        if self.diagram_type.text == 'RB':
            # 2D scatter plot
            self.axes = self.figure.add_subplot()

            # Plot point by point, each with own color
            for color in self.palette._colors:
                rgb = color.to_RGB()
                point = self.axes.scatter(rgb.R, rgb.B, s=50.0, marker='o', color=rgb)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('R')
            self.axes.set_ylabel('B')

        # Set color (white)
        self.axes.xaxis.label.set_color('white')
        self.axes.yaxis.label.set_color('white')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
    
        # Set background (dark)
        self.figure.patch.set_facecolor((0.23, 0.23, 0.23))
        self.axes.patch.set_facecolor((0.23, 0.23, 0.23))

        # Draw content
        self.diagram_area.add_widget(FigureCanvasKivyAgg(self.figure))