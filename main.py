from window  import Window 
from tkinter import Tk 
from statement import Statement

root        =       Tk()
database    =       Statement()
window      =       Window(root, database)

root.mainloop()