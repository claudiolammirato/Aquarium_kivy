import sqlite3

class SQL_Database:

    def __init__(self, name=None):
        
        self.conn = None
        self.cursor = None

        if name:
            self.open(name)

    def open(self,name):
        
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")


    
    def close(self):
        
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def get(self,table,columns,limit=None):

        query = "SELECT {0} from {1};".format(columns,table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows)-limit if limit else 0:]


    def getLast(self,table,columns):
        
        return self.get(table,columns,limit=1)[0]

    
    def write(self,table,columns,data):
       
        query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table,columns,data)
        self.cursor.execute(query)

    def create_table(self,tablename):

        query = "CREATE TABLE IF NOT EXISTS {0} (id integer PRIMARY KEY, temp integer);".format(tablename)
        self.cursor.execute(query)

