#from w1thermsensor import W1ThermSensor, Unit
from sqlite_database import SQL_Database
import threading
import random
import time

class Ds18:

    def retrieve_temp_int():
        try:
            #sensor = W1ThermSensor()
            #temperature_in_celsius = sensor.get_temperature()
            #temperature_in_fahrenheit = sensor.get_temperature(Unit.DEGREES_F)
            #temperature_in_all_units = sensor.get_temperatures([
                #Unit.DEGREES_C,
                #Unit.DEGREES_F,
                #Unit.KELVIN])

            #print (temperature_in_all_units[0])
            temperature_in_all_units = random.randint(24,31)
            table = "sensors_int"
            coloumns = ("temp_int", "date_int")
            data = (temperature_in_all_units, time.time())
            SQL_Database.write(table,coloumns,temperature_in_all_units, data)
        except:
            print('error')
    t = threading.Timer(1800.0, retrieve_temp_int).start()


ds18 = Ds18()

ds18.retrieve_temp_int()
