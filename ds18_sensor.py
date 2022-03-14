import os
import glob
import time
from sqlite_database import SQL_Database
import threading
from send_email import SendEmail
from settings import Aq_Settings



#these tow lines mount the device:
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
 
class DS18B20:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.base_dir = r'/sys/bus/w1/devices/28*'
        self.sensor_path = []        
        self.sensor_name = []
        self.temps = []
        self.log = []
        self.ALARM = 0
        self.ERROR = 0

    def find_sensors(self):
        self.sensor_path = glob.glob(self.base_dir)
        self.sensor_name = [path.split('/')[-1] for path in self.sensor_path]

    def strip_string(self, temp_str):
        i = temp_str.index('t=')
        if i != -1:
            t = temp_str[i+2:]
            temp_c = float(t)/1000.0
            temp_f = temp_c * (9.0/5.0) + 32.0
        return temp_c, temp_f

    def read_temp(self):
        tstamp = time.time()
        if(self.sensor_name and self.sensor_path):
            for sensor, path in zip(self.sensor_name, self.sensor_path):
            # open sensor file and read data
                with open(path + '/w1_slave','r') as f:
                    valid, temp = f.readlines()
                # check validity of data
                if 'YES' in valid:
                    self.log.append((tstamp, sensor) + self.strip_string(temp))
                    time.sleep(2)
                    datab = SQL_Database()
                    datab.open('test.db')
                    #print(self.log[0][2])
                    datab.write('sensors_int','temp_int, date_int',str(self.log[0][2])+','+str(tstamp))
                    datab.close()
            print('Temperature retrieved')
            email_alert = Aq_Settings.read_settings('User_info', 'email_alert')
            if (email_alert == "True"):
                if ((self.log[0][2] < 24 or self.log[0][2] > 30) and self.ALARM == 0):
                    SendEmail.email_temp_error(self.log[0][2],1)
                    self.ALARM = 1
                elif(self.log[0][2] > 24 or self.log[0][2] < 30):
                    self.ALARM = 0
                self.ERROR = 0
            
        else:
            datab = SQL_Database()
            datab.open('test.db')
            datab.write('sensors_int','temp_int, date_int','-1000,'+str(time.time()))
            datab.close()
            print('Internal Sensor Error!!!')
            if (self.ERROR == 0):
                SendEmail.email_error(1)
                self.ERROR = 1
                      
    
    def print_temps(self):
        #print('-'*90)
        for t, n, c, f in self.log:
            print(f'Sensor: {n}  C={c:,.3f}  F={f:,.3f}  DateTime: {t}')

    def clear_log(self):
        self.log.clear()

    def run(self):
        #print('cycle')
        self.find_sensors()
        self.read_temp()
         #self.print_temps()
        self.clear_log()
        
        t = threading.Timer(60*30, self.run).start()
