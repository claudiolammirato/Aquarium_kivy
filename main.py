from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import time


class MainWidget(BoxLayout):
    pass

class AquariumApp(App):
    def on_start(self):
        Clock.schedule_interval(self.update_label, 2)

    def update_label(self, *args):
        print(args)


AquariumApp().run()