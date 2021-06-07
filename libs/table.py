import config
import libs.orm as sql
import tkinter
from tkinter import ttk

from libs.crud import Crud
from libs.filters import Filters
from libs import static


# Create table
class Table:
    """
        The Table class:
            - Use the libs/crud.py for all the CRUD actions.
            - Use the libs/filters.py for filtering results.
            - Use the libs/orm.py for connect with the database.
    """

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
        # self.title = 'Preguntas para EIR y OPE'
        self.title = 'Preguntas EIR y OPE'

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
        self.pagination.grid(row=11, columnspan=self.columns_total, padx=40, pady=20)

        # Current filters
        self.current_filters = []

        # Get the values from the database
        self.results = sql.questions(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
            self.db_filter,
        )

        # Render the table
        self.table_render(self.results)

        # Render table pagination
        self.table_pagination(self.results)

        # Render the table filters
        # The Filter class from libs/filters.py
        self.table_filters = Filters(self)

    """
        The Table operations:
            - Render table: using the method -> table_render()
            - Paginate table results:  using the method -> table_pagination()
                - Previous page: using the method -> prev_page()
                - Next page: using the method -> next_page()
            - Sort the table columns by single click: using the method -> table_sort_columns()
            - Edit table rows: using the method -> table_row_edit()
    """

    # Render the table
    def table_render(self, results):
        title_label = tkinter.Label(self.root, text=self.title, font=('Verdana', 30), pady=20)
        title_label.grid(row=0, column=0, columnspan=self.columns_total, sticky='w', padx=20)

        # Set the table headers, columns and sort  the columns
        for (i, col) in enumerate(self.columns):
            # Populate the table headings
            # _col for avoid vars by reference in python 3
            self.table.heading(
                col,
                text=self.headers[i],
                command=lambda _col=col: self.table_sort_columns(_col, self.db_direction)
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

            """ 
                Create a double click event for edit row.
                This event will fired the table_row_edit() method
            """
            self.table.bind("<Double-1>", self.table_row_edit)

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
        ).grid(row=12, column=0, padx=10, pady=10)

        # Reset table
        tkinter.Button(
            self.pagination,
            font=('Verdana', 18),
            width=10,
            pady=20,
            text='⟳ Reiniciar',
            command=lambda: self.reset(self),
            foreground='red'
        ).grid(row=12, column=1, padx=10, pady=10)

        # Next button
        tkinter.Button(
            self.pagination,
            b_config,
            text='Siguiente ⇨',
            command=lambda: self.next_page(self.db_page, results),
            foreground='#666666'
        ).grid(row=12, column=2, padx=10)

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

    # Sort table columns
    def table_sort_columns(self, order_by, direction):
        # Define order
        if direction == 'ASC':
            self.db_direction = 'DESC'
        else:
            self.db_direction = 'ASC'

        # Define column to order by...
        self.db_order = order_by

        # Refresh the table
        self.refresh(self)

    """
        Create and edit table rows
    """

    # Edit row on double click
    # This method will be fired from table_render()
    # All the magic is in the libs.crud.py
    def table_row_create(self):
        # Edit the row values
        Crud(self, []).render(action='create')

    # Edit row on double click
    # This method will be fired from table_render()
    def table_row_edit(self, event):
        # Get the row
        row = self.table.focus()

        # Get row information
        values = self.table.item(row).get('values')

        # Clean the values
        filter_values = []

        for i in values:
            filter_values.append(str(i).replace('\n', ' ').replace(config.empty_results, '').strip())

        # Edit the row values
        Crud(self, filter_values).render(action='edit')

    """
        The Table auxiliary methods: 
            - Refresh the table. 
            - Reset the table.
    """

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
    def reset(self):
        # Reset the variables
        self.db_per_page = config.database['per_page']
        self.db_page = config.database['page']
        self.db_order = config.database['order']
        self.db_direction = config.database['direction']
        self.db_filter.clear()

        # Reset the table
        self.refresh(self)
