from kivy.config import Config
'''
#Raspberry settings
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics','show_cursor','0')
'''

#Windows Settings
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')



#show keyboard on text input and hide mouse
Config.set('kivy', 'keyboard_mode', 'systemanddock')


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime
from sqlite_database import SQL_Database
from kivy.uix.screenmanager import ScreenManager, Screen
from plot_graph import MatPlot
from settings import Aq_Settings

class SettingScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingScreen, self).__init__(**kwargs)
        username_input = Aq_Settings.read_settings('User_info', 'username')
        self.ids.username_input.text = str(username_input)
        email_input = Aq_Settings.read_settings('User_info', 'email')
        self.ids.email_input.text = str(email_input)
        password_input = Aq_Settings.read_settings('User_info', 'password')
        self.ids.password_input.text = str(password_input)

    def update_settings(self):
        username_input = Aq_Settings.read_settings('User_info', 'username')
        self.ids.username_input.text = str(username_input)
        email_input = Aq_Settings.read_settings('User_info', 'email')
        self.ids.email_input.text = str(email_input)
        password_input = Aq_Settings.read_settings('User_info', 'password')
        self.ids.password_input.text = str(password_input)


    def save_settings(self):
        username = self.ids.username_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        #print(username)
        Aq_Settings.write_settings('User_info', 'username', username)
        Aq_Settings.write_settings('User_info', 'email', email)
        Aq_Settings.write_settings('User_info', 'password', password)
        #print("save")

class Settings_Sensors(Screen):
    pass

class GraphScreen(Screen):
    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation ='vertical')
        self.add_widget(layout)
        self.update_graph()
    
    def update_graph(self):
        self.ids.box.clear_widgets()
        number = self.ids.btn.text
        num= number.split()
        try:
            #print(number)
            ig = MatPlot()
            #print(self.ids.btn.text)
            canvas = ig.graph_internal(int(num[1]))
        except:
            #print(number)
            ig = MatPlot()
            #print(self.ids.btn.text)
            canvas = ig.graph_internal(10)
        self.ids.box.add_widget(canvas)

class MainWidget(Screen):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        
        Clock.schedule_once(self.update_sensors, 1)
        Clock.schedule_interval(self.update_sensors, 10) 
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_once(self.on_start)

    def on_start(self, *args):
        self.ids.username.text = str(Aq_Settings.read_settings('User_info', 'username'))
           
    def update_sensors(self, nap):
        #Data Extraction from Database
        database = SQL_Database('test.db')
        data_int = database.getLast("sensors_int", ("temp_int, date_int"))
        data_ext = database.getLast("sensors_ext", ("temp_ext, hum_ext, date_ext"))
        #print(data_int)
        #print(data_ext)
        if(data_int):
            if(data_int[0]==-1000):
                self.ids.temp_int.text = str('SENSOR ERROR')
            else:
                self.ids.temp_int.text = str(data_int[0])[0:4]+'°C'
            self.ids.date_int.text = str(datetime.fromtimestamp(data_int[1]).strftime('%I:%M %p'))
        else:
            print('internal value error')

        if(data_ext):
            if(data_ext[0]==-1000):
                self.ids.temp_ext.text = ' SENSOR ERROR'
                self.ids.hum_ext.text = ' SENSOR ERROR'
            else:
                self.ids.temp_ext.text = str(data_ext[0])[0:4]+'°C'
                self.ids.hum_ext.text = str(data_ext[1])[0:4]+'%'
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
        sm.add_widget(SettingScreen(name='settings'))
        sm.add_widget(GraphScreen(name='graphs'))
        sm.add_widget(Settings_Sensors(name='settings_sensors'))

        return sm
