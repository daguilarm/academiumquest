import libs.orm as sql
import tkinter
from tkinter import ttk


class Filters:
    def __init__(self, app):
        self.app = app

        # Set default value if there is a selected value for the Checkbutton
        if 'used' in self.app.db_filter:
            self.used_status = tkinter.IntVar(value=1)
        else:
            self.used_status = tkinter.IntVar(value=0)

        # Categories
        self.categories = sql.categories()

        # Render the filters
        self.filter_by_type()
        self.filter_by_category()
        self.filter_by_used()

    def filter_by_used(self):
        # Filter by used
        filter_by_used = ttk.Checkbutton(
            self.app.root,
            text='Preguntas sin usar',
            var=self.used_status,
            command=self.filter_by_used_callback
        )
        filter_by_used.grid(row=0, column=1, padx=5, pady=5, sticky='e')

    # Filter by used
    def filter_by_used_callback(self):
        # Toggle status
        if self.used_status.get():
            self.app.db_filter['used'] = 'used_at_null'
        else:
            self.app.db_filter.pop('used', None)

        # Update table
        self.app.refresh(self.app)

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

        # Set default value if there is a selected value
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
        categories = {}
        for category in list(self.categories):
            categories['{} - {}'.format(category.get('id'), category.get('name'))] = category.get('id')

        # Create the select
        filter_by_category = ttk.Combobox(
            self.app.root,
            values=list(categories.keys()),
            font=('Verdana', 18),
            state='readonly'
        )
        filter_by_category.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        # Set default value if there is a selected value
        if 'category' in self.app.db_filter:
            # We have to search the id in the filters
            for category in self.categories:
                if category.get('id') == self.app.db_filter.get('category'):
                    # Now we have the category name
                    filter_by_category.set(category.get('name'))

        # Bind the event to the select
        filter_by_category.bind('<<ComboboxSelected>>', self.filter_by_category_callback)

    # Filter by type
    def filter_by_category_callback(self, event):
        # Get event
        value = event.widget.get().split(' - ')

        # Get the current id
        for category in self.categories:
            if category.get('name') == value[1]:
                current_id = category.get('id')

        # Get values
        if value:
            self.app.db_filter.update(category=current_id)
            self.app.db_page = 1
            self.app.refresh(self.app)