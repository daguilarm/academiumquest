import config
import orm as sql
import tkinter

from libs import static
from menu import MenuBar
from tkinter import ttk
from ttkbootstrap import Style


class Application(tkinter.Frame):
    def __init__(self, root, db_per_page, db_current_page, db_order_by, db_direction, db_filter=None):
        # Initialize the application frame
        tkinter.Frame.__init__(self, root)

        # Define the application root
        if db_filter is None:
            db_filter = {}
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
        self.db_filter = db_filter

        # Default application values
        self.table_title = 'Preguntas para EIR y OPE'

        # Define table columns variables
        self.columns = config.columns['columns']
        self.columns_total = len(self.columns)
        self.headers = config.columns['headers']
        self.width = config.columns['width']

        # Create the table
        self.table = ttk.Treeview(self.root, columns=self.columns, show='headings')

        # Create pagination
        self.pagination = tkinter.Frame(self.root)
        self.pagination.grid(row=12, columnspan=self.columns_total, padx=40, pady=20)

        # Max application width
        self.max_width = int(self.table.winfo_screenwidth())

        # Initialize the application user interface
        self.__init()

    # Application GUI
    def __init(self):
        # Define the Application Title / Label
        title_label = tkinter.Label(self.root, text=self.table_title, font=('Verdana', 40), pady=20)
        title_label.grid(row=0, column=0, columnspan=self.columns_total, sticky='w', padx=20)

        # Set column header style
        self.style.configure('Treeview', rowheight=100, font=('Verdana', 12))
        self.style.configure('Treeview.Heading', padding=15, font=('Verdana', 14), relief='ridge')

        # Set the combobox font
        combobox_font = tkinter.font.Font(family="Verdana", size=28)
        self.root.option_add("*TCombobox*Listbox*Font", combobox_font)

        # Get the values from the database
        sql_results = sql.questions(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
            self.db_filter,
        )

        # Add the filters
        self.table_filter()

        # Render the table
        self.table_render(sql_results)

        # Create pagination buttons
        self.table_pagination(sql_results)

    # Render the table
    def table_render(self, sql_results):
        # Set the table headers, columns and sort  the columns
        for (i, col) in enumerate(self.columns):
            # Populate the table headings
            # _col for avoid vars by reference in python 3
            self.table.heading(col, text=self.headers[i],
                               command=lambda _col=col: self.table_order(_col, self.db_direction))

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
    def table_order(self, order_by, direction):
        # Define order
        if direction == 'ASC':
            self.db_direction = 'DESC'
        else:
            self.db_direction = 'ASC'

        # Define column to order by...
        self.db_order = order_by

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
        # Pagination label
        label_title = 'Mostrando página {} de {} páginas, de un total de {} resultados'.format(results.current_page, results.last_page, results.total)
        self.pagination.label = tkinter.Label(self.pagination, text=label_title, font=('Verdana', 16), fg="#999999")
        self.pagination.label.grid(row=11, column=0, columnspan=self.columns_total, padx=60, pady=(0, 15))

        # Button config
        b_config = {
            'fg': '#333333',
            'font': ('Verdana', 18),
            'width': 40,
            'padx': 20,
            'pady': 20,
        }

        # Prev button
        button_prev = tkinter.Button(self.pagination, b_config, text='⇦ Anterior',
                                     command=lambda: self.table_prev_page(self.db_page), foreground="#666666")
        button_prev.grid(row=12, column=0, padx=10)

        # Next button
        button_next = tkinter.Button(self.pagination, b_config, text='Siguiente ⇨',
                                     command=lambda: self.table_next_page(self.db_page, results), foreground="#666666")
        button_next.grid(row=12, column=1, padx=10)

    # Define the filters
    def table_filter(self):
        # Reset
        filter_reset = ttk.Button(self.root, text='Reiniciar', command=lambda: self.table_reset())
        filter_reset.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        # Not used
        filter_used = ttk.Checkbutton(self.root, text='Preguntas sin usar')
        filter_used.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        # Filter by category
        filter_by_category_values = list(sql.categories().flatten().unique())
        filter_by_category = ttk.Combobox(self.root, values=filter_by_category_values, font=('Verdana', 18),
                                          state="readonly")
        filter_by_category.grid(row=0, column=2, padx=5, pady=5, sticky='e')
        filter_by_category.bind('<<ComboboxSelected>>', self.filter_by_category_callback)

        # Filter by type
        filter_by_type = ttk.Combobox(self.root, values=['eir', 'ope'], font=('Verdana', 18), state="readonly")
        filter_by_type.grid(row=0, column=3, padx=5, pady=5)
        filter_by_type.bind('<<ComboboxSelected>>', self.filter_by_type_callback)

        # Select default value
        for key, value in self.db_filter.items():
            # Create a dynamic value
            current_filter = "filter_by_{}".format(key)
            locals()[current_filter].set(value)

    # Filter by type
    def filter_by_type_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.db_filter.update(type=value)
            self.table_refresh(self)

    # Filter by type
    def filter_by_category_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.db_filter.update(category=value)
            self.table_refresh(self)

    # Reset table
    def table_reset(self):
        # Reset table
        self.destroy()

        Application(
            self.root,
            config.database['per_page'],
            config.database['page'],
            config.database['order'],
            config.database['direction'],
            {},
        )

    # Refresh table
    def table_refresh(self, table):
        # Reset table
        self.destroy()

        Application(
            table.root,
            table.db_per_page,
            table.db_page,
            table.db_order,
            table.db_direction,
            table.db_filter,
        )


# Launch the application
app = Application(
    tkinter.Tk(),
    config.database['per_page'],
    config.database['page'],
    config.database['order'],
    config.database['direction'],
)

# App event loop
app.root.mainloop()
