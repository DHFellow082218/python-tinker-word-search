from database import Database 

class Statement(Database): 

    def __init__(self):
        
        Database.__init__(self)
        self.cursor.execute("CREATE TABLE IF NOT EXISTS statements (id INTEGER PRIMARY KEY, statement TEXT)")
        self.connection.commit() 

    def create(self, data):
        
        self.cursor.execute("INSERT INTO statements VALUES (NULL, ?)", (data['statement'],))
        self.connection.commit()
        
        return self.fetch(self.cursor.lastrowid)
        
    def read(self):
       
        self.cursor.execute("SELECT * FROM statements")
        rows = self.cursor.fetchall() 
        
        return rows 

    def update(self, data):
       
        self.cursor.execute("Update statements SET statement=? WHERE id=?", (data['statement'], data['id'], )) 
        self.connection.commit()
        
        return self.fetch(data['id'])

    def delete(self, id):  
        
        self.cursor.execute("DELETE FROM statements WHERE id=?", [id,]) 
        self.connection.commit()

    def fetch(self, id): 
        
        self.cursor.execute("SELECT * FROM statements WHERE id=?", (id,)) 

        return self.cursor.fetchone() 
        
    def clear(self): 
      
        self.cursor.execute("DELETE FROM statements") 
        self.connection.commit()
        