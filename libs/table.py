import config
import libs.orm as sql
import tkinter
from tkinter import ttk
from libs.filters import Filters
from libs import static


# Create table
class Table:
    def __init__(
            self,
            root,
            max_width,
            db_per_page,
            db_current_page,
            db_order_by,
            db_direction,
            db_filter=None,
    ):
        # Default root
        self.root = root

        # Table name
        self.title = 'Preguntas para EIR y OPE'

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
        self.max_width = max_width

        # Create the table
        self.table = ttk.Treeview(self.root, columns=self.columns, show='headings')

        # Create pagination
        self.pagination = tkinter.Frame(self.root)
        self.pagination.grid(row=12, columnspan=self.columns_total, padx=40, pady=20)

        # Current filters
        self.current_filters = []

        # Get the values from the database
        results = sql.questions(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
            self.db_filter,
        )

        # Render table
        self.render(results)

        # Render pagination
        self.table_pagination(results)

        # Filters
        self.filters = Filters(self)

    # Render the table
    def render(self, results):
        title = '{} - Con los filtros: {}'.format(self.title, ', '.join(self.db_filter.values()))
        title_label = tkinter.Label(self.root, text=title, font=('Verdana', 30), pady=20)
        title_label.grid(row=0, column=0, columnspan=self.columns_total, sticky='w', padx=20)

        # Set the table headers, columns and sort  the columns
        for (i, col) in enumerate(self.columns):
            # Populate the table headings
            # _col for avoid vars by reference in python 3
            self.table.heading(
                col,
                text=self.headers[i],
                command=lambda _col=col: self.sort(_col, self.db_direction)
            )

            # Define the column width
            column_width_ = static.column_width(self.max_width, self.width[i])

            # Config the columns
            self.table.column(col, width=column_width_, anchor='center')

        # Insert the rows
        for result in results:
            # Populate the list with values
            list_of_values = static.table_cell_value(
                self.width,
                self.max_width,
                self.columns,
                result
            )

            self.table.insert("", "end", values=list_of_values)

        # Set the table grid
        self.table.grid(row=1, column=0, columnspan=self.columns_total)

    # Table pagination
    def table_pagination(self, results):
        # Pagination label
        label_title = 'Mostrando página {} de {} páginas, de un total de {} resultados'.format(
            results.current_page,
            results.last_page,
            results.total
        )
        self.pagination.label = tkinter.Label(
            self.pagination,
            text=label_title,
            font=('Verdana', 16),
            fg="#999999"
        )
        self.pagination.label.grid(row=11, column=0, columnspan=self.columns_total, padx=60, pady=(0, 15))

        # Button config
        b_config = {
            'font': ('Verdana', 18),
            'width': 40,
            'padx': 20,
            'pady': 20,
        }

        # Prev button
        tkinter.Button(
            self.pagination,
            b_config,
            text='⇦ Anterior',
            command=lambda: self.prev_page(self.db_page),
            foreground='#666666'
        ).grid(row=12, column=0, padx=10)

        # Reset table
        tkinter.Button(
            self.pagination,
            font=('Verdana', 18),
            width=10,
            pady=20,
            text='⟳ Reiniciar',
            command=lambda: self.reset(self),
            foreground='red'
        ).grid(row=12, column=1, padx=10)

        # Next button
        tkinter.Button(
            self.pagination,
            b_config,
            text='Siguiente ⇨',
            command=lambda: self.next_page(self.db_page, results),
            foreground='#666666'
        ).grid(row=12, column=2, padx=10)

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
        self.refresh(self)

    # Pagination: previous page
    def prev_page(self, current):
        # Set the minimum page in 1
        if current <= 1:
            self.db_page = 1
        else:
            self.db_page = current - 1

        # Refresh the table
        self.refresh(self)

    # Pagination: next page
    def next_page(self, current, results):
        # Update the page if not the last one
        if not self.db_page == results.last_page:
            self.db_page = current + 1

            # Refresh the table
            self.refresh(self)

    # Refresh table
    def refresh(self, app):
        self.table = Table(
            app.root,
            app.max_width,
            app.db_per_page,
            app.db_page,
            app.db_order,
            app.db_direction,
            app.db_filter,
        )

    # Reset table
    def reset(self, app):
        self.table = Table(
            app.root,
            app.max_width,
            config.database['per_page'],
            config.database['page'],
            config.database['order'],
            config.database['direction'],
            config.database['filter'],
        )