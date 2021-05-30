import config
import libs.orm as sql
from tkinter import ttk


class Filters:
    def __init__(self, app):
        self.app = app

        # Render the filters
        self.filter_by_type = self.filter_by_type()
        self.filter_by_category = self.filter_by_category()
        self.filter_by_used = self.filter_by_used()

        # Set the default values for the filters
        self.default_values_for_filters()

    def filter_by_used(self):
        filter_used = ttk.Checkbutton(self.app.root, text='Preguntas sin usar')
        filter_used.grid(row=0, column=1, padx=5, pady=5, sticky='e')

    # Filter by type
    def filter_by_type(self):
        # Create the select
        filter_by_type = ttk.Combobox(
            self.app.root,
            values=['', 'eir', 'ope'],
            font=('Verdana', 18),
            state='readonly'
        )
        filter_by_type.grid(row=0, column=3, padx=5, pady=5)
        # Bind the event to the select
        filter_by_type.bind('<<ComboboxSelected>>', self.filter_by_type_callback)

    # Filter by type
    def filter_by_type_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.app.table.db_filter.update(type=value)
            self.app.table.db_page = 1
            self.app.table.refresh(self.app.table)

    # Filter by category
    def filter_by_category(self):
        # Get all the categories from the database
        filter_by_category_values = list(sql.categories().flatten().unique().prepend(''))
        # Create the select
        filter_by_category = ttk.Combobox(
            self.app.root,
            values=filter_by_category_values,
            font=('Verdana', 18),
            state='readonly'
        )
        filter_by_category.grid(row=0, column=2, padx=5, pady=5, sticky='e')
        # Bind the event to the select
        filter_by_category.bind('<<ComboboxSelected>>', self.filter_by_category_callback)

    # Filter by type
    def filter_by_category_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.app.table.db_filter.update(category=value)
            self.app.table.db_page = 1
            self.app.refresh(self.app.table)

    # Set the default values for filters
    def default_values_for_filters(self):
        # Select default value
        for key, value in self.app.table.db_filter.items():
            # Create a dynamic value
            current_filter = "filter_by_{}".format(key)
            locals()[current_filter].set(value)
