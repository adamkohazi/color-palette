
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

    # Static properties
    color_models = ListProperty([model.ID for model in cm.color_models])
    diagram_types = ListProperty(['3D Plot', '2D Plot'])

    color_model = ObjectProperty(cm.SRGB)
    component_names = ListProperty(cm.SRGB.component_names)

    def on_palette(self, instance, value):
        if isinstance(value, palette.Palette):
            pass
            #self.update()
    
    def set_color_model(self, ID):
        self.color_model = next((cm for cm in cm.color_models if cm.ID == ID), None)
    
    def on_color_model(self, instance, value):
        if isinstance(value, cm.ColorModel):
            self.component_names = value.component_names
            self.ids.horizontal_axis.text = self.component_names[0]
            self.ids.vertical_axis.text = self.component_names[1]
            # Recreate diagram to correctly set ranges and labels
            self.create()
    
    def update(self):
        diagram_type = self.ids.diagram_type.text

        # Validate color model and component names
        if not isinstance(self.color_model, cm.ColorModel):
            print("Invalid color model.")
            return

        try:
            for point, color in zip(self.points, self.palette._colors):
                srgb = color.get(SRGB)
                point.set_color(srgb)
                point.set_edgecolor('black')

                components = color.get(self.color_model)

                if diagram_type == '3D Plot':
                    point._offsets3d = ([components[0]], [components[1]], [components[2]])

                elif diagram_type == '2D Plot':

                    horizontal_axis = self.ids.horizontal_axis.text
                    vertical_axis = self.ids.vertical_axis.text

                    if horizontal_axis not in self.color_model.component_names or vertical_axis not in self.color_model.component_names:
                        print(f"Invalid axis names: {horizontal_axis}, {vertical_axis}")
                        continue

                    x_index = self.color_model.component_names.index(horizontal_axis)
                    y_index = self.color_model.component_names.index(vertical_axis)

                    x = components[x_index]
                    y = components[y_index]
                    point.set_offsets((x, y))
            
            self._canvas.draw()

        except Exception as e:
            print(f"Error updating plot: {e}")

    def create(self):
        # Clear area
        self.ids.diagram_area.clear_widgets()
        self.points = []

        if self.ids.diagram_type.text == 'None':
            return
        
        # Prepare chart
        self.figure = plt.figure()

        if self.ids.diagram_type.text == '3D Plot':
            # 3D scatter plot
            self.axes = self.figure.add_subplot(projection='3d')

            # Plot point by point, each with own color
            for color in self.palette._colors:
                srgb = color.get(SRGB)
                # Get color componenets to plot
                components = color.get(self.color_model)

                point = self.axes.scatter(components[0], components[1], components[2], s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
                self.points.append(point)

            # Set range
            self.axes.set_xlim(self.color_model.ranges[0])
            self.axes.set_ylim(self.color_model.ranges[1])
            #self.axes.set_zlim(self.color_model.ranges[2])

            # Set labels
            self.axes.set_xlabel(self.color_model.component_names[0])
            self.axes.set_ylabel(self.color_model.component_names[1])
            #self.axes.set_zlabel(self.color_model.component_names[2])
            
            # 3rd axis
            self.axes.tick_params(axis='z', colors='white')
        
        if self.ids.diagram_type.text == '2D Plot':
            # 2D scatter plot
            self.axes = self.figure.add_subplot()

            x_index = self.color_model.component_names.index(self.ids.horizontal_axis.text)
            y_index = self.color_model.component_names.index(self.ids.vertical_axis.text)

            # Plot point by point, each with own color
            for color in self.palette._colors:
                srgb = color.get(SRGB)
                components = color.get(self.color_model)
                x = components[x_index]
                y = components[y_index]
                point = self.axes.scatter(x, y, s=100.0, marker='o', color=srgb, edgecolor='black', linewidth=1)
                self.points.append(point)

            # Set range
            self.axes.set_xlim(self.color_model.ranges[x_index])
            self.axes.set_ylim(self.color_model.ranges[y_index])

            # Set labels
            self.axes.set_xlabel(self.color_model.component_names[x_index])
            self.axes.set_ylabel(self.color_model.component_names[y_index])
        

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
        self.ids.diagram_area.add_widget(self._canvas)