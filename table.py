import json
from tkinter import Text, ttk, BooleanVar
from tkinter.ttk import Scrollbar
from ttkwidgets import Table

# Configuration values
headers = {
    'headers': ['Usuario', 'Categoría', 'Preguntas', 'Respuestas'],
    'columns': ['user', 'category', 'question', 'answers'],
}


# Get the config values
def get_config():
    columns = headers['columns']

    return [
        # Column labels
        headers['headers'],
        # All the columns
        columns,
        # Total number of columns
        len(columns)
    ]


# Add styles to table
def _table_style(app):
    style = ttk.Style(app)
    style.theme_use('alt')


# Init table
def _init_table(app, titles):
    # Add sortable
    sortable = BooleanVar(app, True)

    # Generate table with the headers
    return sortable, Table(app, columns=titles, sortable=sortable.get(), height=10)


# Render table headers
def _render_headers(app_table, columns):
    for col in columns:
        app_table.heading(col, text=col)
        app_table.column(col, width=10,  stretch=True)


# Render rows
def _render_rows(app_table, columns, results):
    for result in results:
        app_table.insert('', 'end', values=_values(columns, result))


# Populate table with values
def _values(table_columns, result):
    values = []
    for index in table_columns:
        # This is a JSON array and its needs to be formatted
        if index == 'answers':
            item = _values_answers(result[index])
        else:
            item = result[index]

        values.append(item)

    return values


def _values_answers(values):
    values = json.loads(values)
    item = ''
    for value in values:
        item += '- ' + value + '\n'

    return item


# Show scroll-bars
def _show_scroll_bars(app, app_table, table_sortable):
    x = Scrollbar(app, orient='horizontal', command=app_table.xview)
    y = Scrollbar(app, orient='vertical', command=app_table.yview)
    app_table.configure(yscrollcommand=y.set, xscrollcommand=x.set, sortable=table_sortable.get())

    return x, y


# Set table grid
def _table_grid(app_table, x, y):
    app_table.grid(sticky='ewns')
    x.grid(row=1, column=0, sticky='ew')
    y.grid(row=0, column=1, sticky='ns')


# Generate table
def table(app, results):
    # Get the configuration values
    table_th, table_columns, table_total = get_config()

    # Add styles to table
    _table_style(app)

    # Generate the table with its headers and the sortable option
    _sortable, _table = _init_table(app, table_th)

    # Render headers
    _render_headers(_table, table_th)

    # Render the rows
    _render_rows(_table, table_columns, results)

    # Add the table scrollbars
    x, y = _show_scroll_bars(app, _table, _sortable)

    # Set table grid
    _table_grid(_table, x, y)
