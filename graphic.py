from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime
from kivy.properties import StringProperty
from sqlite_database import SQL_Database
from kivy.uix.screenmanager import ScreenManager, Screen

class MenuScreen(Screen):
    pass

class MainWidget(Screen):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.update_sensors, 1)
        Clock.schedule_interval(self.update_sensors, 60*30) 
        Clock.schedule_interval(self.update_time, 1)      
    
    def update_sensors(self, nap):
        #Data Extraction from Database
        database = SQL_Database('test.db')
        data_int = database.getLast("sensors_int", ("temp_int, temp_int, date_int"))
        data_ext = database.getLast("sensors_ext", ("temp_ext, hum_ext, date_ext"))
        if(data_int):
            self.ids.temp_int.text = str(data_int[0])+'°C'
            self.ids.date_int.text = str(datetime.fromtimestamp(data_int[1]).strftime('%I:%M %p'))
        else:
            print('internal value error')

        if(data_ext):
            self.ids.temp_ext.text = str(data_ext[0])+'°C'
            self.ids.hum_ext.text = str(data_ext[1])+'%'
            self.ids.date_ext.text = str(datetime.fromtimestamp(data_ext[2]).strftime('%I:%M %p'))
        else:
            print('external value error')

    def update_time(self, nap):
        now = datetime.now()
        self.ids.time.text = now.strftime('%H:%M:%S')
    
class AquariumApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MainWidget(name='menu'))
        sm.add_widget(MenuScreen(name='settings'))

        return sm
        




