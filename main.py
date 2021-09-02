from graphic import AquariumApp
from sqlite_database import SQL_Database


#AquariumApp().run()

database = SQL_Database('test.db')

database.write( "aqua", "id, temp", '1, 34' )