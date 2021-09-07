from graphic import AquariumApp
from sqlite_database import SQL_Database

import traceback

def check_database():
    try:
        database = SQL_Database('test.db')
        print(database.get("sensors","temp_int"))
        database.close()
    except Exception:
        #traceback.print_exc()
        columns = "(id INTEGER PRIMARY KEY,temp_int FLOAT,temp_ext FLOAT,hum_ext FLOAT, date_int FLOAT, date_ext FLOAT)"
        database.create_table("sensors", columns)

#check if Database is ok!!
check_database()

#Run Graphic environment
AquariumApp().run()



