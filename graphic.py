from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from datetime import datetime


class MainWidget(BoxLayout):
    pass


class AquariumApp(App):
    def update_time(self, nap):
        now = datetime.now()
        self.root.ids.time.text = now.strftime('%H:%M:%S')

    def on_start(self):
        Clock.schedule_interval(self.update_time, 1)




