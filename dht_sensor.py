from sqlite_database import SQL_Database
import time
from send_email import SendEmail
from settings import Aq_Settings



class DHT:
    def __init__(self):
        self.ERROR = 0
        self.ALARM = 0
    def run(self):
        
        try:
            import Adafruit_DHT
            import threading
            
            DHT_SENSOR = Adafruit_DHT.DHT22
            DHT_PIN = 17
                                             
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
                #return temperature, humidity
                datab = SQL_Database()
                datab.open('test.db')
                datab.write('sensors_ext','temp_ext,hum_ext, date_ext',str(temperature)+','+str(humidity)+','+ str(time.time()))
                datab.close()
            else:
                print("Failed to retrieve data from humidity sensor")
                #return error
            email_alert = Aq_Settings.read_settings('User_info', 'email_alert')
            if (email_alert == "True"):
                if ((temperature < 15 or temperature > 30) and self.ALARM == 0):
                    SendEmail.email_temp_error(temperature,0)
                    self.ALARM = 1
                elif(temperature > 15 or temperature < 30):
                    self.ALARM = 0
                self.ERROR = 0
            t = threading.Timer(60*30, self.run).start()
        except:
            import threading
            datab = SQL_Database()
            datab.open('test.db')
            datab.write('sensors_ext','temp_ext,hum_ext, date_ext','-1000, -1000,'+ str(time.time()))
            datab.close()
            print('External Sensor Error!!!')
            email_alert = Aq_Settings.read_settings('User_info', 'email_alert')
            if (email_alert == "True"):
                if (self.ERROR == 0):
                    SendEmail.email_error(0)
                    self.ERROR = 1
            
            t = threading.Timer(60, self.run).start()

