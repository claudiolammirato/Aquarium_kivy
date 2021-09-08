from w1thermsensor import W1ThermSensor, Unit
from sqlite import insert_item
import threading
import time

def retrieve_temp_int():
    time.sleep(3)
    sensor = W1ThermSensor()
    temperature_in_celsius = sensor.get_temperature()
    temperature_in_fahrenheit = sensor.get_temperature(Unit.DEGREES_F)
    temperature_in_all_units = sensor.get_temperatures([
        Unit.DEGREES_C,
        Unit.DEGREES_F,
        Unit.KELVIN])

    print (temperature_in_all_units[0])

    table = "SENSORS_INT"
    insert_item(999, 999,temperature_in_all_units[0], table)
    t = threading.Timer(1800.0, retrieve_temp_int).start()