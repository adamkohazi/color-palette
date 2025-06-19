from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.graphics import RenderContext, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

class Palettediagram(BoxLayout):

    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        super(Palettediagram, self).__init__(**kwargs)

    def update_shader(self, *args):
        self.canvas['projection_mat'] = Window.render_context['projection_mat']
        self.canvas['time'] = Clock.get_boottime()
        self.canvas['resolution'] = list(map(float, self.size))
        self.canvas.ask_update()
