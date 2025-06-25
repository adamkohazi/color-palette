from components.shaderbox.shaderbox import Shaderbox

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.core.window import Window
from kivy.clock import Clock

import palette
import color_model as cm
from color_model import CIEXYZ, CIERGB, SRGB, SRGB255, OKLAB, HSV

class PaletteDiagram(BoxLayout):
    palette = ObjectProperty(None)

    # Static properties
    color_models = ListProperty([model.ID for model in cm.color_models])
    diagram_types = ListProperty(['3D Plot', '2D Plot'])

    color_model = ObjectProperty(cm.SRGB)
    component_names = ListProperty(cm.SRGB.component_names)

    def __init__(self, **kwargs):
        super(PaletteDiagram, self).__init__(**kwargs)

    def on_palette(self, instance, value):
        if isinstance(value, palette.Palette):
            self.update()
    
    def set_color_model(self, ID):
        self.color_model = next((cm for cm in cm.color_models if cm.ID == ID), None)
    
    def on_color_model(self, instance, value):
        if isinstance(value, cm.ColorModel):
            self.component_names = value.component_names
            self.ids.horizontal_axis.text = self.component_names[0]
            self.ids.vertical_axis.text = self.component_names[1]

    def update(self, *args):
        try:
            self.ids.shader.fragment_shader_body = '''
                void main (void){
                    // Output to screen
                    gl_FragColor = vec4(tex_coord0.xy, 0.0, 1.0);
                }
            '''
            self.ids.shader.vertex_shader_body = '''
                void main (void) {
                frag_color = color;
                tex_coord0 = vTexCoords0;
                gl_Position = projection_mat * modelview_mat * vec4(vPosition.xy, 0.0, 1.0);
                }
            '''
            self.ids.shader.update_shader()

            x_index = self.color_model.component_names.index(self.ids.horizontal_axis.text)
            y_index = self.color_model.component_names.index(self.ids.vertical_axis.text)

            x_min, x_max = self.color_model.ranges[x_index]
            y_min, y_max = self.color_model.ranges[y_index]

            DOT_SIZE = 20

            viewer = self.ids.viewer
            viewer.canvas.after.clear()
            with viewer.canvas.after:
                # Plot point by point, each with own color
                for color in self.palette._colors:
                    # Set color
                    Color(rgb = color.get(SRGB))

                    # Find coordinates
                    components = color.get(self.color_model)
                    x = components[x_index]
                    y = components[y_index]

                    # Transform to 0-1 range for plotting
                    x_percent = (x - x_min) / (x_max - x_min)
                    y_percent = (y - y_min) / (y_max - y_min)

                    # Align with widget position
                    x_pos = viewer.pos[0] + (viewer.size[0]-DOT_SIZE) * x_percent
                    y_pos = viewer.pos[1] + (viewer.size[1]-DOT_SIZE) * y_percent

                    # Infill
                    Ellipse(
                        pos = [x_pos, y_pos], 
                        size = [DOT_SIZE, DOT_SIZE]
                    )

                    # Outline
                    Color(rgb = (0,0,0))
                    Line(
                        width = 1,
                        ellipse = [
                            x_pos, y_pos,
                            DOT_SIZE, DOT_SIZE
                        ]
                    )

        except Exception as e:
            print(f"Error updating diagram: {e}")
