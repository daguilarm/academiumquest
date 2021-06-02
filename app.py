import config
import tkinter
from libs.table import Table
from menu import MenuBar
from ttkbootstrap import Style


class Application(tkinter.Frame):
    """
        The main application Class.
        It will manage all the application operations.
    """
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

        # Define table columns variables
        self.columns = config.columns['columns']
        self.columns_total = len(self.columns)
        self.headers = config.columns['headers']
        self.width = config.columns['width']

        # Style the application
        self.style = Style()
        self.style.theme_use('minty')

        # Max application width
        self.max_width = int(self.root.winfo_screenwidth())

        # Define the table
        self.table = []

        # Define the filters
        self.filters = []

        # Initialize the application user interface
        self.__init()

    # Application GUI
    def __init(self):
        # Set column header style
        self.style.configure('Treeview', rowheight=100, font=('Verdana', 12))
        self.style.configure('Treeview.Heading', padding=15, font=('Verdana', 14), relief='ridge')

        # Set the combobox font for all the application
        combobox_font = tkinter.font.Font(family="Verdana", size=28)
        self.root.option_add("*TCombobox*Listbox*Font", combobox_font)

        # Create the table
        self.table = Table(
            self.root,
            self.max_width,
            config.database['per_page'],
            config.database['page'],
            config.database['order'],
            config.database['direction'],
            config.database['filter'],
        )


# Launch the application
app = Application(tkinter.Tk())

# App event loop
app.root.mainloop()
