import libs.orm as sql
from tkinter import ttk

class Filters:
    def __init__(self, table):
        self.table = table

        # Render the filters
        self.render()

    def render(self):
        # Reset
        filter_reset = ttk.Button(self.table.root, text='Reiniciar', command=lambda: self.table.reset(self.table))
        filter_reset.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        # Not used
        filter_used = ttk.Checkbutton(self.table.root, text='Preguntas sin usar')
        filter_used.grid(row=0, column=1, padx=5, pady=5, sticky='e')

        # Filter by category
        filter_by_category_values = list(sql.categories().flatten().unique())
        filter_by_category = ttk.Combobox(self.table.root, values=filter_by_category_values, font=('Verdana', 18),
                                          state="readonly")
        filter_by_category.grid(row=0, column=2, padx=5, pady=5, sticky='e')
        filter_by_category.bind('<<ComboboxSelected>>', self.filter_by_category_callback)

        # Filter by type
        filter_by_type = ttk.Combobox(self.table.root, values=['eir', 'ope'], font=('Verdana', 18), state="readonly")
        filter_by_type.grid(row=0, column=3, padx=5, pady=5)
        filter_by_type.bind('<<ComboboxSelected>>', self.filter_by_type_callback)

        # Select default value
        for key, value in self.table.db_filter.items():
            # Create a dynamic value
            current_filter = "filter_by_{}".format(key)
            locals()[current_filter].set(value)

    # Filter by type
    def filter_by_type_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.table.db_filter.update(type=value)
            self.table.db_page = 1
            self.table.refresh(self.table)

    # Filter by type
    def filter_by_category_callback(self, event):
        # Get event
        value = event.widget.get()

        # Get values
        if value:
            self.table.db_filter.update(category=value)
            self.table.db_page = 1
            self.table.refresh(self.table)
