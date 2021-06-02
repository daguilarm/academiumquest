import config
from tkinter.font import Font

"""
    All the static methods:
        - table_cell_value() -> Resolve the table cell value base on the width.
        - table_cell_wrap() -> A helper function that will wrap a given value based on column width.
        - column_width() -> Calculate the column width base on the screen width.
        - format_date() -> Format date from database format.
"""


# Resolve the table cell value base on the width
def table_cell_value(columns_width, max_width, columns, row):
    # Default values
    result = []
    # Add all the row values to a list
    values = list(row.values())

    for (index, value) in enumerate(values):
        # Get the width % for this column
        width = int(columns_width[index])

        # Calculate relative width base on % and screen size
        calculate_width = column_width(max_width, width)

        # If column is a date
        if columns[index] == 'used':
            if value == '' or value == 'null' or value == 'None':
                value = config.empty_results
            else:
                value = format_date(value)

        # Add the value to the cell, wrapping the content
        result.append(table_cell_wrap(value, calculate_width))

    return result


# A helper function that will wrap a given value based on column width
def table_cell_wrap(val, width, pad=1):
    # Set the font
    f = Font(font='TkDefaultFont')

    # If value is not a string
    if not isinstance(val, str):
        return val

    # If value is a string
    else:
        # Split the words and init the lines
        words = val.split()
        lines = [[], ]

        # Split the lines base on the width and the words
        for word in words:
            line = lines[-1] + [word, ]

            if f.measure(' '.join(line)) < (width - pad):
                lines[-1].append(word)
            else:
                lines[-1] = ' '.join(lines[-1])
                lines.append([word, ])

        if isinstance(lines[-1], list):
            lines[-1] = ' '.join(lines[-1])

        # Join the lines
        return '\n'.join(lines)


# Calculate the column width base on the screen width
def column_width(max_width, percent):
    return round(max_width * int(percent) / 100)


# Format date from database format
def format_date(value):
    if value:
        # Separate the string to values
        date, time = value.split(' ')
        # Separate the string to values
        year, month, day = date.split('-')

        return '/'.join([day, month, year])

    return value
