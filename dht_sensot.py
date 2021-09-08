import Adafruit_DHT
import threading
from sqlite import insert_item
 
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

def retrieve_temp_hum_ext():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        #return temperature, humidity
        table = "SENSORS_EXT"
        insert_item(temperature, humidity, 999, table)
    else:
        print("Failed to retrieve data from humidity sensor")
        #return error
    t = threading.Timer(1800.0, retrieve_temp_hum_ext).start()