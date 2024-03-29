import email
from kivy.config import Config
from kivy.core.window import Window

"""
#Raspberry settings
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics','show_cursor','0')
"""
'''
#Windows Settings
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')
'''
Window.size = (1024, 600)

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
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

class SettingScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingScreen, self).__init__(**kwargs)
        username_input = Aq_Settings.read_settings('User_info', 'username')
        self.ids.username_input.text = str(username_input)
        email_input = Aq_Settings.read_settings('User_info', 'email')
        self.ids.email_input.text = str(email_input)
        password_input = Aq_Settings.read_settings('User_info', 'password')
        self.ids.password_input.text = str(password_input)
        email_alert = Aq_Settings.read_settings('User_info', 'email_alert')
        if (email_alert == "True"):
            self.ids.email_alert.active = True
        else:   
            self.ids.email_alert.active = False

    def update_settings(self):
        username_input = Aq_Settings.read_settings('User_info', 'username')
        self.ids.username_input.text = str(username_input)
        email_input = Aq_Settings.read_settings('User_info', 'email')
        self.ids.email_input.text = str(email_input)
        password_input = Aq_Settings.read_settings('User_info', 'password')
        self.ids.password_input.text = str(password_input)
        email_alert = Aq_Settings.read_settings('User_info', 'email_alert')
        if (email_alert == "True"):
            self.ids.email_alert.active = True
        else:   
            self.ids.email_alert.active = False
        


    def save_settings(self):
        username = self.ids.username_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        email_alert = self.ids.email_alert.active
        #print(email_alert)
        #print(username)
        Aq_Settings.write_settings('User_info', 'username', username)
        Aq_Settings.write_settings('User_info', 'email', email)
        Aq_Settings.write_settings('User_info', 'password', password)
        Aq_Settings.write_settings('User_info', 'email_alert', str(email_alert))
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
        self.ids.int_temp.clear_widgets()
        self.ids.ext_temp.clear_widgets()
        self.ids.ext_hum.clear_widgets()
        number = self.ids.btn.text
        num= number.split()
        try:
            #print(number)
            ig_int = MatPlot()
            #print(self.ids.btn.text)
            canvas1 = ig_int.graph_internal(int(num[0])*2)
            ig_ext = MatPlot()
            #print(self.ids.btn.text)
            canvas2 = ig_ext.graph_external(int(num[0])*2)
            ig_ext_hum = MatPlot()
            #print(self.ids.btn.text)
            canvas3 = ig_ext_hum.graph_external_hum(int(num[0])*2)
        except:
            #print(number)
            ig_int = MatPlot()
            #print(self.ids.btn.text)
            canvas1 = ig_int.graph_internal(16)
            ig_ext = MatPlot()
            #print(self.ids.btn.text)
            canvas2 = ig_ext.graph_external(16)
            ig_ext_hum = MatPlot()
            #print(self.ids.btn.text)
            canvas3 = ig_ext_hum.graph_external_hum(16)
        self.ids.int_temp.add_widget(canvas1)
        self.ids.ext_temp.add_widget(canvas2)
        self.ids.ext_hum.add_widget(canvas3)

class MainWidget(Screen):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        
        Clock.schedule_once(self.update_sensors, 1)
        Clock.schedule_interval(self.update_sensors, 10) 
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_once(self.on_start)

    def on_start(self, *args):
        database = SQL_Database('test.db')
        data_int = database.getLast("sensors_int", ("temp_int, date_int"))
        self.ids.username.text = str(Aq_Settings.read_settings('User_info', 'username'))
        if(data_int[0] < 22 or data_int[0] > 30):
            self.anim1 = Animation(angle=-50, duration=2)
        elif(data_int[0] >= 22 and data_int[0] < 24):
            self.anim1 = Animation(angle=(data_int[0]-22.25)*40, duration=2)
        elif(data_int[0] >= 28 and data_int[0] < 30):
            self.anim1 = Animation(angle=(data_int[0]-29.75)*-40, duration=2)
        else:
            self.anim1 = Animation(angle=110, duration=2)
        #self.anim.repeat = True    # repeat forever
        self.anim1.start(self.ids.graph_temp_int_arrow)
        data_ext = database.getLast("sensors_ext", ("temp_ext, hum_ext, date_ext"))

        if(data_ext[0] < 14 or data_ext[0] > 35):
            self.anim2 = Animation(angle=-50, duration=2)
        elif(data_ext[0] >= 14 and data_ext[0] < 22):
            self.anim2 = Animation(angle=(data_ext[0]-16)*10, duration=2)
        else:
            self.anim2 = Animation(angle=110, duration=2)
        #self.anim.repeat = True    # repeat forever
        self.anim2.start(self.ids.graph_temp_ext_arrow)
        if(data_ext[1] < 30 or data_ext[1] > 70):
            self.anim3 = Animation(angle=-50, duration=2)
        elif(data_ext[1] >= 30 and data_ext[1] < 50):
            self.anim3 = Animation(angle=(data_ext[1]-32.5)*4, duration=2)
        elif(data_ext[1] >= 50 and data_ext[1] < 80):
            self.anim3 = Animation(angle=(data_ext[1]-76.25)*-2.6666, duration=2)
        else:
            self.anim3 = Animation(angle=110, duration=2)
        #self.anim3 = Animation(angle=(80-76.25)*-2.6666, duration=2)
        #self.anim.repeat = True    # repeat forever
        self.anim3.start(self.ids.graph_hum_ext_arrow)

           
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
            self.ids.date_ext_b.text = str(datetime.fromtimestamp(data_ext[2]).strftime('%I:%M %p'))
        else:
            print('external value error')

        self.ids.username.text = str(Aq_Settings.read_settings('User_info', 'username'))
        if(data_int[0] < 22 or data_int[0] > 30):
            self.anim1 = Animation(angle=-50, duration=2)
        elif(data_int[0] >= 22 and data_int[0] < 24):
            self.anim1 = Animation(angle=(data_int[0]-22.25)*40, duration=2)
        elif(data_int[0] >= 28 and data_int[0] < 30):
            self.anim1 = Animation(angle=(data_int[0]-29.75)*-40, duration=2)
        else:
            self.anim1 = Animation(angle=110, duration=2)
        #self.anim.repeat = True    # repeat forever
        self.anim1.start(self.ids.graph_temp_int_arrow)

        if(data_ext[0] < 14 or data_ext[0] > 35):
            self.anim2 = Animation(angle=-50, duration=2)
        elif(data_ext[0] >= 14 and data_ext[0] < 22):
            self.anim2 = Animation(angle=(data_ext[0]-16)*10, duration=2)
        else:
            self.anim2 = Animation(angle=110, duration=2)
        #self.anim.repeat = True    # repeat forever
        self.anim2.start(self.ids.graph_temp_ext_arrow)
        if(data_ext[1] < 30 or data_ext[1] > 70):
            self.anim3 = Animation(angle=-50, duration=2)
        elif(data_ext[1] >= 30 and data_ext[1] < 50):
            self.anim3 = Animation(angle=(data_ext[1]-32.5)*4, duration=2)
        elif(data_ext[1] >= 50 and data_ext[1] < 80):
            self.anim3 = Animation(angle=(data_ext[1]-76.25)*-2.6666, duration=2)
        else:
            self.anim3 = Animation(angle=110, duration=2)
        #self.anim3 = Animation(angle=(80-76.25)*-2.6666, duration=2)
        #self.anim.repeat = True    # repeat forever
        self.anim3.start(self.ids.graph_hum_ext_arrow)

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
