from graphic import AquariumApp
from sqlite_database import SQL_Database
import threading
import traceback
from ds18_sensor import DS18B20
from dht_sensor import DHT
import time, os


def check_database():
    print('check database')
    try:
        database = SQL_Database('test.db')
        database.get("sensors_int","temp_int")
        database.get("sensors_ext","temp_ext")
        #print('in')
        database.close()
    except Exception:
        database = SQL_Database('test.db')
        traceback.print_exc()
        columns_int = "(id INTEGER PRIMARY KEY,temp_int FLOAT, date_int FLOAT)"
        columns_ext = "(id INTEGER PRIMARY KEY,temp_ext FLOAT,hum_ext FLOAT, date_ext FLOAT)"
        database.create_table("sensors_int", columns_int)
        database.create_table("sensors_ext", columns_ext)
        database.close()
        #print('error')


def main():
    
    #check if Database is ok!!
    #p0 = threading.Thread(target = check_database())
    #p0.start()
    #p0.join()
    #check_database()
    '''
    #THREADING SECTION
    #Sensor Section
    sensor_internal = DS18B20()
    #p1 = threading.Thread(target=sensor_internal.run())
    #p1.start()

    sensor_external = DHT()
    #p2 = threading.Thread(target=sensor_external.run())
    #p2.start()

'''
    

    #Graphic Section - HAS TO BE LAST!!!!
    p4 = threading.Thread(target=AquariumApp().run())
    p4.start()
    

if __name__ == "__main__":
    main()
    





