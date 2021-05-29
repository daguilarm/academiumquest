import config
import orm as sql
import tkinter

from libs import static
from menu import MenuBar
from tkinter import ttk
from ttkbootstrap import Style


class Application(tkinter.Frame):
    def __init__(self, root, db_per_page, db_current_page, db_order_by, db_direction):
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
        self.db_per_page = db_per_page
        self.db_page = db_current_page
        self.db_order = db_order_by
        self.db_direction = db_direction

        # Default application values
        self.table_title = 'Preguntas para EIR y OPE'

        # Define table columns variables
        self.columns = config.columns['columns']
        self.columns_total = len(self.columns)
        self.headers = config.columns['headers']
        self.width = config.columns['width']

        # Create the table
        self.table = ttk.Treeview(self.root, columns=self.columns, show='headings')

        # Max application width
        self.max_width = int(self.table.winfo_screenwidth())

        # Create pagination buttons
        b1 = tkinter.Button(self.root, text='Next >', fg='black',
                            command=lambda: Application(self.root,
                                                        config.database['per_page'],
                                                        (self.db_page + 1),
                                                        config.database['order'],
                                                        config.database['direction']
                                                        ))
        b1.grid(row=12, column=1)

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

        # Get the values from the database
        sql_results = sql.questions(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
        )

        # Render the table
        self.render_table(sql_results)

    def render_table(self, sql_results):
        # Set the table headers, columns and sort  the columns
        for (i, col) in enumerate(self.columns):
            # Populate the table headings
            self.table.heading(col, text=self.headers[i], command=lambda: self.order_table(self.db_direction))

            # Define the column width
            column_width_ = static.column_width(self.max_width, self.width[i])

            # Config the columns
            self.table.column(col, width=column_width_, anchor='center')

        # Insert the rows
        for result in sql_results:
            # Populate the list with values
            list_of_values = static.table_cell_value(self.width, self.max_width, self.columns, result)

            self.table.insert("", "end", values=list_of_values)

        # Set the table grid
        self.table.grid(row=1, column=0, columnspan=self.columns_total)

    # Order table
    def order_table(self, direction):
        # Define order
        if direction == 'ASC':
            self.db_direction = 'DESC'
        else:
            self.db_direction = 'ASC'

        # Re-built the table
        Application(self.root, self.db_per_page, self.db_page, self.db_order, self.db_direction)


# Launch the application
app = Application(
    tkinter.Tk(),
    config.database['per_page'],
    config.database['page'],
    config.database['order'],
    config.database['direction']
)
app.root.mainloop()
