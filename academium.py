from menu import MenuBar
from orm import *
from table import Table
from tkinter import *



class App(Tk):
    # Init the application
    def __init__(self):
        Tk.__init__(self)

        # Configure the application
        configure_application(self)

        # Menu bar
        menubar = MenuBar(self)
        self.config(menu=menubar)


# Configure the application
def configure_application(self):
    # Full screen
    tk_width = self.winfo_screenwidth()
    tk_height = self.winfo_screenheight()
    self.geometry('%dx%d+0+0' % (tk_width, tk_height))


if __name__ == "__main__":
    app = App()

    results = db.table('questions').get()
    Table(app, results)

    app.mainloop()
