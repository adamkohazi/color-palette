
import palette
import color_model as cm
from color_model import CIEXYZ, CIERGB, SRGB, SRGB255, OKLAB, HSV

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class ColorDiagram(BoxLayout):
    # These need to be set from outside
    palette = ObjectProperty(None)

    color_models = ListProperty([model.ID for model in cm.color_models])

    diagram_types = ListProperty(['3D Plot', '2D Plot'])

    color_model = ObjectProperty(cm.SRGB)
    component_names = ListProperty(cm.SRGB.component_names)

    def on_palette(self, instance, value):
        if isinstance(value, palette.Palette):
            self.update()
        else:
            pass
    
    def update(self):
        if self.diagram_type.text == 'None':
            return
        
        for point, color in zip(self.points, self.palette._colors):
            # Update point color
            srgb = color.get(SRGB)
            point.set_color(srgb)
            point.set_edgecolor('black')

            if self.diagram_type.text == 'RGB':
                # Update 3D scatter plot
                point._offsets3d = ([srgb.R], [srgb.G], [srgb.B])
        
            elif self.diagram_type.text == 'RG':
                # Update 2D scatter plot
                point.set_offsets((srgb.R, srgb.G))
            
            elif self.diagram_type.text == 'GB':
                # Update 2D scatter plot
                point.set_offsets((srgb.G, srgb.B))
            
            elif self.diagram_type.text == 'RB':
                # Update 2D scatter plot
                point.set_offsets((srgb.R, srgb.B))
        
            
            elif self.diagram_type.text == 'HSB':
                # Update 3D scatter plot
                hsb = color.get(HSB)
                point._offsets3d = ([hsb.H], [hsb.S], [hsb.B])
        
            elif self.diagram_type.text == 'HS':
                # Update 2D scatter plot
                hsb = color.get(HSB)
                point.set_offsets((hsb.H, hsb.S))
            
            elif self.diagram_type.text == 'SB':
                # Update 2D scatter plot
                hsb = color.get(HSB)
                point.set_offsets((hsb.S, hsb.B))
            
            elif self.diagram_type.text == 'HB':
                # Update 2D scatter plot
                hsb = color.get(HSB)
                point.set_offsets((hsb.H, hsb.B))

        self._canvas.draw()

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
                srgb = color.get(SRGB)
                point = self.axes.scatter(srgb.R, srgb.G, srgb.B, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
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
                srgb = color.get(SRGB)
                point = self.axes.scatter(srgb.R, srgb.G, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
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
                srgb = color.get(SRGB)
                point = self.axes.scatter(srgb.G, srgb.B, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
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
                srgb = color.get(SRGB)
                point = self.axes.scatter(srgb.R, srgb.B, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('R')
            self.axes.set_ylabel('B')
        

        if self.diagram_type.text == 'HSB':
            # 3D scatter plot
            self.axes = self.figure.add_subplot(projection='3d')

            # Plot point by point, each with own color
            for color in self.palette._colors:
                srgb = color.get(SRGB)
                hsb = color.get(HSB)
                point = self.axes.scatter(hsb.H, hsb.S, hsb.B, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))
            self.axes.set_zlim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('H')
            self.axes.set_ylabel('S')
            
            # 3rd axis
            self.axes.tick_params(axis='z', colors='white')
        
        if self.diagram_type.text == 'HS':
            # 2D scatter plot
            self.axes = self.figure.add_subplot()

            # Plot point by point, each with own color
            for color in self.palette._colors:
                srgb = color.get(SRGB)
                hsb = color.get(HSB)
                point = self.axes.scatter(hsb.H, hsb.S, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('H')
            self.axes.set_ylabel('S')
        
        if self.diagram_type.text == 'SB':
            # 2D scatter plot
            self.axes = self.figure.add_subplot()

            # Plot point by point, each with own color
            for color in self.palette._colors:
                srgb = color.get(SRGB)
                hsb = color.get(HSB)
                point = self.axes.scatter(hsb.S, hsb.B, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('S')
            self.axes.set_ylabel('B')

        if self.diagram_type.text == 'HB':
            # 2D scatter plot
            self.axes = self.figure.add_subplot()

            # Plot point by point, each with own color
            for color in self.palette._colors:
                srgb = color.get(SRGB)
                hsb = color.get(HSB)
                point = self.axes.scatter(hsb.H, hsb.B, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
                self.points.append(point)

            # Set range
            self.axes.set_xlim((-0.02, 1.02))
            self.axes.set_ylim((-0.02, 1.02))

            # Set labels
            self.axes.set_xlabel('H')
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
        self._canvas = FigureCanvasKivyAgg(self.figure)
        self.diagram_area.add_widget(self._canvas)