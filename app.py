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

        # Initialize the application user interface
        self.__init()

    # Application GUI
    def __init(self):
        # Define the Application Title / Label
        title_label = tkinter.Label(self.root, text=self.table_title, font=('Arial', 40), pady=30)
        title_label.grid(row=0, columnspan=self.columns_total)

        # Set column header style
        self.style.configure('Treeview', rowheight=100, font=('Verdana', 12))
        self.style.configure('Treeview.Heading', padding=15, font=('Verdana', 14), relief='ridge')

        # Get the values from the database
        sql_results = sql.questions(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
        )

        # Render the table
        self.table_render(sql_results)

        # Create pagination buttons
        self.table_pagination(sql_results)

    # Render the table
    def table_render(self, sql_results):
        # Set the table headers, columns and sort  the columns
        for (i, col) in enumerate(self.columns):
            # Populate the table headings
            self.table.heading(col, text=self.headers[i], command=lambda: self.table_order(self.db_direction))

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
    def table_order(self, direction):
        # Define order
        if direction == 'ASC':
            self.db_direction = 'DESC'
        else:
            self.db_direction = 'ASC'

        # Refresh the table
        self.table_refresh(self)

    # Pagination: previus page
    def table_prev_page(self, current):
        if current <= 1:
            self.db_page = 1
        else:
            self.db_page = current - 1

        # Refresh the table
        self.table_refresh(self)

    # Pagination: next page
    def table_next_page(self, current, results):
        self.db_page = current + 1

        # Refresh the table
        if self.db_page <= results.last_page:
            self.table_refresh(self)

    def table_pagination(self, results):
        # Pagination frame
        pagination = tkinter.Frame(self.root)
        pagination.grid(row=12, columnspan=self.columns_total, padx=40, pady=40)

        # Prev button
        button_prev = tkinter.Button(pagination, text='⇦ Anterior', fg='#333333', command=lambda: self.table_prev_page(self.db_page), width=40, padx=20, pady=20, font=('Arial', 18))
        button_prev.grid(row=12, column=0, padx=10, pady=10)

        # Next button
        button_next = tkinter.Button(pagination, text='Siguiente ⇨', fg='#333333', command=lambda: self.table_next_page(self.db_page, results), width=40, padx=20, pady=20, font=('Arial', 18))
        button_next.grid(row=12, column=1, padx=10, pady=10)

    # Refresh table
    def table_refresh(self, table):
        Application(
            table.root,
            table.db_per_page,
            table.db_page,
            table.db_order,
            table.db_direction
        )


# Launch the application
app = Application(
    tkinter.Tk(),
    config.database['per_page'],
    config.database['page'],
    config.database['order'],
    config.database['direction']
)

app.root.mainloop()
