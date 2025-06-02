
import palette

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class ColorDiagram(BoxLayout):
    palette = ObjectProperty(None)

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
            rgb = color.to_RGB()
            point.set_color(rgb)
            point.set_edgecolor('black')

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
        
            
            elif self.diagram_type.text == 'HSB':
                # Update 3D scatter plot
                hsb = color.to_HSB()
                point._offsets3d = ([hsb.H], [hsb.S], [hsb.B])
        
            elif self.diagram_type.text == 'HS':
                # Update 2D scatter plot
                hsb = color.to_HSB()
                point.set_offsets((hsb.H, hsb.S))
            
            elif self.diagram_type.text == 'SB':
                # Update 2D scatter plot
                hsb = color.to_HSB()
                point.set_offsets((hsb.S, hsb.B))
            
            elif self.diagram_type.text == 'HB':
                # Update 2D scatter plot
                hsb = color.to_HSB()
                point.set_offsets((hsb.H, hsb.B))

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
                point = self.axes.scatter(rgb.R, rgb.G, rgb.B, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
                point = self.axes.scatter(rgb.R, rgb.G, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
                point = self.axes.scatter(rgb.G, rgb.B, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
                point = self.axes.scatter(rgb.R, rgb.B, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
                rgb = color.to_RGB()
                hsb = color.to_HSB()
                point = self.axes.scatter(hsb.H, hsb.S, hsb.B, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
                rgb = color.to_RGB()
                hsb = color.to_HSB()
                point = self.axes.scatter(hsb.H, hsb.S, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
                rgb = color.to_RGB()
                hsb = color.to_HSB()
                point = self.axes.scatter(hsb.S, hsb.B, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
                rgb = color.to_RGB()
                hsb = color.to_HSB()
                point = self.axes.scatter(hsb.H, hsb.B, s=100.0, marker='o', color=rgb, edgecolor='black', linewidth=1)
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
        self.diagram_area.add_widget(FigureCanvasKivyAgg(self.figure))