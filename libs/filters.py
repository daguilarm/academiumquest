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

        # Default value
        if 'type' in self.app.db_filter:
            filter_by_type.set(self.app.db_filter.get('type'))

        # Bind the event to the select
        filter_by_type.bind('<<ComboboxSelected>>', self.filter_by_type_callback)

    # Filter by type
    def filter_by_type_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.app.db_filter.update(type=value)
            self.app.db_page = 1
            self.app.refresh(self.app)

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

        # Default value
        if 'category' in self.app.db_filter:
            filter_by_category.set(self.app.db_filter.get('category'))

        # Bind the event to the select
        filter_by_category.bind('<<ComboboxSelected>>', self.filter_by_category_callback)

    # Filter by type
    def filter_by_category_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.app.db_filter.update(category=value)
            self.app.db_page = 1
            self.app.refresh(self.app)
