from graphic import AquariumApp
from sqlite_database import SQL_Database
import threading
from sqlite_database import SQL_Database
import traceback

def check_database():
    try:
        database = SQL_Database('test.db')
        print(database.get("sensors_int","temp_int"))
        database.close()
    except Exception:
        #traceback.print_exc()
        columns_int = "(id INTEGER PRIMARY KEY,temp_int FLOAT, date_int FLOAT)"
        columns_ext = "(id INTEGER PRIMARY KEY,temp_ext FLOAT,hum_ext FLOAT, date_ext FLOAT)"
        database.create_table("sensors_int", columns_int)
        database.create_table("sensors_ext", columns_ext)

#check if Database is ok!!
check_database()

#THREADING SECTION
#Graphic Section

x = threading.Thread(target=AquariumApp().run(), args=(1,))
x.start()