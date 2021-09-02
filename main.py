from graphic import AquariumApp
from sqlite_database import SQL_Database
import threading

#INIT SECTION
#SQlite database Section
database = SQL_Database('test.db')
#Table TEMP_INT
database.create_table("temp_int")
database.close()


#THREADING SECTION
#Graphic Section
#AquariumApp().run()

x = threading.Thread(target=AquariumApp().run(), args=(1,))
x.start()
