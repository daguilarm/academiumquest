# Created by @daguilarm at 25/5/21
from tkinter import END, Entry


class Table:

    # Configuration values
    __config = {
        'labels': ['usuario', 'pregunta', 'respuestas'],
        'columns': ['user_id', 'question', 'answers'],
        'columns_width': [5, 150, 50],
        'column_font': ('Arial', 16, 'bold'),
    }

    def __init__(self, root, results):

        # code for creating table
        # https://www.geeksforgeeks.org/create-table-using-tkinter/

        # Set the variables
        columns, total_columns, columns_width, column_font, labels = self.__get_config()

        # Create the rows
        i = 0

        for result in results:
            for j in range(total_columns):
                text = result[columns[j]]
                e = Entry(root, width=columns_width[j], fg='blue', font=column_font)
                e.grid(row=i, column=j)
                e.insert(END, text)
            i += 1

    # Generate a table from sql values
    def __get_config(self):
        config = self.__config
        columns = config['columns']

        return [
            # All the columns
            columns,
            # Total number of columns
            len(columns),
            # The list with all the columns widths
            config['columns_width'],
            # Column font
            config['column_font'],
            # Column labels
            config['labels']
        ]
