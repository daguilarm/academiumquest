import config
import orm as sql
import libs.table
import tkinter
from menu import MenuBar
from tkinter import ttk
from ttkbootstrap import Style


class Application(tkinter.Frame):

    def __init__(self, root):
        # Initialize the application frame
        tkinter.Frame.__init__(self, root)

        # Define the application root
        self.root = root

        # Define the application menu
        self.menu = MenuBar(self)
        self.root.config(menu=self.menu)

        # Configure the root for the Application
        self.root.title("Academium Quest - Premium version")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Style the application
        self.style = Style()
        self.style.theme_use('minty')

        # Set default database values
        self.db_per_page = config.database['per_page']
        self.db_page = config.database['page']
        self.db_order = config.database['order']
        self.db_direction = config.database['direction']

        # Default application values
        self.table_title = 'Preguntas para EIR y OPE'

        # Define results
        self.results = sql.questions(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
        )

        # Define table columns variables
        self.columns = config.columns['columns']
        self.columns_total = len(self.columns)
        self.headers = config.columns['headers']
        self.width = config.columns['width']

        # Create the table
        self.table = ttk.Treeview(self.root, columns=self.columns, show='headings')

        # Max application width
        self.max_width = int(self.table.winfo_screenwidth())

        # Initialize the application user interface
        self.__init()

    # Application GUI
    def __init(self):
        # Define the Application Title / Label
        title_label = tkinter.Label(self.root, text=self.table_title, font=('Arial', 40), pady=30)
        title_label.grid(row=0, columnspan=self.columns_total)

        # Set column header style
        self.style.configure('Treeview', rowheight=100, font=('Verdana', 12))
        self.style.configure('Treeview.Heading', padding=15, font=('Verdana', 14))

        # Set the table headers, columns and sort  the columns
        libs.table.columns(self)

        # Set the table grid
        self.table.grid(row=1, column=0, columnspan=self.columns_total)


app = Application(tkinter.Tk())
app.root.mainloop()
