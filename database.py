import sqlite3 

class Database: 

    Database        =       'statement.db' 

    def __init__(self): 
        self.connection     =       sqlite3.connect(self.Database)
        self.cursor         =       self.connection.cursor()        

    def __del__(self): 
        self.connection.close()