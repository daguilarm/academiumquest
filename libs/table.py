import libs.static as static


# Populate the columns
def columns(self):
    # Set the table headers, columns and sort  the columns
    for (i, col) in enumerate(self.columns):
        # Populate the table headings
        self.table.heading(col, text=self.headers[i], command=lambda _col=col: column_sort(self, _col, False))

        # Define the column width
        column_width_ = static.column_width(self.max_width, self.width[i])

        # Config the columns
        self.table.column(col, width=column_width_, anchor='center')

    # Insert the rows
    for result in self.results:
        # Populate the list with values
        list_of_values = static.table_cell_value(self.width, self.max_width, self.columns, result)

        self.table.insert("", "end", values=list_of_values)


# Order columns by click...
# https://www.programmersought.com/article/56864033946/
def column_sort(self, col, reverse):
    # Get the elements
    elements = [(self.table.set(k, col), k) for k in self.table.get_children('')]
    elements.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(elements):
        # Move according to the index after sorting
        self.table.move(k, '', index)

    # Refresh the table in reverse order
    self.table.heading(col, command=lambda: column_sort(self, col, not reverse))