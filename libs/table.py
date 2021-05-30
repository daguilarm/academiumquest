import config
import tkinter
from tkinter import ttk
from libs import static


class Table():
    def __init__(
            self,
            root,
            db_per_page,
            db_current_page,
            db_order_by,
            db_direction,
            db_filter=None
    ):
        # Table name
        self.table_title = 'Preguntas para EIR y OPE'

        # Set default database values
        self.db_per_page = db_per_page
        self.db_page = db_current_page
        self.db_order = db_order_by
        self.db_direction = db_direction
        self.db_filter = db_filter

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

    # Render the table
    def render(self, sql_results):
        # Set the table headers, columns and sort  the columns
        for (i, col) in enumerate(self.columns):
            # Populate the table headings
            # _col for avoid vars by reference in python 3
            self.table.heading(col, text=self.headers[i],
                               command=lambda _col=col: self.sort(_col, self.db_direction))

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

    # Table pagination
    def pagination(self, results):
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
                                     command=lambda: self.prev_page(self.db_page), foreground="#666666")
        button_prev.grid(row=12, column=0, padx=10)

        # Next button
        button_next = tkinter.Button(self.pagination, b_config, text='Siguiente ⇨',
                                     command=lambda: self.next_page(self.db_page, results), foreground="#666666")
        button_next.grid(row=12, column=1, padx=10)

    # Order table columns
    def sort(self, order_by, direction):
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
    def prev_page(self, current):
        if current <= 1:
            self.db_page = 1
        else:
            self.db_page = current - 1

        # Refresh the table
        self.table_refresh(self)

    # Pagination: next page
    def next_page(self, current, results):
        self.db_page = current + 1

        # Refresh the table
        if self.db_page <= results.last_page:
            self.table_refresh(self)

    # Reset table
    def reset(self):
        # Reset table
        self.destroy()

        Table(
            self.root,
            config.database['per_page'],
            config.database['page'],
            config.database['order'],
            config.database['direction'],
            {},
        )

    # Refresh table
    def refresh(self, table):
        # Reset table
        self.destroy()

        Table(
            table.root,
            table.db_per_page,
            table.db_page,
            table.db_order,
            table.db_direction,
            table.db_filter,
        )