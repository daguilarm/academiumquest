from menu import MenuBar
from orm import orm_results
from tkinter import *

from table import table


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


# Application
if __name__ == "__main__":
    # Create application
    app = App()

    # Configure application
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)

    # Get the database results
    results = orm_results()

    # Generate the table
    table(app, results)

    # Events loop
    app.mainloop()
