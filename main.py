from graphic import AquariumApp
from sqlite_database import SQL_Database

#Graphic Section
#AquariumApp().run()


#SQlite database Section
database = SQL_Database('test.db')

database.create_table("temp_int")
database.close()
