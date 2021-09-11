from sqlite_database import SQL_Database
import time

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
