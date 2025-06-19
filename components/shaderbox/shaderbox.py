from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.graphics import RenderContext, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

fragment_shader_header = '''
    #ifdef GL_ES
        precision highp float;
    #endif

    /* Outputs from the vertex shader */
    varying vec4 frag_color;
    varying vec2 tex_coord0;

    /* uniform texture samplers */
    uniform sampler2D texture0;

    /* custom one */
    uniform vec2 resolution;
    uniform float time;
'''
vertex_shader_header = '''
    #ifdef GL_ES
        precision highp float;
    #endif

    /* Outputs to the fragment shader */
    varying vec4 frag_color;
    varying vec2 tex_coord0;

    /* vertex attributes */
    attribute vec2 vPosition;
    attribute vec2 vTexCoords0;

    /* uniform variables */
    uniform mat4 modelview_mat;
    uniform mat4 projection_mat;
    uniform vec4 color;
'''

class Shaderbox(BoxLayout):
    fragment_shader_body = StringProperty(None)
    vertex_shader_body = StringProperty(None)

    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        super(Shaderbox, self).__init__(**kwargs)

    def update_shader(self, *args):
        self.canvas['projection_mat'] = Window.render_context['projection_mat']
        self.canvas['time'] = Clock.get_boottime()
        self.canvas['resolution'] = list(map(float, self.size))
        self.canvas.ask_update()

    def on_fragment_shader_body(self, instance, value):
        self.canvas.shader.fs = fragment_shader_header + value

    def on_vertex_shader_body(self, instance, value):
        self.canvas.shader.vs = vertex_shader_header + value