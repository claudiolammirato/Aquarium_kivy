from os import name
import sqlite3
import mysql.connector as mysql
from settings import Aq_Settings


class SyncDatabase:
    def __init__(self) -> None:
        self.con_sqlite = sqlite3.connect("test.db")
        self.con_mysql = mysql.connect(
        host=Aq_Settings.read_settings('MySql', 'server'),
        user=Aq_Settings.read_settings('MySql', 'username'),
        password=Aq_Settings.read_settings('MySql', 'password'),
        database=Aq_Settings.read_settings('MySql', 'databasename')
        )
        self.cur = self.con_sqlite.cursor()
        self.cursor = self.con_mysql.cursor(buffered=True)
        self.database_structure = []
        self.query = ''


    def database_sync(self):
        rowsline = self.read_database()
        new_name_query = ''    
        item_row=''
        update_name=''
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        for table in tables:
            #print(table[0])
            coloumns = self.cur.execute("PRAGMA table_info({0})".format(table[0]))
            for coloumn in coloumns:
                self.database_structure.append([table[0],coloumn[1], coloumn[2]])
            
            self.query = "CREATE TABLE IF NOT EXISTS "+table[0]+" ("
            for data in self.database_structure:
                self.query += data[1]
                self.query += ' '
                self.query += data[2]
                self.query += ', '

                #self.table_coloumn.append(data[1])
                #self.table_type.append(data[2])
            self.query = self.query[:len(self.query)-2]
            self.query += ', UNIQUE ({0}));'.format(self.database_structure[0][1])
            #print(self.query)
            
            self.cursor.execute(self.query)
            self.database_structure.clear()
            self.query = ''
           
                            

            query1 = "SELECT * from {0};".format(table[0])
            self.cur.execute(query1)
            # fetch data
            rows = self.cur.fetchall()
            names = list(map(lambda x: x[0], self.cur.description))
            for name_query in names:
                new_name_query += "`"
                new_name_query += name_query
                new_name_query += "`"
                new_name_query += ","

            new_name_query = new_name_query[:len(new_name_query)-1]

            for row in rows[rowsline:]:
                for item in row:
                    #print (item)
                    item = str(item)
                    item_row += "'"
                    item_row += item
                    item_row +="'"
                    item_row +=","
                    #print(item_row)
                item_row = item_row[:len(item_row)-1]
                i=0
                for name in names:
                    update_name += name
                    update_name +="="
                    update_name +=str(row[i])
                    update_name +=","
                    i += 1
                update_name = update_name[:len(update_name)-1]



                
                #print(row[0])
                #string_row = row.replace(" ","'")
                query = 'INSERT INTO `{0}` ({1}) VALUES ({2}) ON DUPLICATE KEY UPDATE {3};'.format(table[0], new_name_query, item_row,update_name)
                #print(query)
                item_row= ''
                update_name=''
                #print (names[1])
                self.cursor.execute(query)
                self.con_mysql.commit()
            new_name_query=''
            
    def read_database(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        rows = []
        tavola = []

        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        for table in tables:
            #print(table[0])
            coloumns = self.cur.execute("PRAGMA table_info({0})".format(table[0]))
            for coloumn in coloumns:
                self.database_structure.append([table[0],coloumn[1], coloumn[2]])

            self.query = "CREATE TABLE IF NOT EXISTS "+table[0]+" ("
            for data in self.database_structure:
                self.query += data[1]
                self.query += ' '
                self.query += data[2]
                self.query += ', '

                #self.table_coloumn.append(data[1])
                #self.table_type.append(data[2])
            self.query = self.query[:len(self.query)-2]
            self.query += ', UNIQUE ({0}));'.format(self.database_structure[0][1])
            #print(self.query)
            
            self.cursor.execute(self.query)
            self.database_structure.clear()
            self.query = ''
        
        for table in tables:
            self.cursor.execute("SELECT * FROM {0};".format(table[0]))
            
            for row in self.cursor:
                #print(row)
                rows.append(row)
            #print(rows[len(rows)-1][0])
                try:
                    tavola.append(rows[len(rows)-1][0])
                    #print(min(tavola))
                    return min(tavola) 
                except:
                    tavola.append(rows[0][0])
                    #print(tavola)
                    return tavola
            
            
                
    def create_table_mysql(self):
        self.cursor.execute("CREATE TABLE sensors_int (id INTEGER AUTO_INCREMENT PRIMARY KEY, temp_int FLOAT, date_int FLOAT)")    
        self.cursor.execute("INSERT INTO sensors_int (temp_int, date_int) VALUES (25, 0)")
        self.cursor.execute("CREATE TABLE sensors_ext (id INTEGER AUTO_INCREMENT PRIMARY KEY, temp_ext FLOAT, hum_ext FLOAT, date_ext FLOAT)")    
        self.cursor.execute("INSERT INTO sensors_ext(temp_ext, hum_ext, date_ext) VALUES (25, 50, 0)")
        self.con_mysql.commit()

data = SyncDatabase()

data.database_sync()
#data.read_database()
#data.create_table_mysql()