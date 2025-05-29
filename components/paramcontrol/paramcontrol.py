
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ColorProperty


class ParamControl(BoxLayout):
    name = StringProperty('')
    callback = ObjectProperty(None)

    min = NumericProperty(0.0)
    max = NumericProperty(1.0)
    step = NumericProperty(0.01)

    value = NumericProperty(0.0)

    def on_slider_value(self, instance, value):
        self.value = value
        self.ids.text_input.text = f"{value:.2f}"
        if callable(self.callback):
                self.callback()

    def on_text_input(self, instance, value):
        try:
            self.value = min(max(self.min, float(value)), self.max)
            if callable(self.callback):
                self.callback()
        except:
            pass