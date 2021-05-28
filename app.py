import tkinter
from tkinter.font import Font

import orm as sql
from tkinter import ttk

# Columns
columns = {
    'headers': ['ID', 'Usuario', 'Categoría', 'Preguntas', 'Respuesta 1', 'Respuesta 2', 'Respuesta 3', 'Respuesta 4',
                'Correcta', 'Tipo', 'Utilizada en...'],
    'columns': ['id', 'user', 'category', 'question', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct', 'type',
                'used'],
    # Width in %
    'width': ['1', '5', '5', '40', '10', '10', '10', '10', '2', '2', '4'],
}


# Determine odd or even alternate element
def table_even_odd(current):
    if current == 'odd':
        return 'even'
    else:
        return 'odd'


def table_cell_value(row, max_width):
    result = []
    values = list(row.values())

    for (index, value) in enumerate(values):
        width = int(columns['width'][index])
        calculate_width = column_width(max_width, width)

        result.append(table_cell_wrap(value, calculate_width))

    return result


def column_width(max_width, percent):
    return round(max_width * int(percent) / 100)


# A helper function that will wrap a given value based on column width
def table_cell_wrap(val, width, pad=80):
    f = Font(font='TkDefaultFont')
    if not isinstance(val, str):
        return val
    else:
        words = val.split()
        lines = [[], ]
        for word in words:
            line = lines[-1] + [word, ]
            if f.measure(' '.join(line)) < (width - pad):
                lines[-1].append(word)
            else:
                lines[-1] = ' '.join(lines[-1])
                lines.append([word, ])

        if isinstance(lines[-1], list):
            lines[-1] = ' '.join(lines[-1])

        return '\n'.join(lines)


class Application(tkinter.Frame):
    def __init__(self, root):
        # Define root
        self.root = root

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Set default database values
        self.db_per_page = 10
        self.db_page = 0
        self.db_order = 'questions.id'
        self.db_direction = 'ASC'

        # Default values
        self.table_title = 'Preguntas para EIR y OPE'
        self.columns = columns['columns']
        self.headers = columns['headers']
        self.width = columns['width']
        self.columns_total = len(self.columns)
        self.even_odd = 'odd'

        # Define results
        self.results = sql.questions_results(
            self.db_per_page,
            self.db_page,
            self.db_order,
            self.db_direction,
        )

        # Create the table
        self.table = ttk.Treeview(self.root, columns=self.columns, show='headings')

        # Max application width
        self.max_width = int(self.table.winfo_screenwidth())

        # Init
        self.init_user_interface()

    def init_user_interface(self):
        # Configure the root object for the Application
        self.root.title("Academium Quest - Premium version")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Define the Application Title / Label
        title_label = tkinter.Label(self.root, text=self.table_title, font=('Arial', 30), pady=30)
        title_label.grid(row=0, columnspan=self.columns_total)

        # Set column header style
        self.style.configure('Treeview', rowheight=80)
        self.style.configure('Treeview.Heading', padding=15)

        # Set the table headers, columns and sort  the columns
        for (i, col) in enumerate(self.columns):
            self.table.heading(col, text=self.headers[i], command=lambda _col=col: self.table_sort(self.table, _col, False))
            # Define the column width
            column_width_ = column_width(self.max_width, self.width[i])
            # Applicate the column width
            self.table.column(col, width=column_width_)

        # Insert the rows
        for row in self.results:
            list_of_values = table_cell_value(row, self.max_width)

            self.table.insert("", "end", values=list_of_values, tags=(self.even_odd,))
            self.even_odd = table_even_odd(self.even_odd)

        # Set the table grid
        self.table.grid(row=1, column=0, columnspan=self.columns_total)

        # # Set alternate row colors
        # self.table.tag_configure('even', background='#efefef')
        # self.table.tag_configure('odd', background='#fff')

    # Order columns by click...
    # https://www.programmersought.com/article/56864033946/
    def table_sort(self, table, col, reverse):
        l = [(table.set(k, col), k) for k in table.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            # Move according to the index after sorting
            table.move(k, '', index)

        # Refresh the table in reverse order
        table.heading(col, command=lambda: self.table_sort(table, col, not reverse))


app = Application(tkinter.Tk())
app.root.mainloop()