from tkinter import Button, Entry, Label, Tk, W, Frame, Listbox, LabelFrame, END


class Window: 
    
    index_item          =       None; 

    def __init__(self, master, database): 

        self.master             =       master 
        self.database           =       database 
        self.master.title('Tkinter Word Search')
        self.master.geometry('750x600')

        self.master.grid_columnconfigure(0, weight=1)
        
        self.frame_statement            =       LabelFrame(self.master, text='Entry', width=500, height=150)
        self.frame_statement_list       =       LabelFrame(self.master, text='Statements', width=500, height=270)
        self.frame_vocalbulary          =       LabelFrame(self.master, text='Vocalbulary', width=200, height=420)
        self.frame_vectors              =       LabelFrame(self.master, text='Occurrences', width=750, height=150)

        self.label_statement            =       Label(self.frame_statement,text="Enter Statement:")
        self.label_statement.grid(row=0, column=0, sticky=W, pady=5, padx=10) 

        self.entry_statement            =       Entry(self.frame_statement, width=58)
        self.entry_statement.grid(row=1, column=0, sticky=W, pady=5, padx=10, columnspan=4) 

        self.listbox_statements         =       Listbox(self.frame_statement_list, width=59, height=10)
        self.listbox_statements.grid(row=0, column=0, sticky=W, pady=5, padx=10, columnspan=4) 

        #Bind Select 
        self.listbox_statements.bind('<<ListboxSelect>>', self.select_statement)

        self.listbox_vocalbulary        =       Listbox(self.frame_vocalbulary, width=23, height=20)
        self.listbox_vocalbulary.grid(row=0, column=0, sticky=W, pady=10, padx=5) 

        self.listbox_vectors            =       Listbox(self.frame_vectors, width=87, height=6)
        self.listbox_vectors.grid(row=0, column=0, sticky=W, pady=10, padx=5) 

        self.button_create              =       Button(self.frame_statement, text='Add', width=10, command=self.add)
        self.button_create.grid(row=2, column=0, sticky=W, pady=5, padx=10) 

        self.button_update              =       Button(self.frame_statement, text='Update', width=10, command=self.update)
        self.button_update.grid(row=2, column=3, sticky=W, pady=5, padx=10) 

        #self.button_vocalbulary         =       Button(self.frame_statement_list, text='Get Vocalbulary', width=15, command=self.generate_vocalbulary)
        #self.button_vocalbulary.grid(row=1, column=3, sticky=W, pady=5, padx=10)

        self.button_clear               =       Button(self.frame_statement_list, text='Clear List', width=15, command=self.clear)
        self.button_clear.grid(row=1, column=3, sticky=W, pady=5, padx=10)

        self.button_delete              =       Button(self.frame_statement_list, text='Remove', width=10, command=self.remove)
        self.button_delete.grid(row=1, column=0, sticky=W, pady=5, padx=10)

        self.button_delete["state"]         =       "disabled"
        self.button_update["state"]         =       "disabled"

        self.frame_statement.grid(row=0, column=0, sticky=W, pady=10, padx=10)
        self.frame_statement.grid_propagate(False)
    
        self.frame_statement_list.grid(row=1, column=0, sticky=W, pady=0, padx=10)
        self.frame_statement_list.grid_propagate(False) 
   
        self.frame_vocalbulary.grid(row=0, column=1, sticky=W, pady=0, padx=15, rowspan=2)
        self.frame_vocalbulary.grid_propagate(False)

        self.frame_vectors.grid(row=2, column=0, sticky=W, pady=0, padx=15, columnspan=2)
        self.frame_vectors.grid_propagate(False)

        self.populate_listbox_statement()


    def populate_listbox_statement(self): 

        self.listbox_statements.delete(0, END)

        count = 0

        for item in self.database.read(): 

            self.listbox_statements.insert(count, item)

            count += 1

        self.entry_statement.delete(0, END)

        self.index_item == None

        if self.listbox_statements.size() == 0: 
            self.button_clear["state"]          =       "disabled"
        else: 
            self.button_clear["state"]          =       "active"

        self.button_delete["state"]         =       "disabled"
        self.button_update["state"]         =       "disabled"

        self.generate_vocalbulary() 

    def add(self): 

        if not self.entry_statement.get().strip(): 
            return 

        statement           =           self.entry_statement.get().strip()   
        
        self.database.create({'statement' : statement})

        self.populate_listbox_statement()
        
    def update(self): 
        
        if self.index_item == None or not self.entry_statement.get().strip(): 
            return 
       
        data            =   {
                                'id'        :       self.index_item, 
                                'statement' :       self.entry_statement.get().strip()
                            }

        self.database.update(data)

        self.populate_listbox_statement()
    
    def remove(self):

        if self.index_item == None: 
            return 

        self.database.delete(self.index_item)

        self.populate_listbox_statement()

    def clear(self): 

        self.database.clear()
        self.populate_listbox_statement()

    def generate_vocalbulary(self): 
        
        vocalbulary     =           [];
        vector          =           [];

        for item in self.listbox_statements.get(0, END): 

            for word in item[1].split():
               
                if word.lower() not in vocalbulary: 
                    vocalbulary.append(word.lower())  
                 
        self.listbox_vocalbulary.delete(0, END)
        self.listbox_vectors.delete(0, END)

        index   =   0
        
        for word in vocalbulary:
            
            self.listbox_vocalbulary.insert(index, f"{index+1}.) {word}")
            index+=1


        index   =   0

        for statement in self.listbox_statements.get(0, END): 
            
            self.listbox_vectors.insert(index, self.generate_vectors(vocalbulary, statement[1]))
            index+=1

    def generate_vectors(self, vocalbulary, statement): 

        count       =       0 
        vector      =       []

        for v in vocalbulary: 
            
            count   =       0
            
            for s in statement.lower().split():
                if(v == s): 
                    count   +=  1

            vector.append(count)

        return vector 

    def select_statement(self, event): 
        
        if not self.listbox_statements.curselection(): 
            return 

        index                               =       self.listbox_statements.curselection()[0]

        self.entry_statement.delete(0, END)
        self.entry_statement.insert(END, self.listbox_statements.get(index)[1])

        self.index_item                     =       self.listbox_statements.get(index)[0]

        self.button_delete["state"]         =       "active"
        self.button_update["state"]         =       "active"

    