import config
import orm as sql
import libs.table
import tkinter
from menu import MenuBar
from tkinter import ttk


class Application(tkinter.Frame):

    def __init__(self, root):
        # Define application frame
        tkinter.Frame.__init__(self, root)

        # Define root
        self.root = root

        # Define menu
        self.menu = MenuBar(self)
        self.root.config(menu=self.menu)
        
        # Configure the root object for the Application
        self.root.title("Academium Quest - Premium version")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Set default database values
        self.db_per_page = config.database['per_page']
        self.db_page = config.database['page']
        self.db_order = config.database['order']
        self.db_direction = config.database['direction']

        # Default values
        self.table_title = 'Preguntas para EIR y OPE'

        # Columns
        self.columns = config.columns['columns']
        self.columns_total = len(self.columns)
        self.headers = config.columns['headers']
        self.width = config.columns['width']

        # Define results
        self.results = sql.questions(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
        )

        # Create the table
        self.table = ttk.Treeview(self.root, columns=self.columns, show='headings')

        # Max application width
        self.max_width = int(self.table.winfo_screenwidth())

        # Init
        self.init_gui()

    # Initialize the user interface
    def init_gui(self):
        # Define the Application Title / Label
        title_label = tkinter.Label(self.root, text=self.table_title, font=('Arial', 30), pady=30)
        title_label.grid(row=0, columnspan=self.columns_total)

        # Set column header style
        self.style.configure('Treeview', rowheight=80)
        self.style.configure('Treeview.Heading', padding=15)

        # Set the table headers, columns and sort  the columns
        libs.table.columns(self)

        # Set the table grid
        self.table.grid(row=1, column=0, columnspan=self.columns_total)


app = Application(tkinter.Tk())
app.root.mainloop()
