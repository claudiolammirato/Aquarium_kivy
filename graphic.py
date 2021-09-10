from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime
from kivy.properties import StringProperty
from sqlite_database import SQL_Database
from kivy.uix.pagelayout import PageLayout

class PageLayout(PageLayout):
    pass

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.update_sensors, 1)
        Clock.schedule_interval(self.update_sensors, 60*30) 
        Clock.schedule_interval(self.update_time, 1)      
    
    def update_sensors(self, nap):
        #Data Extraction from Database
        database = SQL_Database('test.db')
        data = database.getLast("sensors", ("temp_int, temp_ext, hum_ext, date_int, date_ext"))
        self.ids.temp_int.text = str(data[0])+'°C'
        self.ids.temp_ext.text = str(data[1])+'°C'
        self.ids.hum_ext.text = str(data[2])+'%'
        self.ids.date_int.text = str(datetime.fromtimestamp(data[3]).strftime('%I:%M %p'))
        self.ids.date_ext.text = str(datetime.fromtimestamp(data[4]).strftime('%I:%M %p'))

    def update_time(self, nap):
        now = datetime.now()
        self.ids.time.text = now.strftime('%H:%M:%S')
    
class AquariumApp(App):
    pass
        




